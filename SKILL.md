---
name: postqueen
description: PostQueen schedules social media and chat posts from the postqueen CLI to 30+ networks, such as X, LinkedIn, LinkedIn Page, Reddit, Instagram, Facebook Page, Threads, YouTube, Google Business Profile, TikTok, Pinterest, Dribbble, Discord, Slack, Kick, Twitch, Mastodon, Bluesky, Lemmy, Farcaster, Telegram, Nostr, VK, DEV, Hashnode, WordPress, Listmonk, MeWe, Whop, Skool, Moltbook and Tumblr. Some of them are marked Soon on the hosted service.
homepage: https://docs.postqueen.ai/public-api/introduction
metadata: {"openclaw":{"emoji":"🌎","requires":{"bins":["postqueen"],"env":["POSTQUEEN_API_KEY"]}}}
---

## Install PostQueen if it doesn't exist

```bash
npm install -g postqueen
# or
pnpm install -g postqueen
```

npm release: https://www.npmjs.com/package/postqueen
postqueen github: https://github.com/GkhanKINAY/postqueen-app
postqueen cli github: https://github.com/GkhanKINAY/postqueen-agent
official website: https://postqueen.ai
---


| Property | Value |
|----------|-------|
| **name** | postqueen |
| **description** | Social media automation CLI for scheduling posts across 30+ networks, including X, LinkedIn, LinkedIn Pages, Instagram, Facebook, Threads, YouTube, TikTok, Reddit, Pinterest, Bluesky, Mastodon, Google Business Profile, Discord, Slack, Telegram, Twitch, Kick, Lemmy, Farcaster, Nostr, VK, MeWe, Tumblr, Skool, Whop, Moltbook, Dribbble, DEV, Hashnode, WordPress and Listmonk. Some are marked Soon on the hosted service (see Networks) |
| **allowed-tools** | Bash(postqueen:*) |

---

## ⚠️ Four Hard Rules (Read First)

**Rule 1: Authenticate before anything.** All commands fail without valid credentials.

**Rule 2: Every file passed to `-m` (or to `image` in JSON mode) MUST first go through `postqueen upload`.** Raw filesystem paths (`image.jpg`, `video.mp4`) and external URLs (`https://example.com/...`) are **NOT** accepted by the publishing pipeline. Always:

```bash
URL=$(postqueen upload <file> | tail -n +2 | jq -r '.path')
postqueen posts:create ... -m "$URL" ...
```

Most commands print one status line before their JSON, so drop it with `tail -n +2` before `jq` (see Output).

**Rule 3: When posting to TikTok, `content_posting_method` MUST be `"DIRECT_POST"`** unless the user has explicitly asked to finish the post inside the TikTok app. `"UPLOAD"` does not publish: it drops the media into the account's TikTok inbox to be completed manually within 24 hours, while the PostQueen API still reports success. A user saying "upload this video to TikTok" means `"DIRECT_POST"`.

**Rule 4: Fetch `postqueen integrations:settings <id>` before scheduling and honor the returned `rules` and per-field `description`s.** They state which settings apply and when. A setting that doesn't apply (wrong posting method, wrong media type, etc.) is **silently discarded**, not rejected. The post still reports success, so this is your only chance to catch it.

---

## ⚠️ Authentication Required

**You MUST authenticate before running any PostQueen CLI command.** All commands will fail without valid credentials.

Before doing anything else, check auth status:
```bash
postqueen auth:status
```

If not authenticated, ask the user for their API key and set it:
```bash
export POSTQUEEN_API_KEY=your_api_key
```

The key is in PostQueen under **Connections > API Keys**. Only workspace admins can see it, and each workspace has one.

**Do NOT proceed with any other commands until authentication is confirmed.**

---

## Networks

PostQueen supports 30+ networks. On the hosted service (app.postqueen.ai) some are marked **Soon**: they are listed, but nobody can connect them yet. As of September 2026:

