from __future__ import annotations

PACKAGE_NAME = "streamflow"
PACKAGE_VERSION = "0.1.5"

ACCEPT_ENCODING_IDENTITY = "identity"
ACCEPT_ENCODING_FALLBACK = "gzip, deflate, br, zstd"
ACCEPT_ENCODING_DEFAULT = f"{ACCEPT_ENCODING_IDENTITY}, {ACCEPT_ENCODING_FALLBACK}"

CHROME_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

SEC_CH_UA = '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"'
SEC_CH_UA_PLATFORM = '"Windows"'

DEFAULT_BROWSER_HEADERS: dict[str, str] = {
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    ),
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": ACCEPT_ENCODING_DEFAULT,
    "cache-control": "max-age=0",
    "sec-ch-ua": SEC_CH_UA,
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": SEC_CH_UA_PLATFORM,
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": CHROME_USER_AGENT,
}

API_BROWSER_HEADERS: dict[str, str] = {
    **DEFAULT_BROWSER_HEADERS,
    "accept": "application/json, text/plain, */*",
    "accept-encoding": ACCEPT_ENCODING_DEFAULT,
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
}

BROWSER_HEADER_ORDER: tuple[str, ...] = (
    "accept",
    "accept-language",
    "accept-encoding",
    "cache-control",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "sec-fetch-user",
    "upgrade-insecure-requests",
    "user-agent",
)

API_HEADER_ORDER: tuple[str, ...] = (
    "accept",
    "accept-language",
    "accept-encoding",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "sec-ch-ua-platform",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "user-agent",
)

DEFAULT_TIMEOUT = 30.0
RECOMMENDED_HTTP_PRESET = "chrome-latest"
