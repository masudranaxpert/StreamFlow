from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from streamflow.platforms.vidara.constants import (
    resolve_base_url,
    resolve_site_base_url,
    stream_endpoint,
    upload_endpoint,
    upload_server_endpoint,
)

PLATFORM_NAME = "vidara"
PLATFORM_TITLE = "Vidara"

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

Set in `VidaraClient` constructor or per-request.

`http_version` options: `"HTTP/1.1"`, `"HTTP/2"`, `"HTTP/3"` (requires udp_proxy)
"""


def build_help_text(
    base_url: str | None = None,
    site_base_url: str | None = None,
    show_proxy: bool = False,
) -> str:
    upload_url = upload_endpoint(base_url)
    upload_server_url = upload_server_endpoint(base_url)
    stream_url = stream_endpoint(site_base_url)
    api_base = resolve_base_url(base_url)
    site_base = resolve_site_base_url(site_base_url)
    help_text = f"""# Vidara

Upload videos and fetch HLS master links.

---

## Upload (remote URL)

```
GET {upload_url}?api_key=KEY&url=VIDEO_URL
```
- **Required:** `api_key`, `url` (direct HTTPS file link)
- **Returns:** `data.filecode`, `data.title`, `data.size`
- ❌ **Google Drive links are not supported.**

---

## Upload server

```
GET {upload_server_url}?api_key=KEY
```
- **Required:** `api_key`
- **Returns:** `result.upload_server`

---

## Master link (HLS)

```
POST {stream_url}
```
- **Body:** `{{"filecode": "FILECODE", "device": "web"}}`
- **Returns:** `streaming_url` (`.m3u8`), `title`, `thumbnail`, `subtitles`

---

## Usage

```python
from streamflow.platforms.vidara import VidaraClient, get_master_link

client = VidaraClient(api_key="YOUR_API_KEY")
server = client.upload_server()
print(server.result.upload_server)

upload = client.upload("https://example.com/video.mp4")
print(upload.data.filecode)

stream = client.master_link("FILECODE")
print(stream.streaming_url)

stream = get_master_link("FILECODE")
```

---

## Embed URL

```python
client = VidaraClient(api_key="YOUR_API_KEY")
print(client.embed_url("FILECODE"))
# https://vidara.so/e/FILECODE
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


def show_help(
    base_url: str | None = None,
    site_base_url: str | None = None,
    show_proxy: bool = False,
) -> None:
    console = Console()
    md = Markdown(build_help_text(base_url, site_base_url, show_proxy), code_theme="monokai")
    console.print(Panel(md, title="[bold green]Vidara[/]", border_style="green"))


def get_help(
    base_url: str | None = None,
    site_base_url: str | None = None,
    show_proxy: bool = False,
) -> str:
    return build_help_text(base_url, site_base_url, show_proxy)
