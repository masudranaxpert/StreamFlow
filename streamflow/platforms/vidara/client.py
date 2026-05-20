from __future__ import annotations

from streamflow.constants import DEFAULT_TIMEOUT
from streamflow.platforms.vidara.api import upload_from_url
from streamflow.platforms.vidara.constants import resolve_base_url, resolve_site_base_url
from streamflow.platforms.vidara.master_link import get_master_link
from streamflow.platforms.vidara.models import MasterLinkResponse, UploadResponse, UploadServerResponse
from streamflow.platforms.vidara.upload_server import get_upload_server


class VidaraClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
        site_base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        tcp_proxy: str | None = None,
        udp_proxy: str | None = None,
        local_address: str | None = None,
        http_version: str | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = resolve_base_url(base_url)
        self.site_base_url = resolve_site_base_url(site_base_url)
        self.timeout = timeout
        self.tcp_proxy = tcp_proxy
        self.udp_proxy = udp_proxy
        self.local_address = local_address
        self.http_version = http_version

    def upload(self, url: str) -> UploadResponse:
        return upload_from_url(
            self.api_key,
            url,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def upload_server(self) -> UploadServerResponse:
        return get_upload_server(
            self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def master_link(
        self,
        filecode: str,
        *,
        device: str = "web",
        cookie: str | None = None,
    ) -> MasterLinkResponse:
        return get_master_link(
            filecode,
            device=device,
            site_base_url=self.site_base_url,
            cookie=cookie,
            timeout=self.timeout,
            tcp_proxy=self.tcp_proxy,
            udp_proxy=self.udp_proxy,
            local_address=self.local_address,
            http_version=self.http_version,
        )

    def embed_url(self, filecode: str) -> str:
        return f"{self.site_base_url}/e/{filecode}"
