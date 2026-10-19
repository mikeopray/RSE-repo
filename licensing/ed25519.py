"""Ed25519 signature VERIFICATION in pure Python (RFC 8032), so activation needs no extra package. Public-domain reference algorithm; verify only."""
import hashlib
b = 256; q = 2 ** 255 - 19; l = 2 ** 252 + 27742317777372353535851937790883648493
def _H(m): return hashlib.sha512(m).digest()
def _inv(x): return pow(x, q - 2, q)
d = (-121665 * _inv(121666)) % q; I = pow(2, (q - 1) // 4, q)
def _xrecover(y):
    xx = (y * y - 1) * _inv(d * y * y + 1); x = pow(xx, (q + 3) // 8, q)
    if (x * x - xx) % q != 0: x = (x * I) % q
    if x % 2 != 0: x = q - x
    return x
By = 4 * _inv(5); Bx = _xrecover(By); B = (Bx % q, By % q)
def _edwards(P, Q):
    x1, y1 = P; x2, y2 = Q; t = d * x1 * x2 * y1 * y2
    return (((x1 * y2 + x2 * y1) * _inv(1 + t)) % q, ((y1 * y2 + x1 * x2) * _inv(1 - t)) % q)
def _scalarmult(P, e):
    Q = (0, 1)
    for i in range(e.bit_length() - 1, -1, -1):
        Q = _edwards(Q, Q)
        if (e >> i) & 1: Q = _edwards(Q, P)
    return Q
def _bit(h, i): return (h[i // 8] >> (i % 8)) & 1
def _decodeint(s): return sum(2 ** i * _bit(s, i) for i in range(b))
def _oncurve(P): x, y = P; return (-x * x + y * y - 1 - d * x * x * y * y) % q == 0
def _decodepoint(s):
    y = sum(2 ** i * _bit(s, i) for i in range(b - 1)); x = _xrecover(y)
    if x & 1 != _bit(s, b - 1): x = q - x
    P = (x, y)
    if not _oncurve(P): raise ValueError("point not on curve")
    return P
def _encodepoint(P):
    x, y = P; bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]; return bytes(sum(bits[i * 8 + j] << j for j in range(8)) for i in range(b // 8))
def verify(sig: bytes, msg: bytes, pk: bytes) -> bool:
    try:
        if len(sig) != 64 or len(pk) != 32: return False
        R = _decodepoint(sig[:32]); A = _decodepoint(pk); S = _decodeint(sig[32:])
        if S >= l: return False
        h = int.from_bytes(_H(_encodepoint(R) + pk + msg), "little") % l
        return _scalarmult(B, S) == _edwards(R, _scalarmult(A, h))
    except Exception: return False
