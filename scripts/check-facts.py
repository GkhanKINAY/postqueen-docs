#!/usr/bin/env python3
"""Facts check: the numbers and names the docs repeat, against facts/facts.json.

1. docs.json variables equal facts.json (prices, trial days, the refund window
   and the withdrawal days, tool counts, the MCP and API addresses, the network
   count).
2. facts.json's MCP tools equal the app's tool list on GitHub main
   (tool.list.ts, raw fetch), minus the classes facts.json keeps out of the docs.
3. Banned strings: removed routes and tools, wrong tool counts, Windsurf, Medium,
   the old API key location, trial and rate-limit claims that are not true,
   Bearer on the public API, veo3, the removed withdrawal waiver, a year of
   credits at once.
4. Channel and agent pages describe the product in production (owner,
   2026-09-24): no status line or Soon/In review tag on a network, no platform-review
   note ("In review", "testers", "until Meta approves" ...), no agent test status.
5. mcp/tools names exactly facts.json's tools.
6. Prices, trial days, refund and withdrawal days and monthly credits written in
   a page equal facts.json, and no page promises a refund the rule does not
   give (Terms section 9, owner 2026-10-21): a full refund of any charge, yearly
   charges treated like monthly ones, or a refund that leaves the plan running.
   Accounts created before the current Terms keep their earlier promise (a full
   refund within 30 days), so a sentence with "Accounts created before" may say it.

Checks 3 to 6 run on every page without an OVERHAUL-TODO marker (check 3 also
on the snippets and on SKILL.md); pages still marked, and openapi.json while it carries
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

SPELLED = "ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-three|twenty-four|twenty-five"
BANNED: list[tuple[str, re.Pattern]] = [
    ("the /mcp-oauth-claude or /mcp-oauth-chatgpt route (never published)", re.compile(r"mcp-oauth-(?:claude|chatgpt)\b")),
    ("schedulePostTool (the tool is integrationSchedulePostTool)", re.compile(r"(?<![A-Za-z])schedulePostTool")),
    ("a tool count other than 25 or 24", re.compile(r"\b(?:1\d|2[0-3]|2[6-9]|[3-9]\d|\d{3,})(?:\s+|-)(?:(?:MCP|hosted|PostQueen)\s+)*tools?\b", re.I)),
    ("a spelled-out tool count", re.compile(rf"\b(?:{SPELLED})(?:\s+|-)(?:(?:MCP|hosted|PostQueen)\s+)*tools?\b", re.I)),
    ("Windsurf (the product is Devin Desktop)", re.compile(r"windsurf", re.I)),
    # **Medium** in bold is the AI image quality label, not the network.
    ("Medium (the network was removed)", re.compile(r"(?<!\*\*)\bMedium\b(?!\*\*)(?![- ](?:priority|size|risk|term))")),
    # The retired network. Lemmy's and Farcaster's lowercase `subreddit` field and
    # `subreddits` tool are API names and stay allowed.
    ("Reddit (the network was removed)", re.compile(r"(?<!sub)reddit", re.I)),
    ("Subreddit as a product noun (the network was removed)", re.compile(r"\bSubreddits?\b")),
    ("flairs (the network was removed)", re.compile(r"\bflairs?\b", re.I)),
    ("Settings > API Keys (the key is under Connections > API key)", re.compile(r"Settings\s*(?:→|>|->|&gt;|/)\s*API Keys", re.I)),
    ("app.postqueen.ai/settings as the key location", re.compile(r"app\.postqueen\.ai/settings(?![?\w/])")),
    ('"no card" (the trial takes a card)', re.compile(r"\bno (?:credit )?card\b", re.I)),
    ('"60-day" (no 60-day refund or withdrawal exists)', re.compile(r"\b60-day\b", re.I)),
    ("the withdrawal waiver (checkout no longer asks anyone to give up the right of withdrawal, owner 2026-10-21)",
     re.compile(r"\blose my 14-day right\b|\bright to withdraw once I use\b|\bconsent box\b", re.I)),
    ("a year of credits at once (plans bought from the current Terms add credits once a month; a yearly plan bought "
     "before gets \"the whole year's credits\" at the start of each yearly period)",
     re.compile(r"\b(?:twelve|12) months of credits\b|\b(?:a |the |full )year of credits\b", re.I)),
    ('"ten connectors" (nine networks report analytics)', re.compile(r"\bten connectors\b", re.I)),
    ("api.postqueen.ai/docs (the internal Swagger list, never linked)", re.compile(r"api\.postqueen\.ai/docs\b")),
    ("veo3 (no such video type)", re.compile(r"veo3", re.I)),
    ("monthly AI image or video counts (plans add credits now)", re.compile(r"\bAI (?:images|videos) a month\b|\b(?:image|video) credits?\b", re.I)),
    ("an old AI quota message (the 402 is Not enough credits)", re.compile(r"out of AI credits for this month|maximum number of generated videos|No AI video credits are available", re.I)),
    ("an X analytics add-on (none exists)", re.compile(r"\bX analytics add-on\b|\banalytics add-on\b", re.I)),
]
FENCE_RE = re.compile(r"^([ \t]*)(```|~~~)[^\n]*\n(.*?)^\1\2", re.M | re.S)
COMMENT_RE = re.compile(r"\{/\*.*?\*/\}", re.S)
CHANNEL_STATUS_RE = re.compile(r"<ChannelStatus\s+status=\"([^\"]+)\"\s*>(.*?)</ChannelStatus>", re.S)
CHANNEL_STATUS_EMPTY_RE = re.compile(r"<ChannelStatus\s+status=\"([^\"]+)\"\s*/>")
AGENT_STATUS_RE = re.compile(r"<AgentStatus\b", re.S)
TEST_NOTE_RE = re.compile(r"\bnot tested\b|\buntested\b|\bnot possible yet\b|\bkey tested\b|\bpartly tested\b", re.I)
OWN_WORDS = {"PostQueen", "The", "A", "Your", "On", "Or", "And", "To", "From"}
REVIEW_NOTE_RE = re.compile(
    r"(?<!week )\bin review\b|\btesters?\b|\buntil (?:Meta|TikTok|Google)\b|\bSelf only until\b|\bopens soon\b"
    r"|\bcannot (?:be )?connect(?:ed)? (?:on PostQueen )?yet\b|\bapproves PostQueen'?s app\b", re.I)
STATUS_TAG_RE = re.compile(r'^tag: "(?:Soon|In review)"', re.M)
# Accounts created before the current Terms keep their earlier refund promise (owner, 2026-10-21).
LEGACY_ACCOUNTS_RE = re.compile(r"\baccounts? created before\b", re.I)


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
        "mcpBearerUrl": addr["bearer"]["url"],
        "mcpOauthUrl": addr["signin"]["url"],
        "mcpToolsKey": str(facts["mcp"]["toolCount"]["key"]),
        "mcpToolsOauth": str(facts["mcp"]["toolCount"]["signin"]),
        "networks": str(facts["channelCounts"]["total"]),
        "trialDays": str(facts["trial"]["days"]),
        "refundWindowDays": str(facts["refund"]["refundWindowDays"]),
        "withdrawalDays": str(facts["refund"]["withdrawalDays"]),
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
        if re.search(r"/public/v1|\{\{apiBase\}\}", code) and re.search(r"Bearer", code):
            line = body.count("\n", 0, fence.start()) + 1
            report(pending, f"{rel}:{line}: Bearer in a /public/v1 example (the API takes the raw key)")


def check_variable_use(rel: str, text: str, names: set[str], pending: bool) -> None:
    """A {{variable}} that docs.json does not define reaches the reader as written."""
    body = COMMENT_RE.sub("", text)
    for m in re.finditer(r"\{\{([A-Za-z]\w*)\}\}", body):
        if m.group(1) not in names:
            line = body.count("\n", 0, m.start()) + 1
            report(pending, f"{rel}:{line}: {{{{{m.group(1)}}}}} is not a docs.json variable")


def check_numbers(rel: str, text: str, facts: dict, pending: bool) -> None:
    body = COMMENT_RE.sub("", text)
    tiers = {t["name"]: t for t in facts["plans"]["tiers"]}
    for m in re.finditer(r"\b(Creator|Growth|Pro|Ultimate)\b(?: plan)?[^$\n|]{0,12}\$(\d+)", body):
        # "Claude Pro", "Hashnode Pro": another product's plan, not PostQueen's
        before = re.search(r"([A-Za-z][\w.]*)\s+$", body[max(0, m.start() - 30):m.start()])
        if before and before.group(1)[0].isupper() and before.group(1) not in OWN_WORDS:
            continue
        tier = tiers[m.group(1)]
        if int(m.group(2)) not in (tier["monthly"], tier["yearly"]):
            report(pending, f"{rel}: {m.group(1)} at ${m.group(2)}, facts.json says ${tier['monthly']} a month or ${tier['yearly']} a year")
    # A plan's credits: "Pro ... 500 credits a month" on one line or table row.
    for m in re.finditer(r"\b(Creator|Growth|Pro|Ultimate)\b[^\n]{0,60}?\b([\d,]+) credits a month\b", body):
        want = tiers[m.group(1)]["monthlyCredits"]
        if int(m.group(2).replace(",", "")) != want:
            report(pending, f"{rel}: {m.group(1)} with {m.group(2)} credits a month, facts.json says {want}")
    for m in re.finditer(r"\b(\d+)[- ]day (?:free )?trial\b", body, re.I):
        if int(m.group(1)) != facts["trial"]["days"]:
            report(pending, f"{rel}: a {m.group(1)}-day trial, facts.json says {facts['trial']['days']}")
    refund = facts["refund"]
    window, withdrawal = refund["refundWindowDays"], refund["withdrawalDays"]
    for m in re.finditer(r"\brefund[^.\n]{0,80}?\b(\d+) days\b", body, re.I):
        days = int(m.group(1))
        if days in (window, withdrawal):
            continue
        if days == refund["legacyAccountsRefundDays"] and LEGACY_ACCOUNTS_RE.search(sentence(body, m)):
            continue
        report(pending, f"{rel}: a refund within {days} days, facts.json says {window} (the refund rule) or {withdrawal} (withdrawal); "
                        f"{refund['legacyAccountsRefundDays']} only in a sentence about accounts created before the current Terms")
    for m in re.finditer(r"\bwithdraw\w*[^.\n]{0,60}?\b(\d+) days\b|\b(\d+)-day right (?:of|to) withdraw", body, re.I):
        days = int(m.group(1) or m.group(2))
        if days != withdrawal:
            report(pending, f"{rel}: withdrawal within {days} days, facts.json says {withdrawal}")
    for label, pattern in refund_claims(refund):
        for m in pattern.finditer(body):
            if LEGACY_ACCOUNTS_RE.search(sentence(body, m)):
                continue
            line = body.count("\n", 0, m.start()) + 1
            report(pending, f"{rel}:{line}: {label}: {m.group(0)!r}")


def sentence(body: str, m: re.Match) -> str:
    """The sentence a match sits in: from the last full stop or line break before it to the next one after it."""
    start = max(body.rfind(". ", 0, m.start()), body.rfind("\n", 0, m.start())) + 1
    ends = [i for i in (body.find(".", m.end()), body.find("\n", m.end())) if i != -1]
    return body[start:min(ends) if ends else len(body)]


def refund_claims(refund: dict) -> list[tuple[str, re.Pattern]]:
    """Wording that promises more than the refund rule in facts.json gives. A sentence about
    accounts created before the current Terms may still state their earlier promise."""
    claims = []
    if refund["oneMonthMax"]:
        claims.append((
            "a full refund of any charge (the rule is at most one month's plan fee per account)",
            re.compile(r"\b(?:any|every) charge (?:is )?refunded in full\b|\brefunds? (?:any|every) charge in full\b", re.I),
        ))
    if not refund["yearlyUnderRule"]:
        claims.append((
            "yearly charges refunded like monthly ones (the rule does not cover yearly charges)",
            re.compile(r"\bmonthly(?:,| and) yearly\b[^.\n]{0,60}\btreated the same\b", re.I),
        ))
    if refund["fullRefundEndsPlan"]:
        claims.append((
            "a refund that leaves the plan running (a full refund of the current period ends the plan)",
            re.compile(r"\brefund on its own does not cancel\b", re.I),
        ))
    return claims


def check_channel(rel: str, text: str, channel: dict, pending: bool) -> None:
    """Channel pages describe the network in production (owner, 2026-09-24): no
    status line or tag, no platform-review note."""
    body = COMMENT_RE.sub("", text)
    if CHANNEL_STATUS_RE.search(body) or CHANNEL_STATUS_EMPTY_RE.search(body) or STATUS_TAG_RE.search(body):
        report(pending, f"{rel}: a channel status line or tag; channel pages carry none")
    check_review_notes(rel, body, pending)


def check_review_notes(rel: str, body: str, pending: bool) -> None:
    for m in REVIEW_NOTE_RE.finditer(body):
        line = body.count("\n", 0, m.start()) + 1
        report(pending, f"{rel}:{line}: a platform-review note {m.group(0)!r}; describe the production state")


def check_agent(rel: str, text: str, agent: dict, pending: bool) -> None:
    """Agent pages say how to connect, not what PostQueen has tested: no status
    line, no "not tested" or "untested" note (owner, 2026-09-24)."""
    body = COMMENT_RE.sub("", text)
    if AGENT_STATUS_RE.search(body):
        report(pending, f"{rel}: an <AgentStatus> line; agent pages carry no test status")
    for m in TEST_NOTE_RE.finditer(body):
        report(pending, f"{rel}: a test-status note {m.group(0)!r}; agent pages carry none")
    check_review_notes(rel, body, pending)


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
        check_variable_use(rel, text, set(docs.get("variables") or {}), pending)
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
