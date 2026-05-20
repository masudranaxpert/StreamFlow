"""Platform structure audit - display all platforms features."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from streamflow.platforms import anonstream, byse, streamembed, vidara, voe

console = Console()


def _get_platform_features() -> list[dict]:
    """Get features for all platforms."""
    return [
        {
            "name": "anonstream",
            "base_url": True,
            "site_base_url": False,
            "master_link": False,
            "proxy": True,
            "purge_all": True,
        },
        {
            "name": "byse",
            "base_url": True,
            "site_base_url": False,
            "master_link": True,
            "proxy": True,
            "purge_all": True,
        },
        {
            "name": "streamembed",
            "base_url": False,
            "site_base_url": True,
            "master_link": True,
            "proxy": True,
            "purge_all": False,
        },
        {
            "name": "voe",
            "base_url": True,
            "site_base_url": True,
            "master_link": True,
            "proxy": True,
            "purge_all": True,
        },
        {
            "name": "vidara",
            "base_url": True,
            "site_base_url": True,
            "master_link": True,
            "proxy": True,
            "purge_all": False,
        },
    ]


def _get_help_signatures() -> dict[str, str]:
    """Get function signatures for help functions."""
    return {
        "anonstream": "show_help(base_url)",
        "byse": "show_help(base_url, site_base_url)",
        "streamembed": "show_help()",
        "voe": "show_help(base_url, site_base_url, show_proxy)",
        "vidara": "show_help(base_url, site_base_url, show_proxy)",
    }


def _get_master_link_info() -> dict[str, dict]:
    """Get master link info for platforms."""
    return {
        "streamembed": {
            "import": "from streamflow.platforms.streamembed import get_master_link, StreamembedMasterLink",
            "returns": "filecode, title, streaming_url, thumbnail",
        },
        "voe": {
            "import": "from streamflow.platforms.voe import get_master_link, VoeMasterLink",
            "returns": "streaming_url, title",
        },
        "vidara": {
            "import": "from streamflow.platforms.vidara import get_master_link, VidaraMasterLink",
            "returns": "streaming_url, title, thumbnail, subtitles",
        },
        "byse": {
            "import": "from streamflow.platforms.byse import get_master_link, ByseMasterLink",
            "returns": "filecode, title, streaming_url, thumbnail",
        },
    }


def show_platform_audit() -> None:
    """Show platform structure audit with rich formatting."""
    features = _get_platform_features()
    signatures = _get_help_signatures()
    ml_info = _get_master_link_info()

    # Main features table
    table = Table(title="[bold]Platform Features Summary[/]", show_header=True, header_style="bold magenta")
    table.add_column("Platform", style="cyan", justify="left")
    table.add_column("base_url", justify="center")
    table.add_column("site_base", justify="center")
    table.add_column("master", justify="center")
    table.add_column("proxy", justify="center")
    table.add_column("purge", justify="center")
    table.add_column("Help Signature", style="dim", justify="left")

    for p in features:
        name = p["name"]
        table.add_row(
            f"[bold]{name}[/]",
            "[green]✓[/]" if p["base_url"] else "[red]✗[/]",
            "[green]✓[/]" if p["site_base_url"] else "[red]✗[/]",
            "[green]✓[/]" if p["master_link"] else "[red]✗[/]",
            "[green]✓[/]" if p["proxy"] else "[red]✗[/]",
            "[green]✓[/]" if p["purge_all"] else "[red]✗[/]",
            signatures.get(name, "-"),
        )

    # Master link info table
    ml_table = Table(title="[bold]Master Link Functions[/]", show_header=True, header_style="bold magenta")
    ml_table.add_column("Platform", style="cyan", justify="left")
    ml_table.add_column("Import", style="green", justify="left")
    ml_table.add_column("Returns", style="yellow", justify="left")

    for name, info in ml_info.items():
        ml_table.add_row(
            f"[bold]{name}[/]",
            info["import"],
            info["returns"],
        )

    # Consistency notes
    notes = """
[bold yellow]Consistency Notes:[/bold yellow]

1. [cyan]byse[/cyan]: site_base_url param in signature but NOT used in help text
2. [cyan]voe/vidara[/cyan]: have show_proxy param, byse/anonstream don't
3. [cyan]anonstream[/cyan]: no master link, no site_base_url (clean structure)
4. [cyan]vidara[/cyan]: no purge_all (different use case - streaming only)

[bold]Standard Patterns:[/bold]

Basic (anonstream):     show_help(base_url)
Extended (voe/vidara):  show_help(base_url, site_base_url, show_proxy)
"""
    notes_text = Text.from_markup(notes)

    # Print all
    console.print(Panel(table, title="[bold cyan]Platform Audit[/]", border_style="cyan"))
    console.print()
    console.print(Panel(ml_table, border_style="yellow"))
    console.print()
    console.print(Panel(notes_text, title="[bold yellow]Notes[/]", border_style="yellow"))