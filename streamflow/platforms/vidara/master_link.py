from __future__ import annotations

import json
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_post
from streamflow.platforms.vidara.api import VidaraAPIError
from streamflow.platforms.vidara.constants import (
    STREAM_DEVICE_DEFAULT,
    STREAM_PRESET,
    embed_page_url,
    resolve_site_base_url,
    stream_endpoint,
)
from streamflow.platforms.vidara.models import MasterLinkResponse


def stream_request_headers(filecode: str, *, site_base_url: str | None = None, cookie: str | None = None) -> dict[str, str]:
    site = resolve_site_base_url(site_base_url)
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": site,
        "referer": embed_page_url(filecode, site_base_url),
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }
    if cookie:
        headers["cookie"] = cookie
    return headers


def get_master_link(
    filecode: str,
    *,
    device: str = STREAM_DEVICE_DEFAULT,
    site_base_url: str | None = None,
    cookie: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> MasterLinkResponse:
    url = stream_endpoint(site_base_url)
    body = {"filecode": filecode, "device": device}
    headers = stream_request_headers(filecode, site_base_url=site_base_url, cookie=cookie)

    try:
        response = browser_post(
            url,
            json=body,
            timeout=timeout,
            preset=STREAM_PRESET,
            without_cookie_jar=cookie is None,
            header_order=False,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
            http_version=http_version,
            **headers,
        )
    except Exception as exc:
        raise VidaraAPIError(f"Vidara stream request failed: {exc}") from exc

    raw = response.text
    http_status = int(response.status_code)

    if http_status >= 400:
        raise VidaraAPIError(
            f"Vidara stream request failed with HTTP {http_status}",
            status=http_status,
            body=raw,
        )

    payload: dict[str, Any] = json.loads(raw)
    if not payload.get("streaming_url"):
        raise VidaraAPIError("Vidara stream response missing streaming_url", body=raw)

    return MasterLinkResponse.from_dict(payload)
