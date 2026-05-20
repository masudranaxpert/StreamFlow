"""Streamembed help functions."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from streamflow.platforms.streamembed.constants import (
    AES_KEY_HEX,
    AES_IV_HEX,
    base_url,
    resolve_base_url,
    site_url,
    advance_upload_endpoint,
    advance_upload_detail_endpoint,
)


PLATFORM_NAME = "streamembed"
PLATFORM_TITLE = "StreamEmbed Platform"


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

Set in `StreamembedClient` constructor or per-request.

`http_version` options: `"HTTP/1.1"`, `"HTTP/2"`, `"HTTP/3"` (requires udp_proxy)
"""


def build_help_text(api_key: str | None = None, provider: str | None = None, show_proxy: bool = False) -> str:
    """Build formatted help text with Rich styling."""
    
    provider = provider or "seekstreaming"
    
    # Provider URL mapping
    provider_urls = {
        "seekstreaming": "https://seekstreaming.com",
        "streamp2p": "https://streamp2p.com",
        "player4me": "https://player4me.com",
    }
    
    provider_site_url = provider_urls.get(provider, provider_urls["seekstreaming"])
    api_base = resolve_base_url(None)
    
    help_text = f"""# StreamEmbed Platform

Video upload and streaming via master link.

**Provider:** {provider}

---

## Supported Providers

| Provider | URL |
|----------|-----|
| seekstreaming | https://seekstreaming.com |
| streamp2p | https://streamp2p.com |
| player4me | https://player4me.com |

---

## Master Link (get streaming URL)

Get streaming URL from video filecode.

```
GET {provider_site_url}/api/v1/master/<video_id>
```

Decrypt AES-128-CBC encrypted response to get m3u8 URL.

```python
from streamflow.platforms.streamembed import get_master_link, StreamembedMasterLink

# Simple call:
result = get_master_link("VIDEO_ID")

# With provider:
result = get_master_link("VIDEO_ID", provider="{provider}")

# With custom base URL:
result = get_master_link("VIDEO_ID", base_url="https://seekstreaming.com")

# Returns StreamembedMasterLink with:
#   .filecode       - video filecode
#   .title          - video title or None
#   .streaming_url  - m3u8 streaming URL
#   .thumbnail      - thumbnail URL or None
```

**Master Link Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `video_id` | required | Video filecode |
| `--provider` | `{provider}` | Provider name |
| `--base-url` | auto | Override site URL |
| `--width` | 2048 | Video width (pixels) |
| `--height` | 1152 | Video height (pixels) |
| `--timeout` | 30 | Request timeout (seconds) |

---

## Advance Upload

Remote upload with progress tracking.

```
GET {advance_upload_endpoint()}?key=KEY&url=FILE_URL
POST {advance_upload_endpoint()}?key=KEY&url=FILE_URL&name=VIDEO_NAME
```

```python
from streamflow.platforms.streamembed import StreamembedClient

client = StreamembedClient(api_key="YOUR_API_KEY")

# Start upload:
upload = client.upload("https://example.com/video.mp4", name="MyVideo")
# Returns: (task_id, filecode)

# Check status:
status = client.get_task(upload.task_id)
# Returns: AdvanceUploadDetailResponse
```

**Upload Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--api-key` | required | Your StreamEmbed API key |
| `--url` | required | Video URL to upload |
| `--name` | auto | Optional video name |
| `--base-url` | auto | Override API base URL |
| `--timeout` | 120 | Request timeout (seconds) |

---

## Usage

```python
from streamflow.platforms.streamembed import StreamembedClient

client = StreamembedClient(api_key="YOUR_API_KEY")

# Upload video:
upload = client.upload("https://example.com/video.mp4", name="MyVideo")
task_id, filecode = upload.task_id, upload.filecode

# Check upload status:
status = client.get_task(task_id)
print(f"Status: {{status.status}}, Progress: {{status.progress}}%")

# Master link:
from streamflow.platforms.streamembed import get_master_link
result = get_master_link(filecode, provider="{provider}")
print(f"Streaming URL: {{result.streaming_url}}")
```

---

**Optional:**
- `base_url` - API base (default: `{api_base}`)
- `site_url` - Site base (default: `{provider_site_url}`)

**Supports proxy:** `tcp_proxy`, `udp_proxy`, `local_address`, `http_version`
"""
    
    if show_proxy:
        help_text += _proxy_example
    
    return help_text


def show_help(api_key: str | None = None, provider: str | None = None, show_proxy: bool = False) -> None:
    """Print formatted help to console."""
    console = Console()
    md = Markdown(build_help_text(api_key, provider, show_proxy), code_theme="monokai")
    console.print(Panel(md, title=f"[bold cyan]StreamEmbed[/] - {provider or 'seekstreaming'}", border_style="cyan"))


def get_help(api_key: str | None = None, provider: str | None = None, show_proxy: bool = False) -> str:
    """Get formatted help text as string."""
    return build_help_text(api_key, provider, show_proxy)
