"""Byse platform help."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from streamflow.platforms.byse.constants import (
    account_stats_endpoint,
    DEFAULT_BASE_URL,
    file_delete_endpoint,
    file_list_endpoint,
    remote_add_endpoint,
)

PLATFORM_NAME = "byse"
PLATFORM_TITLE = "Byse"

HELP_TEMPLATE = """# Byse

Video upload, file management, and account stats.

---

## Account Stats

```
GET {account_stats_endpoint}?key=KEY&last=7
```
- **Optional:** `last` (days, default 7)
- **Returns:** `result[]` with downloads, views, profits, referrals

---

## Remote Add (queue upload)

```
GET {remote_add_endpoint}?key=KEY&url=FILE_URL
```
- **Required:** `url` (direct video file URL)
- **Returns:** `result.filecode`

---

## File List

```
GET {file_list_endpoint}?key=KEY&page=1&per_page=20
```
- **Optional:** `fld_id`, `title`, `created`, `public`
- **Returns:** `result[].filecode`, `name`, `views`, `length`, `uploaded`

---

## File Delete

```
GET {file_delete_endpoint}?key=KEY&file_code=CODE
```
- **Required:** `file_code`

---

## Master Link (get streaming URL)

```python
from streamflow.platforms.byse import get_master_link, ByseMasterLink

# Simple call:
result = get_master_link("FILECODE")

# With challenge auth (viewer_id, device_id, token, fingerprint):
result = get_master_link(
    "FILECODE",
    viewer_id="VIEWER_ID",   # optional
    device_id="DEVICE_ID",   # optional
    token="TOKEN",           # optional
    fingerprint="FINGERPRINT",  # optional
)

# Returns ByseMasterLink with:
#   .filecode      - file code
#   .title         - video title or None
#   .streaming_url - m3u8 streaming URL
#   .thumbnail     - thumbnail URL or None
```

---

## Usage

```python
from streamflow.platforms.byse import ByseClient

client = ByseClient(api_key="YOUR_API_KEY")
upload = client.add_remote("https://example.com/video.mp4")
stats = client.account_stats(last=30)
```

---

**Optional:**
- `base_url` - API base (default: https://api.byse.sx)
- `site_base_url` - Site base (default: {site_base})
"""


def build_help_text(
    base_url: str | None = None,
    site_base_url: str | None = None,
) -> str:
    """Build help text with optional base URL."""
    title = PLATFORM_TITLE
    account_stats = account_stats_endpoint(base_url)
    remote_add = remote_add_endpoint(base_url)
    file_list = file_list_endpoint(base_url)
    file_delete = file_delete_endpoint(base_url)
    site_base = site_base_url or DEFAULT_BASE_URL

    return HELP_TEMPLATE.format(
        title=title,
        account_stats_endpoint=account_stats,
        remote_add_endpoint=remote_add,
        file_list_endpoint=file_list,
        file_delete_endpoint=file_delete,
        site_base=site_base,
    )


def get_help(
    base_url: str | None = None,
    site_base_url: str | None = None,
) -> str:
    """Get help text."""
    return build_help_text(base_url=base_url, site_base_url=site_base_url)


def show_help(
    base_url: str | None = None,
    site_base_url: str | None = None,
) -> None:
    """Print help text with rich formatting."""
    console = Console()
    md = Markdown(build_help_text(base_url=base_url, site_base_url=site_base_url), code_theme="monokai")
    console.print(Panel(md, title="[bold magenta]Byse[/]", border_style="magenta"))