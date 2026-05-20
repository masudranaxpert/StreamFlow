from __future__ import annotations

DEFAULT_API_BASE_URL = "https://api.vidara.so/v1"
DEFAULT_SITE_BASE_URL = "https://vidara.so"
UPLOAD_PATH = "/upload/url"
UPLOAD_SERVER_PATH = "/upload/server"
STREAM_PATH = "/api/stream"
STREAM_PRESET = "firefox-148"
STREAM_DEVICE_DEFAULT = "web"


def resolve_base_url(base_url: str | None = None) -> str:
    return (base_url or DEFAULT_API_BASE_URL).rstrip("/")


def resolve_site_base_url(site_base_url: str | None = None) -> str:
    return (site_base_url or DEFAULT_SITE_BASE_URL).rstrip("/")


def upload_endpoint(base_url: str | None = None) -> str:
    return f"{resolve_base_url(base_url)}{UPLOAD_PATH}"


def upload_server_endpoint(base_url: str | None = None) -> str:
    return f"{resolve_base_url(base_url)}{UPLOAD_SERVER_PATH}"


def stream_endpoint(site_base_url: str | None = None) -> str:
    return f"{resolve_site_base_url(site_base_url)}{STREAM_PATH}"


def embed_page_url(filecode: str, site_base_url: str | None = None) -> str:
    return f"{resolve_site_base_url(site_base_url)}/e/{filecode}"
