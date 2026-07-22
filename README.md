<p align="center">
  <a href="https://postqueen.ai">
    <img src="https://postqueen.ai/icon.svg" width="76" alt="PostQueen" />
  </a>
</p>

<h1 align="center">PostQueen Docs</h1>

<p align="center">
  <strong>Documentation for PostQueen — the open-source, AI-native social media scheduler.</strong><br />
  The Mintlify source powering docs.postqueen.ai: self-hosting guides, the Public API, CLI, SDK, MCP, and 34 provider integrations.
</p>

<p align="center">
  <a href="https://postqueen.ai">Website</a> ·
  <a href="https://app.postqueen.ai">Live App</a> ·
  <a href="https://api.postqueen.ai/docs">API Reference</a> ·
  <a href="https://github.com/GkhanKINAY/postqueen-app">App Repo</a> ·
  <a href="https://www.npmjs.com/package/postqueen">CLI</a>
</p>

<p align="center">
  <a href="https://github.com/GkhanKINAY/postqueen-docs/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.npmjs.com/package/postqueen"><img src="https://img.shields.io/npm/v/postqueen?label=CLI&color=6d28d9" alt="CLI on npm"></a>
  <a href="https://www.npmjs.com/package/@postqueen/node"><img src="https://img.shields.io/npm/v/@postqueen/node?label=SDK&color=7c3aed" alt="SDK on npm"></a>
  <a href="https://www.npmjs.com/package/n8n-nodes-postqueen"><img src="https://img.shields.io/npm/v/n8n-nodes-postqueen?label=n8n&color=e0189e" alt="n8n node on npm"></a>
</p>

<p align="center">
  <img alt="X" src="https://postqueen.ai/channel-icons/x.svg" width="28" />
  <img alt="LinkedIn" src="https://postqueen.ai/channel-icons/linkedin.svg" width="28" />
  <img alt="Instagram" src="https://postqueen.ai/channel-icons/instagram.svg" width="28" />
  <img alt="Facebook" src="https://postqueen.ai/channel-icons/facebook.svg" width="28" />
  <img alt="TikTok" src="https://postqueen.ai/channel-icons/tiktok.svg" width="28" />
  <img alt="YouTube" src="https://postqueen.ai/channel-icons/youtube.svg" width="28" />
  <img alt="Threads" src="https://postqueen.ai/channel-icons/threads.svg" width="28" />
  <img alt="Pinterest" src="https://postqueen.ai/channel-icons/pinterest.svg" width="28" />
  <img alt="Reddit" src="https://postqueen.ai/channel-icons/reddit.svg" width="28" />
  <img alt="Bluesky" src="https://postqueen.ai/channel-icons/bluesky.svg" width="28" />
  <img alt="Discord" src="https://postqueen.ai/channel-icons/discord.svg" width="28" />
  <img alt="Slack" src="https://postqueen.ai/channel-icons/slack.svg" width="28" />
  <img alt="Telegram" src="https://postqueen.ai/channel-icons/telegram.svg" width="28" />
  <img alt="Mastodon" src="https://postqueen.ai/channel-icons/mastodon.svg" width="28" />
  <img alt="Twitch" src="https://postqueen.ai/channel-icons/twitch.svg" width="28" />
  <img alt="Kick" src="https://postqueen.ai/channel-icons/kick.svg" width="28" />
  <img alt="Nostr" src="https://postqueen.ai/channel-icons/nostr.svg" width="28" />
  <img alt="Farcaster" src="https://postqueen.ai/channel-icons/warpcast.svg" width="28" />
  <img alt="Lemmy" src="https://postqueen.ai/channel-icons/lemmy.svg" width="28" />
  <img alt="VK" src="https://postqueen.ai/channel-icons/vk.svg" width="28" />
  <img alt="Mewe" src="https://postqueen.ai/channel-icons/mewe.svg" width="28" />
  <img alt="WordPress" src="https://postqueen.ai/channel-icons/wordpress.svg" width="28" />
  <img alt="Medium" src="https://postqueen.ai/channel-icons/medium.svg" width="28" />
  <img alt="Dev.to" src="https://postqueen.ai/channel-icons/devto.svg" width="28" />
  <img alt="Hashnode" src="https://postqueen.ai/channel-icons/hashnode.svg" width="28" />
  <img alt="Dribbble" src="https://postqueen.ai/channel-icons/dribbble.svg" width="28" />
  <img alt="Google Business" src="https://postqueen.ai/channel-icons/google-business.svg" width="28" />
  <img alt="Whop" src="https://postqueen.ai/channel-icons/whop.svg" width="28" />
  <img alt="Skool" src="https://postqueen.ai/channel-icons/skool.svg" width="28" />
  <img alt="Listmonk" src="https://postqueen.ai/channel-icons/listmonk.svg" width="28" />
</p>

---

## About this repository

This repository is the **Mintlify documentation site** for PostQueen — the source behind **docs.postqueen.ai**. It covers installation and self-hosting, configuration, provider setup, and the full developer surface: the Public REST API, CLI, NodeJS SDK, n8n node, and MCP server.

> PostQueen is a fork of [Postiz](https://github.com/gitroomhq/postiz-app) (AGPL-3.0). Huge thanks to Nevo David and the Postiz contributors for the foundation this project stands on.

The rest of this file is a quick cURL cheat-sheet for the Public API. For the complete, browsable docs, run this site locally (see below) or read the pages under [`public-api/`](public-api/).

## Resources & ecosystem

| Resource | Where |
| --- | --- |
| **Website** | [postqueen.ai](https://postqueen.ai) |
| **Live app** | [app.postqueen.ai](https://app.postqueen.ai) |
| **Full docs** | this repo — pages under [`public-api/`](public-api/), [`cli/`](cli/), [`mcp/`](mcp/), [`providers/`](providers/) |
| **Public API reference** | live Swagger at [api.postqueen.ai/docs](https://api.postqueen.ai/docs) |
| **CLI** | [`postqueen`](https://www.npmjs.com/package/postqueen) — `npm i -g postqueen` |
| **NodeJS SDK** | [`@postqueen/node`](https://www.npmjs.com/package/@postqueen/node) |
| **n8n node** | [`n8n-nodes-postqueen`](https://www.npmjs.com/package/n8n-nodes-postqueen) |
| **MCP server** | connect any MCP client to `https://api.postqueen.ai/mcp/<API_KEY>` |
| **Application source** | [github.com/GkhanKINAY/postqueen-app](https://github.com/GkhanKINAY/postqueen-app) |

PostQueen ships **34 integrations across 30+ networks** — every action available in the UI is also a public API call, a CLI command, an SDK method, an n8n node, or an MCP tool.

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

1. Open **Settings → Developers → Public API** in the app.
2. Click **Reveal** to show your API key.
3. Set it as an environment variable:
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

Each channel has its own `settings.__type` schema; providers with custom settings are documented under [`public-api/providers/`](public-api/providers/). PostQueen supports **34 integrations across 30+ networks**: X, LinkedIn, LinkedIn Page, Instagram, Instagram Standalone, Facebook, TikTok, YouTube, Threads, Pinterest, Reddit, Bluesky, Discord, Slack, Telegram, Mastodon, Twitch, Kick, MeWe, Nostr, Farcaster, Lemmy, VK, WordPress, Medium, Dev.to, Hashnode, Listmonk, Google Business Profile, Whop, Skool, Moltbook, Tumblr, and Dribbble.

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

## License

This repository is available under the [MIT license](LICENSE) (the Mintlify docs template license).

Original work © Nevo David / Gitroom and the Postiz contributors. Modifications © PostQueen.
