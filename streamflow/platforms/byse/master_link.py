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
) -> ByseMasterLink:
    """Get master link for a Byse filecode.
    
    Args:
        filecode: The file code to get master link for
        api_key: Optional API key for authenticated requests
        base_url: Base URL (default: https://byse.sx)
        timeout: Request timeout
        tcp_proxy: TCP proxy URL
        udp_proxy: UDP proxy URL
        local_address: Local address to bind to
        http_version: HTTP version (HTTP/1.1, HTTP/2, HTTP/3)
        viewer_id: Optional viewer ID from challenge flow
        device_id: Optional device ID from challenge flow
        token: Optional token from challenge flow
        fingerprint: Optional fingerprint from challenge flow
    
    Returns:
        ByseMasterLink with streaming URL and metadata
    """
    # Build master link URL
    master_url = f"https://{base_url.replace('https://', '')}/media/{filecode}/master.m3u8"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://{base_url.replace('https://', '')}/d/{filecode}",
        "Origin": f"https://{base_url.replace('https://', '')}",
    }

    # Add optional authentication headers if provided
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
        # Try master link first
        try:
            resp = session.get(master_url, headers=headers, timeout=int(timeout))
            if resp.status_code == 200:
                return ByseMasterLink(
                    filecode=filecode,
                    title=None,
                    streaming_url=master_url,
                    thumbnail=None,
                )
        except Exception:
            pass

        # Fallback: try video page and decrypt sources
        video_url = f"https://{base_url.replace('https://', '')}/d/{filecode}"
        try:
            resp = session.get(video_url, headers=headers, timeout=int(timeout))
            if resp.status_code == 200:
                html = resp.text
                
                # Look for encrypted source in script tags
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
                                    streaming_url=source.get("file", master_url),
                                    thumbnail=decrypted.get("image") or source.get("image"),
                                )
                        except Exception:
                            continue

                # Try to find thumbnail
                thumb_match = re.search(r'"image"\s*:\s*"([^"]+)"', html)
                thumbnail = thumb_match.group(1) if thumb_match else None

                return ByseMasterLink(
                    filecode=filecode,
                    title=None,
                    streaming_url=master_url,
                    thumbnail=thumbnail,
                )
        except Exception:
            pass

    # Ultimate fallback
    return ByseMasterLink(
        filecode=filecode,
        title=None,
        streaming_url=master_url,
        thumbnail=None,
    )