"""Streamwish API endpoints."""

from urllib.parse import urljoin

DEFAULT_API_BASE_URL = "https://seekstreaming.com/api/v1"
DEFAULT_SITE_URL = "https://seekstreaming.com"
DEFAULT_TIMEOUT = 30.0

AES_KEY_HEX = "6b69656d7469656e6d75613931316361"
AES_IV_HEX = "313233343536373839306f6975797472"

DEFAULT_VIDEO_WIDTH = 2048
DEFAULT_VIDEO_HEIGHT = 1152


def base_url() -> str:
    """Get current API base URL."""
    return DEFAULT_API_BASE_URL


def site_url() -> str:
    """Get current site URL."""
    return DEFAULT_SITE_URL


def api_url(endpoint: str, base_url: str | None = None) -> str:
    """Build full API URL."""
    base = base_url or DEFAULT_API_BASE_URL
    clean_endpoint = endpoint.lstrip("/")
    return f"{base}/{clean_endpoint}"


def resolve_base_url(base_url: str | None = None) -> str:
    """Resolve API base URL with default."""
    return base_url or DEFAULT_API_BASE_URL


def resolve_site_base_url(site_base_url: str | None = None) -> str:
    """Resolve site base URL with default."""
    return site_base_url or DEFAULT_SITE_URL


# Advance upload endpoints
def advance_upload_endpoint(base_url: str | None = None) -> str:
    """POST /api/v1/video/advance-upload - Create upload task."""
    return api_url("/video/advance-upload", base_url)


def advance_upload_detail_endpoint(task_id: str, base_url: str | None = None) -> str:
    """GET /api/v1/video/advance-upload/{id} - Get task detail."""
    return api_url(f"/video/advance-upload/{task_id}", base_url)


# Embed URL
def embed_url(filecode: str, site_base_url: str | None = None) -> str:
    """Build embed URL for a file."""
    base = resolve_site_base_url(site_base_url)
    return f"{base}/embed/{filecode}"