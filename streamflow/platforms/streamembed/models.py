"""Streamembed response models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class StreamembedAPIError(Exception):
    """API error exception."""

    message: str
    status_code: int | None = None

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


@dataclass
class AdvanceUploadResponse:
    """Response from advance upload creation."""

    id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AdvanceUploadResponse:
        return cls(id=data.get("id", ""))


@dataclass
class VideoInfo:
    """Video info from task detail."""

    video_id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VideoInfo:
        return cls(video_id=data.get("videoId", ""))


@dataclass
class AdvanceUploadDetailResponse:
    """Response from advance upload task detail."""

    id: str
    name: str | None
    status: str
    videos: list[str]
    updated_at: str | None
    created_at: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AdvanceUploadDetailResponse:
        videos = data.get("videos", [])
        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            status=data.get("status", ""),
            videos=videos,
            updated_at=data.get("updatedAt"),
            created_at=data.get("createdAt"),
        )


# FileItem alias for consistent API across platforms
FileItem = VideoInfo


@dataclass
class StreamembedMasterLink:
    """Master link response for StreamEmbed video."""

    filecode: str
    title: str | None
    streaming_url: str
    thumbnail: str | None
    master_url: str | None = None
    cf_url: str | None = None
    swarm_id: str | None = None
    torrent_trackers: list[str] | None = None
    ice_servers: list[dict] | None = None
