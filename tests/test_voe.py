import pytest

from streamflow.platforms.voe import get_help
from streamflow.platforms.voe.constants import (
    account_stats_endpoint,
    file_delete_endpoint,
    file_list_endpoint,
    upload_server_endpoint,
    upload_url_endpoint,
)
from streamflow.platforms.registry import list_platforms, show_help


def test_voe_help_google_drive_supported() -> None:
    text = get_help()
    assert "Google Drive" in text
    assert "supported" in text.lower()


def test_voe_help_lists_endpoints() -> None:
    text = get_help()
    assert upload_url_endpoint() in text
    assert upload_server_endpoint() in text
    assert account_stats_endpoint() in text
    assert file_list_endpoint() in text
    assert file_delete_endpoint() in text
    assert "purge_all" in text


def test_list_platforms_includes_voe() -> None:
    assert "voe" in list_platforms()


def test_show_help_voe() -> None:
    show_help("voe")


@pytest.mark.live
def test_voe_live_master_link() -> None:
    """Test VOE get_master_link with a real filecode."""
    from streamflow.platforms.voe import get_master_link

    stream = get_master_link("iscxoesxwzko")

    assert stream.streaming_url.startswith("https://")
    assert ".m3u8" in stream.streaming_url
    assert stream.title is not None
