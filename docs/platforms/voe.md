# VOE Platform

VOE provides file management and account operations for voe.sx.

## Default URLs

| URL | Value | What it's for |
|-----|-------|---------------|
| **API Base URL** (`base_url=`) | `https://voe.sx/api` | All JSON calls: `account_stats`, `list_files`, `upload`, `delete_files`, `purge_all`, `upload_server`. |
| **Site URL** (`site_base_url=`) | `https://voe.sx` | The video player / `/e/{filecode}` embed page (`file_page_url(filecode)`). This is the host your viewers actually hit. |

> Don't pass the Site URL to `base_url=` — the JSON API isn't served
> from the bare `voe.sx` host; it lives under `/api`. The library's
> default (`DEFAULT_API_BASE_URL = "https://voe.sx/api"`) already
> includes the `/api` segment, so you normally don't need to override
> anything.

## Installation

```python
from streamflow.platforms.voe import VOEClient, get_master_link
```

## get_master_link()

Get the **master link (m3u8 streaming URL)** for a VOE video. This is
the URL your player loads — it does **not** need an API key, because
the video is served from the public site, not the JSON API.

```python
from streamflow.platforms.voe import get_master_link

result = get_master_link("FILECODE")
print(result.streaming_url)  # the m3u8 URL
print(result.title)           # video title (when the page exposes it)
```

### How it works

1. Loads the player page at `{site_base_url}/e/{filecode}` (default
   `https://voe.sx/e/{filecode}`).
2. Detects the short JS-redirect bootstrap and follows
   `window.location.href = "..."` if present.
3. Locates the encrypted `<script type="application/json">["..."]</script>`
   payload on the final page.
4. Reverses VOE's obfuscation chain (ROT13 → delimiter strip → base64
   decode → Caesar shift by -3 → reverse → base64 decode → JSON).
5. Returns the `source` field as `streaming_url`.

### Signature

```python
get_master_link(
    filecode: str,
    *,
    site_base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> VoeMasterLink
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | **required** | The VOE filecode (the `XXXX` in `voe.sx/e/XXXX`). |
| `site_base_url` | str | `None` → `https://voe.sx` | **Site URL** (player host). Use this to point at a VOE mirror domain. Do **not** pass the API base URL here. |
| `timeout` | float | `30.0` | Request timeout in seconds. |
| `tcp_proxy` | str | `None` | HTTP CONNECT proxy URL. |
| `udp_proxy` | str | `None` | SOCKS5 / UDP proxy URL. |
| `local_address` | str | `None` | Local IP to bind the socket to. |
| `http_version` | str | `None` | Force `"HTTP/1.1"`, `"HTTP/2"`, or `"HTTP/3"` (the last requires `udp_proxy`). |

### Returns

`VoeMasterLink` (frozen dataclass):

```python
@dataclass(frozen=True, slots=True)
class VoeMasterLink:
    streaming_url: str        # the m3u8 URL the player should load
    title: str | None = None  # video title from the decrypted config
```

### Raises

- `VoeAPIError` — when the encrypted script tag isn't found on the
  page, decryption fails, or the decrypted config has no `source`
  field. Inspect `err.body` for the truncated upstream HTML.

### Examples

```python
from streamflow.platforms.voe import get_master_link, VoeAPIError

result = get_master_link("abc123xyz")
print(result.streaming_url)

result = get_master_link("abc123xyz", site_base_url="https://voe-mirror.example")

result = get_master_link(
    "abc123xyz",
    tcp_proxy="http://user:pass@proxy:8080",
    timeout=60.0,
)

try:
    result = get_master_link("badcode")
except VoeAPIError as exc:
    print(f"VOE failed: {exc}")
    print(f"Body snippet: {exc.body!r}")
```

> The master link flow uses the **Site URL** (`https://voe.sx` by
> default), not the API Base URL. Don't pass `https://voe.sx/api` here
> — that endpoint serves JSON, not the player page.

## VOEClient

Client for VOE API operations.

```python
client = VOEClient(
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
| `api_key` | str | required | VOE API key |
| `base_url` | str | None | Override API base URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy URL |
| `udp_proxy` | str | None | UDP proxy URL |
| `local_address` | str | None | Local bind address |

### Client Methods

#### account_stats()

Get account statistics.

```python
stats = client.account_stats() -> AccountStatsResponse
```

**Returns:** `AccountStatsResponse` with fields:
- `storage_used` - Storage used in bytes
- `storage_limit` - Storage limit
- `traffic_used` - Traffic used in bytes
- `traffic_limit` - Traffic limit
- `files_count` - Total file count

#### list_files()

List files in account/folder.

```python
files = client.list_files(
    *,
    page: int = 1,
    per_page: int = 100,
    fld_id: int = 0,
    created: str | None = None,
    name: str | None = None,
    preview: bool | None = None,
) -> FileListResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 100 | Items per page |
| `fld_id` | int | 0 | Folder ID |
| `created` | str | None | Filter by creation date |
| `name` | str | None | Filter by name |
| `preview` | bool | None | Include preview URLs |

