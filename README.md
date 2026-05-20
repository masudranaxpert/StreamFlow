# StreamFlow

**Multi-platform video streaming utilities for Python.**

[![PyPI Version](https://img.shields.io/pypi/v/streamflow.svg)](https://pypi.org/project/streamflow/)
[![Python](https://img.shields.io/pypi/pyversions/streamflow.svg)](https://pypi.org/project/streamflow/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Features

- **Master Link Resolution** — Get m3u8 streaming URLs from video platforms
- **Remote Upload** — Upload files from direct URLs
- **File Management** — List, delete, and manage files
- **Proxy Support** — TCP, UDP, SOCKS5, MASQUE proxies
- **HTTP Version Control** — Force HTTP/1.1, HTTP/2, or HTTP/3

---

## Installation

```bash
pip install streamflow
```

Or from source:

```bash
git clone https://github.com/YOUR_USERNAME/streamflow.git
cd streamflow
pip install -e .
```

---

## Quick Start

### Get Streaming URL

```python
from streamflow.platforms.streamembed import get_master_link

# Get m3u8 streaming URL
result = get_master_link("abc123", provider="streamp2p")
print(result.streaming_url)  # https://example.com/stream.m3u8
```

### Upload File

```python
from streamflow.platforms.voe import VOEClient

client = VOEClient(api_key="YOUR_API_KEY")
upload = client.upload("https://example.com/video.mp4")
print(f"Uploaded: {upload.result.filecode}")
```

### List Files

```python
from streamflow.platforms.byse import ByseClient

client = ByseClient(api_key="YOUR_API_KEY")
files = client.list_files(page=1, per_page=20)
for f in files:
    print(f.filecode, f.name)
```

---

## Supported Platforms

| Platform | Features |
|----------|----------|
| **StreamEmbed** | Master link + upload (seekstreaming, streamp2p, player4me) |
| **VOE** | Account stats, file management, upload |
| **Anonstream** | Remote upload, file management |
| **Byse** | Upload, file management, master link |
| **Vidara** | Upload, HLS master link, proxy support |

---

## Test Streams Online

Test your m3u8 streams with free online players:

- **[Livepush HLS Player](https://livepush.io/hls-player/index.html)** — Simple HLS stream tester
- **[VideoJS Demo](https://testvideojs.vercel.app/)** — Video.js based player

---

## CLI Usage

```bash
# Show help for a platform
streamflow help streamembed

# Show all platforms
streamflow help

# Show proxy help
streamflow help proxy

# Platform audit
streamflow audit
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
