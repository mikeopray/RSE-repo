#!/usr/bin/env python3
"""Reels Sin Editor health check. Prints PASS/FAIL per item with a fix hint; final line READY or NOT READY."""
import os, pathlib, sys
_V = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")) / "venv" / ("python.exe" if os.name == "nt" else "bin/python")      # the product's own Python 3.12
if _V.exists() and os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(str(_V)) and not os.environ.get("RSE_NO_REEXEC"):
    if os.name == "nt": sys.exit(__import__("subprocess").call([str(_V), "-X", "utf8"] + sys.argv))          # Windows has no exec: run the product's Python and pass its exit code on
    os.execv(str(_V), [str(_V)] + sys.argv)
elif os.name == "nt" and not sys.flags.utf8_mode and not os.environ.get("RSE_NO_REEXEC"): sys.exit(__import__("subprocess").call([sys.executable, "-X", "utf8"] + sys.argv))          # Windows: read/write files as UTF-8
import os, platform, shutil, subprocess, sys, pathlib
_VD = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")) / "venv"; WIN = os.name == "nt"
INST = "cmd /c setup\\install.cmd" if WIN else "sh setup/install.sh"
os.environ["PATH"] = os.pathsep.join([str(d) for d in ([_VD, _VD / "Scripts", _VD / "Library" / "bin", _VD / "Library" / "usr" / "bin"] if WIN else [_VD / "bin"]) if d.is_dir()] + [os.environ.get("PATH", "")])          # the product's own ffmpeg / node live here
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
HOME = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor"))
res = []; rows = []
if not (ROOT / "engine" / "run_edit.py").exists():
    print("NOT INSTALLED: this folder is the starter package. Activate it with your licence key to download the product:\n  python3 setup/activate.py --key RSE-XXXXX-XXXXX-XXXXX-XXXXX\n\nNOT READY"); sys.exit(1)
def chk(name, ok, hint=""):
    res.append(ok); rows.append((name, ok, hint)); print(("PASS  " if ok else "FAIL  ") + name + ("" if ok else f"  -> {hint}"))
