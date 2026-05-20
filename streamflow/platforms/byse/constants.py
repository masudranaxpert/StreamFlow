"""Byse API endpoints."""

from urllib.parse import urljoin

DEFAULT_BASE_URL = "https://api.byse.sx"


def api_url(endpoint: str, base_url: str | None = None) -> str:
    """Build full API URL."""
    base = base_url or DEFAULT_BASE_URL
    # endpoint like "/account/stats" -> base + endpoint (no /remote prefix)
    clean_endpoint = endpoint.lstrip("/")
    return f"{base}/{clean_endpoint}"


def account_stats_endpoint(base_url: str | None = None) -> str:
    return api_url("/account/stats", base_url)


def remote_add_endpoint(base_url: str | None = None) -> str:
    return api_url("/remote/add", base_url)


def file_list_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/list", base_url)


def file_delete_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/delete", base_url)


def resolve_base_url(base_url: str | None = None) -> str:
    """Resolve base URL with default."""
    return base_url or DEFAULT_BASE_URL