"""Byse master link system."""

from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass
from typing import Any

import httpcloak

from streamflow.constants import DEFAULT_TIMEOUT


@dataclass
class ByseMasterLink:
    """Decrypted master link response."""
    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None


def _decrypt_byse_source(enc_str: str) -> dict[str, Any]:
    """Decrypt Byse encrypted source string."""
    # Reverse the process
    s = enc_str

    # 1. Base64 decode (first layer)
    try:
        s = base64.b64decode(s).decode('utf-8')
    except Exception:
        pass

    # 2. Each char + 3
    s = ''.join(chr(ord(c) + 3) for c in s)

    # 3. Reverse string
    s = s[::-1]

    # 4. Base64 decode (second layer)
    try:
        s = base64.b64decode(s).decode('utf-8')
    except Exception:
        pass

    # 5. Replace delimiters with underscores and remove
    for delimiter in ['@$', '^^', '~@', '%?', '*~', '!!', '#&']:
        s = s.replace(delimiter, '_')
    s = s.replace('_', '')

    # 6. ROT13 cipher
    def rot13_char(c: str) -> str:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            return chr((ord(c) - base + 13) % 26 + base)
        return c

    s = ''.join(rot13_char(c) for c in s)

    return json.loads(s) if s else {}


def _normalize_host(base_url: str) -> str:
    """Return the bare host (no scheme, no trailing slash) of ``base_url``."""
    return (
        base_url
        .replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
    )


def _looks_like_m3u8(body: str | None) -> bool:
    """Return True iff ``body`` is the contents of an actual HLS playlist.

    Many Byse hosts are single-page apps that serve their HTML index for
    *every* unknown path (including ``/media/<x>/master.m3u8``) with
    ``200 OK``. Status alone is therefore not enough — we must look at
    the body to make sure it really is an ``#EXTM3U`` playlist.
    """
    if not body:
        return False
    return body.lstrip().startswith("#EXTM3U")


def get_master_link(
    filecode: str,
    *,
    api_key: str | None = None,
    base_url: str = "https://byse.sx",
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
    viewer_id: str | None = None,
    device_id: str | None = None,
    token: str | None = None,
    fingerprint: str | None = None,
    use_hardcoded_master_url: bool = False,
) -> ByseMasterLink:
    """Get master link for a Byse filecode.

    By default this resolver goes **straight to the video page** at
    ``{base_url}/d/{filecode}`` and extracts the streaming URL from the
    embedded (encrypted) sources. The legacy "guess the URL by following
    a hardcoded ``/media/{filecode}/master.m3u8`` pattern" path is
    available as an opt-in via ``use_hardcoded_master_url=True``.

    Args:
        filecode: The file code to get master link for.
        api_key: Optional API key for authenticated requests.
        base_url: Base URL (default: ``https://byse.sx``).
        timeout: Request timeout.
        tcp_proxy: TCP proxy URL.
        udp_proxy: UDP proxy URL.
        local_address: Local address to bind to.
        http_version: HTTP version (``HTTP/1.1``, ``HTTP/2``, ``HTTP/3``).
        viewer_id: Optional viewer ID from challenge flow.
        device_id: Optional device ID from challenge flow.
        token: Optional token from challenge flow.
        fingerprint: Optional fingerprint from challenge flow.
        use_hardcoded_master_url: If ``True``, *also* try the legacy
            ``/media/{filecode}/master.m3u8`` URL pattern first and
            return it when the body actually looks like an ``#EXTM3U``
            playlist. The response body is content-verified, so a 200
            OK that returns the SPA's HTML index will *not* be returned
            as a streaming URL. Defaults to ``False``.

    Returns:
        ``ByseMasterLink`` with streaming URL and metadata.
    """
    host = _normalize_host(base_url)
    fallback_master_url = f"https://{host}/media/{filecode}/master.m3u8"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://{host}/d/{filecode}",
        "Origin": f"https://{host}",
    }

    if viewer_id or device_id:
        cookies = []
        if viewer_id:
            cookies.append(f"byse_viewer_id={viewer_id}")
        if device_id:
            cookies.append(f"byse_device_id={device_id}")
        headers["Cookie"] = "; ".join(cookies)

    with httpcloak.Session(
        timeout=int(timeout),
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    ) as session:
        if use_hardcoded_master_url:
            try:
                resp = session.get(fallback_master_url, headers=headers, timeout=int(timeout))
                if resp.status_code == 200 and _looks_like_m3u8(resp.text):
                    return ByseMasterLink(
                        filecode=filecode,
                        title=None,
                        streaming_url=fallback_master_url,
                        thumbnail=None,
                    )
            except Exception:
                pass

        video_url = f"https://{host}/d/{filecode}"
        try:
            resp = session.get(video_url, headers=headers, timeout=int(timeout))
            if resp.status_code == 200:
                html = resp.text

                patterns = [
                    r'sources\s*:\s*\[\{file:"([^"]+)"',
                    r'"sources"\s*:\s*\[.*?"file"\s*:\s*"([^"]+)"',
                    r'decodeURIComponent\("([^"]+)"\)',
                    r'atob\("([^"]+)"\)',
                ]

                for pattern in patterns:
                    match = re.search(pattern, html, re.DOTALL)
                    if match:
                        enc_str = match.group(1)
                        try:
                            decrypted = _decrypt_byse_source(enc_str)
                            if decrypted.get("sources"):
                                source = decrypted["sources"][0]
                                return ByseMasterLink(
                                    filecode=filecode,
                                    title=decrypted.get("title"),
                                    streaming_url=source.get("file", ""),
                                    thumbnail=decrypted.get("image") or source.get("image"),
                                )
                        except Exception:
                            continue

                thumb_match = re.search(r'"image"\s*:\s*"([^"]+)"', html)
                thumbnail = thumb_match.group(1) if thumb_match else None

                return ByseMasterLink(
                    filecode=filecode,
                    title=None,
                    streaming_url="",
                    thumbnail=thumbnail,
                )
        except Exception:
            pass

    return ByseMasterLink(
        filecode=filecode,
        title=None,
        streaming_url="",
        thumbnail=None,
    )