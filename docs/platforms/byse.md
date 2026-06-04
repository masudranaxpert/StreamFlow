# Byse

Video upload, file management, account stats, and master link resolution for Byse platform.

## Default URLs

| URL | Value | What it's for |
|-----|-------|---------------|
| **API Base URL** (`base_url=` on `ByseClient`) | `https://api.byse.sx` | JSON API: `account_stats`, `add_remote`, `list_files`, `delete_file`. |
| **Site URL** (`base_url=` on `get_master_link`) | `https://byse.sx` | Master link endpoint and the player / embed page. This is where viewers actually watch. |

> Byse splits the API and the site onto **different hosts**:
> `api.byse.sx` serves only the JSON API, while `byse.sx` serves the
> master link and the player. Don't aim `ByseClient(base_url=...)` at
> `byse.sx` or `get_master_link(base_url=...)` at `api.byse.sx` — the
> defaults are already correct.

## Installation

```bash
pip install streamflow
```

## Quick Example

```python
from streamflow.platforms.byse import ByseClient, get_master_link

# Initialize client
client = ByseClient(api_key="YOUR_API_KEY")

# Queue remote upload
upload = client.add_remote("https://example.com/video.mp4")
print(f"Queued: {upload.result.filecode}")

# Get master link (m3u8 streaming URL)
stream = get_master_link("FILECODE")
print(f"Stream URL: {stream.streaming_url}")
```

## ByseClient

### Constructor

```python
from streamflow.platforms.byse import ByseClient

client = ByseClient(api_key="YOUR_API_KEY", base_url=None, site_base_url=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | **Required** | Your Byse API key |
| `base_url` | str | `None` | API base URL (default: https://api.byse.sx) |
| `site_base_url` | str | `None` | Site base URL |

### Methods

#### `account_stats(last=7)`

Get account statistics for the last X days.

```python
stats = client.account_stats(last=30)
for day in stats:
    print(day.downloads, day.views, day.profits, day.referrals)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `last` | int | `7` | Number of days to fetch |

**Returns:** List of daily stats with `downloads`, `views`, `profits`, `referrals`

#### `add_remote(url)`

Queue a remote upload from a direct URL.

```python
result = client.add_remote("https://example.com/video.mp4")
print(result.result.filecode)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | **Required** | Direct video file URL |

**Returns:** Upload result with `result.filecode`

#### `list_files(**kwargs)`

List files with optional filters.

```python
files = client.list_files(page=1, per_page=20)
for f in files:
    print(f.filecode, f.name, f.views)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | `1` | Page number |
| `per_page` | int | `20` | Items per page |
| `fld_id` | int | `None` | Filter by folder ID |
| `title` | str | `None` | Search by title |
| `created` | str | `None` | Filter by creation date |
| `public` | int | `None` | Filter by public status |

**Returns:** List of files with `filecode`, `name`, `views`, `length`, `uploaded`

#### `delete_file(file_code)`

Delete a file by its code.

```python
client.delete_file("abc123")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_code` | str | **Required** | The file code to delete |

## get_master_link()

Get the master link (m3u8 streaming URL) for a file.

By default the resolver goes **straight to the video page** at
`{base_url}/d/{filecode}` and extracts the streaming URL from the
embedded (encrypted) sources. This is the right behavior for the
canonical `byse.sx` host and any mirror that ships the same
single-page-app frontend.

### Simple Usage

```python
from streamflow.platforms.byse import get_master_link

result = get_master_link("FILECODE")
print(result.streaming_url)  # m3u8 URL
print(result.title)          # video title
```

### With Challenge Auth

```python
result = get_master_link(
    "FILECODE",
    viewer_id="VIEWER_ID",
    device_id="DEVICE_ID",
    token="TOKEN",
    fingerprint="FINGERPRINT"
)
```

### Legacy `/media/.../master.m3u8` shortcut (opt-in)

