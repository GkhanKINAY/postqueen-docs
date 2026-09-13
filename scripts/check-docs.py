#!/usr/bin/env python3
"""Docs CI: nav slugs exist, no orphan pages, User Guide bans .env / docker compose."""
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


def walk_pages(node) -> list[str]:
    pages: list[str] = []
    if isinstance(node, str):
        pages.append(node)
        return pages
    if isinstance(node, dict):
        if "pages" in node:
            pages.extend(walk_pages(node["pages"]))
        if "groups" in node:
            pages.extend(walk_pages(node["groups"]))
        if "tabs" in node:
            pages.extend(walk_pages(node["tabs"]))
        return pages
    if isinstance(node, list):
        for item in node:
            pages.extend(walk_pages(item))
    return pages


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
        and not p.as_posix().startswith(str(ROOT / ".github"))
    }
    orphans = sorted(on_disk - seen)
    # README.mdx etc none expected; ignore nothing else
    for slug in orphans:
        ERRORS.append(f"mdx not in docs.json navigation: {slug}")

    banned = re.compile(r"(?:\.env\b|docker compose)", re.IGNORECASE)
    for mdx in sorted(ROOT.rglob("*.mdx")):
        rel = mdx.relative_to(ROOT).as_posix()
        if rel.startswith("snippets/"):
            continue
        slug = rel[:-4] if rel.endswith(".mdx") else rel
        if not slug.startswith(GUIDE_PREFIXES) and slug not in GUIDE_PREFIXES:
            continue
        text = mdx.read_text()
        # skip YAML fences that are not body — still ban anywhere in Guide files
        if banned.search(text):
            ERRORS.append(f"User Guide forbids `.env` / `docker compose`: {rel}")

    if ERRORS:
        print("docs check failed:\n" + "\n".join(f"- {e}" for e in ERRORS))
        return 1
    print(f"docs check ok: {len(seen)} nav pages, User Guide env/compose ban clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
