"""Streamembed master link resolver using AES decryption."""

from __future__ import annotations

import logging
import re

from Crypto.Cipher import AES  # type: ignore

from streamflow.core.transport import browser_get
from streamflow.platforms.streamembed.constants import (
    AES_KEY_HEX,
    AES_IV_HEX,
    DEFAULT_SITE_URL,
    DEFAULT_VIDEO_HEIGHT,
    DEFAULT_VIDEO_WIDTH,
    DEFAULT_TIMEOUT,
    resolve_site_base_url,
)

from .models import StreamembedMasterLink

logger = logging.getLogger(__name__)


def _hex_to_bytes(hex_text: str) -> bytes:
    """Convert hex string to bytes."""
    cleaned = (hex_text or "").strip()
    if len(cleaned) % 2 != 0:
        raise ValueError("Invalid hex length")
    return bytes.fromhex(cleaned)


def _pkcs7_unpad(data: bytes) -> bytes:
    """Remove PKCS7 padding from decrypted data."""
    if not data:
        raise ValueError("Empty decrypted payload")
    pad_len = data[-1]
    
    if 1 <= pad_len <= 16 and data[-pad_len:] == bytes([pad_len]) * pad_len:
        return data[:-pad_len]
    
    if data[-1] == 0x80:
        for i in range(len(data) - 2, -1, -1):
            if data[i] != 0:
                return data[:i + 1]
        return b''
    
    if 1 <= pad_len <= 16:
        padding_content = data[-pad_len:]
        if padding_content[:-1] == b'\x00' * (pad_len - 1):
            return data[:-pad_len]
    
    for pad_value in range(1, 17):
        padding = bytes([pad_value]) * pad_value
        if data.endswith(padding):
            if all(b == pad_value for b in data[-pad_value:]):
                potential_json = data[:-pad_value]
                try:
                    potential_json.decode('utf-8')
                    return potential_json
                except UnicodeDecodeError:
                    continue
    
    raise ValueError("Invalid padding")


def _decrypt_response(cipher_hex: str, key_hex: str, iv_hex: str) -> dict:
    """Decrypt AES-128-CBC encrypted response and parse JSON."""
    key = bytes.fromhex((key_hex or "").strip())
    iv = bytes.fromhex((iv_hex or "").strip())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_bytes = _hex_to_bytes(cipher_hex)
    plaintext = cipher.decrypt(cipher_bytes)
    unpadded = _pkcs7_unpad(plaintext)
    json_str = unpadded.decode("utf-8", errors="strict")
    import json
    return json.loads(json_str)


def _extract_master_txt_link(text: str | None) -> str | None:
    """Extract master.txt URL using regex from any text."""
    if not text:
        return None
    # Look for master.txt URL
    pattern = r'https?://[^\s"\'<>]+master\.txt[^\s"\'<>]*'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    return None


def _build_master_url(base_url: str, path: str) -> str:
    """Build master.m3u8 URL from decrypted response."""
    if not path:
        return ""
    path = path.strip()
    if path.startswith("//"):
        path = "https:" + path
    elif path.startswith("/"):
        base = base_url.rstrip("/")
        return f"{base}{path}"
    elif not path.startswith("http"):
        base = base_url.rstrip("/")
        return f"{base}/{path}"
    return path


def get_master_link(
    filecode: str,
    *,
    base_url: str | None = None,
    width: int = DEFAULT_VIDEO_WIDTH,
    height: int = DEFAULT_VIDEO_HEIGHT,
    aes_key_hex: str | None = None,
    aes_iv_hex: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> StreamembedMasterLink:
    """Get master link for a StreamEmbed video.

    Args:
        filecode: The video ID to get master link for
        base_url: Base URL of the embed site (default: resolved from environment)
        width: Video width for API request (default: 2048)
        height: Video height for API request (default: 1152)
        aes_key_hex: AES key for decryption (default: built-in key)
        aes_iv_hex: AES IV for decryption (default: built-in IV)
        timeout: Request timeout
        tcp_proxy: TCP proxy URL
        udp_proxy: UDP proxy URL
        local_address: Local address to bind to
        http_version: HTTP version (HTTP/1.1, HTTP/2, HTTP/3)

    Returns:
        StreamembedMasterLink with streaming URL and metadata
    """
    resolved_base = resolve_site_base_url(base_url)
    effective_base = resolved_base.replace("https://", "").replace("http://", "")

    key_hex = aes_key_hex or AES_KEY_HEX
    iv_hex = aes_iv_hex or AES_IV_HEX

    video_url = f"https://{effective_base}/api/v1/video?id={filecode}&w={width}&h={height}&r="

    resp = browser_get(
        video_url,
        api=True,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
        Referer=f"https://{effective_base}/",
        **{
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        },
    )

    if resp.status_code != 200:
        return StreamembedMasterLink(
            filecode=filecode,
            title=None,
            streaming_url="",
            thumbnail=None,
            raw={"status_code": resp.status_code, "text": resp.text},
        )

    cipher_hex = (resp.text or "").strip()
    if not cipher_hex:
        return StreamembedMasterLink(
            filecode=filecode,
            title=None,
            streaming_url="",
            thumbnail=None,
            raw={"error": "empty_response"},
        )

    try:
        payload = _decrypt_response(cipher_hex, key_hex, iv_hex)
    except Exception as e:
        logger.error(f"Streamembed decryption failed: {e}")
        return StreamembedMasterLink(
            filecode=filecode,
            title=None,
            streaming_url="",
            thumbnail=None,
            raw={"error": f"decryption_failed: {e}", "cipher_hex": cipher_hex[:100] + "..." if len(cipher_hex) > 100 else cipher_hex},
        )

    title = payload.get("title") or None
    thumbnail = payload.get("thumbnail") or payload.get("poster") or None
    cf_url = payload.get("cf") or None
    swarm_id = payload.get("swarmId") or None

    torrent_trackers_list: list[str] | None = None
    if "torrentTrackers" in payload:
        trackers = payload.get("torrentTrackers")
        if isinstance(trackers, list):
            torrent_trackers_list = [str(t) for t in trackers]

    ice_servers_list: list[dict] | None = None
    if "iceServers" in payload:
        ice_servers_list = payload.get("iceServers")
        if not isinstance(ice_servers_list, list):
            ice_servers_list = None

    streaming_url = payload.get("source") or payload.get("master") or payload.get("masterUrl") or ""
    master_url = ""

    if cf_url:
        master_txt = _extract_master_txt_link(cf_url)
        if master_txt:
            master_url = master_txt
        else:
            try:
                resp = browser_get(cf_url, api=False, timeout=timeout)
                if resp.status_code == 200:
                    master_txt = _extract_master_txt_link(resp.text)
                    if master_txt:
                        master_url = master_txt
            except Exception as e:
                logger.warning(f"Failed to fetch cf_url: {e}")
    else:
        payload_str = str(payload)
        master_txt = _extract_master_txt_link(payload_str)
        if master_txt:
            master_url = master_txt

    return StreamembedMasterLink(
        filecode=filecode,
        title=title,
        streaming_url=streaming_url,
        thumbnail=thumbnail,
        master_url=master_url,
        cf_url=cf_url,
        swarm_id=swarm_id,
        torrent_trackers=torrent_trackers_list,
        ice_servers=ice_servers_list,
        raw=payload,
    )