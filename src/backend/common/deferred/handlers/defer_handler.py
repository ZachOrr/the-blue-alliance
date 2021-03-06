import logging
import pickle
from typing import Any

from flask import abort, Flask, request, Response


class PermanentTaskFailure(Exception):
    """Indicates that a task failed, and will never succeed."""


def run(data: bytes) -> Any:
    """Unpickles and executes a task.

    Args:
        data: A pickled tuple of (function, args, kwargs) to execute.
    Returns:
        The return value of the function invocation.
    """
    try:
        func, args, kwargs = pickle.loads(data)
    except Exception as e:
        raise PermanentTaskFailure(e)
    else:
        return func(*args, **kwargs)


def handle_defer(path: str) -> Response:
    if "X-AppEngine-TaskName" not in request.headers:
        logging.error(
            'Detected an attempted XSRF attack. The header "X-AppEngine-TaskName" was not set.'
        )
        abort(403)

    run(request.data)
    return Response(status=200)


def install_defer_routes(app: Flask) -> None:
    app.add_url_rule(
        '/_ah/queue/<regex("deferred.*"):path>',
        view_func=handle_defer,
        methods=["POST"],
    )
