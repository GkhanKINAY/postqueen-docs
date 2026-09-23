<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/banner-dark.png">
    <img src=".github/assets/banner-light.png" width="100%" alt="PostQueen docs, open for edits. The source of docs.postqueen.ai: the app, channels, AI agents, the CLI, the public API and self-hosting.">
  </picture>
</p>

<p align="center">
  The source of <a href="https://docs.postqueen.ai/introduction">docs.postqueen.ai</a>, the documentation for PostQueen, built with <a href="https://mintlify.com">Mintlify</a>.
</p>

<p align="center">
  <a href="https://postqueen.ai"><b>Website</b></a> ·
  <a href="https://docs.postqueen.ai/introduction"><b>Docs</b></a> ·
  <a href="https://postqueen.ai/pricing"><b>Pricing</b></a> ·
  <a href="https://api.postqueen.ai/docs"><b>API reference</b></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-7C3AED?labelColor=15131C" alt="License: MIT"></a>
  <a href="https://mintlify.com"><img src="https://img.shields.io/badge/built%20with-Mintlify-7C3AED?labelColor=15131C" alt="Built with Mintlify"></a>
</p>

<p align="center">
  <a href="https://docs.postqueen.ai/agents/grok-bot"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/announce-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/announce-light.png" width="100%" alt="New: Grok Bot is here. Connect Claude, ChatGPT, Grok Bot or any AI agent to your socials."></picture></a>
</p>

<p align="center">
  <a href="https://app.postqueen.ai/auth?utm_source=github&utm_medium=readme&utm_campaign=postqueen-docs&utm_content=hero-button"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/btn-trial-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/btn-trial-light.png" width="323" alt="Start 7-day trial for $0"></picture></a><a href="https://docs.postqueen.ai/agents/overview"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/btn-agent-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/btn-agent-light.png" width="297" alt="Connect your AI agent"></picture></a>
</p>

<p align="center">
  <sub><b>$0 due today.</b> A card is required, and you pay nothing if you cancel within 7 days.</sub>
</p>

<p align="center">
  <a href="https://github.com/GkhanKINAY/postqueen-docs/stargazers"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/star-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/star-light.png" width="380" alt="Like PostQueen? Star the repo. It helps others find it."></picture></a>
</p>

<p align="center">
  <a href="https://docs.postqueen.ai/agents/overview"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/works-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/works-light.png" width="100%" alt="Use the agent you already have: Claude, ChatGPT, Grok Bot (new), Grok, Perplexity, Muse (new), Claude Code, Codex, Cursor, Gemini CLI, VS Code, Devin Desktop, Zed, OpenClaw, Hermes, NanoClaw, Paperclip and any MCP app. Posts to 30+ networks."></picture></a>
</p>


PostQueen is a social media scheduler with an AI copilot. It schedules posts to 30+ networks from the app, from AI agents over MCP, from the `postqueen` CLI and from the public API.

## What it covers

