# StreamEmbed Platform

StreamEmbed provides master link resolution and video upload functionality for multiple providers.

## Providers

| Provider | Base URL |
|----------|----------|
| `seekstreaming` | https://seekstreaming.com |
| `streamp2p` | https://streamp2p.com |
| `player4me` | https://player4me.com |

## Installation

```python
from streamflow.platforms.streamembed import get_master_link, StreamembedClient
```

## get_master_link()

Get m3u8 streaming URL from video filecode.

```python
result = get_master_link(
    filecode: str,
    *,
    base_url: str | None = None,
    width: int = 2048,
    height: int = 1152,
    aes_key_hex: str | None = None,
    aes_iv_hex: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> StreamembedMasterLink
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | required | Video filecode/ID |
| `base_url` | str | None | Override site base URL |
| `width` | int | 2048 | Video width in pixels |
| `height` | int | 1152 | Video height in pixels |
| `aes_key_hex` | str | None | Custom AES key (hex) |
| `aes_iv_hex` | str | None | Custom AES IV (hex) |
| `timeout` | float | 30.0 | Request timeout (seconds) |
| `tcp_proxy` | str | None | HTTP CONNECT proxy URL |
| `udp_proxy` | str | None | SOCKS5 proxy URL |
| `local_address` | str | None | Local IP to bind |
| `http_version` | str | None | Force HTTP version |

### Returns

`StreamembedMasterLink` object with:
- `filecode` - Video filecode
- `title` - Video title
- `streaming_url` - m3u8 streaming URL
- `thumbnail` - Thumbnail URL
- `master_url` - Master URL
- `cf_url` - Cloudflare URL
- `swarm_id` - Swarm ID
- `torrent_trackers` - Torrent trackers list
- `ice_servers` - ICE servers list

### Examples

```python
# Basic usage
result = get_master_link("abc123")
print(result.streaming_url)

# With provider
result = get_master_link("abc123", provider="streamp2p")

# Custom dimensions
result = get_master_link("abc123", width=1920, height=1080)

# With proxy
result = get_master_link(
    "abc123",
    tcp_proxy="http://user:pass@proxy:8080"
)

# Force HTTP/3 (requires udp_proxy)
result = get_master_link(
    "abc123",
    udp_proxy="socks5://127.0.0.1:1080",
    http_version="HTTP/3"
)
```

## StreamembedClient

Client for StreamEmbed upload API.

```python
client = StreamembedClient(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
)
```

### Client Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | StreamEmbed API key |
| `base_url` | str | None | Override API base URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy URL |
| `udp_proxy` | str | None | UDP proxy URL |
| `local_address` | str | None | Local bind address |

### Client Methods

#### upload()

Start video upload from URL.

```python
upload = client.upload(
    url: str,
    *,
    name: str | None = None,
) -> AdvanceUploadResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | Video URL to upload |
| `name` | str | None | Optional video name |

**Returns:** `AdvanceUploadResponse` with `id` field.

#### get_task()

Get upload task status.

```python
status = client.get_task(task_id: str) -> AdvanceUploadDetailResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task_id` | str | required | Task ID from upload() |

**Returns:** `AdvanceUploadDetailResponse` with fields:
- `id` - Task ID
- `name` - Video name
- `status` - Status string
- `videos` - List of video URLs
- `updated_at` - Last update time
- `created_at` - Creation time

### Client Examples

```python
from streamflow.platforms.streamembed import StreamembedClient

client = StreamembedClient(api_key="YOUR_API_KEY")

# Start upload
upload = client.upload("https://example.com/video.mp4", name="My Video")
print(f"Task ID: {upload.id}")

# Check status
status = client.get_task(upload.id)
print(f"Status: {status.status}")
print(f"Videos: {status.videos}")

# With proxy
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://proxy:8080"
)
```

## Proxy Configuration

### Supported Proxy Schemes

| Scheme | Type | Example |
|--------|------|---------|
| `http://` | HTTP CONNECT | `http://user:pass@proxy:8080` |
| `https://` | HTTPS CONNECT | `https://proxy:8080` |
| `socks5://` | SOCKS5 | `socks5://127.0.0.1:1080` |
| `socks5h://` | SOCKS5H | `socks5h://127.0.0.1:1080` |
| `masque://` | MASQUE | `masque://proxy:8080` |

### HTTP Version

| Value | Description |
|-------|-------------|
| `"HTTP/1.1"` | Force HTTP/1.1 |
| `"HTTP/2"` | Force HTTP/2 |
| `"HTTP/3"` | Force HTTP/3 (requires `udp_proxy`) |

## Error Handling

```python
from streamflow.platforms.streamembed import (
    StreamembedAPIError,
    StreamembedClient,
    get_master_link,
)

# Handle API errors
try:
    result = get_master_link("invalid_id")
except StreamembedAPIError as e:
    print(f"API Error: {e}")

# Handle client errors
try:
    client = StreamembedClient(api_key="invalid")
    upload = client.upload("https://example.com/video.mp4")
except StreamembedAPIError as e:
    print(f"Upload failed: {e}")
```

## Constants

```python
from streamflow.platforms.streamembed.constants import (
    DEFAULT_API_BASE_URL,  # "https://seekstreaming.com/api/v1"
    DEFAULT_SITE_URL,      # "https://seekstreaming.com"
    DEFAULT_TIMEOUT,       # 30.0
    AES_KEY_HEX,           # AES encryption key
    AES_IV_HEX,            # AES IV
    DEFAULT_VIDEO_WIDTH,   # 2048
    DEFAULT_VIDEO_HEIGHT,  # 1152
)

# Functions
from streamflow.platforms.streamembed.constants import (
    base_url(),
    site_url(),
    api_url(endpoint),
    resolve_base_url(base_url),
    resolve_site_base_url(site_base_url),
    advance_upload_endpoint(),
    advance_upload_detail_endpoint(task_id),
    embed_url(filecode),
)
```