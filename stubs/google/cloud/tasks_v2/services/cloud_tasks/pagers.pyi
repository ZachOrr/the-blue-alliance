from google.cloud.tasks_v2.types import cloudtasks as cloudtasks, queue as queue, task as task
from typing import Any, AsyncIterable, Awaitable, Callable, Iterable, Sequence, Tuple

class ListQueuesPager:
    def __init__(self, method: Callable[..., cloudtasks.ListQueuesResponse], request: cloudtasks.ListQueuesRequest, response: cloudtasks.ListQueuesResponse, *, metadata: Sequence[Tuple[str, str]]=...) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    @property
    def pages(self) -> Iterable[cloudtasks.ListQueuesResponse]: ...
    def __iter__(self) -> Iterable[queue.Queue]: ...

class ListQueuesAsyncPager:
    def __init__(self, method: Callable[..., Awaitable[cloudtasks.ListQueuesResponse]], request: cloudtasks.ListQueuesRequest, response: cloudtasks.ListQueuesResponse, *, metadata: Sequence[Tuple[str, str]]=...) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    @property
    async def pages(self) -> AsyncIterable[cloudtasks.ListQueuesResponse]: ...
    def __aiter__(self) -> AsyncIterable[queue.Queue]: ...

class ListTasksPager:
    def __init__(self, method: Callable[..., cloudtasks.ListTasksResponse], request: cloudtasks.ListTasksRequest, response: cloudtasks.ListTasksResponse, *, metadata: Sequence[Tuple[str, str]]=...) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    @property
    def pages(self) -> Iterable[cloudtasks.ListTasksResponse]: ...
    def __iter__(self) -> Iterable[task.Task]: ...

class ListTasksAsyncPager:
    def __init__(self, method: Callable[..., Awaitable[cloudtasks.ListTasksResponse]], request: cloudtasks.ListTasksRequest, response: cloudtasks.ListTasksResponse, *, metadata: Sequence[Tuple[str, str]]=...) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    @property
    async def pages(self) -> AsyncIterable[cloudtasks.ListTasksResponse]: ...
    def __aiter__(self) -> AsyncIterable[task.Task]: ...
