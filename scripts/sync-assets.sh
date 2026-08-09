#!/usr/bin/env bash
# Mirror the docs artwork into .github/assets, which is what README.md embeds.
#
# GitHub will not render an image from images/ in a README reliably across
# forks and raw views, so the README keeps its own copy. That copy was kept by
# hand and ten files had already drifted from their source, including the
# Claude Code icon, which meant the README showed Claude Code wearing Claude's
# logo long after the docs had been fixed. Run this after touching images/brand.
set -euo pipefail
cd "$(dirname "$0")/.."

copied=0
for src in images/brand/*.svg images/brand/*.png; do
  [ -e "$src" ] || continue
  dst=".github/assets/$(basename "$src")"
  # Only files the README already mirrors; this is not a bulk export.
  [ -e "$dst" ] || continue
  if ! cmp -s "$src" "$dst"; then
    cp "$src" "$dst"
    echo "synced $(basename "$src")"
    copied=$((copied + 1))
  fi
done

for src in images/channels/*; do
  dst=".github/assets/channels/$(basename "$src")"
  [ -e "$dst" ] || continue
  if ! cmp -s "$src" "$dst"; then
    cp "$src" "$dst"
    echo "synced channels/$(basename "$src")"
    copied=$((copied + 1))
  fi
done

echo "sync-assets: $copied file(s) updated"
