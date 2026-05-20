# API Reference

Complete API documentation for StreamFlow platforms.

## StreamEmbed API

- [Functions](streamembed.md#functions) - `get_master_link()`, `advance_upload()`, etc.
- [Client](streamembed.md#client) - `StreamembedClient`
- [Models](streamembed.md#models) - Response data classes

## VOE API

- [Functions](voe.md#functions) - `get_master_link()`, `list_files()`, etc.
- [Client](voe.md#client) - `VOEClient`
- [Models](voe.md#models) - Response data classes

## Common Patterns

### Error Handling

All platforms raise platform-specific API errors:

```python
# StreamEmbed
from streamflow.platforms.streamembed import StreamembedAPIError

# VOE
from streamflow.platforms.voe import VoeAPIError

try:
    result = get_master_link("invalid")
except (StreamembedAPIError, VoeAPIError) as e:
    print(f"API Error: {e}")
```

### Proxy Configuration

Proxy parameters available on all methods:

| Parameter | Description |
|-----------|-------------|
| `tcp_proxy` | HTTP CONNECT proxy URL |
| `udp_proxy` | SOCKS5 proxy URL |
| `local_address` | Local IP to bind |
| `http_version` | Force HTTP version |

### Timeout

All methods accept `timeout` parameter (default: 30 seconds).

```python
result = get_master_link("filecode", timeout=60.0)