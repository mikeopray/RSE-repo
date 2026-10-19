#!/usr/bin/env python3
"""Reels Sin Editor updater / first installer of the core package.
Everything is checked against OUR server with the activation pass: the answer is signed (Ed25519), the package is downloaded only for an activated computer, verified (sha256 + MAC), decrypted
with the release key from the signed manifest, and swapped in with an automatic backup and rollback. Your styles, projects and licence (in ~/ReelsSinEditor) are never touched.
Usage: python3 setup/update.py [--check] [--if-due] [--install] [--skip-doctor]"""
import os, pathlib, sys
_V = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")) / "venv" / ("python.exe" if os.name == "nt" else "bin/python")      # the product's own Python 3.12
if _V.exists() and os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(str(_V)) and not os.environ.get("RSE_NO_REEXEC"):
    if os.name == "nt": sys.exit(__import__("subprocess").call([str(_V), "-X", "utf8"] + sys.argv))          # Windows has no exec: run the product's Python and pass its exit code on
    os.execv(str(_V), [str(_V)] + sys.argv)
elif os.name == "nt" and not sys.flags.utf8_mode and not os.environ.get("RSE_NO_REEXEC"): sys.exit(__import__("subprocess").call([sys.executable, "-X", "utf8"] + sys.argv))          # Windows: read/write files as UTF-8
import argparse, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, tempfile, time, zipfile
ROOT = pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / "licensing"))
import license as L, corecrypt
HOME = L.HOME
def vt(v): return tuple(int(x) for x in v.split("-")[0].split(".")) + (0 if "-" in v else 1,)
def state():
    p = HOME / "state.json"; return json.loads(p.read_text()) if p.exists() else {"schema_version": 0}
def save_state(s): HOME.mkdir(parents=True, exist_ok=True); (HOME / "state.json").write_text(json.dumps(s, indent=1))
def run_migrations(root):
    s = state(); done = s.get("schema_version", 0)
    for f in sorted((root / "migrations").glob("[0-9][0-9][0-9][0-9]_*.py")) if (root / "migrations").exists() else []:
        n = int(f.name[:4])
        if n <= done: continue
        spec = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.migrate(HOME); s["schema_version"] = n; save_state(s); print(f"migrated {f.name}")
def get_manifest():
    tok, p = L.load_pass()
    if not tok or not p: raise L.LicenseError("This copy is not activated yet. Run the activation step first.")
    L.refresh(); tok, p = L.load_pass()
    pk = L.platform_key() if hasattr(L, "platform_key") else ""; r = L.api("/v1/latest" + ("?platform=" + pk if pk else ""), token=tok)
    if not r.get("ok"): raise L.LicenseError(r.get("message", "Could not check for updates."))
    man = L.verify_token(r["manifest"])
    if not man: raise L.LicenseError("The update information was not signed by the product's server, so I ignored it.")
    return man, tok, p
