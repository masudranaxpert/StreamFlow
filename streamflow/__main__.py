from __future__ import annotations

import sys

from streamflow.platforms.registry import list_platforms, show_all_help, show_help


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    
    # No args - show usage
    if not args or args[0] in {"-h", "--help"}:
        names = ", ".join(list_platforms()) or "(none)"
        print(f"Usage: python -m streamflow <platform|all>\nPlatforms: {names}")
        print(f"\nPlatforms under streamembed:")
        print(f"  python -m streamflow streamembed       # Show all providers")
        print(f"  python -m streamflow streamembed <provider>  # Show specific provider")
        return 0
    
    if args[0] == "all":
        show_all_help()
        return 0
    
    # Handle streamembed with sub-commands
    if args[0] == "streamembed":
        if len(args) == 1:
            # Show all providers under streamembed
            print("StreamEmbed Platform - Available Providers:")
            print("=" * 50)
            print("\nProviders:")
            print("  seekstreaming  - https://seekstreaming.com")
            print("  streamp2p      - https://streamp2p.com")
            print("  player4me      - https://player4me.com")
            print("\nUsage:")
            print("  python -m streamflow streamembed <provider>")
            print("\nExamples:")
            print("  python -m streamflow streamembed seekstreaming")
            print("  python -m streamflow streamembed streamp2p")
            print("  python -m streamflow streamembed player4me")
            print("\nCLI Usage:")
            print("  python -m streamflow master streamembed <video_id> --provider <provider>")
            print("  python -m streamflow upload streamembed --api-key KEY --url <url>")
            return 0
        else:
            # Show specific provider help
            provider = args[1]
            valid_providers = ["seekstreaming", "streamp2p", "player4me"]
            if provider not in valid_providers:
                print(f"Unknown provider '{provider}'", file=sys.stderr)
                print(f"Valid providers: {', '.join(valid_providers)}", file=sys.stderr)
                return 1
            # Pass provider as api_key (hack to show provider in help)
            show_help("streamembed", provider=provider)
            return 0
    
    try:
        show_help(args[0])
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
