"""Tests for Anonstream platform."""

import pytest

from streamflow.platforms.anonstream.constants import DEFAULT_BASE_URL
from streamflow.platforms.anonstream.help import get_help
from streamflow.platforms.registry import list_platforms, show_help


def test_list_platforms_includes_anonstream() -> None:
    """Test that anonstream is included in list_platforms."""
    platforms = list_platforms()
    assert "anonstream" in platforms


def test_show_help_anonstream() -> None:
    """Test that show_help('anonstream') runs without error."""
    show_help("anonstream")


def test_anonstream_help_content() -> None:
    """Test that help contains expected content."""
    text = get_help()
    assert "anonstream" in text.lower()
    assert "upload" in text.lower()


def test_anonstream_default_base_url() -> None:
    """Test that DEFAULT_BASE_URL is correctly set."""
    assert DEFAULT_BASE_URL == "https://anonstream.co"