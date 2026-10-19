# Reels Sin Editor

Edit a raw talking-head video into a finished vertical reel, with captions, motion graphics and sound, inside Claude Code. Licensed product: you need a licence key (from your purchase email).
Mac with Apple chip (M1 or newer) for now. Windows is coming.

## Install (no Terminal needed)

**1. Open Claude Code** (the Code tab in the Claude desktop app) and **paste this message**:

```
Install this skill for me: https://github.com/mikeopray/RSE-repo (put it in ~/.claude/skills/reels-sin-editor)
```

**2. Type `/reels-sin-editor` followed by your licence key** (from your purchase email) and press Enter:

```
/reels-sin-editor RSE-XXXXX-XXXXX-XXXXX-XXXXX
```

**3. Wait for READY.** The first time takes about 10 to 30 minutes (it downloads about 6 GB). Claude tells you how it is going. If Claude says a step was stopped, it shows you one line to paste: do that and wait.

**4. Make your first reel.** Close this chat and **open a NEW chat** (important: the new commands only work in a new chat). Type `/reel-signature-warm`, then add your video.

## What the installation does (everything stays in your user folder)

- Puts this skill in `~/.claude/skills/reels-sin-editor` (step 2).
- Creates a private workspace in `~/ReelsSinEditor`: its own Python 3.12, ffmpeg and Node (made with micromamba, pinned and checksum-verified), the Python packages, the speech models and a small headless browser for rendering. No administrator password, nothing is installed system-wide.
- Activates your licence key with the product's licence server (it receives the key and an identifier of this computer) and downloads the rest of the product.
- To remove it: delete the two folders `~/.claude/skills/reels-sin-editor` and `~/ReelsSinEditor`.

---

## Instalar (sin Terminal)

**1. Abre Claude Code** (la pestaña Code de la app de Claude) y **pega este mensaje**:

```
Install this skill for me: https://github.com/mikeopray/RSE-repo (put it in ~/.claude/skills/reels-sin-editor)
```

**2. Escribe `/reels-sin-editor` seguido de tu clave de licencia** (de tu email de compra) y pulsa Enter:

```
/reels-sin-editor RSE-XXXXX-XXXXX-XXXXX-XXXXX
```

**3. Espera a que diga READY.** La primera vez tarda de 10 a 30 minutos (descarga unos 6 GB). Claude te cuenta cómo va. Si Claude dice que un paso fue detenido, te muestra una línea para pegar: hazlo y espera.

**4. Haz tu primer reel.** Cierra este chat y **abre un chat NUEVO** (importante: los comandos nuevos solo funcionan en un chat nuevo). Escribe `/reel-signature-warm` y añade tu video.

Todo queda dentro de tu carpeta de usuario. Para quitarlo, borra las dos carpetas `~/.claude/skills/reels-sin-editor` y `~/ReelsSinEditor`.

---
(c) 2026 melimoyano.com. All rights reserved. Licensed, not sold. See LICENSE. Third-party credits: NOTICES.md.