Some older Byse deployments expose the playlist directly at
`{host}/media/{filecode}/master.m3u8`. Pass `use_hardcoded_master_url=True`
to try that pattern *first*. The body is **content-verified** — if the
response is not an actual `#EXTM3U` playlist (for example, an SPA host
that returns its HTML index for unknown paths with `200 OK`), the
shortcut is skipped and the resolver falls back to scraping the video
page as usual.

```python
result = get_master_link(
    "FILECODE",
    base_url="https://byse.sx",
    use_hardcoded_master_url=True,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | **Required** | The file code |
| `base_url` | str | `"https://byse.sx"` | Site URL (player / master link host) |
| `viewer_id` | str | `None` | Viewer ID for challenge auth |
| `device_id` | str | `None` | Device ID for challenge auth |
| `token` | str | `None` | Auth token |
| `fingerprint` | str | `None` | Device fingerprint |
| `timeout` | float | `30.0` | Request timeout (seconds) |
| `tcp_proxy` | str | `None` | HTTP CONNECT proxy URL |
| `udp_proxy` | str | `None` | SOCKS5 / UDP proxy URL |
| `local_address` | str | `None` | Local IP to bind |
| `http_version` | str | `None` | Force HTTP version |
| `use_hardcoded_master_url` | bool | `False` | Try the legacy `/media/{filecode}/master.m3u8` URL first (content-verified). |

**Returns:** `ByseMasterLink` object with:
- `.filecode` - file code
- `.title` - video title (or None)
- `.streaming_url` - m3u8 streaming URL (empty string if extraction failed)
- `.thumbnail` - thumbnail URL (or None)

> **Behavior change in 2.0.0:** previous versions silently fell back to
> the hardcoded URL `https://{host}/media/{filecode}/master.m3u8`
> whenever extraction from the page failed — even when that URL
> actually returned an HTML index page (200 OK with `Content-Type:
> text/html`). The resolver now (a) skips the URL pattern by default
> and (b) requires the body to start with `#EXTM3U` before returning
> it as a streaming URL. If you relied on the old behavior, pass
> `use_hardcoded_master_url=True` explicitly.

### ByseMasterLink Model

```python
from streamflow.platforms.byse import ByseMasterLink

class ByseMasterLink:
    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/account/stats` | GET | Account statistics |
| `/api/remote/add` | GET | Queue remote upload |
| `/api/file/list` | GET | List files |
| `/api/file/delete` | GET | Delete file |
| `/api/master/link` | GET | Get streaming URL |

## Error Handling

```python
from streamflow.platforms.byse import ByseClient, get_master_link

client = ByseClient(api_key="YOUR_API_KEY")

try:
    upload = client.add_remote("https://example.com/video.mp4")
    print(f"Queued: {upload.result.filecode}")
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
from streamflow.platforms.byse import ByseClient, get_master_link

# Initialize
client = ByseClient(api_key="YOUR_API_KEY")

# Get stats
stats = client.account_stats(last=7)
print(f"Downloads: {sum(s.downloads for s in stats)}")

# Upload
upload = client.add_remote("https://example.com/video.mp4")
filecode = upload.result.filecode

# Get streaming URL
stream = get_master_link(filecode)
print(f"Watch at: {stream.streaming_url}")

# List and delete
files = client.list_files(page=1, per_page=10)
for f in files:
    if f.name.startswith("temp_"):
        client.delete_file(f.filecode)
```

## Constants

```python
from streamflow.platforms.byse.constants import (
    DEFAULT_BASE_URL,  # "https://api.byse.sx"
)

from streamflow.platforms.byse.constants import (
    api_url,                # api_url(endpoint) -> "{base}/{endpoint}"
    resolve_base_url,       # resolve_base_url(override) -> base URL
    account_stats_endpoint, # https://api.byse.sx/account/stats
    remote_add_endpoint,    # https://api.byse.sx/remote/add
    file_list_endpoint,     # https://api.byse.sx/file/list
    file_delete_endpoint,   # https://api.byse.sx/file/delete
)
```