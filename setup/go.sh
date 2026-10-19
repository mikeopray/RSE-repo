#!/bin/sh
# One-step setup for a Mac: places this folder where Claude Code loads skills, prepares the private workspace, activates the licence key and installs everything else.
#   sh setup/go.sh --key RSE-XXXXX-XXXXX-XXXXX-XXXXX [--replace]
# It does exactly what the three separate steps did (install.sh --env-only, activate.sh --key, install.sh), in one command. Safe to re-run: finished steps are skipped.
set -e
SRC="$(cd "$(dirname "$0")/.." && pwd)"; DEST="$HOME/.claude/skills/reels-sin-editor"; KEY=""; MOVE=""
while [ $# -gt 0 ]; do case "$1" in --key) KEY="$2"; shift 2 ;; --replace) MOVE="--replace"; shift ;; *) shift ;; esac; done
[ -n "$KEY" ] || { echo "SETUP_FAILED: I need the licence key from your purchase email (it looks like RSE-XXXXX-XXXXX-XXXXX-XXXXX)."; exit 1; }
if [ "$SRC" != "$DEST" ]; then
  if [ -e "$DEST" ]; then echo "Reels Sin Editor is already in $DEST: using it, nothing was replaced."
  else mkdir -p "$HOME/.claude/skills"; cp -R "$SRC" "$DEST"; echo "Copied the product folder to $DEST"; fi
fi
[ -f "$DEST/setup/install.sh" ] || { echo "SETUP_FAILED: $DEST does not look like the Reels Sin Editor folder. Move it aside and run the setup again."; exit 1; }
sh "$DEST/setup/install.sh" --env-only
sh "$DEST/setup/activate.sh" --key "$KEY" $MOVE
sh "$DEST/setup/install.sh"
