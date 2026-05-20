# Anonstream

Remote upload, file management, and account stats for Anonstream platform.

## Installation

```bash
pip install streamflow
```

## Quick Example

```python
from streamflow.platforms.anonstream import AnonstreamClient

# Initialize client
client = AnonstreamClient(api_key="YOUR_API_KEY")

# Remote upload from URL
upload = client.upload("https://example.com/video.mp4")
print(f"Uploaded: {upload.result.filecode}")

# List files
files = client.list_files(page=1, per_page=20)
for f in files.result.files:
    print(f.file_code, f.title)

# Delete file
client.delete_file("abc123")
```

## AnonstreamClient

### Constructor

```python
from streamflow.platforms.anonstream import AnonstreamClient

client = AnonstreamClient(api_key="YOUR_API_KEY", base_url=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | **Required** | Your Anonstream API key |
| `base_url` | str | `None` | Custom API base URL |

### Methods

#### `upload(url, **kwargs)`

Remote upload a file from a direct URL.

```python
result = client.upload("https://example.com/video.mp4")
print(result.result.filecode)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | **Required** | Direct HTTPS file link |
| `fld_id` | int | `None` | Folder ID |
| `cat_id` | int | `None` | Category ID |
| `file_public` | int | `1` | Public visibility (0 or 1) |
| `file_adult` | int | `0` | Adult content flag (0 or 1) |
| `tags` | str | `None` | Comma-separated tags |

**Returns:** Upload result with `result.filecode`

!!! tip
    **Google Drive links are supported.**

#### `account_stats(last=7)`

Get account statistics for the last X days.

```python
stats = client.account_stats(last=30)
for day in stats.result:
    print(day.downloads, day.views, day.profits)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `last` | int | `7` | Number of days to fetch |

**Returns:** List of daily stats with `downloads`, `views`, `profits`

#### `list_files(**kwargs)`

List files with optional filters.

```python
files = client.list_files(page=1, per_page=20)
for f in files.result.files:
    print(f.file_code, f.title, f.views)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | `1` | Page number |
| `per_page` | int | `20` | Items per page |
| `fld_id` | int | `None` | Filter by folder ID |
| `title` | str | `None` | Search by title |
| `created` | str | `None` | Filter by creation date |
| `public` | int | `None` | Filter by public status |
| `adult` | int | `None` | Filter by adult flag |

**Returns:** List of files with `file_code`, `title`, `thumbnail`, `views`, etc.

#### `delete_file(file_code)`

Delete a file by its code.

```python
client.delete_file("abc123")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_code` | str | **Required** | The file code to delete |

#### `purge_all(fld_id=None)`

Delete all files, optionally in a specific folder.

```python
result = client.purge_all(fld_id=25)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fld_id` | int | `None` | Folder ID to purge (deletes all if None) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload/add` | GET | Remote URL upload |
| `/api/upload/stats` | GET | Account statistics |
| `/api/file/list` | GET | List files |
| `/api/file/delete` | GET | Delete file |

## Error Handling

```python
from streamflow.platforms.anonstream import AnonstreamClient

client = AnonstreamClient(api_key="YOUR_API_KEY")

try:
    upload = client.upload("https://example.com/video.mp4")
    print(f"Success: {upload.result.filecode}")
except Exception as e:
    print(f"Error: {e}")
```