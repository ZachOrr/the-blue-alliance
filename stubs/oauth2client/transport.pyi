from typing import Any, Optional

REFRESH_STATUS_CODES: Any

class MemoryCache:
    cache: Any = ...
    def __init__(self) -> None: ...
    def get(self, key: Any): ...
    def set(self, key: Any, value: Any) -> None: ...
    def delete(self, key: Any) -> None: ...

def get_cached_http(): ...
def get_http_object(*args: Any, **kwargs: Any): ...
def clean_headers(headers: Any): ...
def wrap_http_for_auth(credentials: Any, http: Any): ...
def wrap_http_for_jwt_access(credentials: Any, http: Any): ...
def request(http: Any, uri: Any, method: str = ..., body: Optional[Any] = ..., headers: Optional[Any] = ..., redirections: Any = ..., connection_type: Optional[Any] = ...): ...
