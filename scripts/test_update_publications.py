"""Regression checks for metadata matching and repeatable publication updates."""
import contextlib
from datetime import date
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update_publications as updater


def paper(affiliation="University of California, Irvine"):
    return {"DOI": "10.1021/example.6c00001", "type": "journal-article",
            "title": ["Example article"], "container-title": ["Example Journal"],
            "published-online": {"date-parts": [[2026, 3, 30]]},
            "published-print": {"date-parts": [[2026, 4, 14]]},
            "author": [{"given": "Ray", "family": "Luo", "affiliation": [{"name": affiliation}]}]}


class PublicationTests(unittest.TestCase):
    def test_supporting_information_doi_matches_parent(self):
        self.assertEqual(updater.canonical_doi("https://doi.org/10.1021/example.6c00001.s001"),
                         "10.1021/example.6c00001")
        self.assertEqual(updater.canonical_doi("10.1234/article.s001"), "10.1234/article.s001")

    def test_author_identity_requires_irvine(self):
        self.assertTrue(updater.is_lab_paper(paper()))
        self.assertFalse(updater.is_lab_paper(paper("Another University")))
        item = paper()
        item["author"][0]["given"] = "Someone"
        self.assertFalse(updater.is_lab_paper(item))

    def test_date_uses_first_publication_not_print_issue(self):
        self.assertEqual(updater.published(paper()), date(2026, 3, 30))

    def test_sync_preserves_url_body_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "content/publication/original-url/index.md"
            page.parent.mkdir(parents=True)
            page.write_text("---\ntitle: Old title\ndoi: 10.1021/example.6c00001.s001\n---\nKeep this abstract.\n")
            (root / "publications.bib").write_text("@article{original_key,\n  title = {Old title},\n  doi = {10.1021/example.6c00001.s001}\n}\n")
            with patch.object(updater, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
                updater.sync([paper()], date(2025, 1, 1), date(2026, 10, 15))
                first = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
                updater.sync([paper()], date(2025, 1, 1), date(2026, 10, 15))
                second = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(first, second)
            self.assertIn("Keep this abstract.", page.read_text())
            self.assertIn("date: '2026-03-30'", page.read_text())
            self.assertEqual(len(list((root / 'content/publication').glob('*/index.md'))), 1)

    def test_new_papers_exclude_namesakes_abstracts_and_future_dates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'content/publication').mkdir(parents=True)
            (root / 'publications.bib').write_text('')
            abstract = paper()
            abstract['title'] = ['BPS2026 – Example meeting abstract']
            future = paper()
            future['published-online'] = future['published-print'] = {'date-parts': [[2027, 1, 1]]}
            with patch.object(updater, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                updater.sync([paper('Another University'), abstract, future], date(2025, 1, 1), date(2026, 10, 15))
            self.assertEqual(list((root / 'content/publication').glob('*/index.md')), [])


if __name__ == '__main__':
    unittest.main()
