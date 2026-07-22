<p align="center">
  <a href="https://postqueen.ai">
    <img src=".github/assets/header.svg" width="840" alt="PostQueen: the queen of your posts, your AI social media assistant" />
  </a>
</p>

<h3 align="center">🆕&nbsp; NEW: run your social media by talking to your AI. Plan, generate and schedule a whole month of content to 30+ networks just by asking, then review it all in a visual calendar.</h3>

<br/>

<div align="center">
  <p>
    <strong>Stop writing posts by hand.</strong> Tell PostQueen what is going on (a sale, a new product, a<br/>
    milestone) and she finds the best hook, picks a photo with colors that fit your brand, writes it for<br/>
    every platform, and lines it up on your calendar. A social media manager for you or your whole team,<br/>
    a content creator or a business, that never sleeps.
  </p>
  <p><strong>PostQueen</strong>: an open-source alternative to <strong>Buffer, Hootsuite, Sprout Social, Later</strong> and more.</p>
</div>

<br/>

<p align="center">
  <a href="https://postqueen.ai">Website</a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/pricing">Pricing</a> &nbsp;·&nbsp;
  <a href="https://docs.postqueen.ai">Docs</a> &nbsp;·&nbsp;
  <a href="https://api.postqueen.ai/docs">API Reference</a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/agent">Agents</a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/mcp">MCP</a> &nbsp;·&nbsp;
  <a href="https://www.npmjs.com/package/postqueen">CLI</a>
</p>

<p align="center">
  <a href="https://github.com/GkhanKINAY/postqueen-docs/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/postqueen"><img src="https://img.shields.io/npm/v/postqueen?label=CLI&color=6d28d9" alt="CLI on npm"></a>
  <a href="https://www.npmjs.com/package/@postqueen/node"><img src="https://img.shields.io/npm/v/@postqueen/node?label=SDK&color=7c3aed" alt="SDK on npm"></a>
  <a href="https://www.npmjs.com/package/n8n-nodes-postqueen"><img src="https://img.shields.io/npm/v/n8n-nodes-postqueen?label=n8n&color=e0189e" alt="n8n node on npm"></a>
  <a href="https://github.com/GkhanKINAY/postqueen-docs/commits/main"><img src="https://img.shields.io/github/commit-activity/m/GkhanKINAY/postqueen-docs" alt="Commit activity"></a>
</p>

<p align="center">
  <img src=".github/assets/channels.svg" width="780" alt="Publishes to 30+ social networks" />
</p>

<p align="center">
  <a href="https://postqueen.ai"><img src=".github/assets/cta-cloud.svg" height="48" alt="Start free for 7 days" /></a>
  &nbsp;&nbsp;
  <a href="https://github.com/GkhanKINAY/postqueen-docker-compose"><img src=".github/assets/cta-selfhost.svg" height="48" alt="Self-host it free" /></a>
</p>

<p align="center">
  <a href="https://postqueen.ai/pricing"><strong>See pricing »</strong></a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://docs.postqueen.ai"><strong>Explore the docs »</strong></a>
</p>

---

## 👑 Everything PostQueen does for you

<p align="center">
  <img src=".github/assets/features.svg" width="880" alt="Scheduling, AI Assistant, AI Design, AI Video, Auto Actions, Teamwork, Analytics, Cross-posting" />
</p>

All of it is real, and all of it is yours to run: PostQueen is fully open-source, so you can use the managed cloud or host the whole thing yourself.

---

## 💬 Just talk to your AI

Think of PostQueen as the social media manager on your team, one you simply talk to. Tell her what is happening and she does the thinking: she finds a hook that fits your topic, picks an image with colors that match your brand, writes a version for each platform, and drops it on your calendar. Ask her in plain words, in **your own language** (PostQueen speaks 16 languages, Turkish included), by text or, if your assistant supports voice, hands-free by speaking.

Just say what you want:

> *"Plan a month of content for our coffee shop and fill the calendar."*

> *"Take this photo of today's special and put it on Instagram at lunchtime."*

> *"We just hit 10k followers, write a warm thank-you post for all our channels."*

> *"Turn my latest YouTube video into posts for X, LinkedIn and Threads."*

**You stay in control.** Everything lands in your calendar first, so you can read it, tweak it, or delete it before it goes out. Prefer to sign off on every single post? Ask her to save them as drafts, and nothing publishes until you schedule it yourself.

<br/>

<p align="center">
  <img src=".github/assets/works-with.svg" width="760" alt="Works with Claude Code, ChatGPT, Cursor, OpenClaw, Hermes, Codex" />
