<p align="center">
  <a href="https://postqueen.ai">
    <img src=".github/assets/header.svg" width="840" alt="PostQueen, the queen of your posts, your AI social media assistant" />
  </a>
</p>

<h3 align="center">
  <a href="https://postqueen.ai/agent">🆕 NEW: meet the PostQueen Agent, run your social media from Claude Code, ChatGPT, OpenClaw or Hermes »</a>
</h3>

<br/>

<p align="center">
  <strong>Everything PostQueen, documented.</strong>
</p>

<p align="center">
  This repository is the source of <a href="https://docs.postqueen.ai">docs.postqueen.ai</a>: self-hosting, configuration, per-network provider guides, the CLI, MCP and the full public API.
</p>

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
</p>

<p align="center">
  <img src=".github/assets/channels/instagram.svg" height="44" alt="Instagram" /> <img src=".github/assets/channels/youtube.svg" height="44" alt="YouTube" /> <img src=".github/assets/channels/google-business.svg" height="44" alt="Google Business Profile" /> <img src=".github/assets/channels/dribbble.svg" height="44" alt="Dribbble" /> <img src=".github/assets/channels/linkedin.svg" height="44" alt="LinkedIn" /> <img src=".github/assets/channels/reddit.svg" height="44" alt="Reddit" /> <img src=".github/assets/channels/tiktok.svg" height="44" alt="TikTok" /> <img src=".github/assets/channels/facebook.svg" height="44" alt="Facebook" /> <img src=".github/assets/channels/pinterest.svg" height="44" alt="Pinterest" /> <img src=".github/assets/channels/threads.svg" height="44" alt="Threads" /> <img src=".github/assets/channels/x.svg" height="44" alt="X" /> <img src=".github/assets/channels/slack.svg" height="44" alt="Slack" /> <img src=".github/assets/channels/discord.svg" height="44" alt="Discord" /> <img src=".github/assets/channels/mastodon.svg" height="44" alt="Mastodon" /> <img src=".github/assets/channels/bluesky.svg" height="44" alt="Bluesky" /> <img src=".github/assets/channels/lemmy.svg" height="44" alt="Lemmy" /> <img src=".github/assets/channels/warpcast.svg" height="44" alt="Farcaster" /> <img src=".github/assets/channels/telegram.svg" height="44" alt="Telegram" /> <img src=".github/assets/channels/nostr.svg" height="44" alt="Nostr" /> <img src=".github/assets/channels/vk.svg" height="44" alt="VK" /> <img src=".github/assets/channels/devto.svg" height="44" alt="Dev.to" /> <img src=".github/assets/channels/medium.svg" height="44" alt="Medium" /> <img src=".github/assets/channels/hashnode.svg" height="44" alt="Hashnode" /> <img src=".github/assets/channels/wordpress.svg" height="44" alt="WordPress" /> <img src=".github/assets/channels/whop.svg" height="44" alt="Whop" /> <img src=".github/assets/channels/kick.svg" height="44" alt="Kick" /> <img src=".github/assets/channels/mewe.svg" height="44" alt="MeWe" /> <img src=".github/assets/channels/twitch.svg" height="44" alt="Twitch" /> <img src=".github/assets/channels/listmonk.svg" height="44" alt="Listmonk" /> <img src=".github/assets/channels/skool.svg" height="44" alt="Skool" />
</p>

---

## 📚 Read the docs

