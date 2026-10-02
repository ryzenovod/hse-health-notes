from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_site import check_site


class SiteCheckTests(unittest.TestCase):
    def run_check(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            site_dir = Path(temp_dir)
            for relative, content in files.items():
                path = site_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return check_site(site_dir)

    def test_relative_pretty_url_and_urlencoded_anchor(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<a href="notes/#%D1%82%D0%B5%D1%81%D1%82">notes</a>'
                    "</article>"
                ),
                "notes/index.html": '<article class="md-content__inner"><h1 id="тест">Тест</h1></article>',
            }
        )

        self.assertEqual(errors, [])

    def test_project_prefix_url(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<a href="/hse-health-notes/year-1/">year</a>'
                    "</article>"
                ),
                "year-1/index.html": '<article class="md-content__inner"><h1 id="year">Year</h1></article>',
            }
        )

        self.assertEqual(errors, [])

    def test_base_href_is_followed(self) -> None:
        errors = self.run_check(
            {
                "chapter/page/index.html": (
                    '<base href="/hse-health-notes/chapter/">'
                    '<article class="md-content__inner"><a href="other/">other</a></article>'
                ),
                "chapter/other/index.html": '<article class="md-content__inner"><h1 id="other">Other</h1></article>',
            }
        )

        self.assertEqual(errors, [])

    def test_external_links_are_ignored(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<a href="https://example.com/missing#still-external">external</a>'
                    "</article>"
                ),
            }
        )

        self.assertEqual(errors, [])

    def test_duplicate_article_ids_are_reported(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<h2 id="same">One</h2><p id="same">Two</p>'
                    "</article>"
                ),
            }
        )

        self.assertEqual(errors, ["index.html: duplicate article id #same"])

    def test_void_tag_inside_article_does_not_keep_outside_ids_in_article(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<img id="logo" src="logo.png"><p>Inside</p>'
                    "</article>"
                    '<div id="logo"></div>'
                ),
                "logo.png": "",
            }
        )

        self.assertEqual(errors, [])

    def test_nested_article_duplicate_ids_are_reported(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<h2 id="same">Outer</h2>'
                    '<article class="md-typeset"><p id="same">Nested</p></article>'
                    "</article>"
                ),
            }
        )

        self.assertEqual(errors, ["index.html: duplicate article id #same"])

    def test_self_closing_tags_do_not_drift_article_depth(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<svg><path /></svg><section id="inside" />'
                    '<p id="after">After</p></article>'
                    '<p id="after">Outside</p>'
                ),
            }
        )

        self.assertEqual(errors, [])

    def test_javascript_links_are_reported(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<a href="javascript:alert(1)">bad</a></article>'
                ),
            }
        )

        self.assertEqual(errors, ["index.html: javascript link javascript:alert(1)"])

    def test_theme_toc_duplicates_are_ignored(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<nav><a id="same"></a><a id="same"></a>'
                    '<a id="__toc"></a><a id="__toc"></a></nav>'
                    '<article class="md-content__inner"><h1 id="page">Page</h1></article>'
                ),
            }
        )

        self.assertEqual(errors, [])

    def test_svg_metadata_is_checked_for_new_asset_folders(self) -> None:
        errors = self.run_check(
            {
                "index.html": (
                    '<article class="md-content__inner">'
                    '<img src="assets/oct-2026/chart.svg"></article>'
                ),
                "assets/oct-2026/chart.svg": (
                    '<svg xmlns="http://www.w3.org/2000/svg" '
                    'viewBox="0 0 10 10" role="img">'
                    "<title>Chart</title><desc>Test chart.</desc></svg>"
                ),
            }
        )

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
