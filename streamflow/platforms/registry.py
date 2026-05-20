from __future__ import annotations

from collections.abc import Callable

from streamflow.core.proxy_help import show_proxy_help
from streamflow.platforms import anonstream, byse, streamembed, vidara, voe
from streamflow.platforms.audit import show_platform_audit

PlatformHelpFn = Callable[[], None]

PLATFORM_HELP: dict[str, PlatformHelpFn] = {
    "proxy": show_proxy_help,
    "audit": show_platform_audit,
    anonstream.help.PLATFORM_NAME: anonstream.help.show_help,
    byse.help.PLATFORM_NAME: byse.help.show_help,
    streamembed.help.PLATFORM_NAME: streamembed.help.show_help,
    vidara.help.PLATFORM_NAME: vidara.help.show_help,
    voe.help.PLATFORM_NAME: voe.help.show_help,
}

PLATFORM_TITLES: dict[str, str] = {
    "proxy": "Proxy Configuration",
    "audit": "Platform Audit",
    anonstream.help.PLATFORM_NAME: anonstream.help.PLATFORM_TITLE,
    byse.help.PLATFORM_NAME: byse.help.PLATFORM_TITLE,
    streamembed.help.PLATFORM_NAME: streamembed.help.PLATFORM_TITLE,
    vidara.help.PLATFORM_NAME: vidara.help.PLATFORM_TITLE,
    voe.help.PLATFORM_NAME: voe.help.PLATFORM_TITLE,
}


def list_platforms() -> list[str]:
    return sorted(PLATFORM_HELP)


def show_help(platform: str, **kwargs) -> None:
    key = platform.lower().strip()
    if key not in PLATFORM_HELP:
        available = ", ".join(list_platforms()) or "(none)"
        raise ValueError(f"Unknown platform '{platform}'. Available: {available}")
    help_fn = PLATFORM_HELP[key]
    if hasattr(help_fn, '__code__') and help_fn.__code__.co_argcount > 0:
        # Call with kwargs if function accepts parameters
        help_fn(**kwargs)
    else:
        help_fn()


def show_all_help() -> None:
    names = list_platforms()
    for index, name in enumerate(names):
        if index:
            print()
        PLATFORM_HELP[name]()