**The docs live at [docs.postqueen.ai](https://docs.postqueen.ai).** That is the rendered, searchable version of everything in this repo. Here is the map:

| Section | What you will find | Start at |
| --- | --- | --- |
| Getting started | What PostQueen is and your first post | [/introduction](https://docs.postqueen.ai/introduction) · [/quickstart](https://docs.postqueen.ai/quickstart) · [/howitworks](https://docs.postqueen.ai/howitworks) |
| Self-hosting | Docker Compose, plain Docker, Kubernetes, system requirements | [/installation/docker-compose](https://docs.postqueen.ai/installation/docker-compose) · [/installation/kubernetes-helm](https://docs.postqueen.ai/installation/kubernetes-helm) |
| Configuration | Every environment variable and integration setting | [/configuration/reference](https://docs.postqueen.ai/configuration/reference) |
| Providers | Per-network OAuth app setup guides (X, LinkedIn, Instagram, TikTok and more) | [/providers/overview](https://docs.postqueen.ai/providers/overview) |
| CLI | The `postqueen` command line for scripts and AI agents | [/cli/introduction](https://docs.postqueen.ai/cli/introduction) |
| MCP | Connect AI assistants over the Model Context Protocol | [/mcp/introduction](https://docs.postqueen.ai/mcp/introduction) |
| Public API | 22 REST endpoints with examples | [/public-api/introduction](https://docs.postqueen.ai/public-api/introduction) |
| Reverse proxies | Caddy, nginx, Traefik recipes for HTTPS | [/reverse-proxies/caddy](https://docs.postqueen.ai/reverse-proxies/caddy) |
| Troubleshooting | Fixes for the common failure modes | [/troubleshooting/overview](https://docs.postqueen.ai/troubleshooting/overview) |

The docs also ship `llms.txt` and `llms-full.txt`, so AI assistants can pull the whole site in one request. Mintlify serves both automatically.

---

## 🚀 API quick taste

The public API lives at `https://api.postqueen.ai/public/v1`. Authentication is one header: `Authorization`, set to your raw API key, with no `Bearer` prefix.

<p align="center">
  <img src=".github/assets/api-client.svg" width="620" alt="An API client posting to the PostQueen public API and receiving the scheduled posts response" />
</p>

```bash
curl https://api.postqueen.ai/public/v1/integrations \
  -H "Authorization: $POSTQUEEN_API_KEY"
```

That is the whole handshake. The full reference, every endpoint and every per-network settings schema, is at [docs.postqueen.ai/public-api/introduction](https://docs.postqueen.ai/public-api/introduction), and you can try calls live in the Swagger playground at [api.postqueen.ai/docs](https://api.postqueen.ai/docs).

---

## 🖥️ Run these docs locally

This site is built with [Mintlify](https://mintlify.com):

```bash
npm i -g mint     # install the Mintlify CLI
mint dev          # serve the docs at http://localhost:3000
```

`docs.json` defines the navigation; every page is an `.mdx` file in this repo.

---

## ✍️ Contributing

Fixes and clarifications are welcome. Spot a typo, a stale flag or a missing step? Open a PR: the site deploys from this repo, so merged changes go straight to [docs.postqueen.ai](https://docs.postqueen.ai).

Want to contribute to the app itself? Start with the [developer guide](https://docs.postqueen.ai/developer-guide).

---

## ❤️ Community and support

- 🐛 **Found a bug or have an idea?** [Open an issue](https://github.com/GkhanKINAY/postqueen-docs/issues).
- 💌 **Need a hand?** Email **support@postqueen.ai**.
- 📚 **Getting started?** The [docs](https://docs.postqueen.ai) walk you through everything.

If PostQueen saves you time, a ⭐ on the repo genuinely helps other people find it.

---

## 👑 The PostQueen ecosystem

| Repository | What lives there |
| --- | --- |
| [postqueen-app](https://github.com/GkhanKINAY/postqueen-app) | The application itself: frontend, backend, workers |
| [postqueen-agent](https://github.com/GkhanKINAY/postqueen-agent) | Agent CLI and skill: give any AI assistant hands |
| [postqueen-docker-compose](https://github.com/GkhanKINAY/postqueen-docker-compose) | Self-host the whole stack with one command |
| [postqueen-helmchart](https://github.com/GkhanKINAY/postqueen-helmchart) | Run it on Kubernetes |
| [postqueen-n8n](https://github.com/GkhanKINAY/postqueen-n8n) | The n8n community node for no-code automation |
| [postqueen-docs](https://github.com/GkhanKINAY/postqueen-docs) | Source of [docs.postqueen.ai](https://docs.postqueen.ai) |

On npm: [`postqueen`](https://www.npmjs.com/package/postqueen) (CLI) · [`@postqueen/node`](https://www.npmjs.com/package/@postqueen/node) (SDK) · [`n8n-nodes-postqueen`](https://www.npmjs.com/package/n8n-nodes-postqueen) (n8n)

PostQueen is a fork of [Postiz](https://github.com/gitroomhq/postiz-app) by Nevo David, released under AGPL-3.0. Thank you, Nevo David and every Postiz contributor: this project exists because you open-sourced yours. The full story is in the [main README](https://github.com/GkhanKINAY/postqueen-app#-thank-you-postiz).

## License

This repository is available under the [MIT license](LICENSE) (the Mintlify docs template license).

Original work © Nevo David / Gitroom and the Postiz contributors. Modifications © PostQueen.