**Returns:** `FileListResponse` with `files` list of `FileItem`.

#### upload()

Upload video from URL.

```python
upload = client.upload(
    url: str,
    *,
    folder_id: int | None = None,
) -> UploadUrlResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | Video URL to upload |
| `folder_id` | int | None | Target folder ID |

**Returns:** `UploadUrlResponse` with `upload_url` field.

#### upload_server()

Get upload server URL for direct upload.

```python
result = client.upload_server() -> UploadServerResponse
```

**Returns:** `UploadServerResponse` with upload server URL.

#### delete_files()

Delete files by delete code.

```python
result = client.delete_files(del_code: str) -> FileDeleteResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `del_code` | str | required | Delete code (comma-separated) |

**Returns:** `FileDeleteResponse` with `deleted` count.

#### purge_all()

Delete all files in account or folder.

```python
result = client.purge_all(
    *,
    fld_id: int = 0,
    per_page: int = 100,
) -> PurgeAllResult
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fld_id` | int | 0 | Folder ID (0 = all) |
| `per_page` | int | 100 | Items per page |

**Returns:** `PurgeAllResult` with:
- `deleted` - Number of deleted files
- `file_codes` - Tuple of deleted file codes

### Client Examples

```python
from streamflow.platforms.voe import VOEClient

client = VOEClient(api_key="YOUR_API_KEY")

# Account stats
stats = client.account_stats()
print(f"Storage: {stats.storage_used} / {stats.storage_limit}")
print(f"Files: {stats.files_count}")

# List files
files = client.list_files(page=1, per_page=50)
for f in files.files:
    print(f"{f.name} - {f.size} bytes")

# Upload from URL
upload = client.upload("https://example.com/video.mp4")
print(f"Upload URL: {upload.upload_url}")

# Delete files
result = client.delete_files("abc123,def456")
print(f"Deleted: {result.deleted}")

# Purge all files
result = client.purge_all()
print(f"Purged: {result.deleted} files")
```

## Models

### AccountStatsResponse

```python
@dataclass
class AccountStatsResponse:
    storage_used: int      # bytes
    storage_limit: int    # bytes
    traffic_used: int     # bytes
    traffic_limit: int    # bytes
    files_count: int
```

### FileListResponse

```python
@dataclass
class FileListResponse:
    total: int
    page: int
    per_page: int
    files: list[FileItem]

@dataclass
class FileItem:
    filecode: str
    name: str
    size: int
    created: str
    deleted: str | None
    thumb: str | None
    preview: str | None
    folder: int
```

### UploadUrlResponse

```python
@dataclass
class UploadUrlResponse:
    upload_url: str
```

### UploadServerResponse

```python
@dataclass
class UploadServerResponse:
    status: int
    msg: str
    result: UploadServerResult

@dataclass
class UploadServerResult:
    upload_server: str
```

### PurgeAllResult

```python
@dataclass
class PurgeAllResult:
    deleted: int
    file_codes: tuple[str, ...]
    errors: list[str] | None = None
```

## Error Handling

```python
from streamflow.platforms.voe import VoeAPIError, VOEClient

try:
    client = VOEClient(api_key="invalid")
    stats = client.account_stats()
except VoeAPIError as e:
    print(f"API Error: {e}")
```

## Constants

```python
from streamflow.platforms.voe.constants import (
    DEFAULT_API_BASE_URL,   # "https://voe.sx/api"
    DEFAULT_SITE_BASE_URL,  # "https://voe.sx"
    UPLOAD_URL_PATH,        # "/upload/url"
    UPLOAD_SERVER_PATH,     # "/upload/server"
    ACCOUNT_STATS_PATH,     # "/account/stats"
    FILE_LIST_PATH,         # "/file/list"
    FILE_DELETE_PATH,       # "/file/delete"
    FILE_PAGE_PATH,         # "/e/{filecode}"
)
```

> The full API endpoint is `DEFAULT_API_BASE_URL` (already including
> `/api`) concatenated with each `*_PATH`. For example, the account
> stats endpoint resolves to `https://voe.sx/api/account/stats`.