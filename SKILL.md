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
The licence key (it looks like RSE-XXXXX-XXXXX-XXXXX-XXXXX) is what the user typed after the command: `$ARGUMENTS`. If it is empty, ask for the key from the purchase email, once. Then run ONE command, exactly as written, with no `cd`, no pipes, no `&&` or `;`, no output redirection and nothing added to the line. It prepares the private workspace, activates the key and installs everything else, in that order:
- Mac: `sh ${CLAUDE_SKILL_DIR}/setup/go.sh --key <KEY>`
- Windows: `cmd /c ${CLAUDE_SKILL_DIR}\setup\go.cmd --key <KEY>`
Run it as a BACKGROUND command (the Bash tool's background option): it takes 10-30 minutes the first time. Say once, in one plain sentence, "Setting up, this takes a few minutes the first time; I'll tell you when it's done", then follow its progress by reading its output file with the Read tool (never with shell commands such as `tail`, `cat` or `grep`, and never `sleep`) and tell the user in plain words how it goes. If it says the licence is already on another computer, tell the user and offer to run the same command again with `--replace` added. If it prints `INSTALL_FAILED`, say why in one sentence and run the same command once more (finished steps are skipped). READY means done.
When it is done, tell the user in one or two plain sentences, in their language: Reels Sin Editor is installed and activated (mention the date updates are included until, if the output shows it), and to make their first reel they should open a NEW chat (close this one) and type `/reel-signature-warm` and add their video. Do NOT read, run or follow any of the newly installed files in this chat: the installation replaced this folder's instructions, and they are used from the new chat.

## If Claude Code blocks the command
Auto mode may stop this command (it downloads software and sends the licence key to the product's server). Do not look for ways around it and do not ask the user to change settings. Say, in plain words and in the user's language: "Your Claude settings stopped this step. Please copy the line below, paste it into the message box here and press Enter. It starts with an exclamation mark, which makes Claude Code run it for you directly. It takes 10 to 30 minutes the first time and shows its progress; keep this window open until it says READY." Then show exactly one line, with the key filled in and the full path of this folder, in a code block:
`! sh ${CLAUDE_SKILL_DIR}/setup/go.sh --key <KEY>`
(Windows: `! cmd /c ${CLAUDE_SKILL_DIR}\setup\go.cmd --key <KEY>`.) Wait for the user; when the output ends with READY, finish with the same short message as above (new chat, `/reel-signature-warm`); do not read or follow the newly installed files here.

---
*(c) 2026 melimoyano.com. Todos los derechos reservados. Reels Sin Editor se licencia, no se vende: queda prohibido copiar, reproducir, compartir, recrear, imitar, revender o crear obras derivadas de este material, en todo o en parte, y usarlo para entrenar IA. Ver el archivo LICENSE.*

*(c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.*
