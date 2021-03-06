from firebase_admin import credentials as credentials
from typing import Any, Optional

def initialize_app(credential: Optional[Any] = ..., options: Optional[Any] = ..., name: Any = ...): ...
def delete_app(app: Any) -> None: ...
def get_app(name: Any = ...): ...

class _AppOptions:
    def __init__(self, options: Any) -> None: ...
    def get(self, key: Any, default: Optional[Any] = ...): ...

class App:
    def __init__(self, name: Any, credential: Any, options: Any) -> None: ...
    @property
    def name(self): ...
    @property
    def credential(self): ...
    @property
    def options(self): ...
    @property
    def project_id(self): ...
