"""watermark - after install, mark THIS copy so a leaked copy can be traced to its buyer. The tag comes from the signed pass (wm = HMAC of the licence id, computed by the server), so it cannot be forged for another buyer.
Marks: an HTML comment at the end of every playbook page, an invisible zero-width fingerprint in the first heading of each page, and a comment line at the end of each engine script."""
import pathlib, re
ZW = {"0": "​", "1": "‌"}
def fingerprint(tag): return "".join(ZW[c] for c in bin(int(tag, 16))[2:].zfill(len(tag) * 4))
def apply(root, tag):
    root = pathlib.Path(root); n = 0; fp = fingerprint(tag)
    for p in list(root.glob("brain/**/*.md")) + list(root.glob("flows/*.md")):
        t = p.read_text(encoding="utf-8"); t = re.sub(r"\n<!-- rse:[0-9a-f]+ -->\n?$", "\n", t); t = re.sub(r"[​‌]{16,}", "", t)
        t = re.sub(r"^(#[^\n]*)", lambda m: m.group(1) + fp, t, count=1); p.write_text(t.rstrip() + f"\n<!-- rse:{tag} -->\n", encoding="utf-8"); n += 1
    for p in root.glob("engine/*.py"):
        t = p.read_text(encoding="utf-8"); t = re.sub(r"\n# rse:[0-9a-f]+\n?$", "\n", t); p.write_text(t.rstrip() + f"\n# rse:{tag}\n", encoding="utf-8"); n += 1
    return n
def read_tag(root):
    for p in pathlib.Path(root).glob("brain/BRAIN.md"):
        m = re.search(r"<!-- rse:([0-9a-f]+) -->", p.read_text(encoding="utf-8"))
        if m: return m.group(1)
