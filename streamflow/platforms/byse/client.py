"""Byse API client."""

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.platforms.byse.constants import resolve_base_url
from streamflow.platforms.byse.models import (
    AccountStatsResponse,
    FileDeleteResponse,
    FileListResponse,
    PurgeAllResult,
    RemoteAddResponse,
)


class ByseClient:
    """Byse API client."""

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

    def add_remote(self, url: str) -> RemoteAddResponse:
        """Add remote upload to queue."""
        from streamflow.platforms.byse.api import add_remote_upload

        return add_remote_upload(
            self.api_key,
            url,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def account_stats(self, *, last: int = 7) -> AccountStatsResponse:
        """Get account statistics."""
        from streamflow.platforms.byse.api import get_account_stats

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
        fld_id: int = 0,
        title: str | None = None,
        created: str | None = None,
        public: int | None = None,
        per_page: int = 20,
        page: int = 1,
    ) -> FileListResponse:
        """List files with optional filters."""
        from streamflow.platforms.byse.api import list_files

        return list_files(
            self.api_key,
            fld_id=fld_id,
            title=title,
            created=created,
            public=public,
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
        """Delete a file by file code."""
        from streamflow.platforms.byse.api import delete_file

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

    def purge_all(self, *, fld_id: int = 0, per_page: int = 100) -> PurgeAllResult:
        """Delete all files in account/folder."""
        from streamflow.platforms.byse.api import purge_all_files

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