# Reels Sin Editor

Edit a raw talking-head video into a finished vertical reel, with captions, motion graphics and sound, inside Claude Code. Licensed product: you need a licence key (from your purchase email).
Mac with Apple chip (M1 or newer) for now. Windows is coming.

## Install (no Terminal needed)

**1. Open Claude Code** (the Code tab in the Claude desktop app) and **start a new session**: pick any folder (for example Desktop) and send any first message, such as "hi". Shell lines only work inside a session.

**2. Paste this line into the message box and press Enter** (it starts with `!`, which makes Claude Code run it directly; replace the key with yours):

```
! curl -fsSL https://raw.githubusercontent.com/mikeopray/RSE-repo/bang-install/install.sh | sh -s -- RSE-XXXXX-XXXXX-XXXXX-XXXXX
```

**3. Wait for READY.** The first time takes about 10 to 30 minutes (it downloads about 6 GB) and shows its progress. Keep the window open. If it stops early, paste the same line again: finished steps are skipped.

**4. Make your first reel.** Open a new chat and type `/reel-signature-warm`, then add your video.

## What the installation does (everything stays in your user folder)

- Puts this skill in `~/.claude/skills/reels-sin-editor` (step 2).
- Creates a private workspace in `~/ReelsSinEditor`: its own Python 3.12, ffmpeg and Node (made with micromamba, pinned and checksum-verified), the Python packages, the speech models and a small headless browser for rendering. No administrator password, nothing is installed system-wide.
- Activates your licence key with the product's licence server (it receives the key and an identifier of this computer) and downloads the rest of the product.
- To remove it: delete the two folders `~/.claude/skills/reels-sin-editor` and `~/ReelsSinEditor`.

---

## Instalar (sin Terminal)

**1. Abre Claude Code** (la pestaña Code de la app de Claude) y **empieza una sesión nueva**: elige cualquier carpeta (por ejemplo Escritorio) y envía un primer mensaje, como "hola". Las líneas con ! solo funcionan dentro de una sesión.

**2. Pega esta línea en la caja de mensaje y pulsa Enter** (empieza con `!`, así Claude Code la ejecuta directamente; cambia la clave por la tuya):

```
! curl -fsSL https://raw.githubusercontent.com/mikeopray/RSE-repo/bang-install/install.sh | sh -s -- RSE-XXXXX-XXXXX-XXXXX-XXXXX
```

**3. Espera a que diga READY.** La primera vez tarda de 10 a 30 minutos (descarga unos 6 GB) y muestra el avance. Deja la ventana abierta. Si se detiene antes, pega la misma línea otra vez: los pasos terminados se saltan.

**4. Haz tu primer reel.** Abre un chat nuevo, escribe `/reel-signature-warm` y añade tu video.

Todo queda dentro de tu carpeta de usuario. Para quitarlo, borra las dos carpetas `~/.claude/skills/reels-sin-editor` y `~/ReelsSinEditor`.

---
(c) 2026 melimoyano.com. All rights reserved. Licensed, not sold. See LICENSE. Third-party credits: NOTICES.md.
