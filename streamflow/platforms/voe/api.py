from __future__ import annotations

import json
import urllib.parse
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_get
from streamflow.platforms.voe.constants import resolve_base_url


class VoeAPIError(Exception):
    def __init__(self, message: str, *, status: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


def voe_get(
    path: str,
    api_key: str,
    params: dict[str, Any] | None = None,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> dict[str, Any]:
    base = resolve_base_url(base_url)
    query_params = {"key": api_key, **(params or {})}
    request_url = f"{base}{path}?{urllib.parse.urlencode(query_params)}"

    try:
        response = browser_get(
            request_url,
            api=True,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
        )
    except Exception as exc:
        raise VoeAPIError(f"VOE API request failed: {exc}") from exc

    raw = response.text
    http_status = int(response.status_code)

    if http_status >= 400:
        error_msg = "VOE API request failed"
        try:
            error_data = json.loads(raw)
            error_msg = error_data.get("msg") or error_data.get("message") or error_msg
        except (json.JSONDecodeError, ValueError):
            error_msg = raw if raw else error_msg
        raise VoeAPIError(error_msg, status=http_status, body=raw)

    payload: dict[str, Any] = json.loads(raw)
    api_status = int(payload.get("status", 0))
    if api_status != 200 or not payload.get("success"):
        error_msg = payload.get("msg") or payload.get("message") or "VOE API returned a non-OK status"
        raise VoeAPIError(error_msg, status=api_status, body=raw)

    return payload


# --- Upload Endpoints ---


def upload_from_url(
    api_key: str,
    url: str,
    *,
    folder_id: int | None = None,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """Upload video from remote URL."""
    from streamflow.platforms.voe.models import UploadUrlResponse

    params: dict[str, str | int] = {"url": url}
    if folder_id is not None:
        params["folder_id"] = folder_id
    payload = voe_get(
        "/upload/url",
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    return UploadUrlResponse.from_dict(payload)


def get_upload_server(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """Get upload server URL."""
    from streamflow.platforms.voe.models import UploadServerResponse

    payload = voe_get(
        "/upload/server",
        api_key,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    return UploadServerResponse.from_dict(payload)


# --- Account Endpoints ---


def get_account_stats(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """Get account statistics."""
    from streamflow.platforms.voe.models import AccountStatsResponse

    payload = voe_get(
        "/account/stats",
        api_key,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    return AccountStatsResponse.from_dict(payload)


# --- File Management Endpoints ---


def list_files(
    api_key: str,
    *,
    page: int = 1,
    per_page: int = 100,
    fld_id: int = 0,
    created: str | None = None,
    name: str | None = None,
    preview: bool | None = None,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """List files with optional filtering."""
    from streamflow.platforms.voe.models import FileListResponse

    params: dict[str, str | int | bool] = {
        "page": page,
        "per_page": per_page,
        "fld_id": fld_id,
    }
    if created is not None:
        params["created"] = created
    if name is not None:
        params["name"] = name
    if preview is not None:
        params["preview"] = preview
    payload = voe_get(
        "/file/list",
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    return FileListResponse.from_dict(payload)


def list_all_filecodes(
    api_key: str,
    *,
    fld_id: int = 0,
    per_page: int = 100,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> list[str]:
    """List all filecodes by iterating through all pages."""
    codes: list[str] = []
    page = 1
    while True:
        listing = list_files(
            api_key,
            page=page,
            per_page=per_page,
            fld_id=fld_id,
            base_url=base_url,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
        )
        codes.extend(item.filecode for item in listing.result.data)
        if page >= listing.result.last_page:
            break
        page += 1
    return codes


def delete_files(
    api_key: str,
    del_code: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """Delete files by del_code (comma-separated for batch delete)."""
    from streamflow.platforms.voe.models import FileDeleteResponse

    payload = voe_get(
        "/file/delete",
        api_key,
        {"del_code": del_code},
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    return FileDeleteResponse.from_dict(payload)


# --- Bulk Operations ---


def purge_all_files(
    api_key: str,
    *,
    fld_id: int = 0,
    per_page: int = 100,
    batch_size: int = 50,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
):
    """Delete all files in a folder (batched)."""
    from streamflow.platforms.voe.models import PurgeAllResult

    file_codes = list_all_filecodes(
        api_key,
        fld_id=fld_id,
        per_page=per_page,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
    )
    if not file_codes:
        return PurgeAllResult(deleted=0, file_codes=())

    deleted = 0
    for index in range(0, len(file_codes), batch_size):
        batch = file_codes[index : index + batch_size]
        delete_files(
            api_key,
            ",".join(batch),
            base_url=base_url,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
        )
        deleted += len(batch)

    return PurgeAllResult(deleted=deleted, file_codes=tuple(file_codes))
