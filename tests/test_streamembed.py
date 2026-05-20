"""Tests for Streamembed platform."""

from __future__ import annotations

import pytest


class TeststreamembedConstants:
    """Test constants module."""

    def test_default_urls(self) -> None:
        from streamflow.platforms.streamembed.constants import (
            DEFAULT_API_BASE_URL,
            DEFAULT_SITE_URL,
        )

        assert DEFAULT_API_BASE_URL == "https://seekstreaming.com/api/v1"
        assert DEFAULT_SITE_URL == "https://seekstreaming.com"

    def test_base_url(self) -> None:
        from streamflow.platforms.streamembed.constants import base_url

        assert base_url() == "https://seekstreaming.com/api/v1"

    def test_site_url(self) -> None:
        from streamflow.platforms.streamembed.constants import site_url

        assert site_url() == "https://seekstreaming.com"

    def test_resolve_base_url(self) -> None:
        from streamflow.platforms.streamembed.constants import resolve_base_url

        assert resolve_base_url(None) == "https://seekstreaming.com/api/v1"
        assert resolve_base_url("https://custom.api") == "https://custom.api"

    def test_advance_upload_endpoint(self) -> None:
        from streamflow.platforms.streamembed.constants import advance_upload_endpoint

        assert (
            advance_upload_endpoint()
            == "https://seekstreaming.com/api/v1/video/advance-upload"
        )
        assert (
            advance_upload_endpoint("https://custom.api")
            == "https://custom.api/video/advance-upload"
        )

    def test_advance_upload_detail_endpoint(self) -> None:
        from streamflow.platforms.streamembed.constants import advance_upload_detail_endpoint

        task_id = "abc123"
        assert (
            advance_upload_detail_endpoint(task_id)
            == "https://seekstreaming.com/api/v1/video/advance-upload/abc123"
        )
        assert (
            advance_upload_detail_endpoint(task_id, "https://custom.api")
            == "https://custom.api/video/advance-upload/abc123"
        )


class TeststreamembedModels:
    """Test models module."""

    def test_video_info_creation(self) -> None:
        from streamflow.platforms.streamembed.models import VideoInfo

        video = VideoInfo(video_id="test123")
        assert video.video_id == "test123"

    def test_video_info_to_dict(self) -> None:
        from dataclasses import asdict

        from streamflow.platforms.streamembed.models import VideoInfo

        video = VideoInfo(video_id="test123")
        data = asdict(video)
        assert data == {"video_id": "test123"}

    def test_video_info_from_dict(self) -> None:
        from streamflow.platforms.streamembed.models import VideoInfo

        data = {"videoId": "test123"}
        video = VideoInfo.from_dict(data)
        assert video.video_id == "test123"

    def test_advance_upload_response(self) -> None:
        from streamflow.platforms.streamembed.models import AdvanceUploadResponse

        response = AdvanceUploadResponse(id="task123")
        assert response.id == "task123"

    def test_advance_upload_detail_response(self) -> None:
        from streamflow.platforms.streamembed.models import AdvanceUploadDetailResponse

        detail = AdvanceUploadDetailResponse(
            id="task123",
            name="Test Video",
            status="completed",
            videos=["vid1", "vid2"],
            updated_at="2024-01-01",
            created_at="2024-01-01",
        )
        assert detail.id == "task123"
        assert detail.name == "Test Video"
        assert detail.status == "completed"
        assert detail.videos == ["vid1", "vid2"]


class TeststreamembedHelp:
    """Test help module."""

    def test_platform_name(self) -> None:
        from streamflow.platforms.streamembed.help import PLATFORM_NAME

        assert PLATFORM_NAME == "streamembed"

    def test_platform_title(self) -> None:
        from streamflow.platforms.streamembed.help import PLATFORM_TITLE

        assert PLATFORM_TITLE == "StreamEmbed Platform"

    def test_build_help_text(self) -> None:
        from streamflow.platforms.streamembed.help import build_help_text

        help_text = build_help_text()
        assert "streamembed" in help_text
        assert "seekstreaming" in help_text.lower()
        assert "--api-key" in help_text
        assert "--url" in help_text

    def test_get_help(self) -> None:
        from streamflow.platforms.streamembed.help import get_help

        help_text = get_help()
        assert "streamembed" in help_text

    def test_show_help(self) -> None:
        from streamflow.platforms.streamembed.help import show_help
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        show_help()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        assert "streamembed" in output


class TeststreamembedClient:
    """Test client module."""

    def test_client_initialization(self) -> None:
        from streamflow.platforms.streamembed.client import StreamembedClient

        client = StreamembedClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://seekstreaming.com/api/v1"
        assert client.timeout == 30.0
        assert client.tcp_proxy is None
        assert client.udp_proxy is None
        assert client.local_address is None

    def test_client_custom_base_url(self) -> None:
        from streamflow.platforms.streamembed.client import StreamembedClient

        client = StreamembedClient(api_key="test_key", base_url="https://custom.api")
        assert client.base_url == "https://custom.api"

    def test_client_proxy_options(self) -> None:
        from streamflow.platforms.streamembed.client import StreamembedClient

        client = StreamembedClient(
            api_key="test_key",
            tcp_proxy="http://proxy:8080",
            udp_proxy="socks5://proxy:1080",
            local_address="192.168.1.100",
        )
        assert client.tcp_proxy == "http://proxy:8080"
        assert client.udp_proxy == "socks5://proxy:1080"
        assert client.local_address == "192.168.1.100"


class TeststreamembedMasterLink:
    """Test master link module."""

    def test_master_link_model(self) -> None:
        from streamflow.platforms.streamembed.models import StreamembedMasterLink

        ml = StreamembedMasterLink(
            filecode="abc123",
            title="Test Video",
            streaming_url="https://example.com/master.m3u8",
            thumbnail="https://example.com/thumb.jpg",
        )
        assert ml.filecode == "abc123"
        assert ml.title == "Test Video"
        assert ml.streaming_url == "https://example.com/master.m3u8"
        assert ml.thumbnail == "https://example.com/thumb.jpg"

    def test_master_link_model_optional_fields(self) -> None:
        from streamflow.platforms.streamembed.models import StreamembedMasterLink

        ml = StreamembedMasterLink(
            filecode="abc123",
            title=None,
            streaming_url="https://example.com/master.m3u8",
            thumbnail=None,
        )
        assert ml.filecode == "abc123"
        assert ml.title is None
        assert ml.streaming_url == "https://example.com/master.m3u8"
        assert ml.thumbnail is None

    def test_get_master_link_import(self) -> None:
        from streamflow.platforms.streamembed import get_master_link

        assert callable(get_master_link)

    def test_aes_constants(self) -> None:
        from streamflow.platforms.streamembed.master_link import AES_KEY_HEX, AES_IV_HEX

        assert AES_KEY_HEX == "6b69656d7469656e6d75613931316361"
        assert AES_IV_HEX == "313233343536373839306f6975797472"

    def test_streamembed_live_master_link(self) -> None:
        """Test streamembed get_master_link with a real filecode."""
        from streamflow.platforms.streamembed import get_master_link

        stream = get_master_link("5axmz")
        assert stream.filecode == "5axmz"
        # streaming_url may be empty if API fails, but model should be returned
        assert isinstance(stream.streaming_url, str)
