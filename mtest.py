"""End-to-end check of the Byse master link resolver."""

from __future__ import annotations

import sys

from streamflow.platforms.byse import ByseMasterLinkError, get_master_link

FILECODE = "shbs4bxi79lu"
BASE_URL = "https://bysevepoin.com"


def main() -> int:
    print(f"Target: {BASE_URL}/d/{FILECODE}")
    print("=" * 72)
    try:
        result = get_master_link(FILECODE, base_url=BASE_URL)
    except ByseMasterLinkError as exc:
        print(f"\nRESOLVE FAILED: {exc}")
        return 1

    print(f"  filecode      : {result.filecode}")
    print(f"  title         : {result.title!r}")
    print(f"  streaming_url : {result.streaming_url}")
    print(f"  thumbnail     : {result.thumbnail!r}")
    print(f"  expires_at    : {result.expires_at}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
