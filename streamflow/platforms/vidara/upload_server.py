from __future__ import annotations

import json
import urllib.parse
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_get
from streamflow.platforms.vidara.api import VidaraAPIError
from streamflow.platforms.vidara.constants import upload_server_endpoint
from streamflow.platforms.vidara.models import UploadServerResponse


def get_upload_server(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> UploadServerResponse:
    query = urllib.parse.urlencode({"api_key": api_key})
    request_url = f"{upload_server_endpoint(base_url)}?{query}"

    try:
        response = browser_get(
            request_url,
            api=True,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
            http_version=http_version,
        )
    except Exception as exc:
        raise VidaraAPIError(f"Vidara API request failed: {exc}") from exc

    raw = response.text
    http_status = int(response.status_code)

    if http_status >= 400:
        raise VidaraAPIError(
            f"Vidara API request failed with HTTP {http_status}",
            status=http_status,
            body=raw,
        )

    payload: dict[str, Any] = json.loads(raw)
    if int(payload.get("status", 0)) != 200:
        raise VidaraAPIError(
            str(payload.get("msg", "Vidara API returned a non-OK status")),
            status=int(payload.get("status", 0)),
            body=raw,
        )

    return UploadServerResponse.from_dict(payload)
