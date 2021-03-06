import threading
from typing import Any

def code_info(*args: Any, **kwargs: Any) -> None: ...

DEBUG: bool

def decorator(*args: Any, **kwargs: Any) -> None: ...
def frame_info(*args: Any, **kwargs: Any) -> None: ...
def func_info(*args: Any, **kwargs: Any) -> None: ...
def gen_info(*args: Any, **kwargs: Any) -> None: ...
def get_stack(*args: Any, **kwargs: Any) -> None: ...
def logging_debug(*args: Any, **kwargs: Any) -> None: ...

class keyword_only:
    defaults: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...
    def __call__(self, wrapped: Any): ...

def positional(max_pos_args: Any): ...
threading_local = threading.local

def tweak_logging(*args: Any, **kwargs: Any) -> None: ...
def wrapping(*args: Any, **kwargs: Any) -> None: ...
