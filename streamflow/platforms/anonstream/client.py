"""Anonstream Client."""

from __future__ import annotations

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.platforms.anonstream.api import (
    delete_file,
    get_account_stats,
    list_all_filecodes,
    list_files,
    purge_all_files,
    upload_from_url,
)
from streamflow.platforms.anonstream.constants import resolve_base_url
from streamflow.platforms.anonstream.models import (
    AccountStatsResponse,
    FileDeleteResponse,
    FileListResponse,
    PurgeAllResult,
    UploadResponse,
)


class AnonstreamClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        tcp_proxy: str | None = None,
        udp_proxy: str | None = None,
        local_address: str | None = None,
        http_version: str | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = resolve_base_url(base_url)
        self.timeout = timeout
        self.tcp_proxy = tcp_proxy
        self.udp_proxy = udp_proxy
        self.local_address = local_address
        self.http_version = http_version

    def upload(
        self,
        url: str,
        *,
        fld_id: int | None = None,
        cat_id: int | None = None,
        file_public: int | None = None,
        file_adult: int | None = None,
        tags: str | None = None,
    ) -> UploadResponse:
        return upload_from_url(
            self.api_key,
            url,
            fld_id=fld_id,
            cat_id=cat_id,
            file_public=file_public,
            file_adult=file_adult,
            tags=tags,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def account_stats(self, *, last: int = 7) -> AccountStatsResponse:
        return get_account_stats(
            self.api_key,
            last=last,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def list_files(
        self,
        *,
        fld_id: int | None = None,
        title: str | None = None,
        created: str | None = None,
        public: int | None = None,
        adult: int | None = None,
        per_page: int = 20,
        page: int = 1,
    ) -> FileListResponse:
        return list_files(
            self.api_key,
            fld_id=fld_id,
            title=title,
            created=created,
            public=public,
            adult=adult,
            per_page=per_page,
            page=page,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def delete_file(self, file_code: str) -> FileDeleteResponse:
        return delete_file(
            self.api_key,
            file_code,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def purge_all(self, *, fld_id: int | None = None, per_page: int = 100) -> PurgeAllResult:
        return purge_all_files(
            self.api_key,
            fld_id=fld_id,
            per_page=per_page,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )