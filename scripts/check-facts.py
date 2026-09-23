#!/usr/bin/env python3
"""Facts check: the numbers and names the docs repeat, against facts/facts.json.

1. docs.json variables equal facts.json (prices, trial and refund days, tool
   counts, the MCP and API addresses, the network count).
2. facts.json's MCP tools equal the app's tool list on GitHub main
   (tool.list.ts, raw fetch), minus the classes facts.json keeps out of the docs.
3. Banned strings: removed routes and tools, wrong tool counts, Windsurf, Medium,
   the old API key location, trial and rate-limit claims that are not true,
   Bearer on the public API, clipping, veo3.
4. The status line of each channel and agent page equals facts.json.
5. mcp/tools names exactly facts.json's tools.
6. Prices, trial days and refund days written in a page equal facts.json.

Checks 3 to 6 run on every page without an OVERHAUL-TODO marker, on the
snippets and on SKILL.md; pages still marked, and openapi.json while it carries
"x-overhaul-todo", only report a count. --release (or DOCS_RELEASE=1) applies
every check everywhere. --offline skips the GitHub fetch (check 2).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "--release" in sys.argv or os.environ.get("DOCS_RELEASE") == "1"
OFFLINE = "--offline" in sys.argv
VERBOSE = "--verbose" in sys.argv
TOOL_LIST_URL = (
    "https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/"
    "libraries/nestjs-libraries/src/chat/tools/tool.list.ts"
)
MARKER = "OVERHAUL-TODO"
ERRORS: list[str] = []
DEFERRED: list[str] = []

SPELLED = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty-two|twenty-three"
BANNED: list[tuple[str, re.Pattern]] = [
    ("the /mcp-oauth-claude or /mcp-oauth-chatgpt route (never published)", re.compile(r"mcp-oauth-(?:claude|chatgpt)\b")),
    ("schedulePostTool (the tool is integrationSchedulePostTool)", re.compile(r"(?<![A-Za-z])schedulePostTool")),
    ("a tool count other than 21 or 20", re.compile(r"\b(?:1\d|2[2-9]|[3-9]\d)\s+(?:(?:MCP|hosted|PostQueen)\s+)?tools\b", re.I)),
    ("a spelled-out tool count", re.compile(rf"\b(?:{SPELLED})\s+(?:(?:MCP|hosted|PostQueen)\s+)?tools\b", re.I)),
    ("Windsurf (the product is Devin Desktop)", re.compile(r"windsurf", re.I)),
    ("Medium (the network was removed)", re.compile(r"\bMedium\b(?![- ](?:priority|size|risk|term))")),
    ("Settings > API Keys (the key is under Connections > API Keys)", re.compile(r"Settings\s*(?:→|>|->|&gt;|/)\s*API Keys", re.I)),
    ("app.postqueen.ai/settings as the key location", re.compile(r"app\.postqueen\.ai/settings(?![?\w/])")),
    ('"no card" (the trial takes a card)', re.compile(r"\bno (?:credit )?card\b", re.I)),
    ('"60-day" (refunds are 30 days)', re.compile(r"\b60-day\b", re.I)),
    ('"30 requests per hour" (no production number is published)', re.compile(r"\b30 requests (?:per|an|a) hour", re.I)),
    ('"ten connectors" (nine networks report analytics)', re.compile(r"\bten connectors\b", re.I)),
    ('"every network" (not every network can connect)', re.compile(r"\bevery network\b", re.I)),
    ("clipping (off in production, never documented)", re.compile(r"\bclipping\b", re.I)),
    ("veo3 (no such video type)", re.compile(r"veo3", re.I)),
]
FENCE_RE = re.compile(r"^(\s*)(```|~~~)[^\n]*\n(.*?)^\1\2", re.M | re.S)
COMMENT_RE = re.compile(r"\{/\*.*?\*/\}", re.S)
CHANNEL_STATUS_RE = re.compile(r"<ChannelStatus\s+status=\"([^\"]+)\"\s*>(.*?)</ChannelStatus>", re.S)
CHANNEL_STATUS_EMPTY_RE = re.compile(r"<ChannelStatus\s+status=\"([^\"]+)\"\s*/>")
AGENT_STATUS_RE = re.compile(r"<AgentStatus\b([^>]*?)/?>", re.S)
STATUS_KEY = {"works": "available", "review_gated": "in-review", "no_keys": "soon", "cannot_connect": "soon"}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def report(pending: bool, msg: str) -> None:
    (DEFERRED if pending and not RELEASE else ERRORS).append(msg)


def check_variables(facts: dict, docs: dict) -> None:
    var = docs.get("variables") or {}
    tiers = {t["id"]: t for t in facts["plans"]["tiers"]}
    addr = {a["id"]: a for a in facts["mcp"]["addresses"]}
    want = {
        "appUrl": facts["urls"]["app"],
        "apiBase": facts["urls"]["apiBase"],
        "mcpKeyUrl": addr["key"]["url"],
        "mcpOauthUrl": addr["signin"]["url"],
        "mcpToolsKey": str(facts["mcp"]["toolCount"]["key"]),
        "mcpToolsOauth": str(facts["mcp"]["toolCount"]["signin"]),
        "networks": str(facts["channelCounts"]["total"]),
        "trialDays": str(facts["trial"]["days"]),
        "refundDays": str(facts["refund"]["days"]),
        "priceCreator": f"${tiers['creator']['monthly']}",
        "priceGrowth": f"${tiers['growth']['monthly']}",
        "pricePro": f"${tiers['pro']['monthly']}",
        "priceUltimate": f"${tiers['ultimate']['monthly']}",
    }
    for key, value in want.items():
        if var.get(key) != value:
            ERRORS.append(f"docs.json variable {key} is {var.get(key)!r}, facts.json says {value!r}")
    for key in var:
        if "-" in key:
            ERRORS.append(f"docs.json variable {key} has a hyphen: Mintlify leaves {{{{{key}}}}} unreplaced")


def check_app_tools(facts: dict) -> None:
    if OFFLINE:
        print("check:facts: --offline, the app's tool list was not fetched")
        return
    try:
        with urllib.request.urlopen(TOOL_LIST_URL, timeout=30) as resp:
            source = resp.read().decode()
    except Exception as exc:  # noqa: BLE001
        # A Python without CA certificates (python.org builds on macOS) fails TLS; curl has them.
        try:
            source = subprocess.run(
                ["curl", "-fsSL", "--max-time", "30", TOOL_LIST_URL],
                check=True, capture_output=True, text=True,
            ).stdout
        except Exception:  # noqa: BLE001
            ERRORS.append(f"could not fetch the app's tool list ({exc}); run with --offline to skip")
            return
    body = re.search(r"toolList\s*=\s*\[(.*?)\]", source, re.S)
    if not body:
        ERRORS.append("could not find toolList in the app's tool.list.ts")
        return
    app = set(re.findall(r"\b([A-Z]\w+Tool)\b", body.group(1)))
    documented = {t["class"] for t in facts["mcp"]["tools"] if t["class"]}
    excluded = {t["class"] for t in facts["mcp"]["notInDocs"]}
    for cls in sorted(app - documented - excluded):
        ERRORS.append(f"the app has MCP tool {cls}, facts.json does not: re-run build_facts_json.py")
    for cls in sorted((documented | excluded) - app):
        ERRORS.append(f"facts.json has MCP tool {cls}, the app's tool.list.ts does not")


def scan_banned(rel: str, text: str, pending: bool) -> None:
    body = COMMENT_RE.sub("", text)
    for label, pattern in BANNED:
        for m in pattern.finditer(body):
            line = body.count("\n", 0, m.start()) + 1
            report(pending, f"{rel}:{line}: {label}: {m.group(0)!r}")
    for fence in FENCE_RE.finditer(body):
        code = fence.group(3)
        if "/public/v1" in code and re.search(r"Bearer", code):
            line = body.count("\n", 0, fence.start()) + 1
            report(pending, f"{rel}:{line}: Bearer in a /public/v1 example (the API takes the raw key)")


def check_numbers(rel: str, text: str, facts: dict, pending: bool) -> None:
    body = COMMENT_RE.sub("", text)
    tiers = {t["name"]: t for t in facts["plans"]["tiers"]}
    for m in re.finditer(r"\b(Creator|Growth|Pro|Ultimate)\b(?: plan)?[^$\n|]{0,12}\$(\d+)", body):
        tier = tiers[m.group(1)]
        if int(m.group(2)) not in (tier["monthly"], tier["yearly"]):
            report(pending, f"{rel}: {m.group(1)} at ${m.group(2)}, facts.json says ${tier['monthly']} a month or ${tier['yearly']} a year")
    for m in re.finditer(r"\b(\d+)[- ]day (?:free )?trial\b", body, re.I):
        if int(m.group(1)) != facts["trial"]["days"]:
            report(pending, f"{rel}: a {m.group(1)}-day trial, facts.json says {facts['trial']['days']}")
    for m in re.finditer(r"\brefund[^.\n]{0,80}?\b(\d+) days\b", body, re.I):
        if int(m.group(1)) != facts["refund"]["days"]:
            report(pending, f"{rel}: a refund within {m.group(1)} days, facts.json says {facts['refund']['days']}")


def check_channel(rel: str, text: str, channel: dict, pending: bool) -> None:
    want = STATUS_KEY[channel["status"]]
    found = CHANNEL_STATUS_RE.findall(text) or [(s, "") for s in CHANNEL_STATUS_EMPTY_RE.findall(text)]
    if not found:
        report(pending, f"{rel}: no <ChannelStatus> line (facts.json: {want})")
        return
    status, note = found[0]
    if status != want:
        report(pending, f"{rel}: ChannelStatus {status!r}, facts.json says {want!r}")
    if channel["statusNote"] and norm(note) != norm(channel["statusNote"]):
        report(pending, f"{rel}: the status note differs from facts.json statusNote: {channel['statusNote']!r}")


def check_agent(rel: str, text: str, agent: dict, pending: bool) -> None:
    found = AGENT_STATUS_RE.search(text)
    if not found:
        report(pending, f"{rel}: no <AgentStatus> line (facts.json: {agent['status']})")
        return
    attrs = dict(re.findall(r"(\w+)=\"([^\"]*)\"", found.group(1)))
    if attrs.get("status") != agent["status"]:
        report(pending, f"{rel}: AgentStatus status {attrs.get('status')!r}, facts.json says {agent['status']!r}")
    if norm(attrs.get("label", "")) != norm(agent["badge"]):
        report(pending, f"{rel}: AgentStatus label differs from facts.json badge {agent['badge']!r}")


def check_tools_page(text: str, facts: dict, pending: bool) -> None:
    body = COMMENT_RE.sub("", text)
    names = {t["name"] for t in facts["mcp"]["tools"]}
    for name in sorted(names):
        if not re.search(rf"`{re.escape(name)}`", body):
            report(pending, f"mcp/tools.mdx: tool {name} from facts.json is not documented")
    for name in sorted(set(re.findall(r"`([a-z][A-Za-z]+Tool)`", body)) - names):
        report(pending, f"mcp/tools.mdx: `{name}` is not an MCP tool in facts.json")


def main() -> int:
    facts = json.loads((ROOT / "facts" / "facts.json").read_text())
    docs = json.loads((ROOT / "docs.json").read_text())
    check_variables(facts, docs)
    check_app_tools(facts)

    channels = {c["docs"]: c for c in facts["channels"]}
    channels.update({c["api"]: c for c in facts["channels"]})
    agents = {a["docs"]: a for a in facts["agents"]}

    targets = []
    for path in sorted(ROOT.rglob("*.mdx")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("_templates/", ".github/", "node_modules/")):
            continue
        targets.append(path)
    targets.append(ROOT / "SKILL.md")

    pending_pages = 0
    for path in targets:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text()
        pending = MARKER in text
        pending_pages += pending
        scan_banned(rel, text, pending)
        if rel.startswith("snippets/") or rel == "SKILL.md":
            continue
        check_numbers(rel, text, facts, pending)
        slug = rel[:-4]
        if slug in channels:
            check_channel(rel, text, channels[slug], pending)
        if slug in agents:
            check_agent(rel, text, agents[slug], pending)
        if slug == "mcp/tools":
            check_tools_page(text, facts, pending)

    spec_path = ROOT / "public-api" / "openapi.json"
    spec_text = spec_path.read_text()
    spec_pending = '"x-overhaul-todo"' in spec_text
    for label, pattern in BANNED:
        for m in pattern.finditer(spec_text):
            line = spec_text.count("\n", 0, m.start()) + 1
            report(spec_pending, f"public-api/openapi.json:{line}: {label}: {m.group(0)!r}")

    if ERRORS:
        print("facts check failed:\n" + "\n".join(f"- {e}" for e in ERRORS))
        return 1
    mode = "release run" if RELEASE else "branch run"
    summary = (
        f"facts check ok ({mode}): docs.json variables and the MCP tools match facts.json; "
        f"{len(targets)} files scanned"
    )
    if DEFERRED:
        summary += (
            f"; {len(DEFERRED)} findings on {pending_pages} pages still marked {MARKER}"
            + (" and on openapi.json (x-overhaul-todo)" if spec_pending else "")
            + ", reported only (--verbose lists them)"
        )
    print(summary)
    if VERBOSE:
        print("\n".join(f"  pending: {d}" for d in DEFERRED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
