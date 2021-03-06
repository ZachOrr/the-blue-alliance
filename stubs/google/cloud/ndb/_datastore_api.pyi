from google.cloud.datastore import helpers as helpers
from google.cloud.datastore_v1.proto import datastore_pb2 as datastore_pb2, entity_pb2 as entity_pb2
from google.cloud.ndb import tasklets as tasklets
from typing import Any, Optional

EVENTUAL: Any
EVENTUAL_CONSISTENCY = EVENTUAL
STRONG: Any
log: Any

def stub(): ...
def make_call(rpc_name: Any, request: Any, retries: Optional[Any] = ..., timeout: Optional[Any] = ...): ...
def lookup(key: Any, options: Any) -> None: ...

class _LookupBatch:
    options: Any = ...
    todo: Any = ...
    def __init__(self, options: Any) -> None: ...
    def full(self): ...
    def add(self, key: Any): ...
    def idle_callback(self) -> None: ...
    def lookup_callback(self, rpc: Any) -> None: ...

def get_read_options(options: Any, default_read_consistency: Optional[Any] = ...): ...
def put(entity: Any, options: Any) -> None: ...
def delete(key: Any, options: Any) -> None: ...

class _NonTransactionalCommitBatch:
    options: Any = ...
    mutations: Any = ...
    futures: Any = ...
    def __init__(self, options: Any) -> None: ...
    def full(self): ...
    def put(self, entity_pb: Any): ...
    def delete(self, key: Any): ...
    def idle_callback(self) -> None: ...

def commit(transaction: Any, retries: Optional[Any] = ..., timeout: Optional[Any] = ...): ...

class _TransactionalCommitBatch(_NonTransactionalCommitBatch):
    transaction: Any = ...
    allocating_ids: Any = ...
    incomplete_mutations: Any = ...
    incomplete_futures: Any = ...
    def __init__(self, transaction: Any, options: Any) -> None: ...
    def put(self, entity_pb: Any): ...
    def delete(self, key: Any): ...
    def idle_callback(self) -> None: ...
    def allocate_ids_callback(self, rpc: Any, mutations: Any, futures: Any) -> None: ...
    def commit(self, retries: Optional[Any] = ..., timeout: Optional[Any] = ...) -> None: ...

def allocate(keys: Any, options: Any): ...

class _AllocateIdsBatch:
    options: Any = ...
    keys: Any = ...
    futures: Any = ...
    def __init__(self, options: Any) -> None: ...
    def full(self): ...
    def room_left(self): ...
    def add(self, keys: Any): ...
    def idle_callback(self) -> None: ...
    def allocate_ids_callback(self, rpc: Any) -> None: ...

def begin_transaction(read_only: Any, retries: Optional[Any] = ..., timeout: Optional[Any] = ...) -> None: ...
def rollback(transaction: Any, retries: Optional[Any] = ..., timeout: Optional[Any] = ...) -> None: ...
