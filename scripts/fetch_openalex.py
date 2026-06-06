#!/usr/bin/env python3
"""Fetch an author's works from OpenAlex and write a BibTeX file.

Usage: python3 scripts/fetch_openalex.py <OPENALEX_AUTHOR_ID> [out.bib]

The output BibTeX is consumed by the `academic` importer (see
.github/workflows/import-publications.yml) to generate publication pages.
"""
import sys
import re
import json
import urllib.request

AUTHOR_ID = sys.argv[1] if len(sys.argv) > 1 else "A5032088629"
OUT = sys.argv[2] if len(sys.argv) > 2 else "publications.bib"
BASE = (
    "https://api.openalex.org/works"
    "?filter=author.id:%s,type:article"
    "&per-page=200&sort=publication_date:desc&mailto=ray.luo@uci.edu" % AUTHOR_ID
)


def clean(s):
    return re.sub(r"[{}]", "", s or "").strip()


def bibkey(work, year):
    last = "anon"
    auths = work.get("authorships") or []
    if auths:
        name = auths[0]["author"]["display_name"].split()
        if name:
            last = re.sub(r"[^A-Za-z]", "", name[-1]).lower()
    wid = work["id"].split("/")[-1]
    return "%s%s_%s" % (last, year or "", wid)


def main():
    works, cursor = [], "*"
    while cursor:
        with urllib.request.urlopen(BASE + "&cursor=" + cursor) as r:
            d = json.load(r)
        works += d["results"]
        cursor = d["meta"].get("next_cursor")
        if not d["results"]:
            break

    entries = []
    for w in works:
        if not w.get("title"):
            continue
        year = w.get("publication_year") or ""
        authors = " and ".join(
            a["author"]["display_name"] for a in (w.get("authorships") or [])
        )
        venue = ((w.get("primary_location") or {}).get("source") or {}).get(
            "display_name", ""
        )
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        entries.append(
            "@article{%s,\n"
            "  title = {%s},\n"
            "  author = {%s},\n"
            "  journal = {%s},\n"
            "  year = {%s},\n"
            "  doi = {%s}\n"
            "}\n" % (bibkey(w, year), clean(w["title"]), clean(authors), clean(venue), year, doi)
        )

    with open(OUT, "w") as f:
        f.write("\n".join(entries))
    print("Wrote %d entries to %s" % (len(entries), OUT))


if __name__ == "__main__":
    main()
