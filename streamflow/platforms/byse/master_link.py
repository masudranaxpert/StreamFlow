"""Byse master link resolver.

Implements the Byse **challenge-attest-playback** flow (works against any
Byse mirror that exposes the ``/api/videos/access/*`` endpoints,
e.g. ``byse.sx``, ``bysevepoin.com``, etc.):

    1. POST /api/videos/access/challenge   -> {challenge_id, nonce}
    2. ECDSA P-256 sign nonce locally
    3. POST /api/videos/access/attest      -> {token, viewer_id, device_id}
    4. POST /api/videos/{id}/playback      -> {iv, payload, key_parts, ...}
    5. AES-256-GCM decrypt the payload using the two short (16-byte)
       entries among the obfuscated ``key_parts``, concatenated in
       reverse document order.
    6. Return ``sources[0].url`` as the streaming URL.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass

import httpcloak
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from streamflow.constants import DEFAULT_TIMEOUT


@dataclass
class ByseMasterLink:
    """Resolved Byse master link."""

    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None
    expires_at: str | None = None


class ByseMasterLinkError(Exception):
    """Raised when resolving a Byse master link fails."""


def _strip_scheme(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def _b64url_decode(s: str) -> bytes:
    s = s + "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)


def _b64url_uint(value: int, length: int) -> str:
    return (
        base64.urlsafe_b64encode(value.to_bytes(length, "big"))
        .rstrip(b"=")
        .decode("ascii")
    )


def _public_key_jwk(public_key: ec.EllipticCurvePublicKey) -> dict:
    nums = public_key.public_numbers()
    return {
        "alg": "ES256",
        "crv": "P-256",
        "ext": True,
        "key_ops": ["verify"],
        "kty": "EC",
        "x": _b64url_uint(nums.x, 32),
        "y": _b64url_uint(nums.y, 32),
    }


def _sign_nonce(private_key: ec.EllipticCurvePrivateKey, nonce: str) -> str:
    der_sig = private_key.sign(nonce.encode("utf-8"), ec.ECDSA(hashes.SHA256()))
    r_val, s_val = decode_dss_signature(der_sig)
    raw = r_val.to_bytes(32, "big") + s_val.to_bytes(32, "big")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _candidate_aes_keys(key_parts_b64: list[str]) -> list[tuple[str, bytes]]:
    """Build a list of candidate AES-256-GCM keys from ``key_parts``.

    The Byse playback API returns ~30 ``key_parts`` per response. The
    vast majority (28) are 24-byte decoys and exactly **two** are
    16-byte real key fragments at unpredictable indices. Different
    ``version`` values pack the real key slightly differently, so we
    return all the orderings/derivations we have seen work and let the
    caller try them in turn — AES-GCM is authenticated, so wrong keys
    fail loudly without revealing plaintext.
    """
    import hashlib

    parts = [_b64url_decode(p) for p in key_parts_b64]
    short = [i for i, p in enumerate(parts) if len(p) == 16]

    candidates: list[tuple[str, bytes]] = []
    seen: set[bytes] = set()

    def add(label: str, key: bytes) -> None:
        if len(key) != 32 or key in seen:
            return
        seen.add(key)
        candidates.append((label, key))

    if len(short) == 2:
        a, b = short
        add(f"parts[{b}]+parts[{a}] (reverse)", parts[b] + parts[a])
        add(f"parts[{a}]+parts[{b}] (forward)", parts[a] + parts[b])
        add(f"SHA-256(parts[{a}]+parts[{b}])",
            hashlib.sha256(parts[a] + parts[b]).digest())
        add(f"SHA-256(parts[{b}]+parts[{a}])",
            hashlib.sha256(parts[b] + parts[a]).digest())
        xor = bytes(x ^ y for x, y in zip(parts[a], parts[b]))
        add(f"SHA-256(parts[{a}] XOR parts[{b}])",
            hashlib.sha256(xor).digest())

    for i in range(len(parts)):
        for j in range(len(parts)):
            if i == j:
                continue
            pair = parts[i] + parts[j]
            if len(pair) == 32:
                add(f"parts[{i}]+parts[{j}]", pair)

    return candidates


def _request_headers(
    host: str,
    filecode: str,
    *,
    json_body: bool = False,
    cookie: str | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://{host}/d/{filecode}",
        "Origin": f"https://{host}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=4",
    }
    if json_body:
        headers["Content-Type"] = "application/json"
    if cookie:
        headers["Cookie"] = cookie
    return headers


def get_master_link(
    filecode: str,
    *,
    base_url: str = "https://byse.sx",
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> ByseMasterLink:
    """Resolve a Byse video to its m3u8 master URL.

    Args:
        filecode: Video filecode (the ``XXXX`` in ``/d/XXXX``).
        base_url: Site URL of the Byse mirror that serves the video
            (the host in the ``/d/{filecode}`` page URL). Must expose
            the ``/api/videos/access/*`` and ``/api/videos/{id}/playback``
            challenge flow. Defaults to ``https://byse.sx``; override
            with whichever mirror (``bysevepoin.com``, etc.) the link
            actually uses.
        timeout: Per-request timeout in seconds.
        tcp_proxy: HTTP CONNECT proxy URL.
        udp_proxy: SOCKS5 / UDP proxy URL.
        local_address: Local IP to bind.
        http_version: Force ``"HTTP/1.1"``, ``"HTTP/2"`` or
            ``"HTTP/3"`` (last requires ``udp_proxy``).

    Returns:
        ``ByseMasterLink`` with ``streaming_url``, ``thumbnail`` and
        ``expires_at`` populated.

    Raises:
        ByseMasterLinkError: any step of the flow (challenge, attest,
            playback, decryption, JSON parse) fails.
    """
    host = _strip_scheme(base_url)
    challenge_url = f"https://{host}/api/videos/access/challenge"
    attest_url = f"https://{host}/api/videos/access/attest"
    playback_url = f"https://{host}/api/videos/{filecode}/playback"

    with httpcloak.Session(
        timeout=int(timeout),
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    ) as session:
        try:
            resp = session.post(challenge_url, headers=_request_headers(host, filecode))
        except Exception as exc:
            raise ByseMasterLinkError(f"challenge request failed: {exc}") from exc
        if resp.status_code != 200:
            raise ByseMasterLinkError(
                f"challenge HTTP {resp.status_code}: {(resp.text or '')[:200]}"
            )
        try:
            cdata = resp.json()
        except Exception as exc:
            raise ByseMasterLinkError(f"challenge json parse failed: {exc}") from exc
        challenge_id = cdata.get("challenge_id")
        nonce = cdata.get("nonce")
        if not (challenge_id and nonce):
            raise ByseMasterLinkError(
                f"challenge missing challenge_id/nonce: keys={list(cdata.keys())}"
            )

        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        signature = _sign_nonce(private_key, nonce)
        public_jwk = _public_key_jwk(public_key)

        attest_payload = {
            "challenge_id": challenge_id,
            "nonce": nonce,
            "signature": signature,
            "public_key": public_jwk,
        }
        try:
            resp = session.post(
                attest_url,
                headers=_request_headers(host, filecode, json_body=True),
                json=attest_payload,
            )
        except Exception as exc:
            raise ByseMasterLinkError(f"attest request failed: {exc}") from exc
        if resp.status_code != 200:
            raise ByseMasterLinkError(
                f"attest HTTP {resp.status_code}: {(resp.text or '')[:200]}"
            )
        try:
            adata = resp.json()
        except Exception as exc:
            raise ByseMasterLinkError(f"attest json parse failed: {exc}") from exc
        token = adata.get("token")
        viewer_id = adata.get("viewer_id")
        device_id = adata.get("device_id")
        confidence = adata.get("confidence")
        if not (token and viewer_id and device_id):
            raise ByseMasterLinkError(
                f"attest missing token/viewer_id/device_id: keys={list(adata.keys())}"
            )

        cookie = f"byse_viewer_id={viewer_id}; byse_device_id={device_id}"
        playback_payload = {
            "fingerprint": {
                "token": token,
                "viewer_id": viewer_id,
                "device_id": device_id,
                "confidence": confidence,
            }
        }
        try:
            resp = session.post(
                playback_url,
                headers=_request_headers(host, filecode, json_body=True, cookie=cookie),
                json=playback_payload,
            )
        except Exception as exc:
            raise ByseMasterLinkError(f"playback request failed: {exc}") from exc
        if resp.status_code != 200:
            raise ByseMasterLinkError(
                f"playback HTTP {resp.status_code}: {(resp.text or '')[:200]}"
            )
        try:
            pdata = resp.json()
        except Exception as exc:
            raise ByseMasterLinkError(f"playback json parse failed: {exc}") from exc
        pb = pdata.get("playback")
        if not isinstance(pb, dict):
            raise ByseMasterLinkError(
                f"playback response missing 'playback' object: keys={list(pdata.keys())}"
            )

        iv_b64 = pb.get("iv")
        payload_b64 = pb.get("payload")
        key_parts = pb.get("key_parts") or []
        if not (iv_b64 and payload_b64 and key_parts):
            raise ByseMasterLinkError(
                f"playback missing iv/payload/key_parts: keys={list(pb.keys())}"
            )

        iv_bytes = _b64url_decode(iv_b64)
        payload_bytes = _b64url_decode(payload_b64)
        candidates = _candidate_aes_keys(key_parts)
        if not candidates:
            raise ByseMasterLinkError(
                "could not derive any candidate AES key from key_parts"
            )

        plaintext: bytes | None = None
        last_error: Exception | None = None
        for _label, candidate in candidates:
            try:
                plaintext = AESGCM(candidate).decrypt(iv_bytes, payload_bytes, None)
                break
            except Exception as exc:
                last_error = exc
        if plaintext is None:
            raise ByseMasterLinkError(
                f"AES-256-GCM decrypt failed across {len(candidates)} "
                f"candidate keys (last error: {last_error})"
            )

        try:
            parsed = json.loads(plaintext.decode("utf-8"))
        except Exception as exc:
            raise ByseMasterLinkError(f"decrypted payload not valid JSON: {exc}") from exc

        sources = parsed.get("sources") or []
        if not sources:
            raise ByseMasterLinkError(
                f"decrypted payload has no 'sources': keys={list(parsed.keys())}"
            )
        primary = sources[0]
        streaming_url = primary.get("url") or ""
        if not streaming_url:
            raise ByseMasterLinkError(
                f"first source has no 'url': {primary}"
            )

        return ByseMasterLink(
            filecode=filecode,
            title=parsed.get("title"),
            streaming_url=streaming_url,
            thumbnail=parsed.get("poster_url"),
            expires_at=parsed.get("expires_at"),
        )