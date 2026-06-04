from __future__ import annotations

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.platforms.streamembed.api import (
    DEFAULT_AUTH_HEADER,
    advance_upload,
    get_upload_task,
)
from streamflow.platforms.streamembed.constants import resolve_base_url
from streamflow.platforms.streamembed.models import (
    AdvanceUploadDetailResponse,
    AdvanceUploadResponse,
)


class StreamembedClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        tcp_proxy: str | None = None,
        udp_proxy: str | None = None,
        local_address: str | None = None,
        auth_header: str = DEFAULT_AUTH_HEADER,
    ) -> None:
        self.api_key = api_key
        self.base_url = resolve_base_url(base_url)
        self.timeout = timeout
        self.tcp_proxy = tcp_proxy
        self.udp_proxy = udp_proxy
        self.local_address = local_address
        self.auth_header = auth_header

    def upload(self, url: str, *, name: str | None = None) -> AdvanceUploadResponse:
        return advance_upload(
            self.api_key,
            url,
            name=name,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            auth_header=self.auth_header,
        )

    def get_task(self, task_id: str) -> AdvanceUploadDetailResponse:
        return get_upload_task(
            self.api_key,
            task_id,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            auth_header=self.auth_header,
        )
