#!/usr/bin/env python3
"""Docs CI: nav slugs exist, no orphan pages, User Guide bans .env / docker compose,
redirect targets exist, Snippet files exist, internal doc links resolve."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_JSON = ROOT / "docs.json"
ERRORS: list[str] = []

GUIDE_PREFIXES = (
    "introduction",
    "quickstart",
    "howitworks",
    "concepts",
    "where-things-live",
    "which-interface",
    "using/",
    "providers/",
)

# Mintlify nav containers. Walking only `pages`/`groups`/`tabs` misses dropdowns.
NAV_CONTAINER_KEYS = (
    "pages",
    "groups",
    "tabs",
    "dropdowns",
    "languages",
    "versions",
    "anchors",
    "global",
    "navigation",
)

LINK_RE = re.compile(
    r"(?:\]\(|href=[\"'])(/[^\)\"'\s#]+)(?:#[^\)\"'\s]*)?[\)\"']"
)
SNIPPET_RE = re.compile(r"<Snippet\s+file=\"([^\"]+)\"")
STATIC_PREFIXES = ("/images/", "/logo/", "/favicon")
SKIP_LINK_EXACT = {"/llms.txt", "/llms-full.txt", "/sitemap.xml"}


def walk_pages(node) -> list[str]:
    pages: list[str] = []
    if isinstance(node, str):
        if "://" not in node and not node.startswith("#"):
            pages.append(node.lstrip("/"))
        return pages
    if isinstance(node, dict):
        for key in NAV_CONTAINER_KEYS:
            if key in node:
                pages.extend(walk_pages(node[key]))
        href = node.get("href")
        if isinstance(href, str) and href.startswith("/") and "://" not in href:
            slug = href.split("#", 1)[0].strip("/")
            if slug:
                pages.append(slug)
        return pages
    if isinstance(node, list):
        for item in node:
            pages.extend(walk_pages(item))
    return pages


def is_guide_slug(slug: str) -> bool:
    return slug.startswith(GUIDE_PREFIXES) or slug in GUIDE_PREFIXES


def exists_as_page(slug: str, nav: set[str], redirect_dest: set[str]) -> bool:
    if (ROOT / f"{slug}.mdx").is_file():
        return True
    if (ROOT / f"{slug}.md").is_file():
        return True
    if slug in nav or slug in redirect_dest:
        return True
    return False


def main() -> int:
    data = json.loads(DOCS_JSON.read_text())
    nav_pages = walk_pages(data.get("navigation", {}))
    if not nav_pages:
        ERRORS.append("docs.json navigation produced zero pages")

    seen: set[str] = set()
    for slug in nav_pages:
        if slug in seen:
            ERRORS.append(f"duplicate nav slug: {slug}")
        seen.add(slug)
        path = ROOT / f"{slug}.mdx"
        if not path.is_file():
            ERRORS.append(f"nav slug missing file: {slug} -> {path.relative_to(ROOT)}")

    on_disk = {
        p.relative_to(ROOT).with_suffix("").as_posix()
        for p in ROOT.rglob("*.mdx")
        if "snippets/" not in p.as_posix()
        and "/." not in p.as_posix()
        and ".github/" not in p.as_posix()
    }
    for slug in sorted(on_disk - seen):
        ERRORS.append(f"mdx not in docs.json navigation: {slug}")

    banned = re.compile(r"(?:\.env\b|docker compose)", re.IGNORECASE)
    for mdx in sorted(ROOT.rglob("*.mdx")):
        rel = mdx.relative_to(ROOT).as_posix()
        if rel.startswith("snippets/"):
            continue
        slug = rel[:-4] if rel.endswith(".mdx") else rel
        if not is_guide_slug(slug):
            continue
        if banned.search(mdx.read_text()):
            ERRORS.append(f"User Guide forbids `.env` / `docker compose`: {rel}")

    redirect_sources: set[str] = set()
    redirect_dest: set[str] = set()
    for item in data.get("redirects") or []:
        source = str(item.get("source", "")).split("#", 1)[0].strip("/")
        dest = str(item.get("destination", "")).split("#", 1)[0].strip("/")
        if source:
            redirect_sources.add(source)
        if not dest:
            ERRORS.append(f"redirect missing destination: {item}")
            continue
        redirect_dest.add(dest)
        if not exists_as_page(dest, seen, set()):
            ERRORS.append(f"redirect destination missing file: {source} -> {dest}")

    snippet_dir = ROOT / "snippets"
    for mdx in sorted(ROOT.rglob("*.mdx")):
        rel = mdx.relative_to(ROOT).as_posix()
        text = mdx.read_text()
        for name in SNIPPET_RE.findall(text):
            snippet_path = snippet_dir / name
            if not snippet_path.is_file():
                ERRORS.append(f"missing snippet {name} referenced from {rel}")

    card_icon_re = re.compile(r"<Card\b[^>]*\bicon=[\"'](/[^\"']+)[\"']")
    svg_size_re = re.compile(
        r"""width=["'](\d+)["'][^>]*height=["'](\d+)["']|viewBox=["']0 0 (\d+) (\d+)["']"""
    )
    for mdx in sorted(ROOT.rglob("*.mdx")):
        rel = mdx.relative_to(ROOT).as_posix()
        if rel.startswith("snippets/"):
            continue
        for src in card_icon_re.findall(mdx.read_text()):
            static = ROOT / src.lstrip("/")
            if not static.is_file():
                ERRORS.append(f"missing Card icon in {rel}: {src}")
                continue
            if static.suffix.lower() != ".svg":
                continue
            head = static.read_text(errors="replace")[:1200]
            match = svg_size_re.search(head)
            if not match:
                continue
            width = int(match.group(1) or match.group(3))
            height = int(match.group(2) or match.group(4))
            if width > 120 or height > 120:
                ERRORS.append(
                    f"banner used as Card icon in {rel}: {src} ({width}x{height})"
                )

    checked_links: set[tuple[str, str]] = set()
    for mdx in sorted(ROOT.rglob("*.mdx")):
        rel = mdx.relative_to(ROOT).as_posix()
        if rel.startswith("snippets/"):
            continue
        for match in LINK_RE.finditer(mdx.read_text()):
            raw = match.group(1)
            if raw in SKIP_LINK_EXACT:
                continue
            if any(raw.startswith(prefix) for prefix in STATIC_PREFIXES):
                static = ROOT / raw.lstrip("/")
                if not static.is_file():
                    ERRORS.append(f"broken static path in {rel}: {raw}")
                continue
            slug = raw.split("#", 1)[0].strip("/")
            if not slug:
                continue
            key = (rel, slug)
            if key in checked_links:
                continue
            checked_links.add(key)
            if slug in redirect_sources:
                continue
            if not exists_as_page(slug, seen, redirect_dest):
                ERRORS.append(f"broken internal link in {rel}: /{slug}")

    if ERRORS:
        print("docs check failed:\n" + "\n".join(f"- {e}" for e in ERRORS))
        return 1
    print(
        f"docs check ok: {len(seen)} nav pages, "
        f"{len(checked_links)} internal links, User Guide env/compose ban clean"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
