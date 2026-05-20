# Proxy Configuration

StreamFlow supports proxy configuration for all API requests. This is useful for:
- Bypassing geo-restrictions
- Hiding your IP address
- Improving connection speed
- Avoiding rate limits

## Proxy Parameters

All client constructors and API functions support these proxy parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `tcp_proxy` | str | HTTP CONNECT proxy URL |
| `udp_proxy` | str | SOCKS5 proxy URL |
| `local_address` | str | Local IP to bind to |
| `http_version` | str | Force HTTP version (1.1, 2, 3) |

## Proxy URL Formats

### HTTP CONNECT Proxy

Standard HTTP/HTTPS proxy with authentication:

```
http://user:pass@proxy.example.com:8080
https://proxy.example.com:8443
http://proxy.example.com:8080
```

### SOCKS5 Proxy

SOCKS5 proxy with optional authentication:

```
socks5://127.0.0.1:1080
socks5://user:pass@proxy.example.com:1080
socks5h://127.0.0.1:1080  # DNS resolved on proxy server
```

### MASQUE Proxy

HTTP/3 MASQUE protocol proxy (requires `udp_proxy`):

```
masque://proxy.example.com:443
```

## Usage Examples

### StreamEmbed Client

```python
from streamflow.platforms.streamembed import StreamembedClient

# With HTTP proxy
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://user:pass@proxy.example.com:8080"
)

# With SOCKS5 proxy
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    udp_proxy="socks5://127.0.0.1:1080"
)

# With both proxies
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://proxy.example.com:8080",
    udp_proxy="socks5://proxy.example.com:1080"
)

# Bind to specific local IP
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    local_address="192.168.1.100"
)
```

### VOE Client

```python
from streamflow.platforms.voe import VOEClient

client = VOEClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://proxy.example.com:8080"
)
```

### Master Link Functions

```python
from streamflow.platforms.streamembed import get_master_link

# With proxy
result = get_master_link(
    "VIDEO_ID",
    tcp_proxy="http://proxy.example.com:8080"
)

# With SOCKS5
result = get_master_link(
    "VIDEO_ID",
    udp_proxy="socks5://127.0.0.1:1080"
)

# Force HTTP/3 (requires udp_proxy)
result = get_master_link(
    "VIDEO_ID",
    udp_proxy="socks5://127.0.0.1:1080",
    http_version="HTTP/3"
)
```

## HTTP Version Control

### Available Options

| Value | Description |
|-------|-------------|
| `"HTTP/1.1"` | Force HTTP/1.1 |
| `"HTTP/2"` | Force HTTP/2 |
| `"HTTP/3"` | Force HTTP/3 (requires `udp_proxy`) |

### When to Use HTTP/3

HTTP/3 is recommended when:
- You have a reliable UDP proxy (SOCKS5)
- You want lower latency
- The server supports HTTP/3

**Note:** HTTP/3 requires an `udp_proxy` to be configured.

```python
result = get_master_link(
    "VIDEO_ID",
    udp_proxy="socks5://127.0.0.1:1080",
    http_version="HTTP/3"
)
```

## Local Address Binding

Bind requests to a specific network interface:

```python
from streamflow.platforms.streamembed import StreamembedClient

# Bind to specific IP
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    local_address="192.168.1.100"
)
```

## Free Proxy Sources

For testing, you can use free proxy lists:

```python
# Example: Rotate proxies
import random

free_proxies = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
]

proxy = random.choice(free_proxies)
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy=proxy
)
```

**Warning:** Free proxies are often slow, unreliable, or blocked. For production use, consider dedicated proxy services.

## Recommended Proxy Services

| Service | Type | Features |
|---------|------|----------|
| [Luminati](https://luminati.io/) | Residential | High reliability, global coverage |
| [Oxylabs](https://oxylabs.io/) | Residential/Datacenter | Good performance |
| [SmartProxy](https://smartproxy.com/) | Residential | Easy to use |
| [ProxyMesh](http://proxymesh.com/) | HTTP/SOCKS5 | Rotating IPs |

## Troubleshooting

### Connection Timeout

```python
# Increase timeout
client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy="http://proxy.example.com:8080",
    timeout=120.0  # 2 minutes
)
```

### Proxy Authentication Failed

Ensure credentials are URL-encoded:

```python
# Special characters in password
from urllib.parse import quote

password = "p@ssw0rd!#$"
encoded = quote(password, safe='')

proxy = f"http://user:{encoded}@proxy.example.com:8080"
client = StreamembedClient(api_key="KEY", tcp_proxy=proxy)
```

### HTTP/3 Not Working

1. Ensure `udp_proxy` is set (HTTP/3 requires UDP)
2. Verify proxy supports SOCKS5 UDP extension
3. Check if server supports HTTP/3

```python
# Fallback to HTTP/2
result = get_master_link(
    "VIDEO_ID",
    udp_proxy="socks5://proxy.example.com:1080",
    http_version="HTTP/2"
)
```

## Environment Variables

For convenience, use environment variables:

```bash
export STREAMFLOW_TCP_PROXY="http://proxy.example.com:8080"
export STREAMFLOW_UDP_PROXY="socks5://127.0.0.1:1080"
```

```python
import os

client = StreamembedClient(
    api_key="YOUR_API_KEY",
    tcp_proxy=os.getenv("STREAMFLOW_TCP_PROXY"),
    udp_proxy=os.getenv("STREAMFLOW_UDP_PROXY")
)
```