#!/usr/bin/env python3
"""Validate built MkDocs pages for internal links, anchors, and article IDs."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


SITE_ORIGIN = "https://ryzenovod.github.io"
SITE_PREFIX = "/hse-health-notes/"
LINK_ATTRIBUTES = {
    "a": "href",
    "area": "href",
    "iframe": "src",
    "img": "src",
    "link": "href",
    "script": "src",
    "source": "src",
}
IGNORED_SCHEMES = {"data", "mailto", "tel"}
SVG_METADATA_PREFIXES = (
    Path("assets/oct-2026"),
    Path("assets/eos-materials"),
)
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


@dataclass(frozen=True)
class Link:
    tag: str
    value: str


@dataclass
class Page:
    path: Path
    ids: set[str]
    article_ids: set[str]
    duplicate_article_ids: list[str]
    links: list[Link]
    base_href: str | None


class SiteHTMLParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: set[str] = set()
        self.article_ids: set[str] = set()
        self.duplicate_article_ids: list[str] = []
        self.links: list[Link] = []
        self.base_href: str | None = None
        self._article_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_start(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_start(tag, attrs, self_closing=True)

    def _handle_start(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
        *,
        self_closing: bool,
    ) -> None:
        attr = {name: value for name, value in attrs if value is not None}
        entered_article = False
        if self._article_depth == 0 and self._is_article_start(tag, attr):
            self._article_depth = 1
            entered_article = True
        elif self._article_depth and not self_closing and tag not in VOID_TAGS:
            self._article_depth += 1

        element_id = attr.get("id")
        if element_id:
            self.ids.add(element_id)
            if self._article_depth:
                if element_id in self.article_ids and element_id != "__toc":
                    self.duplicate_article_ids.append(element_id)
                self.article_ids.add(element_id)

        if tag == "base" and attr.get("href") and self.base_href is None:
            self.base_href = attr["href"]

        link_attr = LINK_ATTRIBUTES.get(tag)
        if link_attr and attr.get(link_attr):
            self.links.append(Link(tag=tag, value=attr[link_attr]))

        if entered_article and self_closing:
            self._article_depth = 0

    def handle_endtag(self, tag: str) -> None:
        if self._article_depth and tag not in VOID_TAGS:
            self._article_depth -= 1

    @staticmethod
    def _is_article_start(tag: str, attr: dict[str, str]) -> bool:
        if tag != "article":
            return False
        classes = attr.get("class", "").split()
        return "md-content__inner" in classes or "md-typeset" in classes

    def page(self) -> Page:
        return Page(
            path=self.path,
            ids=self.ids,
            article_ids=self.article_ids,
            duplicate_article_ids=self.duplicate_article_ids,
            links=self.links,
            base_href=self.base_href,
        )


class SVGMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_svg = False
        self.has_title = False
        self.has_desc = False
        self.has_role_img = False
        self.has_viewbox = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {name: value for name, value in attrs if value is not None}
        if tag == "svg":
            self.has_svg = True
            self.has_role_img = attr.get("role") == "img"
            self.has_viewbox = "viewbox" in attr
        elif tag == "title":
            self.has_title = True
        elif tag == "desc":
            self.has_desc = True


def parse_site(site_dir: Path) -> dict[Path, Page]:
    pages: dict[Path, Page] = {}
    for html_path in sorted(site_dir.rglob("*.html")):
        parser = SiteHTMLParser(html_path.relative_to(site_dir))
        parser.feed(html_path.read_text(encoding="utf-8"))
        pages[html_path] = parser.page()
    return pages


def public_url_for(page: Page) -> str:
    rel = page.path.as_posix()
    if rel == "index.html":
        public_path = SITE_PREFIX
    elif rel.endswith("/index.html"):
        public_path = SITE_PREFIX + rel[: -len("index.html")]
    else:
        public_path = SITE_PREFIX + rel
    return SITE_ORIGIN + public_path


def resolve_internal_target(site_dir: Path, url_path: str) -> Path:
    relative = unquote(url_path[len(SITE_PREFIX) :])
    target = site_dir / relative
    if target.is_dir() or url_path.endswith("/"):
        return target / "index.html"
    if target.exists():
        return target
    if not target.suffix:
        return target / "index.html"
    return target


def is_svg_requiring_metadata(relative_path: Path) -> bool:
    return any(
        relative_path == prefix or prefix in relative_path.parents
        for prefix in SVG_METADATA_PREFIXES
    )


def check_svg_metadata(site_dir: Path) -> list[str]:
    errors: list[str] = []
    for svg_path in sorted(site_dir.rglob("*.svg")):
        relative = svg_path.relative_to(site_dir)
        if not is_svg_requiring_metadata(relative):
            continue
        parser = SVGMetadataParser()
        parser.feed(svg_path.read_text(encoding="utf-8"))
        missing = [
            label
            for label, present in (
                ("<title>", parser.has_title),
                ("<desc>", parser.has_desc),
                ('role="img"', parser.has_role_img),
                ("viewBox", parser.has_viewbox),
            )
            if not present
        ]
        if not parser.has_svg:
            missing.insert(0, "<svg>")
        if missing:
            errors.append(f"{relative.as_posix()}: missing SVG metadata {', '.join(missing)}")
    return errors


def check_site(site_dir: Path) -> list[str]:
    site_dir = site_dir.resolve()
    pages = parse_site(site_dir)
    errors: list[str] = []

    for html_path, page in pages.items():
        page_name = page.path.as_posix()
        for duplicate in page.duplicate_article_ids:
            errors.append(f"{page_name}: duplicate article id #{duplicate}")

        page_base = public_url_for(page)
        link_base = urljoin(page_base, page.base_href) if page.base_href else page_base
        for link in page.links:
            parsed = urlsplit(urljoin(link_base, link.value))
            if parsed.scheme == "javascript":
                errors.append(f"{page_name}: javascript link {link.value}")
                continue
            if parsed.scheme in IGNORED_SCHEMES:
                continue
            if parsed.scheme not in {"", "http", "https"}:
                continue
            if parsed.netloc and parsed.netloc != "ryzenovod.github.io":
                continue
            if not parsed.path.startswith(SITE_PREFIX):
                errors.append(f"{page_name}: link outside project prefix {link.value}")
                continue

            target = resolve_internal_target(site_dir, parsed.path)
            if not target.is_file():
                errors.append(f"{page_name}: missing file {link.value}")
                continue

            if link.tag == "a" and parsed.fragment and target.suffix == ".html":
                anchor = unquote(parsed.fragment)
                target_page = pages.get(target)
                if target_page and anchor not in target_page.ids:
                    errors.append(f"{page_name}: missing anchor {link.value}")

    errors.extend(check_svg_metadata(site_dir))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_dir", type=Path, help="Built MkDocs site directory")
    args = parser.parse_args(argv)

    site_dir = args.site_dir.resolve()
    if not site_dir.is_dir():
        print(f"{site_dir}: not a directory", file=sys.stderr)
        return 2

    errors = check_site(site_dir)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"site check failed: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(f"site check passed: {site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
