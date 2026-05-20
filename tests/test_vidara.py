import pytest

VIDARA_TEST_API_KEY = "b85ab43078d36ac7dff213969e96910bfcb90c90830d39491c57efe96367156b"
VIDARA_TEST_VIDEO_URL = (
    "https://avtshare01.rz.tu-ilmenau.de/avt-vqdb-uhd-1/test_1/segments/"
    "bigbuck_bunny_8bit_15000kbps_1080p_60.0fps_h264.mp4"
)
VIDARA_TEST_FILECODE = "DZ5ewUU4OgJ8"

from streamflow.platforms.vidara import (
    DEFAULT_API_BASE_URL,
    VidaraClient,
    get_help,
    get_master_link,
    upload_endpoint,
)
from streamflow.platforms.vidara.constants import stream_endpoint, upload_server_endpoint
from streamflow.platforms.registry import list_platforms, show_help


@pytest.mark.live
def test_vidara_live_upload() -> None:
    client = VidaraClient(api_key=VIDARA_TEST_API_KEY, timeout=300.0)
    result = client.upload(VIDARA_TEST_VIDEO_URL)

    assert result.status == 200
    assert result.msg.upper() == "OK"
    assert result.data.filecode
    assert result.data.size > 0


@pytest.mark.live
def test_vidara_live_upload_server() -> None:
    client = VidaraClient(api_key=VIDARA_TEST_API_KEY, timeout=300.0)
    result = client.upload_server()

    assert result.status == 200
    assert result.msg.upper() == "OK"
    assert result.result.upload_server.startswith("https://")
    assert "/upload" in result.result.upload_server


@pytest.mark.live
def test_vidara_live_master_link() -> None:
    stream = get_master_link(VIDARA_TEST_FILECODE)

    assert stream.filecode == VIDARA_TEST_FILECODE
    assert stream.streaming_url.startswith("https://")
    assert ".m3u8" in stream.streaming_url
    assert stream.title


def test_vidara_help_mentions_google_drive() -> None:
    text = get_help()
    assert "Google Drive" in text
    assert "not supported" in text.lower()


def test_vidara_help_uses_endpoints_from_constants() -> None:
    text = get_help()
    assert upload_endpoint() in text
    assert upload_server_endpoint() in text
    assert stream_endpoint() in text
    assert DEFAULT_API_BASE_URL in text
    assert "master_link" in text.lower() or "master link" in text.lower()


def test_vidara_help_custom_base_url() -> None:
    custom_api = "https://staging.vidara.so/v2"
    custom_site = "https://staging.vidara.so"
    text = get_help(base_url=custom_api, site_base_url=custom_site)
    assert upload_endpoint(custom_api) in text
    assert upload_server_endpoint(custom_api) in text
    assert stream_endpoint(custom_site) in text


def test_list_platforms_includes_vidara() -> None:
    assert "vidara" in list_platforms()


def test_show_help_unknown_platform() -> None:
    with pytest.raises(ValueError, match="Unknown platform"):
        show_help("unknown")
