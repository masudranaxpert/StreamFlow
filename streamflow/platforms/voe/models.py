from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class UploadUrlResult:
    file_code: str
    queue_id: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadUrlResult:
        return cls(
            file_code=str(payload["file_code"]),
            queue_id=int(payload["queueID"]),
        )


@dataclass(frozen=True, slots=True)
class UploadUrlResponse:
    server_time: str
    msg: str
    message: str
    status: int
    success: bool
    result: UploadUrlResult

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadUrlResponse:
        return cls(
            server_time=str(payload["server_time"]),
            msg=str(payload["msg"]),
            message=str(payload["message"]),
            status=int(payload["status"]),
            success=bool(payload["success"]),
            result=UploadUrlResult.from_dict(payload["result"]),
        )


@dataclass(frozen=True, slots=True)
class UploadServerResponse:
    server_time: str
    msg: str
    message: str
    status: int
    success: bool
    result: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadServerResponse:
        return cls(
            server_time=str(payload["server_time"]),
            msg=str(payload["msg"]),
            message=str(payload["message"]),
            status=int(payload["status"]),
            success=bool(payload["success"]),
            result=str(payload["result"]),
        )


@dataclass(frozen=True, slots=True)
class AccountStatsResponse:
    server_time: str
    msg: str
    message: str
    status: int
    success: bool
    result: dict[str, dict[str, Any]]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> AccountStatsResponse:
        result = payload.get("result", {})
        if not isinstance(result, dict):
            result = {}
        return cls(
            server_time=str(payload["server_time"]),
            msg=str(payload["msg"]),
            message=str(payload["message"]),
            status=int(payload["status"]),
            success=bool(payload["success"]),
            result=result,
        )


@dataclass(frozen=True, slots=True)
class FileItem:
    filecode: str
    name: str
    title: str
    uploaded: str
    size: int
    file_money: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FileItem:
        return cls(
            filecode=str(payload["filecode"]),
            name=str(payload["name"]),
            title=str(payload["title"]),
            uploaded=str(payload["uploaded"]),
            size=int(payload.get("size", 0)),
            file_money=str(payload.get("file_money", "")),
        )


@dataclass(frozen=True, slots=True)
class FileListResult:
    current_page: int
    data: tuple[FileItem, ...]
    last_page: int
    total: int
    per_page: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FileListResult:
        items = tuple(FileItem.from_dict(item) for item in payload.get("data", []))
        return cls(
            current_page=int(payload.get("current_page", 1)),
            data=items,
            last_page=int(payload.get("last_page", 1)),
            total=int(payload.get("total", len(items))),
            per_page=int(payload.get("per_page", len(items))),
        )


@dataclass(frozen=True, slots=True)
class FileListResponse:
    server_time: str
    msg: str
    message: str
    status: int
    success: bool
    result: FileListResult

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FileListResponse:
        return cls(
            server_time=str(payload["server_time"]),
            msg=str(payload["msg"]),
            message=str(payload["message"]),
            status=int(payload["status"]),
            success=bool(payload["success"]),
            result=FileListResult.from_dict(payload["result"]),
        )


@dataclass(frozen=True, slots=True)
class FileDeleteResponse:
    server_time: str
    msg: str
    message: str
    status: int
    success: bool

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> FileDeleteResponse:
        return cls(
            server_time=str(payload["server_time"]),
            msg=str(payload["msg"]),
            message=str(payload["message"]),
            status=int(payload["status"]),
            success=bool(payload["success"]),
        )


@dataclass(frozen=True, slots=True)
class PurgeAllResult:
    deleted: int
    file_codes: tuple[str, ...]
