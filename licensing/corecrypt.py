"""crypt - decrypt / encrypt the core package (AES-256-CTR + HMAC-SHA256, encrypt-then-MAC) using the system openssl, so no Python crypto package is needed.
File layout: b'RSEC1' + iv(16) + ciphertext + hmac(32). Keys derive from the release content key: enc = sha256(ck+b'enc'), mac = sha256(ck+b'mac')."""
import hashlib, hmac, os, pathlib, shutil, subprocess
MAGIC = b"RSEC1"
def _openssl():
    """the openssl program: one on the PATH, else the one inside the product's private environment (Windows has none of its own, and activation runs in a shell whose PATH does not include the environment's folders)"""
    w = os.environ.get("RSE_OPENSSL") or shutil.which("openssl")
    if w: return w
    venv = pathlib.Path(os.environ.get("RSE_HOME", pathlib.Path.home() / "ReelsSinEditor")) / "venv"
    for p in (venv / "Library" / "bin" / "openssl.exe", venv / "Library" / "usr" / "bin" / "openssl.exe", venv / "Scripts" / "openssl.exe", venv / "bin" / "openssl"):
        if p.is_file(): return str(p)
    raise RuntimeError("openssl was not found. Run the setup step that prepares the private environment again (install.cmd / install.sh --env-only).")
def _keys(ck: bytes): return hashlib.sha256(ck + b"enc").digest(), hashlib.sha256(ck + b"mac").digest()
def _ctr(data: bytes, key: bytes, iv: bytes, decrypt=False) -> bytes:
    cmd = [_openssl(), "enc", "-aes-256-ctr", "-K", key.hex(), "-iv", iv.hex()] + (["-d"] if decrypt else [])
    r = subprocess.run(cmd, input=data, capture_output=True)
    if r.returncode: raise RuntimeError("openssl failed: " + r.stderr.decode(errors="ignore")[:200])
    return r.stdout
def encrypt(plain: bytes, ck: bytes) -> bytes:
    ek, mk = _keys(ck); iv = os.urandom(16); ct = _ctr(plain, ek, iv); body = MAGIC + iv + ct
    return body + hmac.new(mk, body, hashlib.sha256).digest()
def decrypt(blob: bytes, ck: bytes) -> bytes:
    ek, mk = _keys(ck)
    if blob[:5] != MAGIC or len(blob) < 53: raise ValueError("not a Reels Sin Editor package")
    body, tag = blob[:-32], blob[-32:]
    if not hmac.compare_digest(hmac.new(mk, body, hashlib.sha256).digest(), tag): raise ValueError("the package is damaged or the key is wrong")
    return _ctr(body[21:], ek, body[5:21], decrypt=True)
