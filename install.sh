#!/bin/sh
# Reels Sin Editor - one-step install for a Mac with an Apple chip.
# YOU run it, from the Claude Code prompt (a line that starts with "!"), so Claude does not have to run anything:
#   ! curl -fsSL https://raw.githubusercontent.com/mikeopray/RSE-repo/bang-install/install.sh | sh -s -- RSE-XXXXX-XXXXX-XXXXX-XXXXX
# What it does (everything stays in your user folder; no administrator password):
#   1. puts the small starter skill in ~/.claude/skills/reels-sin-editor (downloaded from the product's own server)
#   2. runs the skill's setup (setup/go.sh): a private Python / ffmpeg / Node, activates your key with the licence server,
#      downloads the product and the speech models (about 6 GB, 10-30 minutes the first time)
# Safe to run again: finished steps are skipped. To remove everything: delete ~/.claude/skills/reels-sin-editor and ~/ReelsSinEditor.
set -e
SERVER="${RSE_SERVER:-https://reels-sin-editor-license.michaelopray.workers.dev}"
fail() { echo "INSTALL_FAILED: $1"; exit 1; }
KEY="${1:-}"; [ "$KEY" = "--key" ] && KEY="${2:-}"
case "$KEY" in RSE-*-*-*-*) ;; *) fail "I need your licence key (RSE-XXXXX-XXXXX-XXXXX-XXXXX) after the command." ;; esac
[ "$(uname -s)" = Darwin ] || fail "this installer is for a Mac (Windows is coming)."
DEST="$HOME/.claude/skills/reels-sin-editor"
mkdir -p "$HOME/.claude/skills"
if [ ! -f "$DEST/setup/go.sh" ]; then
  if [ -e "$DEST" ]; then mv "$DEST" "$DEST.old-$(date +%s)"; echo "(an older folder was moved aside)"; fi
  T="$(mktemp -d)"; echo "Downloading the starter..."
  curl -fsSL "${RSE_STARTER_URL:-$SERVER/download}" -o "$T/s.zip" </dev/null || fail "could not download the starter. Check the internet connection and paste the line again."
  unzip -q "$T/s.zip" -d "$T/x" </dev/null || fail "the starter download was damaged. Paste the line again."
  [ -f "$T/x/reels-sin-editor/setup/go.sh" ] || fail "the starter download does not look right. Paste the line again."
  mv "$T/x/reels-sin-editor" "$DEST"; rm -rf "$T"
fi
echo "Starter in place: $DEST"
if [ -n "$RSE_DRY_RUN" ]; then echo "DRY RUN: would run: sh $DEST/setup/go.sh --key <KEY>"; exit 0; fi
echo "Setting up (this takes 10-30 minutes the first time; it downloads about 6 GB). Keep this window open until it says READY."
exec sh "$DEST/setup/go.sh" --key "$KEY" </dev/null
