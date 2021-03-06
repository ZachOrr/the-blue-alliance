import google.auth
from firebase_admin import _http_client, exceptions as exceptions
from typing import Any, Optional

def reference(path: str = ..., app: Optional[Any] = ..., url: Optional[Any] = ...): ...

class Event:
    def __init__(self, sse_event: Any) -> None: ...
    @property
    def data(self): ...
    @property
    def path(self): ...
    @property
    def event_type(self): ...

class ListenerRegistration:
    def __init__(self, callback: Any, sse: Any) -> None: ...
    def close(self) -> None: ...

class Reference:
    def __init__(self, **kwargs: Any) -> None: ...
    @property
    def key(self): ...
    @property
    def path(self): ...
    @property
    def parent(self): ...
    def child(self, path: Any): ...
    def get(self, etag: bool = ..., shallow: bool = ...): ...
    def get_if_changed(self, etag: Any): ...
    def set(self, value: Any) -> None: ...
    def set_if_unchanged(self, expected_etag: Any, value: Any): ...
    def push(self, value: str = ...): ...
    def update(self, value: Any) -> None: ...
    def delete(self) -> None: ...
    def listen(self, callback: Any): ...
    def transaction(self, transaction_update: Any): ...
    def order_by_child(self, path: Any): ...
    def order_by_key(self): ...
    def order_by_value(self): ...

class Query:
    def __init__(self, **kwargs: Any) -> None: ...
    def limit_to_first(self, limit: Any): ...
    def limit_to_last(self, limit: Any): ...
    def start_at(self, start: Any): ...
    def end_at(self, end: Any): ...
    def equal_to(self, value: Any): ...
    def get(self): ...

class TransactionAbortedError(exceptions.AbortedError):
    def __init__(self, message: Any) -> None: ...

class _Sorter:
    dict_input: bool = ...
    sort_entries: Any = ...
    def __init__(self, results: Any, order_by: Any) -> None: ...
    def get(self): ...

class _SortEntry:
    def __init__(self, key: Any, value: Any, order_by: Any) -> None: ...
    @property
    def key(self): ...
    @property
    def index(self): ...
    @property
    def index_type(self): ...
    @property
    def value(self): ...
    def __lt__(self, other: Any) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...

class _DatabaseService:
    def __init__(self, app: Any) -> None: ...
    def get_client(self, db_url: Optional[Any] = ...): ...
    def close(self) -> None: ...

class _Client(_http_client.JsonHttpClient):
    credential: Any = ...
    params: Any = ...
    def __init__(self, credential: Any, base_url: Any, timeout: Any, params: Optional[Any] = ...) -> None: ...
    def request(self, method: Any, url: Any, **kwargs: Any): ...
    def create_listener_session(self): ...
    @classmethod
    def handle_rtdb_error(cls, error: Any): ...

class _EmulatorAdminCredentials(google.auth.credentials.Credentials):
    token: str = ...
    def __init__(self) -> None: ...
    def refresh(self, request: Any) -> None: ...
