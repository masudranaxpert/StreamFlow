from __future__ import annotations

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.platforms.voe.api import (
    delete_files,
    get_account_stats,
    get_upload_server,
    list_all_filecodes,
    list_files,
    purge_all_files,
    upload_from_url,
)
from streamflow.platforms.voe.constants import resolve_base_url
from streamflow.platforms.voe.models import (
    AccountStatsResponse,
    FileDeleteResponse,
    FileListResponse,
    PurgeAllResult,
    UploadServerResponse,
    UploadUrlResponse,
)


class VoeClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        tcp_proxy: str | None = None,
        udp_proxy: str | None = None,
        local_address: str | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = resolve_base_url(base_url)
        self.timeout = timeout
        self.tcp_proxy = tcp_proxy
        self.udp_proxy = udp_proxy
        self.local_address = local_address

    def upload(self, url: str, *, folder_id: int | None = None) -> UploadUrlResponse:
        return upload_from_url(
            self.api_key,
            url,
            folder_id=folder_id,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )

    def upload_server(self) -> UploadServerResponse:
        return get_upload_server(
            self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )

    def account_stats(self) -> AccountStatsResponse:
        return get_account_stats(
            self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )

    def list_files(
        self,
        *,
        page: int = 1,
        per_page: int = 100,
        fld_id: int = 0,
        created: str | None = None,
        name: str | None = None,
        preview: bool | None = None,
    ) -> FileListResponse:
        return list_files(
            self.api_key,
            page=page,
            per_page=per_page,
            fld_id=fld_id,
            created=created,
            name=name,
            preview=preview,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )

    def delete_files(self, del_code: str) -> FileDeleteResponse:
        return delete_files(
            self.api_key,
            del_code,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )

    def purge_all(self, *, fld_id: int = 0, per_page: int = 100) -> PurgeAllResult:
        return purge_all_files(
            self.api_key,
            fld_id=fld_id,
            per_page=per_page,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
        )
