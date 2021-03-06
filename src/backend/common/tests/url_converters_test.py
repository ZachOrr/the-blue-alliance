import pytest
from flask import Flask

from backend.common.url_converters import install_url_converters


def test_regex_route(app: Flask) -> None:
    install_url_converters(app)

    @app.route('/<regex("[0-9]{4}[a-z]+"):event_key>')
    def view(event_key: str):
        return event_key

    client = app.test_client()
    resp = client.get("/2020nyny")
    assert resp.status_code == 200
    assert resp.data == b"2020nyny"

    assert client.get("/").status_code == 404
    assert client.get("/123abc").status_code == 404
    assert client.get("/1234ABC").status_code == 404


def test_regex_route_throws_when_not_installed(app: Flask) -> None:
    # Do not install the converter, expect we get an error

    with pytest.raises(LookupError):

        @app.route('/<regex("[0-9]{4}[a-z]+"):event_key>')
        def view(event_key: str):
            return event_key
