from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from streamflow.platforms.voe.constants import (
    account_stats_endpoint,
    file_delete_endpoint,
    file_list_endpoint,
    resolve_base_url,
    resolve_site_base_url,
    upload_server_endpoint,
    upload_url_endpoint,
    file_page_url,
)

PLATFORM_NAME = "voe"
PLATFORM_TITLE = "VOE"

_proxy_example = """
## Proxy Configuration (split-config)

| Parameter | Example | Description |
|-----------|---------|-------------|
| `tcp_proxy` | `http://user:pass@proxy:8080` | HTTP CONNECT proxy |
| `udp_proxy` | `socks5://127.0.0.1:1080` | SOCKS5 proxy |
| `local_address` | `192.168.1.100` | Bind to specific interface |
| `http_version` | `HTTP/3` | Force HTTP/3 (requires udp_proxy) |

**Supported proxy schemes:**
- `http://`, `https://` - HTTP CONNECT proxy
- `socks5://`, `socks5h://` - SOCKS5 proxy
- `masque://` - MASQUE proxy (for HTTP/3)

Set in `VoeClient` constructor or per-request.

`http_version` options: `"HTTP/1.1"`, `"HTTP/2"`, `"HTTP/3"` (requires udp_proxy)
"""


def build_help_text(base_url: str | None = None, site_base_url: str | None = None, show_proxy: bool = False) -> str:
    upload_url = upload_url_endpoint(base_url)
    upload_server_url = upload_server_endpoint(base_url)
    stats_url = account_stats_endpoint(base_url)
    list_url = file_list_endpoint(base_url)
    delete_url = file_delete_endpoint(base_url)
    api_base = resolve_base_url(base_url)
    site_base = resolve_site_base_url(site_base_url)
    embed_url = file_page_url("FILECODE", site_base_url)
    help_text = f"""# VOE

Remote upload, file management, and account stats.

---

## Upload URL (remote queue)

```
GET/POST {upload_url}?key=KEY&url=FILE_URL
```
- **Optional:** `folder_id`
- **Returns:** `result.file_code`, `result.queueID`
- ✅ **Google Drive links are supported.**

---

## Upload server

```
GET {upload_server_url}?key=KEY
```
- **Returns:** `result` (upload server URL string)

---

## Account stats (last 32 days)

```
GET {stats_url}?key=KEY
```
- **Returns:** `result` (per-day stats map)

---

## File list

```
GET {list_url}?key=KEY&page=1&per_page=20&fld_id=0
```
- **Optional:** `created`, `name`, `preview`
- **Returns:** `result.data[].filecode`, `name`, `title`, ...

---

## File delete

```
GET {delete_url}?key=KEY&del_code=CODE
```
- `del_code`: one code or comma-separated list

---

## Purge all

Delete every file in account/folder:
```python
client.purge_all()
```
Lists all pages then deletes in batches.

---

## Master link (get streaming URL)

```
GET {embed_url}
```
Extract encrypted source from page, decrypt to get m3u8 URL.

```python
from streamflow.platforms.voe import get_master_link, VoeMasterLink

# Simple call:
result = get_master_link("FILECODE")

# With site_base_url:
result = get_master_link("FILECODE", site_base_url="https://voe.sx")

# Returns VoeMasterLink with:
#   .streaming_url - m3u8 streaming URL
#   .title         - video title or None
```

---

## Usage

```python
from streamflow.platforms.voe import VoeClient

client = VoeClient(api_key="YOUR_API_KEY")
server = client.upload_server()
upload = client.upload("https://example.com/video.mp4")
files = client.list_files(page=1, per_page=20)
client.delete_files("abc123")
result = client.purge_all()
```

---

**Optional:**
- `base_url` - API base (default: `{api_base}`)
- `site_base_url` - Site base (default: `{site_base}`)

**Supports proxy:** `tcp_proxy`, `udp_proxy`, `local_address`, `http_version`
"""
    if show_proxy:
        help_text += _proxy_example
    return help_text


def show_help(base_url: str | None = None, site_base_url: str | None = None, show_proxy: bool = False) -> None:
    console = Console()
    md = Markdown(build_help_text(base_url, site_base_url, show_proxy), code_theme="monokai")
    console.print(Panel(md, title="[bold yellow]VOE[/]", border_style="yellow"))


def get_help(base_url: str | None = None, site_base_url: str | None = None, show_proxy: bool = False) -> str:
    return build_help_text(base_url, site_base_url, show_proxy)
