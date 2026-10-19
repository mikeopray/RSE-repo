#!/usr/bin/env python3
"""Steps 2-6 of the installer (the same on every OS). Run by install.cmd / install.sh with the product's own Python after the private environment exists.
Python packages, animation library, speech model (about 3 GB), person-matte model and NVIDIA GPU libraries where they apply, the renderer's headless browser, slash commands, final health check."""
import hashlib, os, pathlib, shutil, subprocess, sys, urllib.request
HERE = pathlib.Path(__file__).resolve().parent; HOME = pathlib.Path(os.environ.get("RSE_HOME") or pathlib.Path.home() / "ReelsSinEditor"); VENV = HOME / "venv"; IS_WIN = os.name == "nt"
MODNET_URL = "https://huggingface.co/Xenova/modnet/resolve/main/onnx/model.onnx"; MODNET_SHA = "07c308cf0fc7e6e8b2065a12ed7fc07e1de8febb7dc7839d7b7f15dd66584df9"
def step(n, t): print(f"[{n}/6] {t}", flush=True)
def fail(m): print("INSTALL_FAILED: " + m, flush=True); sys.exit(1)
def env_dirs(): return [VENV, VENV / "Scripts", VENV / "Library" / "bin", VENV / "Library" / "usr" / "bin", VENV / "Library" / "mingw-w64" / "bin"] if IS_WIN else [VENV / "bin"]
os.environ["PATH"] = os.pathsep.join([str(d) for d in env_dirs() if d.is_dir()] + [os.environ.get("PATH", "")])
os.environ.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", HF_HUB_DISABLE_SYMLINKS_WARNING="1")
def run(cmd, **kw): return subprocess.run([str(c) for c in cmd], **kw).returncode
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def download(url, dest, sha, what):
    dest = pathlib.Path(dest); dest.parent.mkdir(parents=True, exist_ok=True); part = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(part, "wb") as f: shutil.copyfileobj(r, f)
    except Exception: fail(f"could not download {what}. Check the internet connection and run setup again.")
    if sha256(part) != sha: part.unlink(missing_ok=True); fail(f"the downloaded {what} did not match its checksum, so it was discarded for safety.")
    part.replace(dest)
def nvidia_present():
    return bool(shutil.which("nvidia-smi")) or (IS_WIN and pathlib.Path(r"C:\Windows\System32\nvidia-smi.exe").exists())
def main():
    py = sys.executable
    step(2, "Installing the Python packages...")
    if run([py, "-m", "pip", "install", "-q", "--upgrade", "pip"]): fail("pip could not update. Check the internet connection and run setup again.")
    if run([py, "-m", "pip", "install", "-q", "-r", HERE / "requirements.txt"]): fail("could not install the Python packages. Check the internet connection and run setup again.")
    if not IS_WIN:
        eng = HERE.parent / "engine" / "segbatch-arm64"
        if eng.exists(): eng.chmod(eng.stat().st_mode | 0o755)
    step(3, "Installing the animation library...")
    npm = shutil.which("npm") or "npm"
    if run([npm, "install", "--prefix", HOME, "gsap@3.15.0", "capcut-cli@0.28.0", "--no-audit", "--no-fund", "--silent"]): fail("could not install the animation library and the CapCut helper. Check the internet connection and run setup again.")
    step(4, "Downloading the speech models (about 6 GB in total, one time - this is the long step)" + (" and the person-matte model..." if IS_WIN else "..."))
    if IS_WIN:
        modnet = HOME / "models" / "modnet.onnx"
        if not (modnet.exists() and sha256(modnet) == MODNET_SHA): download(MODNET_URL, modnet, MODNET_SHA, "person-matte model")
        if nvidia_present():          # optional: the CUDA libraries let speech recognition use the NVIDIA card (much faster); if this fails the processor is used
            print("NVIDIA graphics card found: adding the GPU speech libraries (optional, about 1.3 GB)...", flush=True)
            if run([py, "-m", "pip", "install", "-q", "nvidia-cublas-cu12", "nvidia-cudnn-cu12==9.*"], stdout=subprocess.DEVNULL): print("(GPU libraries could not be added; speech recognition will use the processor.)", flush=True)
    if run([py, "-c", "from huggingface_hub import snapshot_download; snapshot_download('Systran/faster-whisper-large-v3')"]): fail("could not download the speech model. Check the internet connection and run setup again.")
    print("Also downloading the Parakeet speech model (about 2.6 GB) and the audio-classifier model (327 MB)...", flush=True)
    if run([py, HERE / "install_parakeet.py"]): print("(The Parakeet extras could not be installed. The app still works: it uses the Whisper speech stage. Run setup again later to retry.)", flush=True)
    step(5, "Preparing the video renderer (downloads a small headless browser)...")
    npx = shutil.which("npx") or "npx"
    if run([npx, "--yes", "hyperframes@0.8.140", "browser", "ensure"], cwd=HERE): fail("could not download the headless browser the video renderer needs. Check the internet connection and run setup again.")
    step(6, "Final check...")
    full = HERE.parent / "SKILL_FULL.md"
    if full.exists():          # the preview package: the full instructions replace the short installer note now that everything is installed
        shutil.copy2(full, HERE.parent / "SKILL.md"); full.unlink()
    run([py, HERE / "sync_commands.py"]); run([py, HERE / "doctor.py"])
if __name__ == "__main__": main()
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
