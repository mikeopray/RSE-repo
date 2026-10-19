#!/bin/sh
# Reels Sin Editor - lets Claude Code's Auto mode run the product's own commands without stopping.
# YOU run it once (from the Claude Code message box:  ! sh ~/.claude/skills/reels-sin-editor/setup/allow.sh   or the raw-link form).
# It adds a few narrow permission rules to your ~/.claude/settings.json (a backup is saved first). It adds ONLY these:
#   Skill(reels-sin-editor) and one Skill(...) rule for each Reels Sin Editor command in ~/.claude/skills (/reel-<style>, /carousel-<style>, /estilo-*)
#   Bash(sh <this skill's folder>/setup/rse.sh *)  - the one command the product's tools run through (and its go.sh / install.sh / activate.sh)
# Nothing else is changed. To undo:  sh allow.sh --remove     (it takes out exactly those rules).
SK="$HOME/.claude/skills/reels-sin-editor"; PY="${RSE_PY:-${RSE_HOME:-$HOME/ReelsSinEditor}/venv/bin/python}"
[ -x "$PY" ] || { echo "ALLOW_FAILED: the product is not installed yet (no private Python found). Install it first."; exit 1; }
[ -d "$SK" ] || { echo "ALLOW_FAILED: $SK not found."; exit 1; }
exec "$PY" - "$SK" "$@" <<'PYEOF'
import json, os, pathlib, shlex, shutil, sys, time
SK = pathlib.Path(sys.argv[1]); remove = "--remove" in sys.argv[2:]
SKILLS = SK.parent; settings = pathlib.Path.home() / ".claude" / "settings.json"
rules = ["Skill(reels-sin-editor)", "Skill(reels-sin-editor *)"]
for d in sorted(SKILLS.iterdir()):
    f = d / "SKILL.md"
    if d.name.startswith(("reel-", "carousel-", "estilo-")) and f.exists() and "managed-by: reels-sin-editor" in f.read_text(errors="ignore"):
        rules += [f"Skill({d.name})", f"Skill({d.name} *)"]
for tool in ("rse.sh", "go.sh", "install.sh", "activate.sh"): rules.append("Bash(sh " + shlex.quote(str(SK / "setup" / tool)) + " *)")
try: cur = json.loads(settings.read_text(encoding="utf-8")) if settings.exists() else {}
except Exception as e: print("ALLOW_FAILED: ~/.claude/settings.json is not valid JSON (" + str(e)[:80] + "). Nothing was changed."); sys.exit(1)
perm = cur.setdefault("permissions", {}); allow = perm.setdefault("allow", [])
if not isinstance(allow, list): print("ALLOW_FAILED: permissions.allow is not a list. Nothing was changed."); sys.exit(1)
before = list(allow)
if remove: allow[:] = [r for r in allow if r not in rules]
else: allow.extend(r for r in rules if r not in allow)
if allow == before: print("Nothing to change: the rules are already " + ("absent." if remove else "in place.")); sys.exit(0)
settings.parent.mkdir(parents=True, exist_ok=True)
had = settings.exists()
if had: shutil.copy2(settings, settings.with_name("settings.json.rse-backup-" + time.strftime("%Y%m%d-%H%M%S")))
tmp = settings.with_name("settings.json.rse-tmp"); tmp.write_text(json.dumps(cur, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); os.replace(tmp, settings)
print(("Removed" if remove else "Added") + " these permission rules in ~/.claude/settings.json" + (" (a backup was saved next to it):" if had else " (the file did not exist, so it was created):"))
for r in rules: print("  " + r)
print("Open a NEW chat for them to apply.")
PYEOF
