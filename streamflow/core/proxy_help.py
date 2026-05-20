"""
Proxy Configuration Help

Centralized proxy configuration documentation for all platforms.
"""

PLATFORM_NAME = "proxy"
PLATFORM_TITLE = "Proxy Configuration"

PROXY_HELP = """
Proxy Configuration (split-config)

Set proxy parameters in Client constructor or per-request.

Parameters
  tcp_proxy     TCP/HTTP requests proxy URL
  udp_proxy     UDP/HTTP3 proxy URL (required for HTTP/3)
  local_address Bind to specific network interface
  http_version  Force HTTP version: HTTP/1.1, HTTP/2, HTTP/3

Proxy URL Schemes
  http://proxy:port      HTTP CONNECT proxy
  https://proxy:port     HTTPS CONNECT proxy (with TLS)
  socks5://proxy:port    SOCKS5 TCP proxy
  socks5h://proxy:port   SOCKS5 with hostname resolution on proxy
  masque://proxy:port     MASQUE proxy (HTTP/3 UDP tunneling)

Examples
  HTTP proxy with authentication:
    client = VoeClient(api_key=KEY, tcp_proxy=http://user:pass@proxy.com:8080)

  SOCKS5 proxy:
    client = VoeClient(api_key=KEY, tcp_proxy=socks5://127.0.0.1:1080)

  Split config: TCP + UDP for HTTP/3:
    client = VidaraClient(
        api_key=KEY,
        tcp_proxy=http://proxy.com:8080,
        udp_proxy=socks5://127.0.0.1:1080,
        http_version=HTTP/3,
    )

  Bind to specific interface:
    client = VoeClient(api_key=KEY, local_address=192.168.1.100)

Per-Request Override
  client.upload(url, tcp_proxy=socks5://proxy:1080)
  client.master_link(FILECODE, http_version=HTTP/2)

HTTP Version Notes
  HTTP/1.1  Default, works with all proxy types
  HTTP/2    Requires proxy support (ALPN)
  HTTP/3    Requires udp_proxy (MASQUE or SOCKS5 UDP ASSOCIATE)
"""


def show_proxy_help() -> None:
    """Print proxy configuration help."""
    print(PROXY_HELP.strip())


def get_proxy_help() -> str:
    """Get proxy configuration help text."""
    return PROXY_HELP.strip()
