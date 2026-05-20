from __future__ import annotations

from typing import Any

import httpcloak

from streamflow.constants import (
    API_BROWSER_HEADERS,
    API_HEADER_ORDER,
    BROWSER_HEADER_ORDER,
    DEFAULT_BROWSER_HEADERS,
    DEFAULT_TIMEOUT,
    RECOMMENDED_HTTP_PRESET,
)


def browser_headers(*, api: bool = False, **overrides: str) -> dict[str, str]:
    base = API_BROWSER_HEADERS if api else DEFAULT_BROWSER_HEADERS
    merged = dict(base)
    merged.update(overrides)
    return merged


def ordered_header_names(*, api: bool = False) -> list[str]:
    return list(API_HEADER_ORDER if api else BROWSER_HEADER_ORDER)


def open_session(
    *,
    api: bool = False,
    preset: str = RECOMMENDED_HTTP_PRESET,
    timeout: float = DEFAULT_TIMEOUT,
    without_cookie_jar: bool | None = None,
    header_order: bool = True,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
    **kwargs: Any,
) -> httpcloak.Session:
    if without_cookie_jar is None:
        without_cookie_jar = api
    session = httpcloak.Session(
        preset=preset,
        timeout=int(timeout),
        without_cookie_jar=without_cookie_jar,
        retry=0,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
        **kwargs,
    )
    if header_order:
        session.set_header_order(ordered_header_names(api=api))
    return session


def browser_get(
    url: str,
    *,
    api: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
    preset: str = RECOMMENDED_HTTP_PRESET,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
    **header_overrides: str,
) -> httpcloak.Response:
    headers = browser_headers(api=api, **header_overrides)
    with open_session(
        api=api,
        preset=preset,
        timeout=timeout,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    ) as session:
        response = session.get(url, headers=headers, timeout=int(timeout))
        return response


def browser_post(
    url: str,
    *,
    json: dict[str, Any],
    api: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
    preset: str = RECOMMENDED_HTTP_PRESET,
    without_cookie_jar: bool | None = None,
    header_order: bool = True,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
    **header_overrides: str,
) -> httpcloak.Response:
    headers = {**browser_headers(api=api), **header_overrides}
    with open_session(
        api=api,
        preset=preset,
        timeout=timeout,
        without_cookie_jar=without_cookie_jar,
        header_order=header_order,
        tcp_proxy=tcp_proxy,
        udp_proxy=udp_proxy,
        local_address=local_address,
        http_version=http_version,
    ) as session:
        response = session.post(url, json=json, headers=headers, timeout=int(timeout))
        return response
