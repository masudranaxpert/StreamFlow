from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class UploadData:
    filecode: str
    title: str
    size: int


@dataclass(frozen=True, slots=True)
class UploadResponse:
    msg: str
    status: int
    server_time: str
    data: UploadData

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadResponse:
        data = payload["data"]
        return cls(
            msg=str(payload["msg"]),
            status=int(payload["status"]),
            server_time=str(payload["server_time"]),
            data=UploadData(
                filecode=str(data["filecode"]),
                title=str(data["title"]),
                size=int(data["size"]),
            ),
        )


@dataclass(frozen=True, slots=True)
class UploadServerResult:
    upload_server: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadServerResult:
        return cls(upload_server=str(payload["upload_server"]))


@dataclass(frozen=True, slots=True)
class UploadServerResponse:
    msg: str
    status: int
    result: UploadServerResult

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadServerResponse:
        return cls(
            msg=str(payload["msg"]),
            status=int(payload["status"]),
            result=UploadServerResult.from_dict(payload["result"]),
        )


@dataclass(frozen=True, slots=True)
class StreamSubtitle:
    id: int
    status: int
    file_id: int
    type: int
    file_path: str
    language: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> StreamSubtitle:
        return cls(
            id=int(payload["id"]),
            status=int(payload["status"]),
            file_id=int(payload["file_id"]),
            type=int(payload["type"]),
            file_path=str(payload["file_path"]),
            language=str(payload["language"]),
        )


@dataclass(frozen=True, slots=True)
class MasterLinkResponse:
    filecode: str
    streaming_url: str
    title: str
    thumbnail: str
    default_sub_lang: str
    vast_ads: str
    subtitles: tuple[StreamSubtitle, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MasterLinkResponse:
        subtitles = tuple(StreamSubtitle.from_dict(item) for item in payload.get("subtitles", []))
        return cls(
            filecode=str(payload["filecode"]),
            streaming_url=str(payload["streaming_url"]),
            title=str(payload["title"]),
            thumbnail=str(payload["thumbnail"]),
            default_sub_lang=str(payload.get("default_sub_lang", "")),
            vast_ads=str(payload.get("vast_ads", "")),
            subtitles=subtitles,
        )
