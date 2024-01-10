class AuthError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message


class InvalidHeaderError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class DecodeError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class CSRFError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class MissingTokenError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class RevokedTokenError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class AccessTokenRequiredError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class RefreshTokenRequiredError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)


class FreshTokenRequiredError(AuthError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(status_code, message)
