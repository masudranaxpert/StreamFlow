from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_get
from streamflow.platforms.voe.api import VoeAPIError
from streamflow.platforms.voe.constants import resolve_site_base_url, file_page_url


@dataclass(frozen=True, slots=True)
class VoeMasterLink:
    """VOE master link response with streaming URL."""
    streaming_url: str
    title: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> VoeMasterLink:
        return cls(
            streaming_url=str(payload["source"]),
            title=payload.get("title"),
        )


def decrypt_voe_source(enc_str: str) -> dict[str, Any]:
    """Decrypt VOE encrypted string to extract source URL."""
    # 1. ROT13 cipher
    def rot13_char(c: str) -> str:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            return chr((ord(c) - base + 13) % 26 + base)
        return c

    s = ''.join(rot13_char(c) for c in enc_str)

    # 2. Replace delimiters with underscore
    for delimiter in ['@$', '^^', '~@', '%?', '*~', '!!', '#&']:
        s = s.replace(delimiter, '_')

    # 3. Remove underscores
    s = s.replace('_', '')

    # 4. Base64 decode
    s = base64.b64decode(s).decode('utf-8')

    # 5. Each char - 3
    s = ''.join(chr(ord(c) - 3) for c in s)

    # 6. Reverse string
    s = s[::-1]

    # 7. Base64 decode again
    s = base64.b64decode(s).decode('utf-8')

    return json.loads(s)


def extract_redirect_url(html: str) -> str | None:
    """Extract redirect URL from VOE page HTML."""
    # Look for window.location.href = 'url'
    pattern = r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]"
    match = re.search(pattern, html)
    if match:
        return match.group(1)
    return None


def get_master_link(
    filecode: str,
    *,
    site_base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> VoeMasterLink:
    """Get VOE master link (m3u8) from filecode."""
    # Step 1: Get the /e/{filecode} page
    page_url = file_page_url(filecode, site_base_url)
    response = browser_get(
        page_url,
        api=False,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    html = response.text

    # Step 2: Check if response is too short (< 1.5KB) - indicates JS redirect page
    if len(html) < 1500:
        # Step 3: Look for window.location.href redirect
        redirect_url = extract_redirect_url(html)
        if redirect_url:
            # Step 4: Follow redirect
            response = browser_get(
                redirect_url,
                api=False,
                timeout=timeout,
                tcp_proxy=tcp_proxy,
                udp_proxy=udp_proxy,
                local_address=local_address,
                http_version=http_version,
            )
            html = response.text

    # Step 5: Find encrypted script tag: <script type="application/json">["..."]</script>
    pattern = r'<script type="application/json">\["([^"]+)"\]</script>'
    match = re.search(pattern, html)

    if not match:
        raise VoeAPIError(
            f"No encrypted script found in VOE page for filecode: {filecode}",
            body=html[:500] if html else "Empty response",
        )

    enc_str = match.group(1)

    # Step 6: Decrypt to get config
    try:
        config = decrypt_voe_source(enc_str)
    except Exception as exc:
        raise VoeAPIError(f"Failed to decrypt VOE source: {exc}") from exc

    if not config.get("source"):
        raise VoeAPIError("VOE response missing 'source' field", body=str(config))

    return VoeMasterLink.from_dict(config)