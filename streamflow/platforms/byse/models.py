"""Byse API response models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AccountStatsItem:
    """Daily account statistics."""
    downloads: str
    profit_views: str
    views_adb: str
    sales: str
    profit_sales: str
    profit_refs: str
    profit_site: str
    views: str
    refs: str
    day: str
    profit_total: str
    views_prem: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AccountStatsItem:
        return cls(
            downloads=data.get("downloads", "0"),
            profit_views=data.get("profit_views", "0"),
            views_adb=data.get("views_adb", "0"),
            sales=data.get("sales", "0"),
            profit_sales=data.get("profit_sales", "0"),
            profit_refs=data.get("profit_refs", "0"),
            profit_site=data.get("profit_site", "0"),
            views=data.get("views", "0"),
            refs=data.get("refs", "0"),
            day=data.get("day", ""),
            profit_total=data.get("profit_total", "0"),
            views_prem=data.get("views_prem", "0"),
        )


@dataclass
class AccountStatsResponse:
    """Account statistics response."""
    msg: str
    server_time: str
    status: int
    result: list[AccountStatsItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AccountStatsResponse:
        result_items = [AccountStatsItem.from_dict(item) for item in data.get("result", [])]
        return cls(
            msg=data.get("msg", ""),
            server_time=data.get("server_time", ""),
            status=int(data.get("status", 0)),
            result=result_items,
        )


@dataclass
class RemoteAddResponse:
    """Remote upload add response."""
    msg: str
    server_time: str
    status: int
    filecode: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RemoteAddResponse:
        result = data.get("result", {})
        return cls(
            msg=data.get("msg", ""),
            server_time=data.get("server_time", ""),
            status=int(data.get("status", 0)),
            filecode=result.get("filecode", ""),
        )


@dataclass
class FileItem:
    """File list item."""
    status: int
    filecode: str
    name: str | None = None
    canplay: int | None = None
    views_started: str | None = None
    views: str | None = None
    length: str | None = None
    uploaded: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileItem:
        return cls(
            status=int(data.get("status", 0)),
            filecode=data.get("filecode", ""),
            name=data.get("name"),
            canplay=data.get("canplay"),
            views_started=data.get("views_started"),
            views=data.get("views"),
            length=data.get("length"),
            uploaded=data.get("uploaded"),
        )


@dataclass
class FileListResponse:
    """File list response."""
    msg: str
    server_time: str
    status: int
    result: list[FileItem]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileListResponse:
        result_items = [FileItem.from_dict(item) for item in data.get("result", [])]
        return cls(
            msg=data.get("msg", ""),
            server_time=data.get("server_time", ""),
            status=int(data.get("status", 0)),
            result=result_items,
        )


@dataclass
class FileDeleteResponse:
    """File delete response."""
    msg: str
    server_time: str
    status: int
    result: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileDeleteResponse:
        return cls(
            msg=data.get("msg", ""),
            server_time=data.get("server_time", ""),
            status=int(data.get("status", 0)),
            result=data.get("result", {}),
        )


@dataclass
class PurgeAllResult:
    """Result of purge_all operation."""
    deleted: int
    file_codes: tuple[str, ...]
    errors: list[str] = field(default_factory=list)