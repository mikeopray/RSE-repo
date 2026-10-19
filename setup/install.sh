#!/bin/sh
# Reels Sin Editor installer (macOS, Apple Silicon). Needs nothing from the user: no Homebrew, no admin password, no Terminal steps.
# It builds a private environment in ~/ReelsSinEditor/venv (Python 3.12, ffmpeg, Node) with micromamba (pinned + checksummed), then adds the Python packages, the animation
# library, the speech model (about 3 GB) and the renderer. The first time takes a few minutes (mostly downloads). Safe to re-run: finished steps are skipped.
set -e
HOME_DIR="${RSE_HOME:-$HOME/ReelsSinEditor}"; VENV="$HOME_DIR/venv"; TOOLS="$HOME_DIR/tools"; HERE="$(cd "$(dirname "$0")" && pwd)"
step() { echo "[$1/6] $2"; }
[ "$(uname -s)" = Darwin ] || { echo "This installer is for a Mac (Windows uses setup\\install.cmd)."; exit 1; }
ARCH=$(uname -m); [ "$(sysctl -n hw.optional.arm64 2>/dev/null)" = 1 ] && ARCH=arm64          # an Apple-chip Mac stays arm64 even when the shell runs under Rosetta
case "$ARCH" in
  arm64) MM_ASSET="micromamba-osx-arm64"; MM_SHA="ec2a072f028e1a7cf20f3e2e74d5a8127cf5a5f27636375b5359811565f4e5be" ;;
  x86_64) MM_ASSET="micromamba-osx-64"; MM_SHA="1e71054bb3ac9a076e21f7ec48acfef536f9b3f1408f371a942784bf5ef83d8a" ;;
  *) echo "INSTALL_FAILED: this Mac's processor ($ARCH) is not supported."; exit 1 ;;
esac
mkdir -p "$HOME_DIR/projects" "$HOME_DIR/styles" "$TOOLS"
MM_VER="2.9.0-0"; MM="$TOOLS/mm-$MM_VER-$ARCH/micromamba"
export MAMBA_ROOT_PREFIX="$TOOLS/mamba"
step 1 "Preparing Python 3.12, ffmpeg and Node (private copy, nothing is installed system-wide)..."
if ! { [ -x "$VENV/bin/python" ] && [ -x "$VENV/bin/ffmpeg" ] && [ -x "$VENV/bin/ffprobe" ] && [ -x "$VENV/bin/node" ] && "$VENV/bin/python" -c "import sys; sys.exit(0 if sys.version_info[:2]==(3,12) else 1)" 2>/dev/null; }; then
  if [ ! -x "$MM" ]; then
    mkdir -p "$TOOLS/mm-$MM_VER-$ARCH"
    curl -fsSL -o "$MM.part" "https://github.com/mamba-org/micromamba-releases/releases/download/$MM_VER/$MM_ASSET" || { echo "INSTALL_FAILED: could not download the environment tool. Check the internet connection and run setup again."; exit 1; }
    [ "$(shasum -a 256 "$MM.part" | cut -d' ' -f1)" = "$MM_SHA" ] || { rm -f "$MM.part"; echo "INSTALL_FAILED: the downloaded environment tool did not match its checksum, so it was discarded for safety."; exit 1; }
    mv "$MM.part" "$MM"; chmod +x "$MM"
  fi
  rm -rf "$VENV"
  "$MM" create -y -q -p "$VENV" -c conda-forge --override-channels python=3.12 ffmpeg nodejs || { echo "INSTALL_FAILED: could not create the environment. Check the internet connection and run setup again."; exit 1; }
fi
export PATH="$VENV/bin:$PATH" HF_HUB_DISABLE_SYMLINKS_WARNING=1
[ "$1" = "--env-only" ] && { echo "ENV_READY"; exit 0; }          # used before activation: gives the product its own Python so nothing depends on the Mac's
step 2 "Installing the Python packages..."
"$VENV/bin/pip" install -q --upgrade pip && "$VENV/bin/pip" install -q -r "$HERE/requirements.txt"
chmod +x "$HERE/../engine/segbatch-arm64"
step 3 "Installing the animation library..."
npm install --prefix "$HOME_DIR" gsap@3.15.0 capcut-cli@0.28.0 --no-audit --no-fund --silent
step 4 "Downloading the speech models (about 6 GB in total, one time - this is the long step)..."
"$VENV/bin/python" - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("Systran/faster-whisper-large-v3")
PY
echo "     Also downloading the Parakeet speech model (about 2.6 GB) and the audio-classifier model (327 MB)..."
"$VENV/bin/python" "$HERE/install_parakeet.py" || echo "     (The Parakeet extras could not be installed. The app still works: it uses the Whisper speech stage. Run setup again later to retry.)"
step 5 "Preparing the video renderer (downloads a small headless browser)..."
(cd "$HERE" && npx --yes hyperframes@0.8.140 browser ensure) || { echo "INSTALL_FAILED: could not download the headless browser the video renderer needs. Check the internet connection and run setup again."; exit 1; }
step 6 "Final check..."
"$VENV/bin/python" "$HERE/sync_commands.py"
"$VENV/bin/python" "$HERE/doctor.py"