def swap(newroot, cur):
    bak = HOME / "backups" / f"reels-sin-editor-{cur}-{int(time.time())}"; bak.parent.mkdir(parents=True, exist_ok=True); shutil.copytree(ROOT, bak, symlinks=True)
    def wipe_nt(p):          # Windows: a compiled module this process has loaded cannot be deleted but CAN be renamed: move it aside (it is removed by the next update)
        if p.is_dir() and not p.is_symlink():
            for c in list(p.iterdir()): wipe_nt(c)
            try: p.rmdir()
            except OSError: pass
        else:
            try: p.unlink()
            except OSError: p.rename(p.with_name(p.name + f".old{int(time.time())}"))
    def wipe():
        for item in list(ROOT.iterdir()):
            if os.name == "nt": wipe_nt(item)
            else: shutil.rmtree(item) if item.is_dir() and not item.is_symlink() else item.unlink()
    def put(src):
        for item in src.iterdir(): (shutil.copytree if item.is_dir() else shutil.copy2)(item, ROOT / item.name, **({"symlinks": True, "dirs_exist_ok": os.name == "nt"} if item.is_dir() else {}))
    return bak, wipe, put
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); ap.add_argument("--if-due", action="store_true"); ap.add_argument("--install", action="store_true"); ap.add_argument("--skip-doctor", action="store_true"); a = ap.parse_args()
    cur = (ROOT / "VERSION").read_text().strip(); installed = (ROOT / "engine" / "run_edit.py").exists()
    if (HERE_CHANNEL := ROOT / "setup" / "CHANNEL").exists():          # a preview build is never replaced by the normal (Mac) release
        print("UPDATE_NOT_INCLUDED: this is a preview build (" + HERE_CHANNEL.read_text().strip() + "); updates are handled by the developer."); return 0
    if a.if_due:
        s = state()
        if time.time() - s.get("last_check", 0) < 86400: return 0
        s["last_check"] = time.time(); save_state(s)
    try: man, tok, p = get_manifest()
    except L.OfflineError as e:
        if not a.if_due: print(f"UPDATE_CHECK_FAILED: no connection to the server ({e}); nothing was changed.")
        return 0
    except L.LicenseError as e:
        if not a.if_due: print(f"UPDATE_CHECK_FAILED: {e}")
        return 1 if not a.if_due else 0
    new = man["version"]
    force = cur in man.get("withdrawn", [])                                  # the installed version was withdrawn by us: move to the current good one even if it is older
    if installed and vt(new) <= vt(cur) and not a.install and not force:
        if not a.if_due: print(f"UP_TO_DATE (version {cur})")
        return 0
    if not man.get("entitled"):
        if not a.if_due: print(f"UPDATE_NOT_INCLUDED: version {new} was released after your updates period ended. You can keep using version {cur}.")
        return 0
    if not installed: print(f"Installing the product (version {new})...")
    else: print(f"Update available: {cur} -> {new}. {man.get('notes', '')}")
    if a.check: print("UPDATE_AVAILABLE"); return 0
    blob = L.api(man["core"]["path"], token=tok, raw=True, timeout=120)
    if isinstance(blob, dict) or hashlib.sha256(blob).hexdigest() != man["core"]["sha256"]: print("UPDATE_FAILED: the download was damaged or unsigned, nothing changed."); return 1
    try: zbytes = corecrypt.decrypt(blob, __import__("base64").b64decode(man["content_key"]))
    except Exception as e: print(f"UPDATE_FAILED: could not open the package ({e}); nothing changed."); return 1
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="rse-up-")); (tmp / "pkg.zip").write_bytes(zbytes)
    with zipfile.ZipFile(tmp / "pkg.zip") as zf:
        zf.extractall(tmp / "new")
        for zi in zf.infolist():                                  # extractall drops the executable flag: restore it (the matte tool and the .sh scripts must stay runnable)
            if (zi.external_attr >> 16) & 0o111 and not zi.is_dir(): (tmp / "new" / zi.filename).chmod(0o755)
    cands = [q for q in (tmp / "new").iterdir() if q.is_dir()]; newroot = cands[0] if len(cands) == 1 and not (tmp / "new" / "SKILL.md").exists() else tmp / "new"
    if not (newroot / "SKILL.md").exists(): print("UPDATE_FAILED: the package has no SKILL.md; nothing changed."); return 1
    bak, wipe, put = swap(newroot, cur)
    try:
        wipe(); put(newroot); (ROOT / "VERSION").write_text(new + "\n"); run_migrations(ROOT)
        try: import watermark; watermark.apply(ROOT, p["wm"])
        except Exception as e: print("note: could not mark this copy:", e)
        subprocess.run([sys.executable, str(ROOT / "setup" / "sync_commands.py")], check=False)
        if not a.skip_doctor and (ROOT / "setup" / "doctor.py").exists() and installed:
            if subprocess.run([sys.executable, str(ROOT / "setup" / "doctor.py")]).returncode: raise RuntimeError("health check failed after update")
    except Exception as e:
        print(f"UPDATE_FAILED: {e}; restoring version {cur}"); wipe(); put(bak); return 1
    print(f"{'INSTALLED' if not installed else 'UPDATED'} version {new}. Your styles, projects and licence were not touched." + ("" if not installed else f" Previous version kept in {bak}"))
    return 0
if __name__ == "__main__": sys.exit(main())
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
