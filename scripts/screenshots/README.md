# Screenshot pipeline

Capture **one dark-theme screenshot per docs page** (Postiz-style). Agents brand SVGs stay in the docs; this pipeline is for product UI shots in the User Guide.

This PR ships the script and this README. It does **not** fail CI when you have no login. Do not block a docs merge on missing Cloud credentials.

## What you need

- Node 20+
- Playwright (`npx playwright install chromium`)
- A PostQueen Cloud (or staging) account
- Optional env:

| Variable | Default | Purpose |
|---|---|---|
| `PQ_APP_URL` | `https://app.postqueen.ai` | App origin |
| `PQ_EMAIL` | unset | Login email |
| `PQ_PASSWORD` | unset | Login password |
| `PQ_STORAGE_STATE` | unset | Playwright `storageState` JSON if you already have a session |
| `PQ_OUT` | `scripts/screenshots/out` | Output directory |

If neither `PQ_STORAGE_STATE` nor both login vars are set, the script prints how to capture and exits **0**.

## Run

```bash
cd postqueen-docs
npx playwright install chromium
PQ_EMAIL='you@example.com' PQ_PASSWORD='…' node scripts/screenshots/capture.mjs
```

Or pass a saved session:

```bash
PQ_STORAGE_STATE=./playwright.auth.json node scripts/screenshots/capture.mjs
```

Shots land in `scripts/screenshots/out/` as `{slug}.png`. Copy the ones you want into `images/guide/` (create that folder when you first commit real UI) and reference one `<Frame>` per page.

## Rules

- Dark appearance (`body.dark` / app dark class)
- Viewport 1440×900
- One shot per listed route
- Keep existing brand SVGs on Agents pages
- Provider OAuth PNGs stay under `images/providers/` for Self-Hosting
