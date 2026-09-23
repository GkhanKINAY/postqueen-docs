# Contributing to the PostQueen docs

The docs at [docs.postqueen.ai](https://docs.postqueen.ai/introduction) are built by Mintlify from this repository.
Every page is an `.mdx` file, and [`docs.json`](docs.json) holds the navigation, the theme and the redirects.

## Run it locally

The Mintlify CLI needs Node.js 22.

```bash
npm i -g mint
mint dev                 # http://localhost:3000
```

Pull request previews are not on the current Mintlify plan, so check a change in `mint dev` before you merge it. Look
at it at 1440 and 390 pixels wide, in the light and the dark theme.

## Checks

Run them all before you push. CI runs the same ones on every push and pull request.

| Command | What it checks |
|---|---|
| `npm run check` | Navigation, orphans, redirects, snippet imports, card icons, internal links, frontmatter (title, description, and an icon except on endpoint pages), alt text, no em dash, no self-hosting words outside the Self-hosting tab |
| `npm run check:facts` | Banned facts (old tool counts, removed routes, the old API key location and more), channel and agent status lines against `facts/facts.json`, the MCP tool list against the app, prices, trial and refund numbers and the `docs.json` variables against `facts/facts.json` |
| `npm run validate` | `mint validate`: the build, failing on warnings |
| `npm run links` | `mint broken-links` |
| `npm run a11y` | `mint a11y`: contrast and alt text |
| `npm run lint:openapi` | `public-api/openapi.json` with Redocly, and its paths against the app's public routes |

`npm run check:release` is the release run: every rule on every page, and a failure on any `OVERHAUL-TODO` marker.
CI runs its checks in release mode (`DOCS_RELEASE=1`) for pushes to `main` and pull requests into `main`.

## Where things live

| Path | What it is |
|---|---|
| `introduction.mdx`, `quickstart.mdx`, `using/`, `channels/` | Guide tab |
| `agents/`, `mcp/`, `cli/` | AI agents tab |
| `public-api/` | API tab; `public-api/openapi.json` drives the endpoint pages and the playground |
| `cloud/` | Plans and billing tab |
| `support.mdx`, `faq.mdx`, `troubleshooting/`, `security-and-privacy.mdx` | Help tab (`troubleshooting/self-host` belongs to Self-hosting) |
| `installation/`, `reverse-proxies/`, `configuration/` | Self-hosting tab |
| `snippets/` | Reusable blocks, imported into pages |
| `facts/facts.json` | The facts pages repeat: prices, trial, refund, MCP addresses and tools, channel and agent status. Generated, never edited by hand |
| `_templates/` | Page templates to copy. Listed in `.mintignore`, so Mintlify never publishes them |
| `style.css`, `fonts/`, `logo/`, `images/og/` | The theme |

## Style guide

### Voice

- Write "PostQueen", never "she" or "her". No persona.
- US English. Plain sentences. No em dashes: use a comma, a colon or a new sentence.
- No narrative openers ("Imagine...", "Let's...") and no marketing adjectives. Say what happens.
- Say **channel**, not integration, on user pages. The API's word is integration; the app-at-a-glance page maps the
  two once.
- Current product names only: Devin Desktop, never "formerly Windsurf". No rename notes.

### Page shape

- Start every page from its template in `_templates/`: `guide-task.mdx`, `channel.mdx`, `agent.mdx` or
  `api-settings.mdx`. Keep the section order.
- Guide task pages run 300 to 600 words and open with a **Where:** line naming the screen.
- Quote the app's labels in bold exactly as the app's English strings show them, and error messages exactly.
- At most one screenshot per page, taken from a throwaway local stack with demo channels, never from a real account.
- Frontmatter always has `title`, `description` and `icon`. Endpoint pages (`openapi:`) skip the icon: the sidebar shows the method instead.

### Facts

- Say what is true today. A network that cannot connect is **Soon**; one limited by the platform's review is
  **In review** with the limit in one sentence. An agent page says whether PostQueen tested it.
- Every number has one owner. Prices, the trial, the refund window and tool counts come from `docs.json` variables
  (`{{trialDays}}`, `{{refundDays}}`, `{{priceCreator}}`, `{{mcpToolsKey}}`, `{{mcpToolsOauth}}`, `{{mcpKeyUrl}}`,
  `{{mcpBearerUrl}}`, `{{apiBase}}` ...), or the page links to the page that owns the fact.
- The status line under a channel or agent title is the `ChannelStatus` or `AgentStatus` snippet, with the values in
  `facts/facts.json`. `check:facts` compares them.
- Examples use networks that work today (Bluesky, WordPress, DEV, Nostr). A network in review appears only with its
  note.
- User tabs (Guide, AI agents, API, Plans and billing, Help) never mention self-hosting, PostQueen as open source,
  AGPL, Docker, `.env` or a server environment variable (`scripts/env-names.txt`). The CLI's `POSTQUEEN_API_KEY` is
  fine. The docs home carries the one fork line and the one link to Self-hosting.
- Never document `/mcp-oauth-claude` or `/mcp-oauth-chatgpt`. Clipping is documented, as **Soon** until the app
  switches it on. The API key is under
  **Connections > API Keys**, and only a workspace Admin or Super Admin can reveal it.
- API examples send the raw key: `Authorization: YOUR_API_KEY`, never `Bearer` on `/public/v1`.

### Mintlify mechanics that bite

- **Snippets are imported, never included with `<Snippet file>`**, which renders nothing:
  `import NeverShare from '/snippets/never-share.mdx';` then `<NeverShare />`. Component snippets export by name:
  `import { ChannelStatus } from '/snippets/status-badge.mdx';`.
- **Variable names are camelCase.** Mintlify leaves `{{trial-days}}` unreplaced and the MDX parser then fails on it.
  An expression that is not a variable, such as n8n's `{{ $json.id }}`, is safe inside a code block only.
- **A bare URL inside a JSX link becomes a second link.** Mintlify autolinks `https://...` text, and a link inside
  `<a>` breaks hydration. Write it as `{"https://..."}` there.
- **Tables inside JSX are markdown tables**, with blank lines around them. A hand-written `<table>` with line breaks
  between rows breaks hydration.
- `<footer>` is dropped from MDX. Use a `<div>`.
- **Icons are Lucide names** (`icons.library` is `lucide`, Mintlify serves v1.16.0). Lucide draws no brand marks: a
  card that needs a network's logo uses its file in `/images/channels/`.
- Internal links point at the page's current path, never at a redirect source. `npm run check` fails on a link through
  a redirect.
- Every image has alt text. Wrap illustrations in `<Frame>`.

### Moving or removing a page

Add a redirect to `docs.json` for the old path in the same change, and point every internal link at the new path.
The app links about forty docs paths; those must keep resolving.

## The overhaul

On the `docs/overhaul` branch every page that still waits for its rewrite carries a marker right after its
frontmatter:

```mdx
{/* OVERHAUL-TODO(B7): write it from _templates/agent.mdx. Sources: ... */}
```

The batch named in the marker owns the page. `grep -rl "OVERHAUL-TODO(B7)" --include="*.mdx" .` lists a batch's
pages. Remove the marker when the page is done: from then on the page must pass every rule above, and the relaxed
checks that marked pages get stop applying to it. A release run fails while any marker is left.

## Pull requests

Follow [the pull request template](.github/PULL_REQUEST_TEMPLATE.md). Report a mistake in the docs as an issue here,
and a bug in the app on [postqueen-app](https://github.com/GkhanKINAY/postqueen-app/issues).