</p>

Already using an AI assistant? Point it at PostQueen and it drives everything over the same Agent CLI and hosted MCP server.

### Claude Code

> *"Announce our new summer menu on X and Instagram tomorrow at noon, and use the photo in `./menu.jpg`."*

Claude Code connects over the CLI or MCP and does the work for you:

```bash
postqueen integrations:list
postqueen upload ./menu.jpg
postqueen posts:create \
  -c "Our summer menu is here 🌞" \
  -m "<uploaded-url>" \
  -s "2026-06-01T12:00:00Z" \
  -i "<instagram-id>"
```

[Claude Code integration »](https://postqueen.ai/claude-code)

### ChatGPT

> *"Write a fun post about our weekend sale, make a matching image, and schedule it for Friday morning on Instagram and Facebook."*

Draft and refine in ChatGPT, then let it publish everywhere through the MCP connector. [ChatGPT integration »](https://postqueen.ai/chatgpt)

### Cursor

> *"Turn our latest blog post into three posts and space them across next week."*

Run your channels without leaving the editor you build in. [Cursor integration »](https://postqueen.ai/cursor)

### OpenClaw

> *"Create a week of gym content: a tip, a quote and a class reminder, and schedule them all."*

Message it from WhatsApp, Telegram, Slack or Discord and it works hands-free. [OpenClaw integration »](https://postqueen.ai/openclaw)

### Hermes

> *"Every Monday, plan the week's posts for our bakery and fill the calendar."*

Hand your whole posting routine to an agent that plans and runs multi-step tasks. [Hermes integration »](https://postqueen.ai/hermes-agent)

### Codex

> *"Draft a short daily tip for our brand and schedule one for each morning next week."*

OpenAI's software agent: one prompt in, a scheduled week out. [Codex integration »](https://postqueen.ai/codex)

**And any other agent.** PostQueen's CLI and MCP server are model-agnostic, so any MCP client or command-running agent works too: **Gemini CLI, Aider, Cline, Warp, Windsurf**, or your own scripts.

---

## 🌐 Supported networks

PostQueen publishes to **30+ social networks** out of the box:

<p align="center">
  <img src=".github/assets/channels.svg" width="820" alt="Supported social networks" />
</p>

- **Major social:** X, LinkedIn, Instagram, Facebook, TikTok, YouTube, Threads, Pinterest, Reddit, Bluesky
- **Community & chat:** Discord, Slack, Telegram, Mastodon, Twitch, Kick, MeWe, VK
- **Publishing & blogs:** WordPress, Medium, Dev.to, Hashnode, Tumblr, Listmonk, Moltbook
- **Web3 & decentralized:** Nostr, Farcaster, Lemmy
- **Creator & business:** Google Business Profile, Whop, Skool, Dribbble

LinkedIn and Instagram each support both personal and page posting, so the number of connectors runs a little higher. New connectors ship regularly.

---

## 🚀 Get started

PostQueen is **fully open-source (AGPL-3.0)**. Pick whichever way suits you:

### ☁️ Cloud

The fastest way to start: connect your channels and schedule your first post in minutes, with a **7-day free trial** and nothing to run yourself. [Start free »](https://postqueen.ai)

### 🐳 Self-host

Own your data and run the whole stack for free. You will need Docker, about 4 GB of RAM, and a domain with TLS (social networks send their OAuth callbacks there).

```bash
git clone https://github.com/GkhanKINAY/postqueen-docker-compose
cd postqueen-docker-compose
# open docker-compose.yaml and set a unique JWT_SECRET and your public URLs
docker compose up -d          # then open http://localhost:4007
```

The stack runs the app, PostgreSQL, Redis and a Temporal cluster (the engine that publishes on time). For the full walkthrough see the [self-host guide](https://docs.postqueen.ai/quickstart), for Kubernetes see [postqueen-helmchart](https://github.com/GkhanKINAY/postqueen-helmchart), and every setting is documented in the [configuration reference](https://docs.postqueen.ai/configuration/reference).

---

## 🧱 Tech stack

- **pnpm workspaces** (monorepo)
- **[Next.js](https://nextjs.org)** (React) for the frontend
- **[NestJS](https://nestjs.com)** for the backend API
- **[Prisma](https://www.prisma.io)** (default: PostgreSQL)
- **[Temporal](https://temporal.io)** for scheduling and publishing workers
- **Redis** for cache and queues
- **[Resend](https://resend.com)** for email notifications

---

## 🔑 Get your API key

You will need an API key to use the CLI, the MCP server, the SDK or the public API. It takes a minute:

1. Open **[app.postqueen.ai/settings](https://app.postqueen.ai/settings)** (or your own self-hosted instance).
2. Go to **Developers → Public API**.
3. Click **Reveal** to show your key.
4. Copy it and set it in your shell:

```bash
export POSTQUEEN_API_KEY="your_api_key"
```

Keep it secret: it grants full access to your account. You can revoke or rotate it any time from the same screen.

---

## 🔌 Connect over MCP

The [Model Context Protocol](https://modelcontextprotocol.io) lets AI assistants call tools. PostQueen ships a hosted MCP server, so any MCP client can draft, schedule and manage posts as if it were built in.

**One line (Claude Code or any CLI client):**

```bash
claude mcp add --transport http postqueen https://api.postqueen.ai/mcp/<YOUR_API_KEY>
```

**Config-file clients (Claude Desktop, Cursor, and others):**

```json
{
  "mcpServers": {
    "postqueen": {
      "url": "https://api.postqueen.ai/mcp/<YOUR_API_KEY>"
    }
  }
}
```

**ChatGPT:** Settings → Connectors → add a custom connector pointing at `https://api.postqueen.ai/mcp/<YOUR_API_KEY>`. Full guide: [postqueen.ai/mcp](https://postqueen.ai/mcp).

---

## 🤖 Build your own agent

Because every action is a public API call, you can point your own agent at PostQueen and let it plan, draft and schedule on a schedule you set. A simple recurring job can wake up, decide what to post, and queue it. Start from the [Agent CLI](https://postqueen.ai/agent) or [MCP](https://postqueen.ai/mcp) guides.

---

## 🧩 Public API, SDK & n8n

| Tool | What it is | Get started |
| --- | --- | --- |
| **Public API** | REST at `https://api.postqueen.ai/public/v1` | [API reference](https://api.postqueen.ai/docs) |
| **NodeJS SDK** | Typed client for Node | [`@postqueen/node`](https://www.npmjs.com/package/@postqueen/node) |
| **n8n node** | No-code automation node | [`n8n-nodes-postqueen`](https://www.npmjs.com/package/n8n-nodes-postqueen) |
| **Webhooks** | Get notified when posts publish | [docs](https://docs.postqueen.ai) |

```bash
curl https://api.postqueen.ai/public/v1/integrations \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

Plug the same API into Make.com, Zapier or your own scripts.

---

# Public API cheat-sheet

A quick reference for the most common Public API calls. The full reference lives in [`public-api/introduction`](public-api/introduction.mdx) and the live Swagger at [api.postqueen.ai/docs](https://api.postqueen.ai/docs).

## Setup

1. **Get your API key:** [app.postqueen.ai/settings](https://app.postqueen.ai/settings) (Developers → Public API → Reveal).
2. Set it as an environment variable:
   ```bash
   export POSTQUEEN_API_KEY="your-api-key"
   ```

Include the key in the `Authorization` header on every request.

## Get all added channels

```bash
curl -X GET "https://api.postqueen.ai/public/v1/integrations" \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

## Get the next available slot for a channel

```bash
curl -X GET "https://api.postqueen.ai/public/v1/find-slot/:id" \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

## Upload a new file (form-data)

```bash
curl -X POST "https://api.postqueen.ai/public/v1/upload" \
  -H "Authorization: $POSTQUEEN_API_KEY" \
  -F "file=@/path/to/your/file.png"
```

## Upload a new file from an existing URL

```bash
curl -X POST "https://api.postqueen.ai/public/v1/upload-from-url" \
  -H "Authorization: $POSTQUEEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/image.png"
  }'
```

## Post list

```bash
curl -X GET "https://api.postqueen.ai/public/v1/posts?startDate=2024-12-14T08:18:54.274Z&endDate=2024-12-14T08:18:54.274Z&customer=optionalCustomerId" \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

## Schedule a new post

Each channel has its own `settings.__type` schema; providers with custom settings are documented under [`public-api/providers/`](public-api/providers/). PostQueen supports **30+ social networks**: X, LinkedIn, LinkedIn Page, Instagram, Instagram Standalone, Facebook, TikTok, YouTube, Threads, Pinterest, Reddit, Bluesky, Discord, Slack, Telegram, Mastodon, Twitch, Kick, MeWe, Nostr, Farcaster, Lemmy, VK, WordPress, Medium, Dev.to, Hashnode, Listmonk, Google Business Profile, Whop, Skool, Moltbook, Tumblr, and Dribbble.

```bash
curl -X POST "https://api.postqueen.ai/public/v1/posts" \
  -H "Authorization: $POSTQUEEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "schedule",
  "date": "2024-12-14T10:00:00.000Z",
  "shortLink": false,
  "tags": [],
  "posts": [
    {
      "integration": {
        "id": "your-x-integration-id"
      },
      "value": [
        {
          "content": "Hello from the PostQueen API! 🚀",
          "image": [{ "id": "img-123", "path": "https://uploads.postqueen.ai/photo.jpg" }]
        }
      ],
      "settings": {
        "__type": "provider name",
        rest of the settings
      }
    }
  ]
}'
```

## Delete a post

```bash
curl -X DELETE "https://api.postqueen.ai/public/v1/posts/:id" \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

---

## Resources & ecosystem

| Resource | Where |
| --- | --- |
| **Website** | [postqueen.ai](https://postqueen.ai) |
| **Cloud (7-day free trial)** | [postqueen.ai/pricing](https://postqueen.ai/pricing) |
| **Live app** | [app.postqueen.ai](https://app.postqueen.ai/auth) |
| **Full docs** | [docs.postqueen.ai](https://docs.postqueen.ai), sourced from this repo ([`public-api/`](public-api/), [`cli/`](cli/), [`mcp/`](mcp/), [`providers/`](providers/)) |
| **Public API reference** | live Swagger at [api.postqueen.ai/docs](https://api.postqueen.ai/docs) |
| **CLI** | [`postqueen`](https://www.npmjs.com/package/postqueen), install with `npm i -g postqueen` |
| **NodeJS SDK** | [`@postqueen/node`](https://www.npmjs.com/package/@postqueen/node) |
| **n8n node** | [`n8n-nodes-postqueen`](https://www.npmjs.com/package/n8n-nodes-postqueen) |
| **MCP server** | connect any MCP client to `https://api.postqueen.ai/mcp/<API_KEY>` |
| **Application source** | [github.com/GkhanKINAY/postqueen-app](https://github.com/GkhanKINAY/postqueen-app) |

PostQueen ships across **30+ social networks**: every action available in the UI is also a public API call, a CLI command, an SDK method, an n8n node, or an MCP tool.

---

## Run these docs locally

This site is built with [Mintlify](https://mintlify.com):

```bash
npm i -g mint     # install the Mintlify CLI
mint dev          # serve the docs at http://localhost:3000
```

`docs.json` defines the navigation; every page is an `.mdx` file in this repo.

---

## 🛡️ Compliance

- PostQueen is an open-source, self-hostable social media scheduler that supports X, LinkedIn, Instagram, Bluesky, Mastodon, Discord and 30+ more.
- The hosted service uses official, platform-approved OAuth flows.
- PostQueen does not automate or scrape content from social media platforms.
- PostQueen does not collect, store, or proxy API keys or access tokens from users.
- PostQueen never asks users to paste social-platform credentials into the hosted product.
- Users always authenticate directly with each platform (X, LinkedIn, Discord, and so on), which keeps every platform's compliance and your data privacy intact.

---

## ❤️ Community & Support

We would love to hear from you, whether you hit a bug, have an idea, or just want to say hi:

- 🐛 **Found a bug or have a doc fix?** [Open an issue](https://github.com/GkhanKINAY/postqueen-docs/issues).
- 💌 **Need a hand?** Email **support@postqueen.ai**.
- 📚 **Getting started?** The [docs](https://docs.postqueen.ai) walk you through everything.

If PostQueen saves you time, a ⭐ on the repo genuinely helps other people find it.

## 💜 Why we built PostQueen, and a thank you

We believe the way we work is about to change. AI is getting better every month, and before long, getting real work done by simply talking to an assistant will feel completely normal. We wanted to build something for that shift, in the spirit of tools we admire like [Chatbase](https://www.chatbase.co) and [Wispr Flow](https://wisprflow.ai).

Social media felt like the perfect place to start: it takes real time and effort, and most of it is work an assistant can carry for you. When we found that Nevo David had open-sourced [Postiz](https://github.com/gitroomhq/postiz-app) under AGPL-3.0, we knew we had the foundation we needed. [PostQueen](https://postqueen.ai) grows that work in its own direction: an assistant that runs your social media, so you can spend your time on everything else.

Thank you, Nevo David and the Postiz contributors. We could not have started this without you. 🙏💜

## License

This repository is available under the [MIT license](LICENSE) (the Mintlify docs template license).

Original work © Nevo David / Gitroom and the Postiz contributors. Modifications © PostQueen.
