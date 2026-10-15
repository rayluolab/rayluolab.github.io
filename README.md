# rayluolab.github.io
Ray Luo Lab Web Page

## Lab notes

Notes live in `content/post/<note-slug>/index.md`. Each note requires a title,
summary, publication date, and `authors` using the display names from People.
Multiple authors are supported. The Notes page shows author links and sorts
posts newest first. See `content/contribute-notes/index.md` for the student
submission guide and `archetypes/post/index.md` for the starter template.

Create a draft with `hugo new content post/your-topic/index.md`, then preview
with `hugo server --buildDrafts`. Draft notes are excluded from normal
production builds. Review the text and attribution, set `draft: false`, and
merge into `main` to publish through the existing GitHub Pages workflow.

## Personal websites

Members can deploy their own websites independently. Set `website` in their
`content/authors/<name>/_index.md` to add a "Personal website" entry to that URL.
Names and portraits on People always open the local lab profile.
Publication author links also retain the lab author archive.

Each local lab profile includes its complete matching publication list in the
lab bibliography, across all years.
The profile groups papers by year and does not limit the number of results.
To match a confirmed alternate publication name, add a `publication_names`
list to the member's author profile. Match only verified full names; do not
infer identity from initials or surnames. Original citation names are retained,
and duplicate DOI records are counted once.

## Publications

Refresh recent journal publications from publisher-deposited Crossref metadata:

```sh
python3 -m pip install -r scripts/requirements-publications.txt
python3 scripts/update_publications.py --since 2025-01-01
```

This updates `publications.bib`, publication pages, and downloadable citations
together. It preserves existing URLs, corrects ACS supporting-information DOIs
when a matching parent article is found, and uses online publication dates for
chronological ordering. New records require a Ray Luo author with an Irvine
affiliation. Existing meeting abstracts remain in the archive but are excluded
from the homepage journal-article list. This command runs on demand; pushing
website changes deploys the saved content, without fetching new literature.

Crossref coverage depends on publisher deposits. Check Google Scholar for
additional preprints and records without affiliations. `scripts/fetch_scholar.py`
is an older full-bibliography scraper; use the incremental command above for
routine updates.

Run metadata regression checks with:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
```

## Research illustrations

Each research page contains its own original `featured.png`. The homepage and
Research page share the same responsive gallery. The figures are conceptual
diagrams, not simulation results or representations of specific proteins.
To regenerate them, install Pillow and run
`python3 scripts/generate_research_figures.py`.
