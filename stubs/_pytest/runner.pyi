from .reports import (
    CollectErrorRepr as CollectErrorRepr,
    CollectReport as CollectReport,
    TestReport as TestReport,
)
from _pytest._code.code import (
    ExceptionChainRepr as ExceptionChainRepr,
    ExceptionInfo as ExceptionInfo,
)
from _pytest.compat import TYPE_CHECKING as TYPE_CHECKING
from _pytest.nodes import Collector as Collector, Node as Node
from _pytest.outcomes import (
    Exit as Exit,
    Skipped as Skipped,
    TEST_OUTCOME as TEST_OUTCOME,
)
from typing import Any, Optional
from typing_extensions import Literal as Literal

def pytest_addoption(parser: Any) -> None: ...
def pytest_terminal_summary(terminalreporter: Any): ...
def pytest_sessionstart(session: Any) -> None: ...
def pytest_sessionfinish(session: Any) -> None: ...
def pytest_runtest_protocol(item: Any, nextitem: Any): ...
def runtestprotocol(item: Any, log: bool = ..., nextitem: Optional[Any] = ...): ...
def show_test_item(item: Any) -> None: ...
def pytest_runtest_setup(item: Any) -> None: ...
def pytest_runtest_call(item: Any) -> None: ...
def pytest_runtest_teardown(item: Any, nextitem: Any) -> None: ...
def pytest_report_teststatus(report: Any): ...
def call_and_report(
    item: Any, when: Literal[setup, call, teardown], log: Any = ..., **kwds: Any
) -> Any: ...
def check_interactive_exception(call: Any, report: Any): ...
def call_runtest_hook(
    item: Any, when: Literal[setup, call, teardown], **kwds: Any
) -> Any: ...

class CallInfo:
    excinfo: Any = ...
    start: Any = ...
    stop: Any = ...
    when: Any = ...
    @property
    def result(self): ...
    @classmethod
    def from_call(cls: Any, func: Any, when: Any, reraise: Any = ...) -> CallInfo: ...
    def __init__(
        self, result: Any, excinfo: Any, start: Any, stop: Any, when: Any
    ) -> None: ...
    def __ne__(self, other: Any) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...

def pytest_runtest_makereport(item: Any, call: Any): ...
def pytest_make_collect_report(collector: Collector) -> CollectReport: ...

class SetupState:
    stack: Any = ...
    def __init__(self) -> None: ...
    def addfinalizer(self, finalizer: Any, colitem: Any) -> None: ...
    def teardown_all(self) -> None: ...
    def teardown_exact(self, item: Any, nextitem: Any) -> None: ...
    def prepare(self, colitem: Any) -> None: ...

def collect_one_node(collector: Any): ...