# VOE API Reference

## Functions

### get_master_link()

```python
from streamflow.platforms.voe import get_master_link

result = get_master_link(
    filecode: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
    http_version: str | None = None,
) -> VoeMasterLink
```

Get video master link.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filecode` | str | required | Video filecode |
| `base_url` | str | None | Override site URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |
| `http_version` | str | None | HTTP version |

**Returns:** `VoeMasterLink` object.

### get_account_stats()

```python
from streamflow.platforms.voe import get_account_stats

response = get_account_stats(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> AccountStatsResponse
```

Get account statistics.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `AccountStatsResponse`

### list_files()

```python
from streamflow.platforms.voe import list_files

response = list_files(
    api_key: str,
    *,
    page: int = 1,
    per_page: int = 100,
    fld_id: int = 0,
    created: str | None = None,
    name: str | None = None,
    preview: bool | None = None,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> FileListResponse
```

List files in account.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `page` | int | 1 | Page number |
| `per_page` | int | 100 | Items per page |
| `fld_id` | int | 0 | Folder ID |
| `created` | str | None | Filter by date |
| `name` | str | None | Filter by name |
| `preview` | bool | None | Include preview |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `FileListResponse`

### upload_from_url()

```python
from streamflow.platforms.voe import upload_from_url

response = upload_from_url(
    api_key: str,
    url: str,
    *,
    folder_id: int | None = None,
    base_url: str | None = None,
    timeout: float = 120.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> UploadUrlResponse
```

Upload video from URL.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `url` | str | required | Video URL |
| `folder_id` | int | None | Folder ID |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 120.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `UploadUrlResponse`

### get_upload_server()

```python
from streamflow.platforms.voe import get_upload_server

response = get_upload_server(
    api_key: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> UploadServerResponse
```

Get upload server URL.

**Returns:** `UploadServerResponse`

### delete_files()

```python
from streamflow.platforms.voe import delete_files

response = delete_files(
    api_key: str,
    del_code: str,
    *,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> FileDeleteResponse
```

Delete files by delete code.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `del_code` | str | required | Delete code (comma-separated) |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `FileDeleteResponse`

### purge_all_files()

```python
from streamflow.platforms.voe import purge_all_files

result = purge_all_files(
    api_key: str,
    *,
    fld_id: int = 0,
    per_page: int = 100,
    batch_size: int = 50,
    base_url: str | None = None,
    timeout: float = 30.0,
    tcp_proxy: str | None = None,
    udp_proxy: str | None = None,
    local_address: str | None = None,
) -> PurgeAllResult
```

Delete all files in account/folder.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | API key |
| `fld_id` | int | 0 | Folder ID (0 = all) |
| `per_page` | int | 100 | Items per page |
| `batch_size` | int | 50 | Delete batch size |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy |
| `udp_proxy` | str | None | UDP proxy |
| `local_address` | str | None | Local address |

**Returns:** `PurgeAllResult`

## Client

### VOEClient

```python
from streamflow.platforms.voe import VOEClient

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

**Constructor Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | VOE API key |
| `base_url` | str | None | Override API URL |
| `timeout` | float | 30.0 | Request timeout |
| `tcp_proxy` | str | None | TCP proxy URL |
| `udp_proxy` | str | None | UDP proxy URL |
| `local_address` | str | None | Local bind address |

#### Methods

##### account_stats()

```python
stats = client.account_stats() -> AccountStatsResponse
```

##### list_files()

```python
files = client.list_files(
    *,
    page: int = 1,
    per_page: int = 100,
    fld_id: int = 0,
) -> FileListResponse
```

##### upload()

```python
upload = client.upload(
    url: str,
    *,
    folder_id: int | None = None,
) -> UploadUrlResponse
```

##### upload_server()

```python
result = client.upload_server() -> UploadServerResponse
```

##### delete_files()

```python
result = client.delete_files(del_code: str) -> FileDeleteResponse
```

##### purge_all()

```python
result = client.purge_all(
    *,
    fld_id: int = 0,
    per_page: int = 100,
) -> PurgeAllResult
```

## Models

### VoeMasterLink

```python
@dataclass
class VoeMasterLink:
    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None
    master_url: str | None = None
```

### AccountStatsResponse

```python
@dataclass
class AccountStatsResponse:
    storage_used: int
    storage_limit: int
    traffic_used: int
    traffic_limit: int
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
```

### FileItem

```python
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

### FileDeleteResponse

```python
@dataclass
class FileDeleteResponse:
    deleted: int
```

### PurgeAllResult

```python
@dataclass
class PurgeAllResult:
    deleted: int
    file_codes: tuple[str, ...]
    errors: list[str] | None = None
```

### VoeAPIError

```python
class VoeAPIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        body: str | None = None,
    )
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

from streamflow.platforms.voe.constants import (
    file_page_url,         # file_page_url(filecode) -> "{site}/e/{filecode}"
    api_url,               # api_url(path) -> "{api_base}{path}"
    resolve_base_url,      # resolve_base_url(override) -> API base URL
    resolve_site_base_url, # resolve_site_base_url(override) -> site URL
    upload_url_endpoint,   # https://voe.sx/api/upload/url
    upload_server_endpoint,# https://voe.sx/api/upload/server
    account_stats_endpoint,# https://voe.sx/api/account/stats
    file_list_endpoint,    # https://voe.sx/api/file/list
    file_delete_endpoint,  # https://voe.sx/api/file/delete
)
```

> `DEFAULT_API_BASE_URL` already includes the `/api` segment. Endpoint
> functions concatenate the per-action path on top — e.g.
> `account_stats_endpoint()` resolves to
> `https://voe.sx/api/account/stats`.