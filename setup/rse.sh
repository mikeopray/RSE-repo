#!/bin/sh
# Runs ONE of the product's own tools with the product's own Python, so a single fixed command can be pre-approved:
#   sh setup/rse.sh engine/run_edit.py auto "<video>" --style signature-warm      (also setup/*.py and engine/*.sh)
# It only runs files inside this product's own engine/ and setup/ folders and refuses anything else. The working folder is kept as it is.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; PY="${RSE_HOME:-$HOME/ReelsSinEditor}/venv/bin/python"
T="$1"; [ -n "$T" ] || { echo "RSE_USAGE: sh setup/rse.sh engine/<tool>.py [arguments]"; exit 2; }
case "$T" in *..*|/*) echo "RSE_REFUSED: this wrapper only runs the product's own engine/ and setup/ tools."; exit 2 ;; esac
shift
case "$T" in
  engine/*.py|setup/*.py)
    [ -x "$PY" ] || { echo "RSE_FAILED: the private environment is not ready. Run the setup again (sh \"$ROOT/setup/install.sh\")."; exit 1; }
    exec "$PY" "$ROOT/$T" "$@" ;;
  engine/*.sh) exec sh "$ROOT/$T" "$@" ;;
  *) echo "RSE_REFUSED: this wrapper only runs the product's own engine/ and setup/ tools."; exit 2 ;;
esac
