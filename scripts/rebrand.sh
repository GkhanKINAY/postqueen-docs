#!/usr/bin/env bash
# Idempotent Postiz -> PostQueen brand sweep for the docs site.
# Re-run after every upstream merge (git fetch upstream && git merge upstream/main).
#
# NOT covered by this script (hand-maintained; re-check after upstream merges).
# These are the real exclusions below, not just a list — the two used to disagree,
# and introduction.mdx / faq.mdx / README.md were being rewritten despite this
# comment claiming otherwise, which turned "a fork of Postiz" into "a fork of
# PostQueen" on every run.
#   - docs.json                          (name, brand colors, logo/favicon, social anchors)
#   - configuration/chrome-extension.mdx (store listing neutralized; PostQueen ext not published yet)
#   - introduction.mdx, faq.mdx, README.md  (AGPL attribution to Postiz — must survive rebranding)
#   - logo/*, favicon.*, images/*        (brand assets)
#
# configuration/polotno.mdx is deliberately NOT excluded: the upstream partner
# coupon was removed by hand, and the file contains no "Postiz" string for this
# script to damage.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# Text files under git, minus hand-maintained / binary paths.
FILES=$(git ls-files -- . \
  ':!scripts/rebrand.sh' \
  ':!LICENSE' \
  ':!docs.json' \
  ':!configuration/chrome-extension.mdx' \
  ':!introduction.mdx' \
  ':!faq.mdx' \
  ':!README.md' \
  ':!logo/**' ':!images/**' \
  | while IFS= read -r f; do [ -f "$f" ] && grep -Iq . "$f" 2>/dev/null && printf '%s\n' "$f"; done)

run() { printf '%s\n' "$FILES" | tr '\n' '\0' | xargs -0 perl -pi -e "$1"; }

# 1. Container/OCI images (lowercase org — Docker/OCI refs must be lowercase) BEFORE slug rule.
run 's/ghcr\.io\/gitroomhq\/postiz/ghcr.io\/gkhankinay\/postqueen/g'

# 2. Repo slugs (github.com/... links), most specific first.
run 's/gitroomhq\/postiz-docker-compose/GkhanKINAY\/postqueen-docker-compose/g'
run 's/gitroomhq\/postiz-helmchart/GkhanKINAY\/postqueen-helmchart/g'
run 's/gitroomhq\/postiz-agent/GkhanKINAY\/postqueen-agent/g'
run 's/gitroomhq\/postiz-docs/GkhanKINAY\/postqueen-docs/g'
run 's/gitroomhq\/postiz-app/GkhanKINAY\/postqueen-app/g'
run 's/gitroomhq\/postiz/GkhanKINAY\/postqueen/g'

# 3. Emails before the generic domain rule.
run 's/\@postiz\.com/\@postqueen.ai/g'

# 4. Domains, subdomain-preserving (api./docs./cli-auth./uploads. + bare postiz.com).
run 's/((?:[a-z0-9-]+\.)*)postiz\.com/${1}postqueen.ai/g'
# 4b. Normalize the app front-door to our standard: platform. -> app.
run 's/platform\.postqueen\.ai/app.postqueen.ai/g'

# 5. npm / package identifiers (before the generic word rules).
run 's/\@postiz\/node/\@postqueen\/node/g'          # published SDK, keep the scope
run 's/n8n-nodes-postiz/n8n-nodes-postqueen/g'       # published n8n node
run 's/\@postiz\/frontend/postqueen-frontend/g'      # actual pnpm workspace package name

# 6. Env vars and remaining all-caps.
run 's/POSTIZ_/POSTQUEEN_/g'
run 's/POSTIZ/POSTQUEEN/g'

# 7. Brand words — TitleCase before lowercase (covers CLI binary `postiz`, ~/.postiz,
#    MCP key, npm pkg `postiz`, and every placeholder like your-postiz-domain.com).
run 's/Postiz/PostQueen/g'
run 's/postiz/postqueen/g'

echo "Docs rebrand sweep complete."
