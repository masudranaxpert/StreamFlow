from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class UploadData:
    filecode: str
    title: str
    size: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UploadData:
        filecode = data.get("filecode")
        title = data.get("title")
        size = data.get("size")
        if filecode is None:
            raise ValueError("UploadData: missing 'filecode' field")
        if title is None:
            raise ValueError("UploadData: missing 'title' field")
        if size is None:
            raise ValueError("UploadData: missing 'size' field")
        return cls(filecode=str(filecode), title=str(title), size=int(size))


@dataclass(frozen=True, slots=True)
class UploadResponse:
    msg: str
    status: int
    server_time: str
    data: UploadData

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> UploadResponse:
        data = payload.get("data")
        if not data:
            raise ValueError("UploadResponse: missing 'data' field")
        return cls(
            msg=str(payload.get("msg", "")),
            status=int(payload.get("status", 0)),
            server_time=str(payload.get("server_time", "")),
            data=UploadData.from_dict(data),
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
        filecode = payload.get("filecode")
        streaming_url = payload.get("streaming_url")
        if not filecode:
            raise ValueError("MasterLinkResponse: missing 'filecode' field")
        if not streaming_url:
            raise ValueError("MasterLinkResponse: missing 'streaming_url' field")
        subtitles_data = payload.get("subtitles", [])
        subtitles = tuple(StreamSubtitle.from_dict(item) for item in subtitles_data) if subtitles_data else ()
        return cls(
            filecode=str(filecode),
            streaming_url=str(streaming_url),
            title=str(payload.get("title", "")),
            thumbnail=str(payload.get("thumbnail", "")),
            default_sub_lang=str(payload.get("default_sub_lang", "")),
            vast_ads=str(payload.get("vast_ads", "")),
            subtitles=subtitles,
        )
