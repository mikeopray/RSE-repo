#!/usr/bin/env python3
"""sync_commands - (re)create the slash commands: the shipped helpers (commands/*), and for every style (built-in + user) one /reel-<style> and one /carousel-<style>. Only touches skill folders marked as managed by Reels Sin Editor.
Run by install.sh, update.py and style_create.py."""
import json, os, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine")); import style_validate as V
HOME = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")); SKILLS = pathlib.Path(os.environ.get("RSE_SKILLS_DIR", pathlib.Path.home() / ".claude" / "skills"))
MARK = "managed-by: reels-sin-editor"
def rse_prefix():
    """the ONE command every product tool is run with, written out as an absolute path. A slash command the user types carries its own allowed-tools, which then apply to exactly this command; a skill that Claude itself loads through the Skill tool is judged as untrusted code by auto mode (found 2026-10-19), so the commands never ask Claude to do that."""
    import shlex
    if os.name == "nt": q = str(ROOT / "setup" / "rse.cmd"); return "cmd /c " + (f'"{q}"' if " " in q else q)
    return "sh " + shlex.quote(str(ROOT / "setup" / "rse.sh"))
RSE = rse_prefix(); RUNLINE = f"Run every product tool with exactly this command prefix: `{RSE}`. Where the documents say `RSE <tool> <arguments>`, run `{RSE} <tool> <arguments>` as ONE plain command (no `cd`, no pipes, no `&&` or `;`, no output redirection)."
def ours(d): 
    f = d / "SKILL.md"; return f.exists() and MARK in f.read_text(errors="ignore")
def style_stub(name, label, desc):
    return f'''---
name: reel-{name}
description: Edit the attached raw video into a finished reel in the "{label}" style (Reels Sin Editor). Use for /reel-{name} with a video attached or its path given, or when the user asks for a reel in the {label} style. {desc}
allowed-tools: Bash({RSE} *)
---
<!-- {MARK} -->
Edit the user's video using the Reels Sin Editor skill with style `{name}`.
1. Use the attached video or the path the user gave; if there is none, ask for it.
2. Read `{ROOT}/SKILL.md` and `{ROOT}/flows/edit.md` with the Read tool, then run the edit with `--style {name}` as AUTOPILOT: do not ask the user questions (the playbook decides lines, retakes, hook, numbers, names and effects); deliver the finished reel and then ONE summary message of what you decided. The style folder is `~/ReelsSinEditor/styles/{name}/` (or the built-in `styles/{name}/`). Use only that style's fonts, colours and effects.
3. {RUNLINE}
4. Talk to the user in the language they write in.
'''
def carousel_stub(name, label, desc):
    return f'''---
name: carousel-{name}
description: Create a finished Instagram carousel (1080x1350 slides) in the "{label}" style (Reels Sin Editor) from a topic, a script, a reel video, or the user's own photos (or graphics only). Use for /carousel-{name} followed by what the carousel is about, or when the user asks for a carousel in the {label} style. {desc}
allowed-tools: Bash({RSE} *)
---
<!-- {MARK} -->
Make the user's carousel using the Reels Sin Editor skill with style `{name}`.
1. The input is whatever the user gave after the command: a topic or idea, a script, a reel video (attached or a path), photos (attached or a folder path), or a mix. With photos the carousel is photo-driven; without photos it is graphics only. If there is nothing at all, ask for the topic in one short question.
2. Read `{ROOT}/SKILL.md` and `{ROOT}/flows/carousel.md` with the Read tool, then follow `flows/carousel.md` with `--style {name}` as AUTOPILOT: write the plan in the creator's own language and words, run the render, check the contact sheet, deliver the slides, then ONE short summary message. The style folder is `~/ReelsSinEditor/styles/{name}/` (or the built-in `styles/{name}/`). Use only that style's fonts and colours.
3. {RUNLINE}
4. Talk to the user in the language they write in.
'''
def main():
    SKILLS.mkdir(parents=True, exist_ok=True); made = []
    for c in sorted((ROOT / "commands").iterdir()) if (ROOT / "commands").exists() else []:
        if c.is_dir() and (c / "SKILL.md").exists():
            t = SKILLS / c.name
            if t.exists() and not ours(t): print(f"skipped {c.name}: another skill with that name exists"); continue
            shutil.copytree(c, t, dirs_exist_ok=True); made.append(c.name)
            f = t / "SKILL.md"; f.write_text(f.read_text(encoding="utf-8").replace("{{RSE}}", RSE).replace("{{ROOT}}", str(ROOT)), encoding="utf-8")
    styles = [p for p in (ROOT / "styles").iterdir() if p.is_dir() and not p.name.startswith("_")] + (list((HOME / "styles").iterdir()) if (HOME / "styles").exists() else [])
    keep = set()
    for s in styles:
        if not (s / "style.json").exists() or V.check(s)[0]: continue      # missing or invalid styles get no command
        j = json.loads((s / "style.json").read_text(encoding="utf-8")); n = j.get("name", s.name)
        for cmd, make in (("reel", style_stub), ("carousel", carousel_stub)):                       # one command per product feature, each checked on its own
            t = SKILLS / f"{cmd}-{n}"; keep.add(t.name)
            if t.exists() and not ours(t): print(f"skipped {cmd}-{n}: another skill with that name exists"); continue
            t.mkdir(exist_ok=True); (t / "SKILL.md").write_text(make(n, j.get("label", n), j.get("description", "")), encoding="utf-8"); made.append(t.name)
    for t in list(SKILLS.glob("reel-*")) + list(SKILLS.glob("carousel-*")):          # style deleted -> remove its commands
        if t.name not in keep and t.is_dir() and ours(t): shutil.rmtree(t)
    print("commands:", ", ".join(made))
if __name__ == "__main__": main()
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
