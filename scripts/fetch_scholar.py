#!/usr/bin/env python3
"""Regenerate publications.bib from Ray Luo's Google Scholar (the source of truth).

Google Scholar has no API and blocks datacenter IPs, so this is a LOCAL tool
(run it on a normal machine), not a CI job:

    pip install --user scholarly
    python3 scripts/fetch_scholar.py        # writes publications.bib

It (1) pulls the Scholar publication list, (2) screens out AMBER software/version
manuals and meeting abstracts (ACS "Abstracts of Papers", Biophysical Journal
abstract supplements, BPS/COMP/BIOT/CINF codes), and (3) enriches each kept paper
with authors + journal + DOI via Crossref. Then the existing
.github/workflows/import-publications.yml turns publications.bib into pages.
"""
import json, re, time, difflib, urllib.request, urllib.parse

SCHOLAR_ID = "CONRN6AAAAAJ"  # Ray Luo

def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
def esc(s): return re.sub(r'[{}]', '', (s or '')).strip()
def yr4(x):
    m = re.search(r'(19|20)\d\d', str(x or '')); return m.group(0) if m else ''
def cr_year(it):
    for k in ("issued", "published-print", "published-online", "published", "created"):
        dp = (it.get(k) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]:
            y = yr4(dp[0][0])
            if y: return y
    return ''

def is_manual(t):
    return bool(re.match(r'\s*amber(tools)?\b', t, re.I) and (re.search(r'\d', t) or re.search(r'tools', t, re.I))) \
        or 'reference manual' in t.lower()

def is_abstract(title, venue):
    v = (venue or '').lower()
    return bool(re.match(r'\s*(bps|comp|biot|cinf|phys|orgn|inor)\s?\d', title, re.I)) \
        or 'abstract' in title.lower() \
        or 'abstracts of papers' in v \
        or re.search(r'\bfaseb\b', v) \
        or re.search(r'biophysical journal.*\d+a\b', v)

def crossref(title):
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 3, "mailto": "ray.luo@uci.edu"})
    try:
        with urllib.request.urlopen("https://api.crossref.org/works?" + q, timeout=20) as r:
            items = json.load(r)["message"]["items"]
    except Exception:
        return None
    for it in items:
        ct = (it.get("title") or [""])[0]
        if difflib.SequenceMatcher(None, norm(ct), norm(title)).ratio() > 0.86:
            return it
    return None

def main():
    from scholarly import scholarly
    a = scholarly.fill(scholarly.search_author_id(SCHOLAR_ID), sections=["publications"])
    pubs = a.get("publications", [])
    entries, enriched = [], 0
    for i, p in enumerate(pubs):
        b = p.get("bib", {})
        title, syear, venue = b.get("title", ""), yr4(b.get("pub_year")), b.get("citation", "")
        if not title or is_manual(title) or is_abstract(title, venue):
            continue
        it = crossref(title)
        if it:
            enriched += 1
            authors = " and ".join(f"{x.get('given','')} {x.get('family','')}".strip() for x in it.get("author", [])) or "Ray Luo"
            journal = (it.get("container-title") or [""])[0]
            doi = it.get("DOI", "")
            y = cr_year(it) or syear
            title = (it.get("title") or [title])[0]
        else:
            authors, journal, doi, y = "Ray Luo", re.sub(r'\s*\d.*$', '', venue).strip() or "Unpublished", "", syear
        if not y:
            continue  # skip entries with no resolvable year
        key = "luo" + y + "_" + norm(title)[:18]
        entries.append("@article{%s,\n  title = {%s},\n  author = {%s},\n  journal = {%s},\n  year = {%s},\n  doi = {%s}\n}\n"
                        % (key, esc(title), esc(authors), esc(journal), y, doi))
        if i % 40 == 0:
            time.sleep(0.5)
    with open("publications.bib", "w") as f:
        f.write("\n".join(entries))
    print("Wrote %d entries (%d Crossref-enriched) to publications.bib" % (len(entries), enriched))

if __name__ == "__main__":
    main()
