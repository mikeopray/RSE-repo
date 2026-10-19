"""license - activation, device binding and signed offline passes for Reels Sin Editor.
How it works: the buyer's licence key is exchanged ONCE for a pass signed by our server (Ed25519). The pass names this computer and is valid for 14 days; the product verifies it OFFLINE with the public key it carries.
It refreshes itself silently (at most once a day) when online. If the internet is down the product keeps working for a 7-day grace period. A pass copied to another computer is rejected (device id).
User data lives in ~/ReelsSinEditor/license (never touched by updates). All messages are plain language for a non-technical buyer."""
import base64, hashlib, json, os, pathlib, subprocess, sys, time, urllib.error, urllib.request, uuid
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent; sys.path.insert(0, str(HERE))
import ed25519
try: import _baked as _B                  # release builds: key + server are compiled into the protected code, so editing config.json or env vars changes nothing
except ImportError: _B = None
CFG = {"server": _B.SERVER, "public_key": _B.PUBLIC_KEY, "grace_days": _B.GRACE_DAYS} if _B else json.loads((HERE / "config.json").read_text())
HOME = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")); LIC = HOME / "license"
GRACE_DAYS = int(CFG.get("grace_days", 7)); SERVER = (CFG["server"] if _B else os.environ.get("RSE_SERVER", CFG["server"])).rstrip("/"); PUB = base64.b64decode(CFG["public_key"])
class LicenseError(Exception): pass
def _u(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
def device_id():
    if not _B and os.environ.get("RSE_DEVICE_ID"): return os.environ["RSE_DEVICE_ID"]
    LIC.mkdir(parents=True, exist_ok=True); f = LIC / "device.id"
    if os.name == "nt":                      # Windows: the machine GUID Windows creates at install time
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as k: uid = winreg.QueryValueEx(k, "MachineGuid")[0]
            if uid: return hashlib.sha256(("rse|" + uid).encode()).hexdigest()[:32]
        except Exception: pass
    try:
        out = subprocess.run([next((x for x in ("/usr/sbin/ioreg", "ioreg") if x == "ioreg" or os.path.exists(x))), "-rd1", "-c", "IOPlatformExpertDevice"], capture_output=True, text=True, timeout=5).stdout
        uid = next((l.split('"')[-2] for l in out.splitlines() if "IOPlatformUUID" in l), None)
        if uid: return hashlib.sha256(("rse|" + uid).encode()).hexdigest()[:32]
    except Exception: pass
    if not f.exists(): f.write_text(uuid.uuid4().hex)
    return hashlib.sha256(("rse|" + f.read_text().strip()).encode()).hexdigest()[:32]
def platform_key():
    """which compiled package this computer needs: '' = a Mac with an Apple chip (the default release), 'windows', or 'mac-x86_64' (Intel Mac)"""
    if os.name == "nt": return "windows"
    if sys.platform == "darwin":
        try:
            if subprocess.run(["sysctl", "-n", "hw.optional.arm64"], capture_output=True, text=True, timeout=3).stdout.strip() != "1": return "mac-x86_64"
        except Exception: pass
    return ""
def device_name():
    if os.name == "nt":
        import socket; return (socket.gethostname() or "Windows PC")[:40]
    try: return subprocess.run([next((x for x in ("/usr/sbin/scutil", "scutil") if x == "scutil" or os.path.exists(x))), "--get", "ComputerName"], capture_output=True, text=True, timeout=3).stdout.strip() or "Mac"
    except Exception: return "Mac"
def verify_token(tok):
    """-> payload dict or None; checks the Ed25519 signature offline"""
    try:
        body, sig = tok.split("."); 
        if not ed25519.verify(_u(sig), body.encode(), PUB): return None
        return json.loads(_u(body))
    except Exception: return None
def api(path, data=None, token=None, method=None, timeout=15, raw=False):
    req = urllib.request.Request(SERVER + path, data=None if data is None else json.dumps(data).encode(), method=method or ("POST" if data is not None else "GET"))
    req.add_header("content-type", "application/json"); req.add_header("user-agent", "ReelsSinEditor/" + (ROOT / "VERSION").read_text().strip() if (ROOT / "VERSION").exists() else "ReelsSinEditor/1.0")
    if token: req.add_header("authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r: b = r.read(); return b if raw else json.loads(b)
    except urllib.error.HTTPError as e:
        try: j = json.loads(e.read()); 
        except Exception: j = {"ok": False, "code": "http_%d" % e.code, "message": "The licence server answered with an error."}
        j["_http"] = e.code; return j
    except Exception as e: raise OfflineError(str(e))
class OfflineError(Exception): pass
def _save_pass(tok, key=None):
    LIC.mkdir(parents=True, exist_ok=True); (LIC / "pass.json").write_text(json.dumps({"pass": tok, "saved": int(time.time())})); (os.chmod(LIC / "pass.json", 0o600) if os.name != "nt" else None)
    if key: (LIC / "license.key").write_text(key.strip().upper()); (os.chmod(LIC / "license.key", 0o600) if os.name != "nt" else None)
def stored_key(): f = LIC / "license.key"; return f.read_text().strip() if f.exists() else None
def load_pass():
    f = LIC / "pass.json"
    if not f.exists(): return None, None
    try: tok = json.loads(f.read_text())["pass"]
    except Exception: return None, None
    return tok, verify_token(tok)
def status():
    """-> dict(state ok|grace|expired|missing|invalid|revoked, message, payload, days_left)"""
    tok, p = load_pass(); rev = LIC / "revoked.txt"
    if rev.exists(): return dict(state="revoked", message=rev.read_text().strip() or "This licence is no longer active.", payload=None)
    if not tok: return dict(state="missing", message="This copy is not activated yet. Activate it with the licence key from your purchase email.", payload=None)
    if not p: return dict(state="invalid", message="The activation file is damaged. Activate again with your licence key.", payload=None)
    if p.get("free"): return dict(state="ok", message="Licensing is switched off (free mode).", payload=p, days_left=999)
    if p.get("did") != device_id(): return dict(state="invalid", message="This activation belongs to a different computer. Activate this computer with your licence key.", payload=p)
    t = time.time(); left = (p["exp"] - t) / 86400
    if left > 0: return dict(state="ok", message=f"Activated ({left:.0f} days until the next online check).", payload=p, days_left=left)
    if -left <= GRACE_DAYS: return dict(state="grace", message=f"Please connect to the internet soon: the activation could not be renewed ({GRACE_DAYS + left:.0f} days left before it pauses).", payload=p, days_left=left)
    return dict(state="expired", message="The activation needs an online check. Connect to the internet and run activation again.", payload=p, days_left=left)
def refresh(force=False):
    """renew the pass if it is older than a day (or force). Returns True if renewed. Offline -> False without error; a clear 'no' from the server is remembered."""
    tok, p = load_pass()
    if not tok or not p or p.get("free") and not force: return False
    if not force and time.time() - p["iat"] < 86400: return False
    try: r = api("/v1/refresh", {}, tok, timeout=6)
    except OfflineError: return False
    if r.get("ok"): _save_pass(r["pass"]); (LIC / "revoked.txt").unlink(missing_ok=True); return True
    if r.get("code") in ("revoked", "device_removed", "unknown_key"): LIC.mkdir(parents=True, exist_ok=True); (LIC / "revoked.txt").write_text(r.get("message", "This licence is no longer active."))
    return False
def activate(key, replace=False):
    key = key.strip().upper().replace(" ", "")
    try: r = api("/v1/activate", {"license_key": key, "device_id": device_id(), "device_name": device_name(), "replace": bool(replace)})
    except OfflineError: raise LicenseError("I could not reach the licence server. Check your internet connection and try again.")
    if not r.get("ok"): raise LicenseError(r.get("message", "Activation failed."), ) if r.get("code") != "device_limit" else DeviceLimit(r.get("message"), r.get("devices", []))
    _save_pass(r["pass"], key); (LIC / "revoked.txt").unlink(missing_ok=True); return verify_token(r["pass"])
class DeviceLimit(LicenseError):
    def __init__(self, msg, devices): super().__init__(msg); self.devices = devices
def deactivate():
    key = stored_key()
    if not key: raise LicenseError("This computer has no stored licence key.")
    try: r = api("/v1/deactivate", {"license_key": key, "device_id": device_id()})
    except OfflineError: raise LicenseError("I could not reach the licence server. Connect to the internet and try again.")
    for f in ("pass.json",): (LIC / f).unlink(missing_ok=True)
    return r
def require():
    """call before doing real work: returns the pass payload or raises LicenseError with a plain message"""
    refresh(); s = status()
    if s["state"] in ("ok", "grace"): return s["payload"]
    if s["state"] == "expired":                                           # last chance: try to renew right now
        if refresh(force=True): return status()["payload"]
    raise LicenseError(s["message"])
