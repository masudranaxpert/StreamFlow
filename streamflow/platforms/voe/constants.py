from __future__ import annotations

DEFAULT_API_BASE_URL = "https://voe.sx/api"
DEFAULT_SITE_BASE_URL = "https://voe.sx"
UPLOAD_URL_PATH = "/upload/url"
UPLOAD_SERVER_PATH = "/upload/server"
ACCOUNT_STATS_PATH = "/account/stats"
FILE_LIST_PATH = "/file/list"
FILE_DELETE_PATH = "/file/delete"
FILE_PAGE_PATH = "/e/{filecode}"


def resolve_base_url(base_url: str | None = None) -> str:
    return (base_url or DEFAULT_API_BASE_URL).rstrip("/")


def resolve_site_base_url(site_base_url: str | None = None) -> str:
    return (site_base_url or DEFAULT_SITE_BASE_URL).rstrip("/")


def api_url(path: str, base_url: str | None = None) -> str:
    return f"{resolve_base_url(base_url)}{path}"


def file_page_url(filecode: str, site_base_url: str | None = None) -> str:
    """Get the VOE embed/video page URL for a filecode."""
    site = resolve_site_base_url(site_base_url)
    return f"{site}/e/{filecode}"


def upload_url_endpoint(base_url: str | None = None) -> str:
    return api_url("/upload/url", base_url)


def upload_server_endpoint(base_url: str | None = None) -> str:
    return api_url("/upload/server", base_url)


def account_stats_endpoint(base_url: str | None = None) -> str:
    return api_url("/account/stats", base_url)


def file_list_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/list", base_url)


def file_delete_endpoint(base_url: str | None = None) -> str:
    return api_url("/file/delete", base_url)
