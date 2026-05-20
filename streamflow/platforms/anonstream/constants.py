"""Anonstream API endpoints."""

from urllib.parse import urljoin

DEFAULT_BASE_URL = "https://anonstream.co"


def api_url(endpoint: str, base_url: str | None = None) -> str:
    """Build full API URL."""
    base = base_url or DEFAULT_BASE_URL
    return urljoin(base + "/", f"api/{endpoint.lstrip('/')}")


def upload_url_endpoint(base_url: str | None = None) -> str:
    return api_url("/upload/url", base_url)


def account_stats_endpoint(base_url: str | None = None) -> str:
    return api_url("/account/stats", base_url)


def file_list_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/list", base_url)


def file_delete_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/delete", base_url)


def resolve_base_url(base_url: str | None = None) -> str:
    """Resolve base URL with default."""
    return base_url or DEFAULT_BASE_URL