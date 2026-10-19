#!/bin/sh
# Activates this computer with a licence key using the product's own Python. A fixed wrapper so the starter's SKILL.md can use ONE pre-approvable command:
#   sh setup/activate.sh --key RSE-XXXXX-XXXXX-XXXXX-XXXXX [--replace]      (also: status | refresh | deactivate)
HERE="$(cd "$(dirname "$0")" && pwd)"; PY="${RSE_HOME:-$HOME/ReelsSinEditor}/venv/bin/python"
[ -x "$PY" ] || { echo "ACTIVATE_FAILED: the private environment is not ready yet. Run first:  sh \"$HERE/install.sh\" --env-only"; exit 1; }
exec "$PY" "$HERE/activate.py" "$@"