| Hosted status | Networks |
|---|---|
| Connect today | Bluesky, DEV, Hashnode (needs Hashnode Pro), Lemmy, Listmonk, Moltbook, Nostr, WordPress |
| Connect with limits until the platform approves PostQueen's app | Facebook and Instagram (only accounts with a role on PostQueen's Meta app), Threads (Threads Testers only), TikTok (every post is Self only), YouTube (uploads stay private), X (after the workspace's 7-day trial ends) |
| Soon | LinkedIn, LinkedIn Page, Pinterest, Reddit, Google Business Profile, Discord, Slack, Mastodon, Tumblr, Twitch, Kick, VK, Dribbble, MeWe, Whop, TikTok Business, Telegram, Farcaster, Skool |

Never tell a user they can connect a Soon network on the hosted service. `postqueen integrations:list` shows what the workspace has actually connected.

---

## Core Workflow

The fundamental pattern for using PostQueen CLI:

1. **Authenticate** - Verify or set up authentication (see above)
2. **Discover** - List integrations and get their settings
3. **Fetch** - Use integration tools to retrieve dynamic data (subreddits and flairs, Pinterest boards, Discord and Slack channels)
4. **Prepare** - Upload media files if needed
5. **Post** - Create posts with content, media, and platform-specific settings
6. **Analyze** - Track performance with platform and post-level analytics
7. **Resolve** - If analytics returns `{"missing": true}`, run `posts:missing` to list provider content, then `posts:connect` to link it

```bash
# 1. Authenticate
postqueen auth:status
# If not authenticated: export POSTQUEEN_API_KEY=your_api_key

# 2. Discover
postqueen integrations:list
postqueen integrations:settings <integration-id>

# 3. Fetch (if needed)
postqueen integrations:trigger <integration-id> <method> -d '{"key":"value"}'

# 4. Prepare
MEDIA=$(postqueen upload image.jpg | tail -n +2 | jq -r '.path')

# 5. Post
postqueen posts:create -c "Content" -m "$MEDIA" -s "2026-12-31T12:00:00Z" -i "<integration-id>"

# 6. Analyze
postqueen analytics:platform <integration-id> -d 30
postqueen analytics:post <post-id> -d 7

# 7. Resolve (if analytics returns {"missing": true})
postqueen posts:missing <post-id>
postqueen posts:connect <post-id> --release-id "<content-id>"
```

---

## Essential Commands

### Authentication

**Option 1: API key (the hosted service)**
```bash
export POSTQUEEN_API_KEY=your_api_key_here

# Check auth status (verifies credentials are still valid)
postqueen auth:status
```

Copy the key from PostQueen > Connections > API Keys. Only workspace admins can see it.

**Option 2: your own auth server**

PostQueen runs no login server for the CLI, so `postqueen auth:login` on its own only explains the API key. If the user runs the device-flow auth server from the CLI repository's `server/` folder, log in through it:
```bash
postqueen auth:login --auth-server https://auth.example.com   # or set POSTQUEEN_AUTH_SERVER
postqueen auth:logout                                          # remove the stored credentials
```

Credentials from `auth:login` are stored in `~/.postqueen/credentials.json` and take priority over `POSTQUEEN_API_KEY`.

**Optional custom API URL:**
```bash
export POSTQUEEN_API_URL=https://custom-api-url.com
```

### Output

Most commands print one status line (for example `🔌 Connected Integrations:`) and then the JSON result. Drop the first line before you parse it:

```bash
postqueen integrations:list | tail -n +2 | jq -r '.[].id'
```

`posts:missing` prints JSON only, and `posts:delete` prints only a confirmation line. Errors go to stderr, and the command exits with code 1.

### Integration Discovery

```bash
# List all connected integrations (each has id, name, identifier, disabled, customer)
postqueen integrations:list

# List integrations belonging to a specific group (customer)
postqueen integrations:list --group <group-id>

# List all groups (customers) as {id, name}
postqueen integrations:groups

# Get settings schema for specific integration
postqueen integrations:settings <integration-id>

# Trigger integration tool to fetch dynamic data
postqueen integrations:trigger <integration-id> <method-name>
postqueen integrations:trigger <integration-id> <method-name> -d '{"param":"value"}'
```

### Creating Posts

```bash
# Simple post (date is REQUIRED)
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -i "integration-id"

# Draft post
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -t draft -i "integration-id"

# Post with media (upload each file FIRST, see Rule 2)
IMG1=$(postqueen upload img1.jpg | tail -n +2 | jq -r '.path')
IMG2=$(postqueen upload img2.jpg | tail -n +2 | jq -r '.path')
postqueen posts:create -c "Content" -m "$IMG1,$IMG2" -s "2026-12-31T12:00:00Z" -i "integration-id"

# Post with comments (each with own media, every file uploaded first)
MAIN=$(postqueen upload main.jpg | tail -n +2 | jq -r '.path')
C1=$(postqueen upload comment1.jpg | tail -n +2 | jq -r '.path')
C2A=$(postqueen upload comment2.jpg | tail -n +2 | jq -r '.path')
C2B=$(postqueen upload comment3.jpg | tail -n +2 | jq -r '.path')
postqueen posts:create \
  -c "Main post" -m "$MAIN" \
  -c "First comment" -m "$C1" \
  -c "Second comment" -m "$C2A,$C2B" \
  -s "2026-12-31T12:00:00Z" \
  -i "integration-id"

# Multi-platform post (the same --settings go to every channel, so mix only
# channels that take the same settings, or use --json)
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -i "bluesky-id,mastodon-id"

# Platform-specific settings
postqueen posts:create \
  -c "Content" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"subreddit":[{"value":{"subreddit":"/r/programming","title":"My Post","type":"self","is_flair_required":false}}]}' \
  -i "reddit-id"

# Complex post from JSON file
postqueen posts:create --json post.json
```

### Managing Posts

```bash
# List posts (defaults to last 30 days to next 30 days)
# Each returned post includes its current `settings` (as a JSON string, so JSON.parse it).
# Workflow: run posts:list to read a post's current settings, then posts:settings to patch them.
postqueen posts:list

# List posts in date range
postqueen posts:list --startDate "2026-01-01T00:00:00Z" --endDate "2026-12-31T23:59:59Z"

# Delete post
postqueen posts:delete <post-id>

# Change post status (draft or schedule)
postqueen posts:status <post-id> --status draft     # Move back to draft, terminates any running publish workflow
postqueen posts:status <post-id> --status schedule  # Promote a draft into the publishing queue (uses the post's stored date)

# Update a post's provider-specific settings (merged: only the keys you pass change)
# Only DRAFT/QUEUE (unpublished) posts can be updated. Pass the MAIN post id, not a comment id.
# Do NOT include __type: the backend adds it automatically from the integration.
postqueen posts:settings <post-id> --settings '{"content_posting_method":"DIRECT_POST"}'   # Switch a TikTok draft to direct publishing
postqueen posts:settings <post-id> --settings '{"subreddit":[{"value":{"subreddit":"/r/selfhosted","title":"My title","type":"self","is_flair_required":true}}]}'  # Set a Reddit post's subreddit
```

### Analytics

```bash
# Get platform analytics (default: last 7 days)
postqueen analytics:platform <integration-id>

# Get platform analytics for last 30 days
postqueen analytics:platform <integration-id> -d 30

# Get post analytics (default: last 7 days)
postqueen analytics:post <post-id>

# Get post analytics for last 30 days
postqueen analytics:post <post-id> -d 30
```

Returns an array of metrics (e.g. Followers, Impressions, Likes, Comments) with daily data points and percentage change over the period.

**⚠️ IMPORTANT: Missing Release ID Handling**

If `analytics:post` returns `{"missing": true}` instead of an analytics array, the post was published but the platform didn't return a usable post ID. You **must** resolve this before analytics will work:

```bash
# 1. analytics:post returns {"missing": true}
postqueen analytics:post <post-id>

# 2. Get available content from the provider
postqueen posts:missing <post-id>
# Returns: [{"id": "7321456789012345678", "url": "https://...cover.jpg"}, ...]

# 3. Connect the correct content to the post
postqueen posts:connect <post-id> --release-id "7321456789012345678"

# 4. Now analytics will work
postqueen analytics:post <post-id>
```

### Connecting Missing Posts

Some platforms (e.g. TikTok) don't return a post ID immediately after publishing. When this happens, the post's `releaseId` is set to `"missing"` and analytics are unavailable until resolved.

```bash
# List recent content from the provider for a post with missing release ID
postqueen posts:missing <post-id>

# Connect a post to its published content
postqueen posts:connect <post-id> --release-id "<content-id>"
```

Returns an empty array if the provider doesn't support this feature or if the post doesn't have a missing release ID.

### Media Upload

**⚠️ IMPORTANT:** Always upload files to PostQueen before using them in posts. Many platforms (TikTok, Instagram, YouTube) **require verified URLs** and will reject external links.

```bash
# Upload file and get URL
postqueen upload image.jpg

# Accepted: JPEG, PNG, GIF, WebP, AVIF, BMP, TIFF images and MP4 or MOV video.
# PostQueen checks the file's real type; anything else is refused as "Unsupported file type."

# Workflow: Upload, extract the path, use it in a post
VIDEO_PATH=$(postqueen upload video.mp4 | tail -n +2 | jq -r '.path')
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -m "$VIDEO_PATH" -i "tiktok-id" \
  --settings '{"privacy_level":"SELF_ONLY","duet":false,"stitch":false,"comment":true,"autoAddMusic":"no","brand_content_toggle":false,"brand_organic_toggle":false,"content_posting_method":"DIRECT_POST"}'
```

---

## Common Patterns

### Pattern 1: Discover & Use Integration Tools

**Reddit: find a subreddit, then its post types and flairs:**
```bash
# Get Reddit integration ID
REDDIT_ID=$(postqueen integrations:list | tail -n +2 | jq -r '.[] | select(.identifier=="reddit") | .id' | head -n 1)

# Search subreddits: each result's "name" is the /r/... path to use as "subreddit"
postqueen integrations:trigger "$REDDIT_ID" subreddits -d '{"word":"programming"}'

# Allowed post types ("allow": self, link, media), whether a flair is required, and the flairs
RULES=$(postqueen integrations:trigger "$REDDIT_ID" restrictions -d '{"subreddit":"/r/programming"}' | tail -n +2)
echo "$RULES" | jq '.output'
FLAIR_ID=$(echo "$RULES" | jq -r '.output.flairs[0].id')
FLAIR_NAME=$(echo "$RULES" | jq -r '.output.flairs[0].name')

# Use in post (here the subreddit requires a flair)
postqueen posts:create \
  -c "My post content" \
  -s "2026-12-31T12:00:00Z" \
  --settings "{\"subreddit\":[{\"value\":{\"subreddit\":\"/r/programming\",\"title\":\"Post Title\",\"type\":\"self\",\"is_flair_required\":true,\"flair\":{\"id\":\"$FLAIR_ID\",\"name\":\"$FLAIR_NAME\"}}}]}" \
  -i "$REDDIT_ID"
```

**Pinterest: pick a board:**
```bash
PINTEREST_ID=$(postqueen integrations:list | tail -n +2 | jq -r '.[] | select(.identifier=="pinterest") | .id' | head -n 1)
BOARD_ID=$(postqueen integrations:trigger "$PINTEREST_ID" boards | tail -n +2 | jq -r '.output[0].id')
PIN=$(postqueen upload pin.jpg | tail -n +2 | jq -r '.path')

postqueen posts:create \
  -c "Pin description" \
  -s "2026-12-31T12:00:00Z" \
  -m "$PIN" \
  --settings "{\"board\":\"$BOARD_ID\",\"title\":\"My Pin\"}" \
  -i "$PINTEREST_ID"
```

**Discord or Slack: pick a channel:**
```bash
DISCORD_ID=$(postqueen integrations:list | tail -n +2 | jq -r '.[] | select(.identifier=="discord") | .id' | head -n 1)
CHANNEL_ID=$(postqueen integrations:trigger "$DISCORD_ID" channels | tail -n +2 | jq -r '.output[] | select(.name=="announcements") | .id')

postqueen posts:create \
  -c "Release notes are out" \
  -s "2026-12-31T12:00:00Z" \
  --settings "{\"channel\":\"$CHANNEL_ID\"}" \
  -i "$DISCORD_ID"
```

### Pattern 2: Upload Media Before Posting

```bash
# Upload a file and keep its path
VIDEO_PATH=$(postqueen upload video.mp4 | tail -n +2 | jq -r '.path')

# Use in post (TikTok needs every required setting, see Platform-Specific Examples)
postqueen posts:create \
  -c "Check out my video!" \
  -s "2026-12-31T12:00:00Z" \
  -m "$VIDEO_PATH" \
  --settings '{"privacy_level":"SELF_ONLY","duet":false,"stitch":false,"comment":true,"autoAddMusic":"no","brand_content_toggle":false,"brand_organic_toggle":false,"content_posting_method":"DIRECT_POST"}' \
  -i "tiktok-id"
```

### Pattern 3: X Thread

```bash
# Upload every image first (Rule 2)
INTRO=$(postqueen upload intro.jpg | tail -n +2 | jq -r '.path')
P1=$(postqueen upload point1.jpg | tail -n +2 | jq -r '.path')
P2=$(postqueen upload point2.jpg | tail -n +2 | jq -r '.path')
OUTRO=$(postqueen upload outro.jpg | tail -n +2 | jq -r '.path')

# -d is the delay between the parts, in minutes
postqueen posts:create \
  -c "🧵 Thread starter (1/4)" -m "$INTRO" \
  -c "Point one (2/4)" -m "$P1" \
  -c "Point two (3/4)" -m "$P2" \
  -c "Conclusion (4/4)" -m "$OUTRO" \
  -s "2026-12-31T12:00:00Z" \
  -d 2 \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "x-id"
```

### Pattern 4: Multi-Platform Campaign

The `--json` file is sent to the API as the request body, so it uses the API's shape: one entry in `posts` per channel, each with its own content and settings. `image` items are `{"id", "path"}` from the `postqueen upload` result.

```bash
cat > campaign.json << 'EOF'
{
  "type": "schedule",
  "date": "2026-12-31T12:00:00Z",
  "shortLink": true,
  "tags": [],
  "posts": [
    {
      "integration": { "id": "<x integration id>" },
      "value": [
        {
          "content": "Short X version #tech",
          "image": [{ "id": "<upload id>", "path": "<upload path>" }]
        }
      ],
      "settings": { "who_can_reply_post": "everyone" }
    },
    {
      "integration": { "id": "<linkedin integration id>" },
      "value": [
        {
          "content": "Professional LinkedIn version with more context...",
          "image": []
        }
      ]
    }
  ]
}
EOF

postqueen posts:create --json campaign.json
```

### Pattern 5: Validate Settings Before Posting

```bash
#!/bin/bash

INTEGRATION_ID="x-id"
CONTENT="Your post content here"

# Get integration settings (drop the status line first)
SETTINGS_JSON=$(postqueen integrations:settings "$INTEGRATION_ID" | tail -n +2)
MAX_LENGTH=$(echo "$SETTINGS_JSON" | jq '.output.maxLength')

# Provider-specific guidance written for agents. Read it and follow it: it explains
# what the settings values actually do (e.g. which enum value publishes vs. silently
# does not). Do not skip this because a field name looks self-explanatory.
echo "$SETTINGS_JSON" | jq -r '.output.rules // empty'

# The settings JSON schema. Property `description` fields carry the same guidance
# per-field; check them before choosing a value.
echo "$SETTINGS_JSON" | jq '.output.settings'

# Check character limit and truncate if needed
if [ ${#CONTENT} -gt "$MAX_LENGTH" ]; then
  echo "Content exceeds $MAX_LENGTH chars, truncating..."
  CONTENT="${CONTENT:0:$((MAX_LENGTH - 3))}..."
fi

# Create post with settings
postqueen posts:create \
  -c "$CONTENT" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "$INTEGRATION_ID"
```

### Pattern 6: Batch Scheduling

```bash
#!/bin/bash

# Schedule posts for the week
DATES=(
  "2026-02-16T09:00:00Z"
  "2026-02-17T09:00:00Z"
  "2026-02-18T09:00:00Z"
)

CONTENT=(
  "Monday motivation 💪"
  "Tuesday tips 💡"
  "Wednesday wisdom 🧠"
)

for i in "${!DATES[@]}"; do
  # Rule 2: upload each file before passing to -m
  IMG=$(postqueen upload "post-${i}.jpg" | tail -n +2 | jq -r '.path')
  postqueen posts:create \
    -c "${CONTENT[$i]}" \
    -s "${DATES[$i]}" \
    -i "x-id" \
    -m "$IMG" \
    --settings '{"who_can_reply_post":"everyone"}'
  echo "Scheduled: ${CONTENT[$i]} for ${DATES[$i]}"
done
```

### Pattern 7: Error Handling & Retry

```bash
#!/bin/bash

CONTENT="Your post content"
INTEGRATION_ID="bluesky-id"
DATE="2026-12-31T12:00:00Z"
MAX_RETRIES=3

for attempt in $(seq 1 $MAX_RETRIES); do
  if postqueen posts:create -c "$CONTENT" -s "$DATE" -i "$INTEGRATION_ID"; then
    echo "Post created successfully"
    break
  else
    echo "Attempt $attempt failed"
    if [ "$attempt" -lt "$MAX_RETRIES" ]; then
      DELAY=$((2 ** attempt))
      echo "Retrying in ${DELAY}s..."
      sleep "$DELAY"
    else
      echo "Failed after $MAX_RETRIES attempts"
      exit 1
    fi
  fi
done
```

---

## Technical Concepts

### Integration Tools Workflow

Some settings need an ID that only the network knows (a subreddit's flair, a Pinterest board, a Discord channel). The tools workflow fetches them:

1. **Check available tools** - `integrations:settings` returns a `tools` array (empty when the network has none)
2. **Review tool schema** - Each tool has `methodName`, `description`, and `dataSchema` (the keys to pass with `-d`)
3. **Trigger tool** - Call `integrations:trigger <id> <methodName>` with those keys
4. **Use output** - The result comes back as `{"output": ...}`; put the IDs you need into the post settings

**Every tool that exists, by network (`identifier` from `integrations:list`):**

| Network | Tools (`methodName`) | Input (`-d`) | Setting it helps fill |
|---|---|---|---|
| Reddit (`reddit`) | `subreddits` | `{"word":"programming"}` | `subreddit[].value.subreddit` (the result's `name`, a `/r/...` path) |
| Reddit (`reddit`) | `restrictions` | `{"subreddit":"/r/programming"}` | `type` (one of `allow`), `is_flair_required`, `flair` (`{id, name}`) |
| Pinterest (`pinterest`) | `boards` | none | `board` |
| Discord (`discord`) | `channels` | none | `channel` |
| Slack (`slack`) | `channels` | none | `channel` |
| Lemmy (`lemmy`) | `subreddits` (communities) | `{"word":"..."}` | `subreddit[].value` |
| Farcaster (`wrapcast`) | `subreddits` (channels) | `{"word":"..."}` | `subreddit[].value.id` |
| DEV (`devto`) | `tags`, `organizations` | none | `tags`, `organization` |
| Hashnode (`hashnode`) | `tagsList`, `publications` | none | `tags`, `publication` |
| WordPress (`wordpress`) | `postTypes`, `categoriesList`, `tagsList` | none | `type`, `categories`, `tags` |
| Listmonk (`listmonk`) | `list`, `templates` | none | `list`, `template` |
| Dribbble (`dribbble`) | `teams` | none | `team` |
| MeWe (`mewe`) | `groups` | none | `group` |
| Skool (`skool`) | `groups`, then `label` | `label`: `{"id":"<group id>"}` | `group`, `label` |
| Whop (`whop`) | `companies`, then `experiences` | `experiences`: `{"id":"<company id>"}` | `company`, `experience` |
| Instagram, Facebook login (`instagram`) | `audioSearch` | `{"q":"...","type":"music"}` or `"original_sound"` | `audio` |
| TikTok Business (`tiktok-business`) | `musicSearch`, `locationSearch` | `{"genre":"POP"}`, `{"q":"..."}` | `music`, `location` |

X, LinkedIn, LinkedIn Page, Facebook, Threads, YouTube, TikTok and the other networks have no tools. A LinkedIn Page is its own channel, not a setting of a LinkedIn profile.

### Provider Settings Structure

Platform-specific settings go in each post's `settings`. The backend adds the `__type` discriminator from the integration, so you never send it:

```json
{
  "posts": [
    {
      "integration": { "id": "reddit-id" },
      "value": [{ "content": "...", "image": [] }],
      "settings": {
        "subreddit": [{
          "value": {
            "subreddit": "/r/programming",
            "title": "Post Title",
            "type": "self",
            "is_flair_required": false
          }
        }]
      }
    }
  ]
}
```

Pass settings directly:
```bash
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" --settings '{"subreddit":[...]}' -i "reddit-id"
# Backend automatically adds "__type" based on integration ID
```

### Comments and Threading

Posts can have comments (threads on X, replies elsewhere). Each comment can have its own media:

```bash
# Upload every file first (Rule 2)
I1=$(postqueen upload image1.jpg | tail -n +2 | jq -r '.path')
I2=$(postqueen upload image2.jpg | tail -n +2 | jq -r '.path')
CI=$(postqueen upload comment-img.jpg | tail -n +2 | jq -r '.path')
A1=$(postqueen upload another.jpg | tail -n +2 | jq -r '.path')
A2=$(postqueen upload more.jpg | tail -n +2 | jq -r '.path')

# -d 5: wait 5 minutes between the post and each comment
postqueen posts:create \
  -c "Main post" -m "$I1,$I2" \
  -c "Comment 1" -m "$CI" \
  -c "Comment 2" -m "$A1,$A2" \
  -s "2026-12-31T12:00:00Z" \
  -d 5 \
  -i "integration-id"
```

Internally creates (note: every path is a PostQueen-uploaded `.path`, not a raw filename):
```json
{
  "posts": [{
    "integration": { "id": "integration-id" },
    "value": [
      { "content": "Main post", "image": [{ "id": "...", "path": "<uploaded image1>" }, { "id": "...", "path": "<uploaded image2>" }], "delay": 5 },
      { "content": "Comment 1", "image": [{ "id": "...", "path": "<uploaded comment-img>" }], "delay": 5 },
      { "content": "Comment 2", "image": [{ "id": "...", "path": "<uploaded another>" }, { "id": "...", "path": "<uploaded more>" }], "delay": 5 }
    ]
  }]
}
```

### Date Handling

All dates use ISO 8601 format:
- Schedule posts: `-s "2026-12-31T12:00:00Z"`
- List posts: `--startDate "2026-01-01T00:00:00Z" --endDate "2026-12-31T23:59:59Z"`
- Defaults: `posts:list` uses 30 days ago to 30 days from now

### Media Upload Response

`postqueen upload` prints `✅ File uploaded successfully!` and then the media record. The fields you need are `id` and `path`. A video can come back with `"status": "processing"` while PostQueen prepares it; a MOV is converted to MP4 in the background, so prefer MP4.

Extract path for use in posts:
```bash
MEDIA_PATH=$(postqueen upload image.jpg | tail -n +2 | jq -r '.path')
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -m "$MEDIA_PATH" -i "integration-id"
```

### JSON Mode vs CLI Flags

**CLI flags** - Quick posts:
```bash
postqueen posts:create -c "Content" -m "$MEDIA_PATH" -s "2026-12-31T12:00:00Z" -i "bluesky-id"
```

**JSON mode** - Complex posts with multiple platforms and settings:
```bash
postqueen posts:create --json post.json
```

JSON mode supports:
- Multiple platforms with different content per platform
- Different settings per platform
- `type` of `draft`, `schedule` or `now`
- Posts with many comments
- Custom delay between comments

---

## Platform-Specific Examples

### Reddit
```bash
# type is self (text), link (needs "url") or media (the post's first image or MP4)
postqueen posts:create \
  -c "Post content" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"subreddit":[{"value":{"subreddit":"/r/programming","title":"My Title","type":"self","is_flair_required":false}}]}' \
  -i "reddit-id"
```

### YouTube
```bash
# Upload video first (required!)
VIDEO_URL=$(postqueen upload video.mp4 | tail -n +2 | jq -r '.path')

# title and type (public, private or unlisted) are required;
# selfDeclaredMadeForKids ("yes" or "no"), tags and thumbnail are optional.
# On the hosted service, YouTube keeps uploads private until Google's audit of PostQueen passes.
postqueen posts:create \
  -c "Video description" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"title":"Video Title","type":"public","selfDeclaredMadeForKids":"no","tags":[{"value":"tech","label":"Tech"}]}' \
  -m "$VIDEO_URL" \
  -i "youtube-id"
```

### TikTok
```bash
# Upload video first (TikTok only accepts verified URLs!)
VIDEO_URL=$(postqueen upload video.mp4 | tail -n +2 | jq -r '.path')

# Required: privacy_level, duet, stitch, comment, autoAddMusic, brand_content_toggle,
# brand_organic_toggle, content_posting_method. Optional: title, video_made_with_ai.
# privacy_level is PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR or SELF_ONLY;
# on the hosted service TikTok publishes every post as Self only until its audit of PostQueen's app passes.
postqueen posts:create \
  -c "Video caption #fyp" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"privacy_level":"SELF_ONLY","duet":false,"stitch":false,"comment":true,"autoAddMusic":"no","brand_content_toggle":false,"brand_organic_toggle":false,"content_posting_method":"DIRECT_POST"}' \
  -m "$VIDEO_URL" \
  -i "tiktok-id"
```

### X
```bash
# who_can_reply_post is required on every regular post:
# everyone, following, mentionedUsers, subscribers or verified. Use everyone unless asked otherwise.
postqueen posts:create \
  -c "Post content" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "x-id"
```

### LinkedIn
```bash
# Personal profile post
postqueen posts:create -c "Content" -s "2026-12-31T12:00:00Z" -i "linkedin-id"

# A LinkedIn Page is its own channel (identifier linkedin-page): post to its integration ID
postqueen posts:create -c "Company announcement" -s "2026-12-31T12:00:00Z" -i "linkedin-page-id"

# Two or more uploaded images as a swipeable carousel
postqueen posts:create \
  -c "Content" \
  -s "2026-12-31T12:00:00Z" \
  -m "$IMG1,$IMG2" \
  --settings '{"post_as_images_carousel":true,"carousel_name":"Launch"}' \
  -i "linkedin-id"
```

### Instagram
```bash
# Upload image first (Instagram requires verified URLs!)
IMAGE_URL=$(postqueen upload image.jpg | tail -n +2 | jq -r '.path')

# post_type is required: post, reel or story
postqueen posts:create \
  -c "Caption #hashtag" \
  -s "2026-12-31T12:00:00Z" \
  --settings '{"post_type":"post"}' \
  -m "$IMAGE_URL" \
  -i "instagram-id"
```
---

## MCP instead of the CLI

An agent that calls tools instead of running shell commands can use PostQueen's MCP server:

- With the API key: `https://api.postqueen.ai/mcp/<API_KEY>`, 21 tools.
- With OAuth sign-in and no key: `https://api.postqueen.ai/mcp-oauth-dynamic`, 20 tools. A workspace admin approves the connection.

Client setup: https://docs.postqueen.ai/mcp/introduction

---

## Supporting Resources

- [CLI documentation](https://docs.postqueen.ai/cli/introduction)
- [Command reference](https://docs.postqueen.ai/cli/command-reference) - Every command and flag
- [INTEGRATION_TOOLS_WORKFLOW.md](https://github.com/GkhanKINAY/postqueen-agent/blob/main/INTEGRATION_TOOLS_WORKFLOW.md) - Complete tools workflow guide
- [Public API reference](https://api.postqueen.ai/docs)
- `postqueen integrations:settings <id>` - The settings schema, rules and tools of one channel, straight from the API. Trust it over any example here.

---

## Common Gotchas

1. **Not authenticated** - `export POSTQUEEN_API_KEY=key` (PostQueen > Connections > API Keys, admins only) before using the CLI
2. **Invalid integration ID** - Run `integrations:list` to get current IDs
3. **Settings schema mismatch** - Check `integrations:settings` for required fields
4. **Media MUST be uploaded to PostQueen first** - ⚠️ **CRITICAL (Rule 2):** Every value passed to `-m` or to an `image` field in JSON mode must be a `.path` returned by `postqueen upload`. Raw local filenames (`image.jpg`) and external URLs (`https://...`) will be rejected. No exceptions: even a "quick test post" needs the upload step.
5. **JSON escaping in shell** - Use single quotes for JSON: `--settings '{...}'`
6. **Date format** - Must be ISO 8601: `"2026-12-31T12:00:00Z"` and is REQUIRED
7. **Tool not found** - Only the tools in `integrations:settings` exist; any other name fails with `Tool not found`
8. **Character limits** - Each platform has different limits, check `maxLength` in settings
9. **Required settings** - Some platforms require specific settings: X `who_can_reply_post`, Reddit `subreddit` (with `title`, `type`, `is_flair_required`), YouTube `title` and `type`, TikTok (see its example), Instagram `post_type`, Pinterest `board`, Discord and Slack `channel`
10. **Status line before the JSON** - Pipe through `tail -n +2` before `jq`
11. **Analytics returns `{"missing": true}`** - The post was published but the platform didn't return a post ID. Run `posts:missing <post-id>` to get available content, then `posts:connect <post-id> --release-id "<id>"` to link it. Analytics will work after connecting.
12. **`posts:settings` merges** - Only the keys you pass change; everything else on the post is preserved, so pass a partial object, not the full settings blob. Only **DRAFT/QUEUE** (unpublished) posts can be updated; published posts are rejected. Pass the **main post id**, not a comment id. Never include `__type`: the backend adds it automatically from the integration.

---

## Quick Reference

```bash
# ⚠️ AUTHENTICATE FIRST - required before any other command
postqueen auth:status                                             # Check if authenticated
export POSTQUEEN_API_KEY=key                                      # Set the API key
postqueen auth:login                                              # Explains the API key (or logs in via your own --auth-server)

# Discovery (only after auth is confirmed)
postqueen integrations:list                           # Get integration IDs
postqueen integrations:list --group <group-id>        # Get integration IDs in a group
postqueen integrations:groups                         # List groups (customers)
postqueen integrations:settings <id>                  # Get settings schema, rules and tools
postqueen integrations:trigger <id> <method> -d '{}'  # Fetch dynamic data

# Posting (date is REQUIRED)
postqueen posts:create -c "text" -s "2026-12-31T12:00:00Z" -i "id"                  # Simple
postqueen posts:create -c "text" -s "2026-12-31T12:00:00Z" -t draft -i "id"        # Draft
postqueen posts:create -c "text" -m "$(postqueen upload img.jpg | tail -n +2 | jq -r '.path')" -s "2026-12-31T12:00:00Z" -i "id"  # With media (upload first, Rule 2)
postqueen posts:create -c "main" -c "comment" -s "2026-12-31T12:00:00Z" -i "id"    # With comment
postqueen posts:create -c "text" -s "2026-12-31T12:00:00Z" --settings '{}' -i "id" # Platform-specific
postqueen posts:create --json file.json                                             # Complex

# Management
postqueen posts:list                                  # List posts
postqueen posts:delete <id>                          # Delete post
postqueen posts:status <id> --status draft           # Move to draft (stops workflow)
postqueen posts:status <id> --status schedule        # Queue draft for publishing
postqueen posts:settings <id> --settings '{}'        # Patch a post's settings (merged; DRAFT/QUEUE only)
postqueen upload <file>                              # Upload media

# Analytics
postqueen analytics:platform <id>                    # Platform analytics (7 days)
postqueen analytics:platform <id> -d 30             # Platform analytics (30 days)
postqueen analytics:post <id>                        # Post analytics (7 days)
postqueen analytics:post <id> -d 30                 # Post analytics (30 days)
# If analytics:post returns {"missing": true}, resolve it:
postqueen posts:missing <id>                         # List provider content
postqueen posts:connect <id> --release-id "<rid>"    # Connect content to post

# Help
postqueen --help                                     # Show help
postqueen posts:create --help                        # Command help
```
