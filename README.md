# Reels Sin Editor

Edit a raw talking-head video into a finished vertical reel, with captions, motion graphics and sound, inside Claude Code. Licensed product: you need a licence key (from your purchase email).
Mac with Apple chip (M1 or newer) for now. Windows is coming.

## Install (no Terminal needed)

**1. Open Claude Code** (the Code tab in the Claude desktop app).

**2. Paste this message and press Enter:**

```
Install this skill for me: https://github.com/mikeopray/RSE-repo (put it in ~/.claude/skills/reels-sin-editor)
```

**3. Type this and press Enter, then give your licence key when it asks:**

```
/reels-sin-editor
```

**4. Wait for READY.** The first time takes about 10 to 30 minutes (it downloads about 6 GB). Claude tells you how it is going. If Claude asks for permission, allow it.

**5. Make your first reel.** Open a new chat and type `/reel-signature-warm`, then add your video.

## What the installation does (everything stays in your user folder)

- Puts this skill in `~/.claude/skills/reels-sin-editor` (step 2).
- Creates a private workspace in `~/ReelsSinEditor`: its own Python 3.12, ffmpeg and Node (made with micromamba, pinned and checksum-verified), the Python packages, the speech models and a small headless browser for rendering. No administrator password, nothing is installed system-wide.
- Activates your licence key with the product's licence server (it receives the key and an identifier of this computer) and downloads the rest of the product.
- To remove it: delete the two folders `~/.claude/skills/reels-sin-editor` and `~/ReelsSinEditor`.

---

## Instalar (sin Terminal)

**1. Abre Claude Code** (la pestaña Code de la app de Claude).

**2. Pega este mensaje y pulsa Enter:**

```
Install this skill for me: https://github.com/mikeopray/RSE-repo (put it in ~/.claude/skills/reels-sin-editor)
```

**3. Escribe esto, pulsa Enter y da tu clave de licencia cuando la pida:**

```
/reels-sin-editor
```

**4. Espera a que diga READY.** La primera vez tarda de 10 a 30 minutos (descarga unos 6 GB). Si Claude pide permiso, permítelo.

**5. Haz tu primer reel.** Abre un chat nuevo, escribe `/reel-signature-warm` y añade tu video.

Todo queda dentro de tu carpeta de usuario. Para quitarlo, borra las dos carpetas `~/.claude/skills/reels-sin-editor` y `~/ReelsSinEditor`.

---
(c) 2026 melimoyano.com. All rights reserved. Licensed, not sold. See LICENSE. Third-party credits: NOTICES.md.
