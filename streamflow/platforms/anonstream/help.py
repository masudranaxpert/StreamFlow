"""Anonstream help documentation."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from streamflow.platforms.anonstream.constants import (
    account_stats_endpoint,
    file_delete_endpoint,
    file_list_endpoint,
    resolve_base_url,
    upload_url_endpoint,
)

PLATFORM_NAME = "anonstream"
PLATFORM_TITLE = "Anonstream"


def build_help_text(base_url: str | None = None) -> str:
    upload_url = upload_url_endpoint(base_url)
    stats_url = account_stats_endpoint(base_url)
    list_url = file_list_endpoint(base_url)
    delete_url = file_delete_endpoint(base_url)
    api_base = resolve_base_url(base_url)
    help_text = f"""# Anonstream

Remote upload, file management, and account stats.

---

## Upload (remote URL)

```
GET {upload_url}?key=KEY&url=FILE_URL
```
- **Required:** `url` (direct HTTPS file link)
- **Optional:** `fld_id`, `cat_id`, `file_public`, `file_adult`, `tags`
- **Returns:** `result.filecode`
- ✅ **Google Drive links are supported.**

---

## Account stats (last X days)

```
GET {stats_url}?key=KEY&last=7
```
- **Optional:** `last` (default: 7 days)
- **Returns:** `result[]` (daily stats with downloads, views, profits)

---

## File list

```
GET {list_url}?key=KEY&page=1&per_page=20
```
- **Optional:** `fld_id`, `title`, `created`, `public`, `adult`
- **Returns:** `result.files[].file_code`, `title`, `thumbnail`, `views`, ...

---

## File delete

```
GET {delete_url}?key=KEY&file_code=CODE
```
- **Required:** `file_code`

---

## Usage

```python
from streamflow.platforms.anonstream import AnonstreamClient

client = AnonstreamClient(api_key="YOUR_API_KEY")
upload = client.upload("https://example.com/video.mp4")
print(upload.result.filecode)

files = client.list_files(page=1, per_page=20)
for f in files.result.files:
    print(f.file_code, f.title)

client.delete_file("abc123")
result = client.purge_all(fld_id=25)
```

---

**Optional:** `base_url` - API base (default: `{api_base}`)
"""
    return help_text


def show_help(base_url: str | None = None) -> None:
    console = Console()
    md = Markdown(build_help_text(base_url), code_theme="monokai")
    console.print(Panel(md, title="[bold cyan]Anonstream[/]", border_style="cyan"))


def get_help(base_url: str | None = None) -> str:
    return build_help_text(base_url)