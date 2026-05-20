"""Anonstream data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class AccountDayStats:
    """Daily account statistics."""
    downloads: int
    profit_views: float
    views_adb: int
    sales: int
    profit_sales: float
    profit_refs: float
    profit_site: float
    views: int
    refs: int
    day: str
    profit_total: float
    views_prem: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AccountDayStats:
        return cls(
            downloads=int(data.get("downloads", 0)),
            profit_views=float(data.get("profit_views", 0)),
            views_adb=int(data.get("views_adb", 0)),
            sales=int(data.get("sales", 0)),
            profit_sales=float(data.get("profit_sales", 0)),
            profit_refs=float(data.get("profit_refs", 0)),
            profit_site=float(data.get("profit_site", 0)),
            views=int(data.get("views", 0)),
            refs=int(data.get("refs", 0)),
            day=str(data.get("day", "")),
            profit_total=float(data.get("profit_total", 0)),
            views_prem=int(data.get("views_prem", 0)),
        )


@dataclass(frozen=True, slots=True)
class AccountStatsResponse:
    """Account stats API response."""
    msg: str
    server_time: str
    status: int
    result: tuple[AccountDayStats, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AccountStatsResponse:
        days = tuple(AccountDayStats.from_dict(d) for d in data.get("result", []))
        return cls(
            msg=str(data.get("msg", "")),
            server_time=str(data.get("server_time", "")),
            status=int(data.get("status", 0)),
            result=days,
        )


@dataclass(frozen=True, slots=True)
class UploadResponse:
    """Upload from URL response."""
    msg: str
    server_time: str
    status: int
    result: UploadResult

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UploadResponse:
        return cls(
            msg=str(data.get("msg", "")),
            server_time=str(data.get("server_time", "")),
            status=int(data.get("status", 0)),
            result=UploadResult.from_dict(data.get("result", {})),
        )


@dataclass(frozen=True, slots=True)
class UploadResult:
    """Upload result data."""
    filecode: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UploadResult:
        return cls(filecode=str(data.get("filecode", "")))


@dataclass(frozen=True, slots=True)
class FileInfo:
    """File info from list response."""
    thumbnail: str
    link: str
    file_code: str
    canplay: int
    length: str
    views: int
    uploaded: str
    public: int
    fld_id: str
    title: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileInfo:
        return cls(
            thumbnail=str(data.get("thumbnail", "")),
            link=str(data.get("link", "")),
            file_code=str(data.get("file_code", "")),
            canplay=int(data.get("canplay", 0)),
            length=str(data.get("length", "")),
            views=int(data.get("views", 0)),
            uploaded=str(data.get("uploaded", "")),
            public=int(data.get("public", 0)),
            fld_id=str(data.get("fld_id", "")),
            title=str(data.get("title", "")),
        )


@dataclass(frozen=True, slots=True)
class FileListResult:
    """File list result data."""
    files: tuple[FileInfo, ...]
    results_total: int
    pages: int
    results: int


@dataclass(frozen=True, slots=True)
class FileListResponse:
    """File list API response."""
    msg: str
    server_time: str
    status: int
    result: FileListResult

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileListResponse:
        result_data = data.get("result", {})
        files = tuple(FileInfo.from_dict(f) for f in result_data.get("files", []))
        return cls(
            msg=str(data.get("msg", "")),
            server_time=str(data.get("server_time", "")),
            status=int(data.get("status", 0)),
            result=FileListResult(
                files=files,
                results_total=int(result_data.get("results_total", 0)),
                pages=int(result_data.get("pages", 0)),
                results=int(result_data.get("results", 0)),
            ),
        )


@dataclass(frozen=True, slots=True)
class FileDeleteResponse:
    """File delete API response."""
    msg: str
    server_time: str
    status: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileDeleteResponse:
        return cls(
            msg=str(data.get("msg", "")),
            server_time=str(data.get("server_time", "")),
            status=int(data.get("status", 0)),
        )


@dataclass
class PurgeAllResult:
    """Result of purge all files operation."""
    deleted: int
    file_codes: tuple[str, ...]
    errors: list[str] = field(default_factory=list)


# Alias for backward compatibility
FileItem = FileInfo