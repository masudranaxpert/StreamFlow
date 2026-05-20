"""Tests for Byse platform."""

import pytest

from streamflow.platforms.byse.constants import DEFAULT_BASE_URL
from streamflow.platforms.byse.help import get_help
from streamflow.platforms.registry import list_platforms, show_help


def test_list_platforms_includes_byse() -> None:
    """Test that byse is included in list_platforms."""
    platforms = list_platforms()
    assert "byse" in platforms


def test_show_help_byse() -> None:
    """Test that show_help('byse') runs without error."""
    show_help("byse")


def test_byse_help_content() -> None:
    """Test that help contains expected content."""
    text = get_help()
    assert "byse" in text.lower()
    assert "upload" in text.lower()
    assert "account" in text.lower()


def test_byse_default_base_url() -> None:
    """Test that DEFAULT_BASE_URL is correctly set."""
    assert DEFAULT_BASE_URL == "https://api.byse.sx"


def test_byse_help_custom_base_url() -> None:
    """Test that help works with custom base URL."""
    custom_url = "https://custom.byse.sx"
    text = get_help(base_url=custom_url)
    assert custom_url in text