| Section | What you will find | Start at |
| --- | --- | --- |
| Getting started | What PostQueen is and how to publish your first post | [/introduction](https://docs.postqueen.ai/introduction) · [/quickstart](https://docs.postqueen.ai/quickstart) |
| Using the app | The calendar, the composer, analytics, teams and settings | [/using/calendar](https://docs.postqueen.ai/using/calendar) |
| Channels | Each network, its status today, and what it supports | [/channels/overview](https://docs.postqueen.ai/channels/overview) |
| Plans and billing | Plans, the free trial, refunds and your subscription | [/cloud/plans](https://docs.postqueen.ai/cloud/plans) |
| AI agents and MCP | Connecting Claude, ChatGPT, Cursor, Codex and other agents | [/agents/overview](https://docs.postqueen.ai/agents/overview) · [/mcp/introduction](https://docs.postqueen.ai/mcp/introduction) |
| CLI | The `postqueen` command line | [/cli/introduction](https://docs.postqueen.ai/cli/introduction) |
| Public API | How to authenticate, and the main endpoints with examples | [/public-api/introduction](https://docs.postqueen.ai/public-api/introduction) |
| Self-hosting | Docker Compose, Kubernetes, configuration and reverse proxies | [/installation/overview](https://docs.postqueen.ai/installation/overview) · [/configuration/reference](https://docs.postqueen.ai/configuration/reference) |
| Help | Common errors, failed posts and how to reach a person | [/troubleshooting/common-errors](https://docs.postqueen.ai/troubleshooting/common-errors) · [/support](https://docs.postqueen.ai/support) |

The site also serves [`llms.txt`](https://docs.postqueen.ai/llms.txt) and `llms-full.txt`, so AI assistants can read the whole site in one request.

## Quick start

Run the site locally (the Mintlify CLI needs Node.js 22):

```bash
npm i -g mint
mint dev              # serves the docs at http://localhost:3000
npm run check         # navigation, links, frontmatter and the style rules
npm run check:facts   # the facts pages repeat, against facts/facts.json
```

Every page is an `.mdx` file in this repository, and [`docs.json`](docs.json) defines the navigation.

## Contributing

1. Read [CONTRIBUTING.md](CONTRIBUTING.md): where things live, the checks and the style guide.
2. Start a new page from its template in `_templates/`, and add it to `docs.json`.
3. Run the checks. The same ones run on every push and pull request.
4. Open a pull request. Merged changes deploy to docs.postqueen.ai.

Report a mistake in the docs as an issue here. Report a bug in the app itself on [postqueen-app](https://github.com/GkhanKINAY/postqueen-app/issues).

## Privacy and security

- Channels connect through each network's official OAuth sign-in where the network offers one.
- Some networks, such as Bluesky, Lemmy, WordPress and Nostr, need an app password, an account password or a key that you paste in.
- PostQueen stores these credentials so it can post for you, and replaces them when you remove the channel.
- Read the [privacy policy](https://postqueen.ai/privacy-policy), or [delete your account](https://postqueen.ai/delete-my-account).

**Want to try what these docs describe?** PostQueen Cloud has a 7-day trial.

<p align="center">
  <a href="https://app.postqueen.ai/auth?utm_source=github&utm_medium=readme&utm_campaign=postqueen-docs&utm_content=closing-band"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/cta-dark.png"><img src="https://raw.githubusercontent.com/GkhanKINAY/postqueen-app/main/.github/assets/showcase/cta-light.png" width="100%" alt="Ready when you are: hand your next post to your agent. Start 7-day trial for $0. $0 due today, cancel in one click."></picture></a>
</p>

## Links

| | |
| --- | --- |
| Docs | [docs.postqueen.ai](https://docs.postqueen.ai/introduction) |
| Hosted service | [postqueen.ai](https://postqueen.ai) · [pricing](https://postqueen.ai/pricing) |
| API reference | [docs.postqueen.ai/public-api](https://docs.postqueen.ai/public-api/introduction) |
| Repositories | [app](https://github.com/GkhanKINAY/postqueen-app) · [CLI and skill](https://github.com/GkhanKINAY/postqueen-agent) · [n8n node](https://github.com/GkhanKINAY/postqueen-n8n) · [docs](https://github.com/GkhanKINAY/postqueen-docs) · [Docker Compose](https://github.com/GkhanKINAY/postqueen-docker-compose) · [Helm chart](https://github.com/GkhanKINAY/postqueen-helmchart) |
| Help | support@postqueen.ai · [GitHub issues](https://github.com/GkhanKINAY/postqueen-docs/issues) |

## License

These docs are open source under the [MIT license](LICENSE), from the Mintlify docs template. PostQueen started as a fork of [Postiz](https://github.com/gitroomhq/postiz-app) by Nevo David, and this repository started from [postiz-docs](https://github.com/gitroomhq/postiz-docs). Original work © Nevo David / Gitroom and the Postiz contributors. Modifications © PostQueen.
