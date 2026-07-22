<p align="center">
  <a href="https://postqueen.ai">
    <img src=".github/assets/header.svg" width="840" alt="PostQueen Docs" />
  </a>
</p>

<h3 align="center">🆕&nbsp; NEW: the PostQueen <a href="https://postqueen.ai/agent">Agent CLI</a> + <a href="https://postqueen.ai/mcp">MCP server</a>: plug Claude&nbsp;Code, ChatGPT, Cursor, OpenClaw, Hermes or Codex straight into your channels.</h3>

<br/>

<div align="center">
  <h2>Docs for the queen of your posts 👑</h2>
  <p>
    Documentation for PostQueen. She writes, designs and schedules<br/>
    across 30+ networks, you just approve.
  </p>
  <p><em>An open-source alternative to Buffer, Hootsuite, Sprout Social and Later.</em></p>
</div>

<br/>

<p align="center">
  <a href="https://postqueen.ai">Website</a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/pricing">Pricing</a> &nbsp;·&nbsp;
  <a href="https://app.postqueen.ai/auth">Start free</a> &nbsp;·&nbsp;
  <a href="https://docs.postqueen.ai">Live docs</a> &nbsp;·&nbsp;
  <a href="https://api.postqueen.ai/docs">API Reference</a> &nbsp;·&nbsp;
  <a href="https://www.npmjs.com/package/postqueen">CLI</a>
</p>

<p align="center">
  <a href="https://github.com/GkhanKINAY/postqueen-docs/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/postqueen"><img src="https://img.shields.io/npm/v/postqueen?label=CLI&color=6d28d9" alt="CLI on npm"></a>
  <a href="https://www.npmjs.com/package/@postqueen/node"><img src="https://img.shields.io/npm/v/@postqueen/node?label=SDK&color=7c3aed" alt="SDK on npm"></a>
  <a href="https://www.npmjs.com/package/n8n-nodes-postqueen"><img src="https://img.shields.io/npm/v/n8n-nodes-postqueen?label=n8n&color=e0189e" alt="n8n node on npm"></a>
  <a href="https://github.com/GkhanKINAY/postqueen-docs/commits/main"><img src="https://img.shields.io/github/commit-activity/m/GkhanKINAY/postqueen-docs" alt="Commit activity"></a>
</p>

<br/>

<p align="center">
  <img src=".github/assets/channels.svg" width="780" alt="Supported social networks" />
</p>

<p align="center">
  <a href="https://docs.postqueen.ai"><strong>Read the docs online »</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://postqueen.ai/pricing"><strong>Start a 7-day free trial »</strong></a>
</p>

<br/>

> PostQueen is a fork of [Postiz](https://github.com/gitroomhq/postiz-app) (AGPL-3.0). Huge thanks to Nevo David and the Postiz contributors for the foundation this project stands on.

---

## About this repository

This repository is the **Mintlify documentation site** for PostQueen, the source behind **[docs.postqueen.ai](https://docs.postqueen.ai)**. It covers installation and self-hosting, configuration, provider setup, and the full developer surface: the Public REST API, CLI, NodeJS SDK, n8n node, and MCP server.

The rest of this file is a quick cURL cheat-sheet for the Public API. For the complete, browsable docs, [read them online](https://docs.postqueen.ai), run this site locally (see below), or browse the `.mdx` pages under [`public-api/`](public-api/).

---

## 💬 Just talk to your AI

You don't need to write a line of code. Connect PostQueen to the AI assistant you already use, then just ask:

> *"Post about our launch on X and LinkedIn tomorrow morning."*

> *"Turn this blog post into a week of posts, one a day."*

> *"Make an image for this post and schedule it for Friday at 9am."*

Your assistant writes it, designs it, and drops it into your **PostQueen queue**, where you review and approve before anything goes live. It works over the built-in **MCP server** or the **Agent CLI**:

<p align="center">
  <a href="https://postqueen.ai/claude-code"><b>Claude Code</b></a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/chatgpt"><b>ChatGPT</b></a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/cursor"><b>Cursor</b></a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/openclaw"><b>OpenClaw</b></a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/hermes-agent"><b>Hermes</b></a> &nbsp;·&nbsp;
  <a href="https://postqueen.ai/codex"><b>Codex</b></a>
</p>

<p align="center"><em>and any other MCP client (Gemini CLI, Aider, Cline, Warp, or your own).</em></p>

> 🔑 **First, grab your API key** at **[app.postqueen.ai/settings](https://app.postqueen.ai/settings)** (Developers → Public API → Reveal).

Then point your assistant at PostQueen with one line:

```bash
# Claude Code (or any MCP client)
claude mcp add --transport http postqueen https://api.postqueen.ai/mcp/<YOUR_API_KEY>
```

Full guide: [postqueen.ai/mcp](https://postqueen.ai/mcp).

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

## ❤️ Community & Support

We would love to hear from you, whether you hit a bug, have an idea, or just want to say hi:

- 🐛 **Found a bug or have a doc fix?** [Open an issue](https://github.com/GkhanKINAY/postqueen-docs/issues).
- 💌 **Need a hand?** Email **support@postqueen.ai**.
- 📚 **Getting started?** The [docs](https://docs.postqueen.ai) walk you through everything.

If PostQueen saves you time, a ⭐ on the repo genuinely helps other people find it.

## License

This repository is available under the [MIT license](LICENSE) (the Mintlify docs template license).

Original work © Nevo David / Gitroom and the Postiz contributors. Modifications © PostQueen.
