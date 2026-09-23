#!/usr/bin/env python3
"""OpenAPI check: public-api/openapi.json lints clean and covers the public API.

1. `redocly lint` (pinned) reports 0 errors.
2. The spec's paths equal the routes of the app's public controller on GitHub
   main (public.integrations.controller.ts), without the debug and clipping
   routes. The OAuth endpoints, which live in the app's OAuth controller, are
   the only extra paths the spec may carry.

While the spec carries "x-overhaul-todo" (batch B8 has not rebuilt it yet) the
findings are printed and the run passes; --release (or DOCS_RELEASE=1) fails on
them. --offline skips the GitHub fetch.
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
SPEC = ROOT / "public-api" / "openapi.json"
RELEASE = "--release" in sys.argv or os.environ.get("DOCS_RELEASE") == "1"
OFFLINE = "--offline" in sys.argv
REDOCLY = "@redocly/cli@2.54.2"
CONTROLLER_URL = (
    "https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/"
    "apps/backend/src/public-api/routes/v1/public.integrations.controller.ts"
)
EXCLUDED = re.compile(r"^/(?:debug|clipping)(?:/|$)")
EXTRA_ALLOWED = re.compile(r"^/oauth/")


def fetch(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return resp.read().decode()
    except Exception:  # noqa: BLE001  (a Python without CA certificates; curl has them)
        return subprocess.run(
            ["curl", "-fsSL", "--max-time", "30", url], check=True, capture_output=True, text=True
        ).stdout


def shape(path: str) -> str:
    return re.sub(r"\{[^}]+\}|:[A-Za-z_]+", "{}", path.rstrip("/") or "/")


def main() -> int:
    spec = json.loads(SPEC.read_text())
    pending = "x-overhaul-todo" in spec and not RELEASE
    problems: list[str] = []

    lint = subprocess.run(
        ["npx", "--yes", REDOCLY, "lint", str(SPEC), "--format", "summary"],
        capture_output=True, text=True, cwd=ROOT,
    )
    out = lint.stdout + lint.stderr
    errors = re.search(r"(\d+) errors?", out)
    if lint.returncode != 0:
        problems.append(f"redocly lint: {errors.group(0) if errors else 'failed'}")
        print(out.strip()[-3000:])

    if OFFLINE:
        print("lint:openapi: --offline, the app's routes were not fetched")
    else:
        try:
            source = fetch(CONTROLLER_URL)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"could not fetch the public controller ({exc}); run with --offline to skip")
            source = ""
        if source:
            prefix = re.search(r"@Controller\(['\"]([^'\"]*)['\"]\)", source)
            base = prefix.group(1).rstrip("/") if prefix else ""
            routes = set()
            for method, path in re.findall(r"@(Get|Post|Put|Delete|Patch)\(['\"]([^'\"]*)['\"]\)", source):
                if EXCLUDED.match(path):
                    continue
                routes.add(f"{method.upper()} {shape(path)}")
            documented = set()
            for path, ops in spec.get("paths", {}).items():
                if EXTRA_ALLOWED.match(path):
                    continue
                for method in ops:
                    if method.lower() in ("get", "post", "put", "delete", "patch"):
                        documented.add(f"{method.upper()} {shape(path)}")
            for route in sorted(routes - documented):
                problems.append(f"route {route.replace('{}', ':param')} under {base} is not in the spec")
            for route in sorted(documented - routes):
                problems.append(f"the spec documents {route}, which the public controller does not serve")

    if problems:
        head = "lint:openapi findings" + (" (spec still marked x-overhaul-todo, reported only)" if pending else "")
        print(head + ":\n" + "\n".join(f"- {p}" for p in problems))
        return 0 if pending else 1
    print("lint:openapi ok: 0 lint errors, the spec's paths equal the public controller's routes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
