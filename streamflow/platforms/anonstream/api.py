"""Anonstream API functions."""

from __future__ import annotations

import json
import urllib.parse
from typing import Any

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.core.transport import browser_get
from streamflow.platforms.anonstream.constants import resolve_base_url


class AnonstreamAPIError(Exception):
    """Anonstream API error."""
    def __init__(self, message: str, *, status: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


def anonstream_get(
    path: str,
    api_key: str,
    params: dict[str, Any] | None = None,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> dict[str, Any]:
    """Make a GET request to Anonstream API."""
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
            http_version=http_version,
        )
    except Exception as exc:
        raise AnonstreamAPIError(f"Anonstream API request failed: {exc}") from exc

    raw = response.text
    http_status = int(response.status_code)

    if http_status >= 400:
        error_msg = f"Anonstream API request failed with HTTP {http_status}"
        try:
            error_data = json.loads(raw)
            error_msg = error_data.get("msg") or error_data.get("message") or error_msg
        except (json.JSONDecodeError, ValueError):
            pass
        raise AnonstreamAPIError(error_msg, status=http_status, body=raw)

    try:
        payload: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AnonstreamAPIError(
            f"Failed to parse JSON response: {exc}",
            status=http_status,
            body=raw,
        ) from exc

    return payload


def upload_from_url(
    api_key: str,
    url: str,
    *,
    fld_id: int | None = None,
    cat_id: int | None = None,
    file_public: int | None = None,
    file_adult: int | None = None,
    tags: str | None = None,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
):
    """Upload file from remote URL."""
    from streamflow.platforms.anonstream.models import UploadResponse

    path = "/api/upload/url"
    params: dict[str, str | int] = {"url": url}
    if fld_id is not None:
        params["fld_id"] = fld_id
    if cat_id is not None:
        params["cat_id"] = cat_id
    if file_public is not None:
        params["file_public"] = file_public
    if file_adult is not None:
        params["file_adult"] = file_adult
    if tags is not None:
        params["tags"] = tags

    payload = anonstream_get(
        path,
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    return UploadResponse.from_dict(payload)


def get_account_stats(
    api_key: str,
    *,
    last: int = 7,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
):
    """Get account statistics for last X days."""
    from streamflow.platforms.anonstream.models import AccountStatsResponse

    path = "/api/account/stats"
    params: dict[str, str | int] = {"last": last}

    payload = anonstream_get(
        path,
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    return AccountStatsResponse.from_dict(payload)


def list_files(
    api_key: str,
    *,
    fld_id: int | None = None,
    title: str | None = None,
    created: str | None = None,
    public: int | None = None,
    adult: int | None = None,
    per_page: int = 20,
    page: int = 1,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
):
    """List files with optional filters."""
    from streamflow.platforms.anonstream.models import FileListResponse

    path = "/api/file/list"
    params: dict[str, str | int] = {"per_page": per_page, "page": page}
    if fld_id is not None:
        params["fld_id"] = fld_id
    if title is not None:
        params["title"] = title
    if created is not None:
        params["created"] = created
    if public is not None:
        params["public"] = public
    if adult is not None:
        params["adult"] = adult

    payload = anonstream_get(
        path,
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    return FileListResponse.from_dict(payload)


def delete_file(
    api_key: str,
    file_code: str,
    *,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
):
    """Delete a file by file code."""
    from streamflow.platforms.anonstream.models import FileDeleteResponse

    path = "/api/file/delete"
    params = {"file_code": file_code}

    payload = anonstream_get(
        path,
        api_key,
        params,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    return FileDeleteResponse.from_dict(payload)


def list_all_filecodes(
    api_key: str,
    *,
    fld_id: int | None = None,
    per_page: int = 100,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> list[str]:
    """List all filecodes by iterating through pages."""
    codes: list[str] = []
    page = 1
    while True:
        listing = list_files(
            api_key,
            fld_id=fld_id,
            per_page=per_page,
            page=page,
            base_url=base_url,
            timeout=timeout,
            tcp_proxy=tcp_proxy,
            udp_proxy=udp_proxy,
            local_address=local_address,
            http_version=http_version,
        )
        codes.extend(item.file_code for item in listing.result.files)
        if page >= listing.result.pages:
            break
        page += 1
    return codes


def purge_all_files(
    api_key: str,
    *,
    fld_id: int | None = None,
    per_page: int = 100,
    batch_size: int = 50,
    base_url: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
):
    """Delete all files in account/folder (batched)."""
    from streamflow.platforms.anonstream.models import PurgeAllResult

    file_codes = list_all_filecodes(
        api_key,
        fld_id=fld_id,
        per_page=per_page,
        base_url=base_url,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    )
    if not file_codes:
        return PurgeAllResult(deleted=0, file_codes=())

    deleted = 0
    errors: list[str] = []
    for index in range(0, len(file_codes), batch_size):
        batch = file_codes[index : index + batch_size]
        for code in batch:
            try:
                delete_file(
                    api_key,
                    code,
                    base_url=base_url,
                    timeout=timeout,
                    tcp_proxy=tcp_proxy,
                    udp_proxy=udp_proxy,
                    local_address=local_address,
                    http_version=http_version,
                )
                deleted += 1
            except Exception as exc:
                errors.append(f"Failed to delete {code}: {exc}")

    return PurgeAllResult(deleted=deleted, file_codes=tuple(file_codes), errors=errors)