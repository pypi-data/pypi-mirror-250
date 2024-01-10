import hmac
import re
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Request, Response, WebSocket
from jwt.algorithms import has_crypto, requires_cryptography

from .config import Config
from .exceptions import (
    AccessTokenRequiredError,
    AuthError,
    CSRFError,
    FreshTokenRequiredError,
    InvalidHeaderError,
    MissingTokenError,
    RefreshTokenRequiredError,
    RevokedTokenError,
)


class EntityAuth(Config):
    def __init__(self, req: Request = None, res: Response = None) -> None:
        if res and self.jwt_in_cookies:
            self._response = res

        if req:
            if self.jwt_in_cookies:
                self._request = req
            if self.jwt_in_headers:
                auth = req.headers.get(self.header_name.lower())
                if auth:
                    self._get_jwt_from_headers(auth)

    def _get_jwt_from_headers(self, auth: str) -> None:
        header_name, header_type = self.header_name, self.header_type

        parts = auth.split()

        if not header_type:
            if len(parts) != 1:
                raise InvalidHeaderError(
                    status_code=422,
                    message=f"Invalid {header_name} header. The expected value was <JWT>",
                )
            self.token = parts[0]
        else:
            expected_parts_count = 2

            if not re.match(rf"{header_type}\s", auth) or len(parts) != expected_parts_count:
                raise InvalidHeaderError(
                    status_code=422,
                    message=f"Invalid {header_name} header. The expected value was {header_type} <JWT>",
                )
            self.token = parts[1]



    @staticmethod
    def _get_int_from_datetime(value: datetime) -> int:
        if not isinstance(value, datetime):
            msg = "A datetime object is required"
            raise TypeError(msg)
        return int(value.timestamp())

    def _get_secret_key(self, algorithm: str, process: str) -> str | None:
        symmetric_algorithms, asymmetric_algorithms = {"HS256", "HS384", "HS512"}, requires_cryptography

        if algorithm not in symmetric_algorithms and algorithm not in asymmetric_algorithms:
            msg = f"The {algorithm} algorithm was not found"
            raise ValueError(msg)

        if algorithm in symmetric_algorithms:
            if not self.secret_key:
                msg = f"auth_jwt_secret_key must be set when using the symmetric algorithm {algorithm}"
                raise RuntimeError(msg)

            return self.secret_key

        if algorithm in asymmetric_algorithms and not has_crypto:
            msg = "There are no dependencies for using asymmetric algorithms. Run 'pip install pyjwt[asymmetric]'"
            raise RuntimeError(msg)

        if process == "encode":
            if not self.private_key:
                msg = f"auth_jwt_private_key must be set when using the asymmetric algorithm {algorithm}"
                raise RuntimeError(msg)

            return self.private_key

        if process == "decode":
            if not self.public_key:
                msg = f"auth_jwt_public_key must be set when using the asymmetric algorithm {algorithm}"
                raise RuntimeError(msg)

            return self.public_key
        return None

    def _create_token(
            self, subject: str | int, type_token: str, exp_time: int | None, fresh: bool | None = None,
            algorithm: str | None = None, headers: dict | None = None, issuer: str | None = None,
            audience: str | None = None, user_claims: dict | None = None,
    ) -> str:
        access_type = "access"

        if user_claims is None:
            user_claims = {}

        if fresh is None:
            fresh = False

        if not isinstance(subject, (str, int)):
            msg = "the subject must be a string or an integer"
            raise TypeError(msg)
        if not isinstance(fresh, bool):
            msg = "fresh must be a boolean value"
            raise TypeError(msg)
        if audience and not isinstance(audience, (str, list, tuple, set, frozenset)):
            msg = "audience must be a string or sequence"
            raise TypeError(msg)
        if algorithm and not isinstance(algorithm, str):
            msg = "The algorithm must be a string"
            raise TypeError(msg)
        if user_claims and not isinstance(user_claims, dict):
            msg = "user_claims should be a dictionary"
            raise TypeError(msg)

        reserved_claims = {
            "sub": subject,
            "iat": self._get_int_from_datetime(datetime.now(timezone.utc)),
            "nbf": self._get_int_from_datetime(datetime.now(timezone.utc)),
            "jti": self._get_jwt_identifier(),
        }

        custom_claims = {"type": type_token}

        if type_token == access_type:
            custom_claims["fresh"] = fresh

        if self.jwt_in_cookies and self.cookie_csrf_protect:
            custom_claims["csrf"] = self._get_jwt_identifier()

        if exp_time:
            reserved_claims["exp"] = exp_time
        if issuer:
            reserved_claims["iss"] = issuer
        if audience:
            reserved_claims["aud"] = audience

        algorithm = algorithm or self.algorithm

        secret_key = self._get_secret_key(algorithm, "encode")

        return jwt.encode(
            {**reserved_claims, **custom_claims, **user_claims},
            secret_key,
            algorithm=algorithm,
            headers=headers,
        )

    def _has_token_in_deny_list_callback(self) -> bool:
        return self.token_in_deny_list_callback is not None

    def _check_token_is_revoked(self, raw_token: dict) -> None:
        if not self.deny_list_enabled:
            return

        if not self._has_token_in_deny_list_callback():
            msg = "The callback is required when the option 'auth_jwt_deny_list_enabled' is set to 'True'"
            raise RuntimeError(msg)

        if self.token_in_deny_list_callback(raw_token):
            raise RevokedTokenError(status_code=401, message="The token has been revoked")

    def _get_expired_time(
            self,
            type_token: str,
            expires_time: timedelta | int | bool | None = None,
    ) -> int | None:
        access_type = "access"
        refresh_type = "refresh"

        if expires_time and not isinstance(expires_time, (timedelta, int, bool)):
            msg = "expires_time must be of the timedelta, int, or bool type"
            raise TypeError(msg)

        if expires_time is not False:
            if type_token == access_type:
                expires_time = expires_time or self.access_token_expires
            if type_token == refresh_type:
                expires_time = expires_time or self.refresh_token_expires

        if expires_time is not False:
            if isinstance(expires_time, bool):
                if type_token == access_type:
                    expires_time = self.access_token_expires
                if type_token == refresh_type:
                    expires_time = self.refresh_token_expires
            if isinstance(expires_time, timedelta):
                expires_time = int(expires_time.total_seconds())

            return self._get_int_from_datetime(datetime.now(timezone.utc)) + expires_time
        return None

    def create_access_token(
            self,
            subject: str | int,
            fresh: bool | None = None,
            algorithm: str | None = None,
            headers: dict | None = None,
            expires_time: timedelta | int | str | None = None,
            audience: str | None = None,
            user_claims: dict | None = None,
    ) -> str:
        if fresh is None:
            fresh = False

        if user_claims is None:
            user_claims = {}

        type_access = "access"

        return self._create_token(
            subject=subject,
            type_token=type_access,
            exp_time=self._get_expired_time(type_access, expires_time),
            fresh=fresh,
            algorithm=algorithm,
            headers=headers,
            audience=audience,
            user_claims=user_claims,
            issuer=self.encode_issuer,
        )

    def create_refresh_token(
            self,
            subject: str | int,
            algorithm: str | None = None,
            headers: dict | None = None,
            expires_time: timedelta | int | bool | None = None,
            audience: str | None = None,
            user_claims: dict | None = None,
    ) -> str:
        type_refresh = "refresh"
        return self._create_token(
            subject=subject,
            type_token=type_refresh,
            exp_time=self._get_expired_time(type_refresh, expires_time),
            algorithm=algorithm,
            headers=headers,
            audience=audience,
            user_claims=user_claims,
        )

    def _get_csrf_token(self, encoded_token: str) -> str:
        return self._verified_token(encoded_token)["csrf"]

    def set_access_cookies(
            self,
            encoded_access_token: str,
            response: Response | None = None,
            max_age: int | None = None,
    ) -> None:
        if not self.jwt_in_cookies:
            msg = "set_access_cookies() is called without setting 'auth_jwt_token_location' to use cookies"
            raise RuntimeWarning(msg)

        if max_age and not isinstance(max_age, int):
            msg = "max_age must be an integer"
            raise TypeError(msg)
        if response and not isinstance(response, Response):
            msg = "response must be a FastAPI response object"
            raise TypeError(msg)

        response = response or self._response

        response.set_cookie(
            self.access_cookie_key,
            encoded_access_token,
            max_age=max_age or self.cookie_max_age,
            path=self.access_cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=True,
            samesite=self.cookie_same_site,
        )

        if self.cookie_csrf_protect:
            response.set_cookie(
                self.access_csrf_cookie_key,
                self._get_csrf_token(encoded_access_token),
                max_age=max_age or self.cookie_max_age,
                path=self.access_csrf_cookie_path,
                domain=self.cookie_domain,
                secure=self.cookie_secure,
                httponly=False,
                samesite=self.cookie_same_site,
            )

    def set_refresh_cookies(
            self,
            encoded_refresh_token: str,
            response: Response | None = None,
            max_age: int | None = None,
    ) -> None:
        if not self.jwt_in_cookies:
            msg = "set_refresh_cookies() is called without setting 'auth_jwt_token_location' to use cookies"
            raise RuntimeWarning(msg)

        if max_age and not isinstance(max_age, int):
            msg = "max_age must be an integer"
            raise TypeError(msg)
        if response and not isinstance(response, Response):
            msg = "response must be a FastAPI response object"
            raise TypeError(msg)

        response = response or self._response

        response.set_cookie(
            self.refresh_cookie_key,
            encoded_refresh_token,
            max_age=max_age or self.cookie_max_age,
            path=self.refresh_cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=True,
            samesite=self.cookie_same_site,
        )

        if self.cookie_csrf_protect:
            response.set_cookie(
                self.refresh_csrf_cookie_key,
                self._get_csrf_token(encoded_refresh_token),
                max_age=max_age or self.cookie_max_age,
                path=self.refresh_csrf_cookie_path,
                domain=self.cookie_domain,
                secure=self.cookie_secure,
                httponly=False,
                samesite=self.cookie_same_site,
            )

    def unset_jwt_cookies(self, response: Response | None = None) -> None:
        self.unset_access_cookies(response)
        self.unset_refresh_cookies(response)

    def unset_access_cookies(self, response: Response | None = None) -> None:
        if not self.jwt_in_cookies:
            msg = "unset_access_cookies() called without 'auth_jwt_token_location' configured to use cookies"
            raise RuntimeWarning(
                msg,
            )

        if response and not isinstance(response, Response):
            msg = "The response must be an object response FastAPI"
            raise TypeError(msg)

        response = response or self._response

        response.delete_cookie(
            self.access_cookie_key,
            path=self.access_cookie_path,
            domain=self.cookie_domain,
        )

        if self.cookie_csrf_protect:
            response.delete_cookie(
                self.access_csrf_cookie_key,
                path=self.access_csrf_cookie_path,
                domain=self.cookie_domain,
            )

    def unset_refresh_cookies(self, response: Response | None = None) -> None:
        if not self.jwt_in_cookies:
            msg = "unset_refresh_cookies() called without 'auth_jwt_token_location' configured to use cookies"
            raise RuntimeWarning(msg)

        if response and not isinstance(response, Response):
            msg = "The response must be an object response FastAPI"
            raise TypeError(msg)

        response = response or self._response

        response.delete_cookie(
            self.refresh_cookie_key,
            path=self.refresh_cookie_path,
            domain=self.cookie_domain,
        )

        if self.cookie_csrf_protect:
            response.delete_cookie(
                self.refresh_csrf_cookie_key,
                path=self.refresh_csrf_cookie_path,
                domain=self.cookie_domain,
            )

    def _verify_and_get_jwt_optional_in_cookies(
            self,
            request: Request | WebSocket,
            csrf_token: str | None = None,
    ) -> None:
        if not isinstance(request, (Request, WebSocket)):
            msg = "request must be an instance of 'Request' or 'WebSocket'"
            raise TypeError(msg)

        cookie_key = self.access_cookie_key
        cookie = request.cookies.get(cookie_key)
        if not isinstance(request, WebSocket):
            csrf_token = request.headers.get(self.access_csrf_header_name)

        if self.cookie_csrf_protect and not csrf_token and (
                isinstance(request, WebSocket) or request.method in self.csrf_methods
        ):
            raise CSRFError(status_code=401, message="Missing CSRF Token")

        self.token = cookie
        self._verify_jwt_optional_in_request(self.token)

        decoded_token = self.get_raw_jwt()

        if (
                decoded_token
                and self.cookie_csrf_protect
                and csrf_token
                and (isinstance(request, WebSocket) or request.method in self.csrf_methods)
                and "csrf" not in decoded_token
                and not hmac.compare_digest(csrf_token, decoded_token["csrf"])
        ):
            raise CSRFError(status_code=401, message="CSRF double submit tokens do not match")

    def _verify_and_get_jwt_in_cookies(
            self,
            type_token: str,
            request: Request | WebSocket,
            csrf_token: str | None = None,
            fresh: bool | None = None,
    ) -> None:

        if fresh is None:
            fresh = False

        if csrf_token is None:
            csrf_token = False

        cookie = None
        cookie_key = None
        access_type = "access"
        refresh_type = "refresh"

        if type_token not in [access_type, refresh_type]:
            msg = "type_token must be between 'access' or 'refresh'"
            raise ValueError(msg)
        if not isinstance(request, (Request, WebSocket)):
            msg = "request must be an instance of 'Request' or 'WebSocket'"
            raise TypeError(msg)

        if type_token == access_type:
            cookie_key = self.access_cookie_key
            cookie = request.cookies.get(cookie_key)
            if not isinstance(request, WebSocket):
                csrf_token = request.headers.get(self.access_csrf_header_name)
        if type_token == refresh_type:
            cookie_key = self.refresh_cookie_key
            cookie = request.cookies.get(cookie_key)
            if not isinstance(request, WebSocket):
                csrf_token = request.headers.get(self.refresh_csrf_header_name)

        if not cookie:
            raise MissingTokenError(status_code=401, message=f"Missing cookie {cookie_key}")

        if self.cookie_csrf_protect and not csrf_token and (
                isinstance(request, WebSocket) or request.method in self.csrf_methods
        ):
            raise CSRFError(status_code=401, message="Missing CSRF Token")

        self.token = cookie
        self._verify_jwt_in_request(self.token, type_token, "cookies", fresh)

        decoded_token = self.get_raw_jwt()

        if (
                decoded_token
                and self.cookie_csrf_protect
                and csrf_token
                and (isinstance(request, WebSocket) or request.method in self.csrf_methods)
                and "csrf" not in decoded_token
                and not hmac.compare_digest(csrf_token, decoded_token["csrf"])
        ):
            raise AuthError(status_code=422, message="Missing claim: csrf") if "csrf" not in decoded_token else \
                CSRFError(status_code=401, message="CSRF double submit tokens do not match")

    def _verify_jwt_optional_in_request(self, token: str) -> None:
        if token:
            self._verifying_token(token)

        if token and self.get_raw_jwt(token)["type"] != "access":
            raise AccessTokenRequiredError(status_code=422, message="Only access tokens are allowed")

    def _verify_jwt_in_request(
            self,
            token: str,
            type_token: str,
            token_from: str,
            fresh: bool | None = None,
    ) -> None:

        if fresh is None:
            fresh = False

        access_type = "access"
        refresh_type = "refresh"
        websocket_type = "websocket"
        headers_type = "headers"
        if type_token not in [access_type, refresh_type]:
            msg = "type_token must be between 'access' or 'refresh'"
            raise ValueError(msg)
        if token_from not in ["headers", "cookies", "websocket"]:
            msg = "token_from must be between 'headers', 'cookies', 'websocket'"
            raise ValueError(msg)
        if not token:
            if token_from == headers_type:
                raise MissingTokenError(status_code=401, message=f"Missing {self.header_name} Header")
            if token_from == websocket_type:
                raise MissingTokenError(
                    status_code=1008,
                    message=f"Missing {type_token} token from Query or Path",
                )

        issuer = self.decode_issuer if type_token == access_type else None
        self._verifying_token(token, issuer)

        if self.get_raw_jwt(token)["type"] != type_token:
            msg = f"Only {type_token} tokens are allowed"
            if type_token == access_type:
                raise AccessTokenRequiredError(status_code=422, message=msg)
            if type_token == refresh_type:
                raise RefreshTokenRequiredError(status_code=422, message=msg)

        if fresh and not self.get_raw_jwt(token)["fresh"]:
            raise FreshTokenRequiredError(status_code=401, message="Fresh token required")

    def _verifying_token(self, encoded_token: str, issuer: str | None = None) -> None:
        raw_token = self._verified_token(encoded_token, issuer)
        if raw_token["type"] in self.deny_list_token_checks:
            self._check_token_is_revoked(raw_token)

    def _verified_token(self, encoded_token: str, issuer: str | None = None) -> dict:
        algorithms = self.decode_algorithms or [self.algorithm]

        try:
            unverified_headers = self.get_unverified_jwt_headers(encoded_token)
        except InvalidHeaderError as err:
            raise InvalidHeaderError(status_code=422, message=str(err)) from err
        try:
            secret_key = self._get_secret_key(unverified_headers["alg"], "decode")
        except AuthError as err:
            raise AuthError(status_code=422, message=str(err)) from err

        try:
            return jwt.decode(
                encoded_token,
                secret_key,
                issuer=issuer,
                audience=self.decode_audience,
                leeway=self.decode_leeway,
                algorithms=algorithms,
            )
        except AuthError as err:
            raise AuthError(status_code=422, message=str(err)) from err

    def jwt_required(
            self,
            csrf_token: str | None = None,
            auth_from: str = "request",
            token: str | None = None,
            websocket: WebSocket | None = None,
    ) -> None:
        if auth_from == "websocket":
            if websocket:
                self._verify_and_get_jwt_in_cookies("access", websocket, csrf_token)
            else:
                self._verify_jwt_in_request(token, "access", "websocket")

        if auth_from == "request":
            token_location_length = 2
            if len(self.token_location) == token_location_length:
                if self.token and self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "access", "headers")
                if not self.token and self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("access", self._request)
            else:
                if self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "access", "headers")
                if self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("access", self._request)

    def jwt_optional(
            self,
            auth_from: str = "request",
            token: str | None = None,
            websocket: WebSocket | None = None,
            csrf_token: str | None = None,
    ) -> None:

        if auth_from == "websocket":
            if websocket:
                self._verify_and_get_jwt_optional_in_cookies(websocket, csrf_token)
            else:
                self._verify_jwt_optional_in_request(token)

        if auth_from == "request":
            token_location_length = 2
            if len(self.token_location) == token_location_length:
                if self.token and self.jwt_in_headers:
                    self._verify_jwt_optional_in_request(self.token)
                if not self.token and self.jwt_in_cookies:
                    self._verify_and_get_jwt_optional_in_cookies(self._request)
            else:
                if self.jwt_in_headers:
                    self._verify_jwt_optional_in_request(self.token)
                if self.jwt_in_cookies:
                    self._verify_and_get_jwt_optional_in_cookies(self._request)

    def jwt_refresh_token_required(
            self,
            auth_from: str = "request",
            token: str | None = None,
            websocket: WebSocket | None = None,
            csrf_token: str | None = None,
    ) -> None:
        if auth_from == "websocket":
            if websocket:
                self._verify_and_get_jwt_in_cookies("refresh", websocket, csrf_token)
            else:
                self._verify_jwt_in_request(token, "refresh", "websocket")

        if auth_from == "request":
            token_location_length = 2
            if len(self.token_location) == token_location_length:
                if self.token and self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "refresh", "headers")
                if not self.token and self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("refresh", self._request)
            else:
                if self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "refresh", "headers")
                if self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("refresh", self._request)

    def fresh_jwt_required(
            self,
            auth_from: str = "request",
            token: str | None = None,
            websocket: WebSocket | None = None,
            csrf_token: str | None = None,
    ) -> None:
        if auth_from == "websocket":
            if websocket:
                self._verify_and_get_jwt_in_cookies("access", websocket, csrf_token, fresh=True)
            else:
                self._verify_jwt_in_request(token, "access", "websocket", fresh=True)

        if auth_from == "request":
            token_location_length = 2
            if len(self.token_location) == token_location_length:
                if self.token and self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "access", "headers", fresh=True)
                if not self.token and self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("access", request=self._request, fresh=True)
            else:
                if self.jwt_in_headers:
                    self._verify_jwt_in_request(self.token, "access", "headers", fresh=True)
                if self.jwt_in_cookies:
                    self._verify_and_get_jwt_in_cookies("access", request=self._request, fresh=True)

    def get_raw_jwt(self, encoded_token: str | None = None) -> dict | None:
        token = encoded_token or self.token

        if token:
            return self._verified_token(token)
        return None

    def get_jti(self, encoded_token: str) -> str:
        return self._verified_token(encoded_token)["jti"]

    def get_jwt_subject(self) -> str | int | None:
        if self.token:
            return self._verified_token(self.token)["sub"]
        return None

    def get_unverified_jwt_headers(self, encoded_token: str | None = None) -> dict:
        return jwt.get_unverified_header(encoded_token or self.token)
