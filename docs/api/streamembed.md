# StreamEmbed API Reference

## Functions

### get_master_link()

```python
from streamflow.platforms.streamembed import get_master_link

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

Get m3u8 streaming URL from video filecode.

**Parameters:**

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

**Returns:** `StreamembedMasterLink` object.

**Raises:** `StreamembedAPIError`

### advance_upload()

```python
from streamflow.platforms.streamembed import advance_upload

response = advance_upload(
    api_key: str,
    url: str,
    *,
    name: str | None = None,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> AdvanceUploadResponse
```

Create advance upload task.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `url` | str | required | Video URL |
| `name` | str | None | Video name |
| `base_url` | str | None | Override API base URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `AdvanceUploadResponse`

### get_upload_task()

```python
from streamflow.platforms.streamembed import get_upload_task

response = get_upload_task(
    api_key: str,
    task_id: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> AdvanceUploadDetailResponse
```

Get upload task status.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `task_id` | str | required | Task ID |
| `base_url` | str | None | Override API base URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `AdvanceUploadDetailResponse`

## Client

### StreamembedClient

```python
from streamflow.platforms.streamembed import StreamembedClient

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

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | StreamEmbed API key |
| `base_url` | str | None | Override API base URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy URL |
| `udp_proxy` | str | None | UDP proxy URL |
| `local_address` | str | None | Local bind address |

#### Methods

##### upload()

```python
response = client.upload(
    url: str,
    *,
    name: str | None = None,
) -> AdvanceUploadResponse
```

##### get_task()

```python
response = client.get_task(task_id: str) -> AdvanceUploadDetailResponse
```

## Models

### StreamembedMasterLink

```python
@dataclass
class StreamembedMasterLink:
    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None
    master_url: str | None = None
    cf_url: str | None = None
    swarm_id: str | None = None
    torrent_trackers: list[str] | None = None
    ice_servers: list[dict] | None = None
```

### AdvanceUploadResponse

```python
@dataclass
class AdvanceUploadResponse:
    id: str
```

### AdvanceUploadDetailResponse

```python
@dataclass
class AdvanceUploadDetailResponse:
    id: str
    name: str | None
    status: str
    videos: list[str]
    updated_at: str | None
    created_at: str | None
```

### VideoInfo

```python
@dataclass
class VideoInfo:
    video_id: str
```

### StreamembedAPIError

```python
@dataclass
class StreamembedAPIError(Exception):
    message: str
    status_code: int | None = None
```

## Constants

```python
from streamflow.platforms.streamembed import (
    DEFAULT_API_BASE_URL,  # "https://seekstreaming.com/api/v1"
    DEFAULT_SITE_URL,       # "https://seekstreaming.com"
    AES_KEY_HEX,            # AES encryption key hex
    AES_IV_HEX,             # AES IV hex
    DEFAULT_TIMEOUT,        # 30.0
    DEFAULT_VIDEO_WIDTH,    # 2048
    DEFAULT_VIDEO_HEIGHT,   # 1152
)
```

## Endpoint Functions

```python
from streamflow.platforms.streamembed.constants import (
    base_url(),                    # Get current API base URL
    site_url(),                    # Get current site URL
    api_url(endpoint),             # Build full API URL
    resolve_base_url(base_url),    # Resolve API base URL
    resolve_site_base_url(url),    # Resolve site base URL
    advance_upload_endpoint(),     # /api/v1/video/advance-upload
    advance_upload_detail_endpoint(task_id),  # /api/v1/video/advance-upload/{id}
    embed_url(filecode),           # Build embed URL
)
```