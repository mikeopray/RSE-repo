---
name: reels-sin-editor
description: Installer for Reels Sin Editor, a tool that edits raw talking-head videos into finished vertical reels inside Claude Code. Use when the user asks to install or set up Reels Sin Editor, or drops this folder in the chat.
allowed-tools: Bash(sh ${CLAUDE_SKILL_DIR}/setup/go.sh *) Bash(cmd /c ${CLAUDE_SKILL_DIR}\setup\go.cmd *) Bash(sh ${CLAUDE_SKILL_DIR}/setup/install.sh *) Bash(sh ${CLAUDE_SKILL_DIR}/setup/activate.sh *) Bash(cmd /c ${CLAUDE_SKILL_DIR}\setup\install.cmd *) Bash(cmd /c ${CLAUDE_SKILL_DIR}\setup\activate.cmd *)
---
<!-- managed-by: reels-sin-editor -->
# Reels Sin Editor - installer

This folder is the small first download of Reels Sin Editor. When the user asks you to install it, you are doing exactly what they asked: installing the tool and everything it needs to run.

## What the installation does
Everything stays inside the user's own folders. No administrator rights are used and nothing is installed system-wide.
- This folder is the skill the user installed from GitHub into their Claude skills folder (`~/.claude/skills/reels-sin-editor`; on Windows `%USERPROFILE%\.claude\skills\reels-sin-editor`). Nothing is copied.
- Creates a private workspace in `~/ReelsSinEditor` (Windows: `%USERPROFILE%\ReelsSinEditor`) holding the components the tool needs, downloaded from official sources with integrity checks.
- Activates the user's licence key with the product's licence server (it receives the key and an identifier of this computer) and downloads the rest of the product.
- Installs the remaining components in the background.

## Steps (the user typed /reels-sin-editor, which authorises them)
Ask for the licence key from the purchase email (it looks like RSE-XXXXX-XXXXX-XXXXX-XXXXX) if the user has not given it. Then run ONE command, exactly as written, with no `cd`, no pipes, no `&&` or `;`, no output redirection and nothing added to the line. It prepares the private workspace, activates the key and installs everything else, in that order:
- Mac: `sh ${CLAUDE_SKILL_DIR}/setup/go.sh --key <KEY>`
- Windows: `cmd /c ${CLAUDE_SKILL_DIR}\setup\go.cmd --key <KEY>`
Run it as a BACKGROUND command (the Bash tool's background option): it takes 10-30 minutes the first time. Say once, in one plain sentence, "Setting up, this takes a few minutes the first time; I'll tell you when it's done", then follow its output (the completion notice, never `sleep`) and tell the user in plain words how it goes. If it says the licence is already on another computer, tell the user and offer to run the same command again with `--replace` added. If it prints `INSTALL_FAILED`, say why in one sentence and run the same command once more (finished steps are skipped). READY means done.
When it is done, read `SKILL.md` in this folder again (the installation replaced it with the full product instructions) and follow its "After setup" section.

## If a step is blocked
If Claude Code asks for approval, or its safety check blocks a step, do not look for ways around it. Tell the user in one plain sentence what you were trying to do, and ask them to reply with the exact sentence below (their own message naming the exact command is what lets Claude Code allow it): `Yes, run: <the exact command>` (in Spanish: `Sí, ejecuta: <el comando exacto>`). When they reply, run exactly that command once. Only if it is still blocked, give them that single command to paste into the Terminal app (Windows: Command Prompt).

---
*(c) 2026 melimoyano.com. Todos los derechos reservados. Reels Sin Editor se licencia, no se vende: queda prohibido copiar, reproducir, compartir, recrear, imitar, revender o crear obras derivadas de este material, en todo o en parte, y usarlo para entrenar IA. Ver el archivo LICENSE.*

*(c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.*