def out(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout
    except Exception: return ""
chk("Windows 10 (1809) or newer, 64-bit" if WIN else "Mac (Apple chip or Intel)", (platform.system() == "Windows" and platform.machine().lower() in ("amd64", "x86_64") and int(platform.version().split(".")[2] if platform.version().count(".") >= 2 else 0) >= 17763) if WIN else (platform.system() == "Darwin" and platform.machine() in ("arm64", "x86_64")), "Windows 10 version 1809 or newer, 64-bit, is needed" if WIN else "this computer type is not supported")
chk("Python 3.12 (the product's own environment)", sys.version_info[:2] == (3, 12) or (HOME / "venv" / ("python.exe" if WIN else "bin/python")).exists(), "run: " + INST + "")
ff = shutil.which("ffmpeg"); chk("ffmpeg + libx264", bool(ff) and "libx264" in out(["ffmpeg", "-encoders"]), "run: " + INST + "")
chk("ffprobe", bool(shutil.which("ffprobe")), "run: " + INST + "")
nd = shutil.which("node"); v = out(["node", "-v"]).strip().lstrip("v").split(".")[0] if nd else "0"
chk("Node 18+", v.isdigit() and int(v) >= 18, "run: " + INST + "")
try:
    sys.path.insert(0, str(ROOT / "engine")); import hw as _hw; _hs = _hw.summary(); _ram = _hw.probe()["ram_gb"]
except Exception: _hs, _ram = None, None
if _hs: chk("this computer: " + _hs, True)
chk(f"memory (the speech model needs about 4 GB free; {_ram} GB found)", _ram is None or _ram >= 6, "this computer has too little memory for the speech model (6 GB or more is recommended)")
free = shutil.disk_usage(str(pathlib.Path.home())).free / 1e9
chk(f"free disk >= 10 GB ({free:.0f} GB)", free >= 10, "free space: the speech model is about 3 GB and each reel needs working room")
venv = HOME / "venv" / ("python.exe" if WIN else "bin/python")
chk("Reels Sin Editor Python environment", venv.exists(), "run: " + INST + "")
if venv.exists():
    r = subprocess.run([str(venv), "-c", "import faster_whisper, cv2, numpy, av, onnxruntime"], capture_output=True)
    chk("Python packages", r.returncode == 0, "run: " + INST + "")
hub = pathlib.Path(os.environ.get("HF_HOME") or pathlib.Path.home() / ".cache/huggingface") / "hub"
chk("speech model (large-v3)", any(hub.glob("models--Systran--faster-whisper-large-v3")), "run: " + INST + " (about 3 GB download)")
chk("font pack", (ROOT / "fonts" / "pack" / "PACK.json").exists(), "re-download the package")
chk("sound pack", (ROOT / "sounds" / "PACK.json").exists(), "re-download the package (sound effects will be skipped)")
try:
    sys.path.insert(0, str(ROOT / "engine")); import rse_platform as _RP; _RP.find_chrome(); _chrome_ok = True
except BaseException: _chrome_ok = False
chk("renderer browser (headless Chrome)", _chrome_ok, "run: " + INST + " (it downloads the browser the renderer needs)")
chk("CapCut export helper (capcut-cli)", (HOME / "node_modules" / "capcut-cli" / "dist" / "index.js").exists(), "run: " + INST + "")
chk("animation library (gsap)", (HOME / "node_modules" / "gsap" / "dist" / "gsap.min.js").exists(), "run: " + INST + "")
if WIN:
    r_m = subprocess.run([str(venv), "-X", "utf8", str(ROOT / "engine" / "matte_onnx.py"), "--selftest"], capture_output=True, text=True, env=dict(os.environ, RSE_HOME=str(HOME)))
    chk("person-matte model works on this PC", r_m.returncode == 0 and "matte ok" in r_m.stdout, "run: " + INST)
else:
    sb = ROOT / "engine" / "segbatch-arm64"
    if sb.exists() and not os.access(sb, os.X_OK):
        try: sb.chmod(sb.stat().st_mode | 0o755)          # self-heal: an older updater extracted files without the executable flag
        except Exception: pass
    r_sb = subprocess.run([str(sb), "--selftest"], capture_output=True, text=True) if sb.exists() and os.access(sb, os.X_OK) else None
    chk("person-matte tool starts on this Mac", bool(r_sb) and r_sb.returncode == 0 and "ok" in r_sb.stdout, "this Mac's macOS may be too old (macOS 12 or newer is needed): update macOS, or run: chmod +x engine/segbatch-arm64")
    chk("macOS 12 or newer", tuple(int(x) for x in (platform.mac_ver()[0] or "0").split(".")[:1] or [0])[0] >= 12, "update macOS (System Settings > General > Software Update)")
chk("bundled fonts", all((ROOT / "fonts" / f).exists() for f in ("Inter.ttf", "PlayfairDisplay-Italic.ttf", "IndieFlower.ttf")), "re-download the Reels Sin Editor package")
r_c = subprocess.run([str(venv), "-X", "utf8", str(ROOT / "engine" / "carousel_render.py"), "styles"], capture_output=True, text=True, env=dict(os.environ, RSE_HOME=str(HOME)))
chk("carousels: styles, fonts and layouts load", r_c.returncode == 0 and "carousel-ready" in r_c.stdout, (r_c.stdout + r_c.stderr).strip().splitlines()[-1][:160] if (r_c.stdout + r_c.stderr).strip() else "run: " + INST)
chk("slash commands installed", all((pathlib.Path(os.environ.get("RSE_SKILLS_DIR", pathlib.Path.home() / ".claude" / "skills")) / n).exists() for n in ("estilo-nuevo", "estilo-copiar", "estilo-manual")), "run: python3 setup/sync_commands.py")
lic = ROOT / "licensing" / "license_check.py"
if lic.exists():
    o = out([sys.executable, str(lic)]).strip(); chk("license", o.startswith("LICENSE_OK"), o or "add your key to ~/ReelsSinEditor/license.txt")
def report():
    """secret-free diagnostic a customer can paste to support (license key shown as last 4 characters only)"""
    import json, datetime
    L = [f"Reels Sin Editor diagnostic  {datetime.datetime.now():%Y-%m-%d %H:%M}", f"version: {(ROOT / 'VERSION').read_text().strip() if (ROOT / 'VERSION').exists() else '?'}",
         f"macOS {platform.mac_ver()[0]} {platform.machine()}  python {sys.version.split()[0]}", f"ffmpeg: {out(['ffmpeg', '-version']).splitlines()[0] if shutil.which('ffmpeg') else 'missing'}",
         f"node: {out(['node', '-v']).strip() or 'missing'}   free disk: {free:.0f} GB", "", "CHECKS"]
    L += [("  PASS " if ok else "  FAIL ") + n + ("" if ok else f"  -> {h}") for n, ok, h in rows]
    kf = HOME / "license.txt"; L += ["", "LICENSE", f"  key file: {'present, ends ...' + kf.read_text().strip()[-4:] if kf.exists() else 'missing'}"]
    tok = HOME / "license_token.json"; L.append(f"  offline pass: {'present' if tok.exists() else 'none'}")
    sf = HOME / "logs" / "stats.jsonl"
    L += ["", "RECENT STAGES (time and peak memory per stage, newest last)"]
    try:
        for ln in sf.read_text(encoding="utf-8").splitlines()[-20:]:
            j = json.loads(ln); L.append(f"  {datetime.datetime.fromtimestamp(j['at']):%m-%d %H:%M}  {j['stage']:8s} {j['seconds']:7.0f} s  peak {j.get('peak_gb')} GB  exit {j.get('rc')}  (RAM {j.get('ram_gb')} GB, {j.get('cores')} cores, speech on {j.get('device')})")
    except Exception: L.append("  (none yet)")
    L += ["", "STYLES"]
    sys.path.insert(0, str(ROOT / "engine"))
    try:
        import style_validate as V
        for base in (ROOT / "styles", HOME / "styles"):
            for s in sorted(base.glob("*/style.json")) if base.exists() else []:
                e, w = V.check(s.parent); L.append(f"  {s.parent.name}: {'ok' if not e else 'PROBLEM ' + '; '.join(e)}")
    except Exception as ex: L.append(f"  (could not check: {ex})")
    L += ["", "COMMANDS"]; sk = pathlib.Path(os.environ.get("RSE_SKILLS_DIR", pathlib.Path.home() / ".claude" / "skills"))
    L.append("  " + ", ".join(sorted(p.name for p in sk.glob("reel*")) + sorted(p.name for p in sk.glob("estilo-*"))) if sk.exists() else "  skills folder missing")
    logs = sorted((HOME / "projects").glob("*/*/logs/*.log")) if (HOME / "projects").exists() else []
    if logs: L += ["", f"LAST LOG ({logs[-1].parent.parent.name}/{logs[-1].name}, last 25 lines)"] + ["  " + x for x in logs[-1].read_text(errors="ignore").splitlines()[-25:]]
    txt = "\n".join(L); (HOME / "diagnostic.txt").parent.mkdir(parents=True, exist_ok=True); (HOME / "diagnostic.txt").write_text(txt); print("\n" + txt); print(f"\nSaved to {HOME / 'diagnostic.txt'} - paste it to support. It contains no secrets.")
def _parakeet_note():
    """information only (does not change READY): the Parakeet speech stage needs the audio-classifier model and the Parakeet packages; without them the app uses the Whisper stage"""
    have_model = (HOME / "models" / "panns_speech.onnx").exists() or bool(os.environ.get("RSE_PANNS_ONNX"))
    try: import onnx_asr, silero_vad; have_pkg = True
    except Exception: have_pkg = False
    print("NOTE  Parakeet speech stage: " + ("ready" if have_model and have_pkg else "not installed (the Whisper stage is used; run " + INST + " to add it)"))
_parakeet_note()
if "--report" in sys.argv: report()
print("\nREADY" if all(res) else "\nNOT READY")
sys.exit(0 if all(res) else 1)
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
