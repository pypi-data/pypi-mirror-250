import uuid
from datetime import timedelta
from typing import Callable, ClassVar


class Config:
    token: str | None = None
    token_location: ClassVar[set[str]] = {"headers"}

    secret_key: str | None
    public_key: str | None = None
    private_key: str | None = None
    algorithm: str = "HS256"
    decode_algorithms: list[str] | None = None
    decode_leeway: timedelta | str = 0
    encode_issuer: str | None = None
    decode_issuer: str | None = None
    decode_audience: str | None = None
    deny_list_enabled: bool | None = False
    deny_list_token_checks: ClassVar[set[str]] = {"access", "refresh"}
    header_name: str | None = "Authorization"
    header_type: str | None = "Bearer"
    token_in_deny_list_callback: Callable[..., bool] = None
    access_token_expires: bool | int | timedelta = timedelta(minutes=60)
    refresh_token_expires: bool | int | timedelta = timedelta(days=30)

    # option for create cookies
    access_cookie_key: str | None = "access_token_cookie"
    refresh_cookie_key: str | None = "refresh_token_cookie"
    access_cookie_path: str | None = "/"
    refresh_cookie_path: str | None = "/"
    cookie_max_age: str | None = None
    cookie_domain: str | None = None
    cookie_secure: bool | None = False
    cookie_same_site: str | None = None

    # option for double submit csrf protection
    cookie_csrf_protect: bool | None = True
    access_csrf_cookie_key: str | None = "csrf_access_token"
    refresh_csrf_cookie_key: str | None = "csrf_refresh_token"
    access_csrf_cookie_path: str | None = "/"
    refresh_csrf_cookie_path: str | None = "/"
    access_csrf_header_name: str | None = "X-CSRF-Token"
    refresh_csrf_header_name: str | None = "X-CSRF-Token"
    csrf_methods: ClassVar[set[str]] = {"POST", "PUT", "PATCH", "DELETE"}

    @property
    def jwt_in_cookies(self) -> bool:
        return "cookies" in self.token_location

    @property
    def jwt_in_headers(self) -> bool:
        return "headers" in self.token_location

    @classmethod
    def token_in_deny_list_loader(cls: type["Config"], callback: Callable[..., bool]) -> None:
        cls.token_in_deny_list_callback = callback

    @staticmethod
    def _get_jwt_identifier() -> str:
        return str(uuid.uuid4())
