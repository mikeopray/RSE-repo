#!/usr/bin/env python3
"""install_parakeet - the extras for the Parakeet speech workflow (1.1.0+). Run by install.sh / install.cmd (step 4) with the PRODUCT'S python, and safe to run again by hand:
    $RSE_HOME/venv/bin/python setup/install_parakeet.py
It (1) installs the extra packages into THAT python only, keeping the numpy / onnxruntime versions already there, (2) downloads the Parakeet speech model (about 2.6 GB, once) and
(3) downloads the audio-classifier model listed in setup/models.json (327 MB, checksum verified) into $RSE_HOME/models. Nothing large is shipped inside the release package.
Exit code 0 = Parakeet workflow ready. Non-zero = something could not be installed; the installers treat that as NON-FATAL because the app then uses the Whisper speech stage instead (it still edits videos)."""
import hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent; HERE = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path(os.environ.get("RSE_HOME") or pathlib.Path.home() / "ReelsSinEditor")
def run(c): print("$", " ".join(map(str, c)), flush=True); return subprocess.run([str(x) for x in c]).returncode
PK_REPO = "istupakov/parakeet-tdt-0.6b-v3-onnx"; PK_REV = "8f23f0c03c8761650bdb5b40aaf3e40d2c15f1ce"          # the revision the workflow was validated on (pinned, so a new upload cannot change it)
PK_FILES = ["config.json", "vocab.txt", "decoder_joint-model.onnx", "encoder-model.onnx", "encoder-model.onnx.data"]; PK_DIR = HOME / "models" / "parakeet-tdt-0.6b-v3"
def materialize_parakeet():
    """The model as REAL files in ONE folder ($RSE_HOME/models/parakeet-tdt-0.6b-v3). The Hugging Face cache links files through chains of symlinks on some computers (found 2026-10-19), and onnxruntime then refuses to load the model ("External data path escapes model directory"). Hard links are used when possible (no extra disk space), else a copy."""
    from huggingface_hub import snapshot_download
    snap = pathlib.Path(snapshot_download(PK_REPO, revision=PK_REV, allow_patterns=PK_FILES)); PK_DIR.mkdir(parents=True, exist_ok=True)
    for n in PK_FILES:
        src = (snap / n).resolve(); dst = PK_DIR / n
        if dst.exists() and dst.stat().st_size == src.stat().st_size: continue
        tmp = dst.with_name(dst.name + ".part"); tmp.unlink(missing_ok=True)
        try: os.link(src, tmp)
        except OSError: shutil.copy2(src, tmp)
        os.replace(tmp, dst)
    return PK_DIR
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def fetch(spec):
    """download spec['file'] into $RSE_HOME/models (resumes a partial file), verify size and sha256; returns the path or None"""
    dest = HOME / "models" / spec["file"]; dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and sha256(dest) == spec["sha256"]: return dest
    part = dest.with_suffix(dest.suffix + ".part")
    for url in spec["urls"]:
        try:
            have = part.stat().st_size if part.exists() else 0; req = urllib.request.Request(url, headers=dict({"User-Agent": "ReelsSinEditor-installer/1.3"}, **({"Range": f"bytes={have}-"} if have else {})))          # Cloudflare answers 403 to the default Python user agent
            with urllib.request.urlopen(req, timeout=120) as r:
                mode = "ab" if (have and getattr(r, "status", 200) == 206) else "wb"
                with open(part, mode) as f: shutil.copyfileobj(r, f)
            if sha256(part) == spec["sha256"]: part.replace(dest); return dest
            print(f"The file from {url} did not match its checksum; discarded.", flush=True); part.unlink(missing_ok=True)
        except Exception as e: print(f"Could not download from {url}: {type(e).__name__}", flush=True)
    return None
def main():
    import importlib.metadata as md
    keep = []
    for pkg in ("numpy", "onnxruntime", "av", "opencv-python-headless", "opencv-python", "faster-whisper", "ctranslate2"):
        try: keep.append(f"{pkg}=={md.version(pkg)}")
        except Exception: pass
    cf = pathlib.Path(tempfile.mkdtemp()) / "keep.txt"; cf.write_text("\n".join(keep) + "\n")
    if run([sys.executable, "-m", "pip", "install", "-q", "-c", cf, "-r", HERE / "requirements-parakeet.txt"]): sys.exit("PARAKEET_PARTIAL: could not install the extra packages")
    print("Downloading / checking the Parakeet speech model (first time: about 2.6 GB)...", flush=True)
    try: pk = materialize_parakeet()
    except Exception as e: sys.exit(f"PARAKEET_PARTIAL: could not download the Parakeet speech model ({type(e).__name__}); check the internet connection")
    if run([sys.executable, "-c", "import onnx_asr, os, sys; onnx_asr.load_model('nemo-parakeet-tdt-0.6b-v3', path=sys.argv[1]); print('Parakeet model ready', flush=True); os._exit(0)", pk]): sys.exit("PARAKEET_PARTIAL: the Parakeet speech model downloaded but did not load on this computer")
    models = json.loads((HERE / "models.json").read_text(encoding="utf-8"))
    pn = os.environ.get("RSE_PANNS_ONNX")
    if not (pn and pathlib.Path(pn).exists()):
        print("Downloading the audio-classifier model (327 MB, once)...", flush=True)
        pn = fetch(models["panns_speech"])
        if not pn: sys.exit("PARAKEET_PARTIAL: the audio-classifier model could not be downloaded. The app will use the Whisper speech stage until you run setup again.")
    if run([sys.executable, "-c", "import onnx_asr, silero_vad, scipy, soundfile, onnxruntime, os; print('imports OK', flush=True); os._exit(0)"]): sys.exit("PARAKEET_PARTIAL: an installed package does not import")
    print("PARAKEET_READY. Audio-classifier model:", pn)
if __name__ == "__main__": main()
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
