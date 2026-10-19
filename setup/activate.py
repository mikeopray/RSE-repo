#!/usr/bin/env python3
"""Activate this computer with a licence key, and manage the activation.
  ~/ReelsSinEditor/venv/bin/python setup/activate.py --key RSE-XXXXX-XXXXX-XXXXX-XXXXX [--replace]   activate (then installs the product if it is not installed yet)
  ~/ReelsSinEditor/venv/bin/python setup/activate.py status | refresh | deactivate"""
import os, pathlib, sys
_V = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")) / "venv" / ("python.exe" if os.name == "nt" else "bin/python")      # the product's own Python 3.12
if _V.exists() and os.path.normcase(os.path.abspath(sys.executable)) != os.path.normcase(str(_V)) and not os.environ.get("RSE_NO_REEXEC"):
    if os.name == "nt": sys.exit(__import__("subprocess").call([str(_V), "-X", "utf8"] + sys.argv))          # Windows has no exec: run the product's Python and pass its exit code on
    os.execv(str(_V), [str(_V)] + sys.argv)
elif os.name == "nt" and not sys.flags.utf8_mode and not os.environ.get("RSE_NO_REEXEC"): sys.exit(__import__("subprocess").call([sys.executable, "-X", "utf8"] + sys.argv))          # Windows: read/write files as UTF-8
import argparse, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / "licensing")); import license as L
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", nargs="?", default="activate"); ap.add_argument("--key"); ap.add_argument("--replace", action="store_true"); a = ap.parse_args()
    if a.cmd == "status": s = L.status(); print(("LICENSE_OK " if s["state"] in ("ok", "grace") else "LICENSE_PROBLEM: ") + s["message"]); return 0 if s["state"] in ("ok", "grace") else 1
    if a.cmd == "refresh": print("RENEWED" if L.refresh(force=True) else "NOT_RENEWED (offline, or the licence is no longer active)"); return 0
    if a.cmd == "deactivate":
        try: r = L.deactivate(); print("DEACTIVATED: this computer no longer uses the licence. You can activate another computer now.")
        except L.LicenseError as e: print("DEACTIVATE_FAILED: " + str(e)); return 1
        return 0
    key = a.key or L.stored_key()
    if not key: print("ACTIVATION_FAILED: I need the licence key from your purchase email (it looks like RSE-XXXXX-XXXXX-XXXXX-XXXXX)."); return 1
    try: p = L.activate(key, a.replace)
    except L.DeviceLimit as e:
        print("DEVICE_LIMIT: " + str(e)); [print(f"  - {d['name']}") for d in e.devices]; print("To move the licence to this computer, say so and I will run the activation again with the move option (--replace) using the product's own Python."); return 1
    except L.LicenseError as e: print("ACTIVATION_FAILED: " + str(e)); return 1
    print("ACTIVATED: this computer is activated" + (" (updates included until " + __import__("time").strftime("%Y-%m-%d", __import__("time").gmtime(p["uu"])) + ")" if p.get("uu") else "") + ".")
    if not (ROOT / "engine" / "run_edit.py").exists():
        print("Downloading the product (a few MB)..."); return subprocess.run([sys.executable, str(ROOT / "setup" / "update.py"), "--install", "--skip-doctor"]).returncode
    return 0
if __name__ == "__main__": sys.exit(main())
# (c) 2026 melimoyano.com. All rights reserved. Reels Sin Editor is licensed, not sold: copying, reproducing, sharing, recreating, imitating, reselling or making derivative works of this material, in whole or in part, or using it to train AI, is prohibited. See the LICENSE file.
