# StreamEmbed Platform

StreamEmbed provides master link resolution and video upload functionality for multiple providers.

## Providers

All three providers share the same `/api/v1` API surface; only the host
differs. The library's default points at `seekstreaming.com`.

| Provider | Site URL *(player / master link / embed)* | API Base URL *(JSON: upload, status)* |
|----------|-------------------------------------------|---------------------------------------|
| `seekstreaming` | `https://seekstreaming.com` | `https://seekstreaming.com/api/v1` *(default)* |
| `streamp2p` | `https://streamp2p.com` | `https://streamp2p.com/api/v1` |
| `player4me` | `https://player4me.com` | `https://player4me.com/api/v1` |

**Which URL goes where:**

| You're calling… | Pass this URL | Parameter |
|-----------------|---------------|-----------|
| `get_master_link(filecode, …)` — get the `m3u8` streaming URL | **Site URL** (e.g. `https://seekstreaming.com`) | `base_url=` *(on this function, `base_url` is the site URL)* |
| `embed_url(filecode, …)` — build a `/embed/{filecode}` page link | **Site URL** | `site_base_url=` |
| `StreamembedClient(...)` / `advance_upload(...)` / `get_upload_task(...)` | **API Base URL** (e.g. `https://seekstreaming.com/api/v1`) | `base_url=` |

> The Site URL is what your viewer's browser hits to watch the video
> (player page, embed page, the master `.m3u8`). The API Base URL is
> only used by your server to talk to the upload/management API.

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
- `swarm_id` - Swarm ID
- `torrent_trackers` - Torrent trackers list
- `ice_servers` - ICE servers list
- `raw` - Full API response dict (for debugging)

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
    auth_header: str = "api-token",
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
| `auth_header` | str | `"api-token"` | HTTP header name carrying the API key. See [Authentication](#authentication). |

### Authentication

By default, `StreamembedClient` (and the underlying `advance_upload` /
`get_upload_task` functions) send the API key in the **`api-token`**
HTTP header — this is what `seekstreaming.com`, `streamp2p.com` and
`player4me.com` expect:

```
api-token: YOUR_API_KEY
```

> **Note:** Earlier StreamFlow releases sent `Authorization: Bearer ...`,
> which caused `401 Invalid credentials` against these providers. The
> default is now `api-token`.

If you ever talk to a deployment that uses a different scheme (for
example, a fork that expects the old Bearer header), override the
header name with the `auth_header` parameter:

```python
# Default — sends "api-token: YOUR_API_KEY"
client = StreamembedClient(api_key="YOUR_API_KEY")

# Custom header name
client = StreamembedClient(api_key="YOUR_API_KEY", auth_header="X-Api-Key")

# Bearer scheme — prepend "Bearer " to the key yourself
client = StreamembedClient(
    api_key="Bearer YOUR_API_KEY",
    auth_header="Authorization",
)
```

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