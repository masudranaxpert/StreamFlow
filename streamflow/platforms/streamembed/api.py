"""Streamembed API calls."""

from __future__ import annotations

import json
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_get, browser_post
from streamflow.platforms.streamembed.constants import (
    advance_upload_detail_endpoint,
    advance_upload_endpoint,
    resolve_base_url,
)
from streamflow.platforms.streamembed.models import (
    AdvanceUploadDetailResponse,
    AdvanceUploadResponse,
)


class StreamembedAPIError(Exception):
    """API error exception."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


def _handle_error(http_status: int, raw: str) -> None:
    """Handle HTTP error responses."""
    if http_status == 401:
        raise StreamembedAPIError("Invalid credentials", status=401, body=raw)
    if http_status == 404:
        raise StreamembedAPIError("Not found", status=404, body=raw)
    if http_status == 429:
        raise StreamembedAPIError("Rate limit exceeded", status=429, body=raw)
    if http_status >= 400:
        try:
            data = json.loads(raw)
            message = data.get("message", "Unknown error")
        except json.JSONDecodeError:
            message = raw or "Unknown error"
        raise StreamembedAPIError(message, status=http_status, body=raw)


def advance_upload(
    api_key: str,
    url: str,
    *,
    name: str | None = None,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> AdvanceUploadResponse:
    """Create advanced upload task. POST /api/v1/video/advance-upload."""
    endpoint = advance_upload_endpoint(base_url)
    payload: dict[str, Any] = {"url": url}
    if name:
        payload["name"] = name

    try:
        response = browser_post(
            endpoint,
            json=payload,
            api=True,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
            Authorization=f"Bearer {api_key}",
        )
        raw = response.text
        http_status = int(response.status_code)
        _handle_error(http_status, raw)
        return AdvanceUploadResponse.from_dict(json.loads(raw))
    except StreamembedAPIError:
        raise
    except Exception as exc:
        raise StreamembedAPIError(f"Request failed: {exc}") from exc


def get_upload_task(
    api_key: str,
    task_id: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> AdvanceUploadDetailResponse:
    """Get upload task detail. GET /api/v1/video/advance-upload/{id}."""
    endpoint = advance_upload_detail_endpoint(task_id, base_url)

    try:
        response = browser_get(
            endpoint,
            api=True,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
            Authorization=f"Bearer {api_key}",
        )
        raw = response.text
        http_status = int(response.status_code)
        _handle_error(http_status, raw)
        return AdvanceUploadDetailResponse.from_dict(json.loads(raw))
    except StreamembedAPIError:
        raise
    except Exception as exc:
        raise StreamembedAPIError(f"Request failed: {exc}") from exc
