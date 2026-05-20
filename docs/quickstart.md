# Quick Start

## Basic Usage

### Get Master Link

Get streaming URL from video filecode:

```python
from streamflow.platforms.streamembed import get_master_link

# Simple usage
result = get_master_link("abc123", provider="seekstreaming")
print(f"Streaming URL: {result.streaming_url}")
print(f"Title: {result.title}")
print(f"Thumbnail: {result.thumbnail}")
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | required | Video filecode/ID |
| `provider` | str | "seekstreaming" | Provider name |
| `base_url` | str | auto | Override site URL |
| `width` | int | 2048 | Video width |
| `height` | int | 1152 | Video height |
| `timeout` | float | 30 | Request timeout |

### Upload Video

Upload video from URL with API key:

```python
from streamflow.platforms.streamembed import StreamembedClient

client = StreamembedClient(api_key="YOUR_API_KEY")

# Start upload
upload = client.upload("https://example.com/video.mp4", name="My Video")
print(f"Task ID: {upload.id}")

# Check status
status = client.get_task(upload.id)
print(f"Status: {status.status}")
print(f"Progress: {status.videos}")
```

**StreamembedClient Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `base_url` | str | auto | Override API base URL |
| `timeout` | float | 30 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy URL |
| `udp_proxy` | str | None | UDP proxy URL |
| `local_address` | str | None | Bind to local address |

### VOE Platform

```python
from streamflow.platforms.voe import VOEClient

client = VOEClient(api_key="YOUR_API_KEY")

# Get account stats
stats = client.get_account_stats()
print(f"Storage: {stats.storage_used}")

# List files
files = client.list_files()
for f in files:
    print(f"{f.name} - {f.size}")
```

## CLI Usage

```bash
# Show all platforms
python -m streamflow all

# Show streamembed with provider
python -m streamflow streamembed seekstreaming

# Show voe platform
python -m streamflow voe
```

## Error Handling

```python
from streamflow.platforms.streamembed import StreamembedAPIError

try:
    result = get_master_link("invalid_id")
except StreamembedAPIError as e:
    print(f"API Error: {e}")
```