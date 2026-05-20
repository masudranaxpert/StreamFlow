# Vidara

Video upload and HLS master link resolution for Vidara platform.

## Installation

```bash
pip install streamflow
```

## Quick Example

```python
from streamflow.platforms.vidara import VidaraClient, get_master_link

# Initialize client
client = VidaraClient(api_key="YOUR_API_KEY")

# Get upload server
server = client.upload_server()
print(f"Upload server: {server.result.upload_server}")

# Remote upload
upload = client.upload("https://example.com/video.mp4")
print(f"Uploaded: {upload.data.filecode}")

# Get master link (m3u8 streaming URL)
stream = get_master_link("FILECODE")
print(f"Stream URL: {stream.streaming_url}")
```

## VidaraClient

### Constructor

```python
from streamflow.platforms.vidara import VidaraClient

client = VidaraClient(
    api_key="YOUR_API_KEY",
    base_url=None,
    site_base_url=None,
    tcp_proxy=None,
    udp_proxy=None,
    local_address=None,
    http_version=None
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | **Required** | Your Vidara API key |
| `base_url` | str | `None` | API base URL |
| `site_base_url` | str | `None` | Site base URL |
| `tcp_proxy` | str | `None` | HTTP CONNECT proxy URL |
| `udp_proxy` | str | `None` | SOCKS5 proxy URL |
| `local_address` | str | `None` | Bind to specific IP |
| `http_version` | str | `None` | Force HTTP version (HTTP/1.1, HTTP/2, HTTP/3) |

### Methods

#### `upload_server()`

Get an upload server URL.

```python
result = client.upload_server()
print(result.result.upload_server)
```

**Returns:** Upload server URL

#### `upload(url, **kwargs)`

Upload a video from a remote URL.

```python
result = client.upload("https://example.com/video.mp4")
print(result.data.filecode)
print(result.data.title)
print(result.data.size)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | **Required** | Direct HTTPS file link |

!!! warning
    Google Drive links are **not supported**.

**Returns:** Upload result with `data.filecode`, `data.title`, `data.size`

#### `master_link(filecode, device="web")`

Get the HLS master link for a file.

```python
stream = client.master_link("FILECODE")
print(stream.streaming_url)
print(stream.title)
print(stream.thumbnail)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | **Required** | The file code |
| `device` | str | `"web"` | Device type |

**Returns:** Master link object with `.streaming_url`, `.title`, `.thumbnail`, `.subtitles`

#### `embed_url(filecode)`

Get the embed URL for a file.

```python
embed = client.embed_url("FILECODE")
print(embed)
# https://vidara.so/e/FILECODE
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | **Required** | The file code |

**Returns:** Embed URL string

## get_master_link()

Standalone function to get master link.

```python
from streamflow.platforms.vidara import get_master_link

stream = get_master_link("FILECODE")
print(stream.streaming_url)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | **Required** | The file code |
| `device` | str | `"web"` | Device type |
| `site_base_url` | str | `None` | Custom site base URL |
| `tcp_proxy` | str | `None` | HTTP CONNECT proxy |
| `udp_proxy` | str | `None` | SOCKS5 proxy |
| `local_address` | str | `None` | Bind to specific IP |
| `http_version` | str | `None` | Force HTTP version |

**Returns:** Master link object

## VidaraMasterLink Model

```python
from streamflow.platforms.vidara import VidaraMasterLink

class VidaraMasterLink:
    filecode: str
    title: str
    streaming_url: str  # .m3u8 URL
    thumbnail: str | None
    subtitles: list | None
```

## Proxy Support

Vidara supports full proxy configuration:

```python
from streamflow.platforms.vidara import VidaraClient

# With HTTP proxy
client = VidaraClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://user:pass@proxy.example.com:8080"
)

# With SOCKS5 proxy
client = VidaraClient(
    api_key="YOUR_API_KEY",
    udp_proxy="socks5://127.0.0.1:1080"
)

# Force HTTP/3 (requires udp_proxy)
client = VidaraClient(
    api_key="YOUR_API_KEY",
    udp_proxy="socks5://proxy.example.com:1080",
    http_version="HTTP/3"
)
```

### Proxy URL Formats

| Type | Format | Example |
|------|--------|---------|
| HTTP CONNECT | `http://host:port` | `http://proxy.example.com:8080` |
| HTTP Auth | `http://user:pass@host:port` | `http://user:pass@proxy.com:8080` |
| SOCKS5 | `socks5://host:port` | `socks5://127.0.0.1:1080` |
| SOCKS5 DNS | `socks5h://host:port` | `socks5h://127.0.0.1:1080` |

### HTTP Version Options

| Value | Description |
|-------|-------------|
| `"HTTP/1.1"` | Force HTTP/1.1 |
| `"HTTP/2"` | Force HTTP/2 |
| `"HTTP/3"` | Force HTTP/3 (requires `udp_proxy`) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload/remote` | GET | Remote URL upload |
| `/api/upload/server` | GET | Get upload server |
| `/api/stream/master` | POST | Get HLS master link |

## Error Handling

```python
from streamflow.platforms.vidara import VidaraClient, get_master_link

client = VidaraClient(api_key="YOUR_API_KEY")

try:
    upload = client.upload("https://example.com/video.mp4")
    print(f"Uploaded: {upload.data.filecode}")
except Exception as e:
    print(f"Upload error: {e}")

try:
    stream = get_master_link("FILECODE")
    print(f"Stream: {stream.streaming_url}")
except Exception as e:
    print(f"Master link error: {e}")
```

## Complete Example

```python
from streamflow.platforms.vidara import VidaraClient, get_master_link

# Initialize with proxy
client = VidaraClient(
    api_key="YOUR_API_KEY",
    udp_proxy="socks5://127.0.0.1:1080",
    http_version="HTTP/3"
)

# Get upload server
server = client.upload_server()

# Upload video
upload = client.upload("https://example.com/video.mp4")
filecode = upload.data.filecode
print(f"Uploaded: {filecode} ({upload.data.title})")

# Get streaming URL
stream = get_master_link(filecode)
print(f"Watch: {stream.streaming_url}")

# Get embed URL
print(f"Embed: {client.embed_url(filecode)}")
```