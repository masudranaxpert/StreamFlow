# StreamFlow

**Video streaming and upload platform library for Python.**

StreamFlow provides unified APIs to work with multiple video streaming platforms including StreamEmbed (SeekStreaming, StreamP2P, Player4Me) and VOE. Get streaming URLs, manage uploads, and handle video operations through a simple, consistent interface.

## Features

- **Multi-platform support**: StreamEmbed, VOE
- **Master link resolution**: Get m3u8 streaming URLs with AES decryption
- **Advance upload**: Remote video upload with progress tracking
- **Proxy support**: TCP/UDP proxy, local address binding, HTTP version selection
- **Rich CLI**: Beautiful terminal output with formatted tables

## Quick Example

```python
from streamflow.platforms.streamembed import get_master_link, StreamembedClient

# Get streaming URL from video filecode
result = get_master_link("VIDEO_ID", provider="seekstreaming")
print(f"Streaming: {result.streaming_url}")

# Upload video
client = StreamembedClient(api_key="YOUR_API_KEY")
upload = client.upload("https://example.com/video.mp4", name="My Video")
print(f"Task ID: {upload.id}")
```

## Supported Platforms

| Platform | Providers | Description |
|----------|-----------|-------------|
| StreamEmbed | seekstreaming, streamp2p, player4me | Master link + upload API |
| VOE | voe.sx | Account stats, file management |

## Installation

```bash
pip install streamflow
```

For development:

```bash
git clone https://github.com/username/streamflow
cd streamflow
pip install -e .
```

## CLI Usage

```bash
# Show all platforms
python -m streamflow all

# Show specific platform
python -m streamflow streamembed
python -m streamflow voe

# With provider
python -m streamflow streamembed seekstreaming
```

## License

MIT License