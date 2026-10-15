#!/usr/bin/env python3
"""Refresh recent publications from publisher-deposited Crossref metadata.

Install scripts/requirements-publications.txt, then run from any directory:
    python scripts/update_publications.py --since 2025-01-01

New records require an exact Ray Luo author with an Irvine affiliation.
Existing records match by DOI (including ACS supporting-information DOIs).
Both BibTeX and Hugo pages are updated together; existing page URLs are kept.
This is an on-demand update, not a scheduled Google Scholar scraper.
"""
import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request

import bibtexparser
import yaml

ROOT = Path(__file__).resolve().parents[1]


def canonical_doi(value):
    value = re.sub(r"^https?://(?:dx\.)?doi.org/", "", str(value or "").strip().lower())
    return re.sub(r"\.s\d+$", "", value) if value.startswith("10.1021/") else value


def clean(value):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", value)).split())


def published(item):
    # The first public journal publication date, not the metadata deposit date.
    dates = []
    for field in ("published-online", "published-print", "published"):
        parts = (item.get(field, {}).get("date-parts") or [[]])[0]
        if parts:
            dates.append(date(*(parts + [1] * (3 - len(parts)))))
    return min(dates) if dates else None


def is_lab_paper(item):
    for author in item.get("author", []):
        if author.get("given", "").casefold() == "ray" and author.get("family", "").casefold() == "luo":
            if "irvine" in json.dumps(author.get("affiliation", [])).casefold():
                return True
    return False


def read_page(path):
    _, front, body = path.read_text().split("---", 2)
    return yaml.safe_load(front), body


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "RayLuoLab-Publications/1.0 (https://rayluolab.org/)"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def sync(items, since, until):
    bibpath = ROOT / "publications.bib"
    bibtext = bibpath.read_text()
    # Preserve untouched bibliography entries byte for byte.
    blocks = list(re.finditer(r"(?ms)^@\w+\{.*?^\}", bibtext))
    entries = {}
    for block in blocks:
        entry = bibtexparser.loads(block.group()).entries[0]
        doi = canonical_doi(entry.get("doi"))
        if doi:
            entries.setdefault(doi, []).append((block, entry))
    pages = {}
    for path in (ROOT / "content/publication").glob("*/index.md"):
        front, body = read_page(path)
        doi = canonical_doi(front.get("doi"))
        if doi:
            pages.setdefault(doi, []).append((path, front, body))
    replacements, additions, report = [], [], []
    seen = set()
    for item in items:
        doi = canonical_doi(item.get("DOI"))
        when = published(item)
        existing = doi in pages or doi in entries
        if (not doi or doi in seen or item.get("type") != "journal-article"
                or not when or not since <= when <= until):
            continue
        if not existing and not is_lab_paper(item):
            continue
        title = clean((item.get("title") or [""])[0])
        journal = clean((item.get("container-title") or [""])[0])
        authors = [clean(f"{a.get('given', '')} {a.get('family', '')}") for a in item.get("author", [])]
        if not title or not journal or not authors:
            continue
        # Keep existing meeting abstracts but don't import new ones.
        abstract = bool(re.match(r"BPS\d{4}\b", title))
        if abstract and not existing:
            continue
        seen.add(doi)
        fields = dict(title=title, author=" and ".join(authors), journal=journal,
                      year=str(when.year), month=str(when.month), day=str(when.day), doi=doi)
        def bib_entry(key):
            return "@article{" + key + ",\n" + "".join(
                f"  {k} = {{{v.replace('{', '').replace('}', '')}}},\n" for k, v in fields.items()
            ).rstrip(",\n") + "\n}"
        matched_entries = entries.get(doi, [])
        for block, entry in matched_entries:
            replacements.append((block.start(), block.end(), bib_entry(entry["ID"])))
        if not matched_entries:
            key = "luo" + str(when.year) + "_" + re.sub(r"[^a-z0-9]", "", title.lower())[:18]
            # DOI-derived suffix prevents collisions between similar titles.
            key += "_" + re.sub(r"[^a-z0-9]", "", doi.split("/")[-1])
            additions.append(bib_entry(key))
        else:
            key = matched_entries[0][1]["ID"]
        matched_pages = pages.get(doi, [])
        if not matched_pages:
            path = ROOT / "content/publication" / key.replace("_", "-") / "index.md"
            matched_pages = [(path, {}, "\n")]
        for path, front, body in matched_pages:
            front.update(title=title, authors=authors, date=when.isoformat(),
                         publication_types=["paper-conference" if abstract else "article-journal"],
                         publication=journal, doi=doi)
            front.setdefault("publishDate", when.isoformat())
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + "---" + body)
            (path.parent / "cite.bib").write_text(bib_entry(key) + "\n")
        report.append(("Updated" if existing else "Added", when.isoformat(), title))
    for start, end, text in sorted(replacements, reverse=True):
        bibtext = bibtext[:start] + text + bibtext[end:]
    if additions:
        bibtext = bibtext.rstrip() + "\n\n" + "\n\n".join(additions) + "\n"
    bibpath.write_text(bibtext)
    for action, when, title in report:
        print(f"{action} {when}: {title}")
    print(f"Refreshed {len(report)} records ({sum(r[0] == 'Added' for r in report)} new).")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", type=date.fromisoformat, default=date(date.today().year - 1, 1, 1))
    parser.add_argument("--until", type=date.fromisoformat, default=date.today())
    parser.add_argument("--source", type=Path, help="Use a saved Crossref works JSON response")
    args = parser.parse_args()
    if args.source:
        result = json.loads(args.source.read_text())
    else:
        params = urllib.parse.urlencode({"query.author": "Ray Luo", "rows": 1000,
            "filter": f"from-pub-date:{args.since},until-pub-date:{args.until},type:journal-article"})
        result = fetch("https://api.crossref.org/works?" + params)
        # Author searches can miss papers with abbreviated names. Also refresh
        # known recent DOIs directly, preserving their existing attribution.
        found = {canonical_doi(item.get("DOI")) for item in result["message"]["items"]}
        for path in (ROOT / "content/publication").glob("*/index.md"):
            front, _ = read_page(path)
            doi = canonical_doi(front.get("doi"))
            when = date.fromisoformat(str(front.get("date", "1900-01-01"))[:10])
            if doi and doi not in found and args.since <= when <= args.until:
                try:
                    item = fetch("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))["message"]
                    result["message"]["items"].append(item)
                    found.add(doi)
                except (OSError, ValueError) as error:
                    print(f"Could not refresh {doi}: {error}", file=sys.stderr)
    sync(result["message"]["items"], args.since, args.until)


if __name__ == "__main__":
    main()
