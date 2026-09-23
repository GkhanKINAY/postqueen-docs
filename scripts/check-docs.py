#!/usr/bin/env python3
"""Docs CI: structure, links and the style rules.

Always, on every page:
  nav slugs exist and are unique, no orphan pages, redirects point at pages and
  never shadow one, snippet imports resolve and no page uses <Snippet file> (it
  renders nothing), card and frontmatter icon files exist, internal links resolve
  without going through a redirect, frontmatter has a title and a description,
  and the Guide tab never mentions `.env` or `docker compose`.

On every page that no longer carries an OVERHAUL-TODO marker (all pages on a
release run): frontmatter has an icon, every image has alt text, no em dash, and
the user tabs (every tab but Self-hosting) never mention self-hosting, PostQueen
as open source, AGPL, Docker, `.env` or a server environment variable (the names
in scripts/env-names.txt).

--release (or DOCS_RELEASE=1) also fails on any OVERHAUL-TODO marker. CI uses it
for main and for pull requests into main; on other branches the markers are
allowed and only counted.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_JSON = ROOT / "docs.json"
RELEASE = "--release" in sys.argv or os.environ.get("DOCS_RELEASE") == "1"
ERRORS: list[str] = []

SELF_HOST_TAB = "Self-hosting"
MARKER = "OVERHAUL-TODO"
# The docs home carries the fork line and the one link to Self-hosting (plan 3.1).
SELF_HOST_WORDS_ALLOWED = {"introduction"}

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

LINK_RE = re.compile(r"(?:\]\(|href=[\"'])(/[^\)\"'\s#]*)(?:#[^\)\"'\s]*)?[\)\"']")
IMPORT_RE = re.compile(r"^import\s+.+?\s+from\s+['\"](/snippets/[^'\"]+)['\"];?\s*$", re.M)
LEGACY_SNIPPET_RE = re.compile(r"<Snippet\s+file=")
STATIC_PREFIXES = ("/images/", "/logo/", "/favicon", "/fonts/")
SKIP_LINK_EXACT = {"/", "/llms.txt", "/llms-full.txt", "/sitemap.xml", "/skill.md"}
FENCE_RE = re.compile(r"^(\s*)(```|~~~).*?^\1\2", re.M | re.S)
COMMENT_RE = re.compile(r"\{/\*.*?\*/\}", re.S)


def walk_nav(node, tab: str | None, out: list[tuple[str, str | None]]) -> None:
    if isinstance(node, str):
        if "://" not in node and not node.startswith("#"):
            out.append((node.lstrip("/"), tab))
        return
    if isinstance(node, dict):
        tab = node.get("tab", tab)
        for key in NAV_CONTAINER_KEYS:
            if key in node:
                walk_nav(node[key], tab, out)
        return
    if isinstance(node, list):
        for item in node:
            walk_nav(item, tab, out)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[4:end], text[end + 5 :]


def fm_value(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.*?)\s*$", fm, re.M)
    if not m:
        return None
    return m.group(1).strip().strip("'\"") or None


def prose(body: str) -> str:
    """The page text without code fences and MDX comments."""
    return FENCE_RE.sub("", COMMENT_RE.sub("", body))


def load_env_names() -> set[str]:
    path = ROOT / "scripts" / "env-names.txt"
    names = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            names.add(line)
    return names


def page_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.mdx"):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(("snippets/", "_templates/", ".github/", "node_modules/")) or "/." in "/" + rel:
            continue
        out.append(p)
    return sorted(out)


def main() -> int:
    data = json.loads(DOCS_JSON.read_text())
    nav: list[tuple[str, str | None]] = []
    walk_nav(data.get("navigation", {}), None, nav)
    if not nav:
        ERRORS.append("docs.json navigation produced zero pages")

    tab_of: dict[str, str | None] = {}
    for slug, tab in nav:
        if slug in tab_of:
            ERRORS.append(f"duplicate nav slug: {slug}")
        tab_of[slug] = tab
        if not (ROOT / f"{slug}.mdx").is_file():
            ERRORS.append(f"nav slug missing file: {slug} -> {slug}.mdx")

    files = page_files()
    on_disk = {p.relative_to(ROOT).with_suffix("").as_posix() for p in files}
    for slug in sorted(on_disk - set(tab_of)):
        ERRORS.append(f"mdx not in docs.json navigation: {slug}")

    # Redirects
    redirect_sources: set[str] = set()
    for item in data.get("redirects") or []:
        source = str(item.get("source", "")).split("#", 1)[0].strip("/")
        dest = str(item.get("destination", "")).split("#", 1)[0].strip("/")
        if source in redirect_sources:
            ERRORS.append(f"duplicate redirect source: /{source}")
        redirect_sources.add(source)
        if source in tab_of or (ROOT / f"{source}.mdx").is_file():
            ERRORS.append(f"redirect source is still a page: /{source}")
        if not dest:
            ERRORS.append(f"redirect missing destination: {item}")
        elif dest not in tab_of:
            ERRORS.append(f"redirect destination is not a nav page: /{source} -> /{dest}")

    env_names = load_env_names()
    env_re = re.compile(r"\b(" + "|".join(sorted(map(re.escape, env_names), key=len, reverse=True)) + r")\b")
    # "open source" only as PostQueen's own pitch: a third-party agent may be open source.
    # "environment variable" alone is fine: the CLI reads POSTQUEEN_API_KEY from one.
    self_host_re = re.compile(
        r"self[- ]?host|\bAGPL|\bdocker\b|docker[- ]compose|\.env\b"
        r"|PostQueen is (?:an? )?open[- ]source|open[- ]source (?:fork|tool|scheduler)",
        re.I,
    )
    guide_ban = re.compile(r"(?:\.env\b|docker compose)", re.I)
    card_icon_re = re.compile(r"<Card\b[^>]*\bicon=[\"'](/[^\"']+)[\"']")
    svg_size_re = re.compile(
        r"""width=["'](\d+)["'][^>]*height=["'](\d+)["']|viewBox=["']0 0 (\d+) (\d+)["']"""
    )
    img_tag_re = re.compile(r"<img\b[^>]*?>", re.S)
    md_img_re = re.compile(r"!\[([^\]]*)\]\(")

    marked: dict[str, int] = {}
    relaxed = 0
    checked_links = 0

    # Snippets: imports they make must resolve, and none may use <Snippet file>.
    for snip in sorted((ROOT / "snippets").glob("*.mdx")):
        text = snip.read_text()
        rel = snip.relative_to(ROOT).as_posix()
        if LEGACY_SNIPPET_RE.search(text):
            ERRORS.append(f"<Snippet file> renders nothing, import the snippet instead: {rel}")
        if "—" in prose(text):
            ERRORS.append(f"em dash in {rel}")

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        slug = rel[:-4]
        text = path.read_text()
        fm, body = split_frontmatter(text)
        tab = tab_of.get(slug)
        is_marked = MARKER in text

        if is_marked:
            m = re.search(r"OVERHAUL-TODO\((B\d+)\)", text)
            batch = m.group(1) if m else "B?"
            marked[batch] = marked.get(batch, 0) + 1
            if RELEASE:
                ERRORS.append(f"{MARKER} left on a release run: {rel} ({batch})")

        if not fm:
            ERRORS.append(f"no frontmatter: {rel}")
        if not fm_value(fm, "title"):
            ERRORS.append(f"frontmatter has no title: {rel}")
        if not fm_value(fm, "description"):
            ERRORS.append(f"frontmatter has no description: {rel}")
        icon = fm_value(fm, "icon")
        if icon and icon.startswith("/") and not (ROOT / icon.lstrip("/")).is_file():
            ERRORS.append(f"frontmatter icon file missing in {rel}: {icon}")

        if LEGACY_SNIPPET_RE.search(text):
            ERRORS.append(f"<Snippet file> renders nothing, import the snippet instead: {rel}")
        for target in IMPORT_RE.findall(text):
            if not (ROOT / target.lstrip("/")).is_file():
                ERRORS.append(f"missing snippet {target} imported in {rel}")

        if tab == "Guide" and guide_ban.search(text):
            ERRORS.append(f"Guide forbids `.env` / `docker compose`: {rel}")

        for src in card_icon_re.findall(text):
            static = ROOT / src.lstrip("/")
            if not static.is_file():
                ERRORS.append(f"missing Card icon in {rel}: {src}")
                continue
            if static.suffix.lower() != ".svg":
                continue
            match = svg_size_re.search(static.read_text(errors="replace")[:1200])
            if match:
                width = int(match.group(1) or match.group(3))
                height = int(match.group(2) or match.group(4))
                if width > 120 or height > 120:
                    ERRORS.append(f"banner used as Card icon in {rel}: {src} ({width}x{height})")

        seen_links: set[str] = set()
        for match in LINK_RE.finditer(text):
            raw = match.group(1)
            if raw in SKIP_LINK_EXACT:
                continue
            if raw.startswith(STATIC_PREFIXES):
                if not (ROOT / raw.lstrip("/")).is_file():
                    ERRORS.append(f"broken static path in {rel}: {raw}")
                continue
            target = raw.strip("/")
            if not target or target in seen_links:
                continue
            seen_links.add(target)
            checked_links += 1
            if target in redirect_sources:
                ERRORS.append(f"link through a redirect in {rel}: /{target}, link the new path")
            elif target not in tab_of:
                ERRORS.append(f"broken internal link in {rel}: /{target}")

        # Style rules: for finished pages, and for every page on a release run.
        if is_marked and not RELEASE:
            relaxed += 1
            continue
        if not icon:
            ERRORS.append(f"frontmatter has no icon: {rel}")
        text_only = prose(body)
        if "—" in text_only:
            ERRORS.append(f"em dash in {rel}")
        for tag in img_tag_re.findall(body):
            alt = re.search(r"\balt=[\"']([^\"']*)[\"']", tag)
            if not alt or not alt.group(1).strip():
                ERRORS.append(f"image without alt text in {rel}: {tag[:80]}")
        for alt in md_img_re.findall(body):
            if not alt.strip():
                ERRORS.append(f"image without alt text in {rel}")
        if tab and tab != SELF_HOST_TAB and slug not in SELF_HOST_WORDS_ALLOWED:
            words = sorted({m.group(0) for m in self_host_re.finditer(text_only)})
            envs = sorted({m.group(0) for m in env_re.finditer(body)})
            if words:
                ERRORS.append(f"self-hosting words on the {tab} tab in {rel}: {', '.join(words)}")
            if envs:
                ERRORS.append(f"server environment variables on the {tab} tab in {rel}: {', '.join(envs)}")

    if ERRORS:
        print("docs check failed:\n" + "\n".join(f"- {e}" for e in ERRORS))
        return 1
    mode = "release run" if RELEASE else "branch run"
    todo = sum(marked.values())
    by_batch = ", ".join(f"{b} {n}" for b, n in sorted(marked.items(), key=lambda x: int(x[0][1:]) if x[0][1:].isdigit() else 99))
    print(
        f"docs check ok ({mode}): {len(tab_of)} nav pages, {checked_links} internal links, "
        f"{len(data.get('redirects') or [])} redirects; "
        + (f"{todo} pages still marked {MARKER} ({by_batch}), style rules skipped on them"
           if todo else "no OVERHAUL-TODO left, style rules on every page")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
