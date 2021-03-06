import datetime
from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fakeredis import FakeRedis
from flask import Flask
from flask_caching.backends.nullcache import NullCache
from flask_caching.backends.rediscache import RedisCache
from freezegun import freeze_time

from backend.common.decorators import cached_public, memoize
from backend.common.flask_cache import configure_flask_cache
from backend.common.redis import RedisClient


def test_no_cached_public(app: Flask) -> None:
    @app.route("/")
    def view():
        return "Hello!"

    resp = app.test_client().get("/")
    assert resp.headers.get("Cache-Control") is None
    assert resp.headers.get("ETag") is None


def test_no_cached_public_on_error(app: Flask) -> None:
    @app.route("/")
    @cached_public
    def view():
        return "Error", 401

    resp = app.test_client().get("/")
    assert resp.headers.get("Cache-Control") is None
    assert resp.headers.get("ETag") is None


def test_cached_public_default(app: Flask) -> None:
    @app.route("/")
    @cached_public
    def view():
        return "Hello!"

    resp = app.test_client().get("/")
    assert resp.headers.get("Cache-Control") == "public, max-age=61, s-maxage=61"


def test_cached_public_timeout(app: Flask) -> None:
    @app.route("/")
    @cached_public(timeout=3600)
    def view():
        return "Hello!"

    resp = app.test_client().get("/")
    assert resp.headers.get("Cache-Control") == "public, max-age=3600, s-maxage=3600"


def test_cached_public_etag(app: Flask) -> None:
    @app.route("/")
    @cached_public
    def view():
        return "Hello!"

    resp = app.test_client().get("/")
    etag = resp.headers.get("ETag")
    assert etag is not None

    # Check that a valid etag returns 304
    resp2 = app.test_client().get("/", headers={"If-None-Match": etag})
    assert resp2.status_code == 304
    assert resp2.get_data(as_text=True) == ""

    # Check that an invalid etag returns a normal response
    resp3 = app.test_client().get("/", headers={"If-None-Match": "bad-etag"})
    assert resp3.status_code == 200
    assert resp3.get_data(as_text=True) == "Hello!"


@pytest.mark.filterwarnings("ignore::UserWarning:flask_caching")
def test_flask_cache_null_cache_by_default(app: Flask) -> None:
    configure_flask_cache(app)

    @app.route("/")
    @cached_public
    def view():
        return "Hello!"

    assert hasattr(app, "cache")
    assert isinstance(app.cache.cache, NullCache)

    resp = app.test_client().get("/")
    assert resp.status_code == 200


def test_flask_cache_with_redis(monkeypatch: MonkeyPatch, app: Flask) -> None:
    fake_redis = FakeRedis()
    monkeypatch.setattr(RedisClient, "get", MagicMock(return_value=fake_redis))
    configure_flask_cache(app)

    @app.route("/")
    @cached_public
    def view():
        return "Hello!"

    assert hasattr(app, "cache")
    assert isinstance(app.cache.cache, RedisCache)

    resp = app.test_client().get("/")
    assert resp.status_code == 200

    assert app.cache.get("view//") == resp.data.decode()


def test_flask_cache_with_redis_after_timeout(
    monkeypatch: MonkeyPatch, app: Flask
) -> None:
    fake_redis = FakeRedis()
    monkeypatch.setattr(RedisClient, "get", MagicMock(return_value=fake_redis))
    configure_flask_cache(app)

    @app.route("/")
    @cached_public(timeout=10)
    def view():
        return "Hello!"

    assert hasattr(app, "cache")
    assert isinstance(app.cache.cache, RedisCache)

    with freeze_time() as frozen_time:
        resp = app.test_client().get("/")
        assert resp.status_code == 200

        assert app.cache.get("view//") == resp.data.decode()

        # Tick past the expiration, so the next get should return None
        frozen_time.tick(delta=datetime.timedelta(seconds=15))

        assert app.cache.get("view//") is None


def test_flask_cache_with_redis_skips_errors(
    monkeypatch: MonkeyPatch, app: Flask
) -> None:
    fake_redis = FakeRedis()
    monkeypatch.setattr(RedisClient, "get", MagicMock(return_value=fake_redis))
    configure_flask_cache(app)

    @app.route("/")
    @cached_public
    def view():
        return "Hello!", 500

    assert hasattr(app, "cache")
    assert isinstance(app.cache.cache, RedisCache)

    resp = app.test_client().get("/")
    assert resp.status_code == 500
    assert app.cache.get("view//") is None


def test_memoize_outside_of_request(app: Flask) -> None:
    @memoize
    def an_expensive_function():
        an_expensive_function.counter += 1
        return an_expensive_function.counter

    an_expensive_function.counter = 0

    resp1 = an_expensive_function()
    assert resp1 == 1

    # By deafult, we shouldn't have memoized anything (because redis isn't configured)
    resp2 = an_expensive_function()
    assert resp2 == 2


def test_memoize_without_setup(app: Flask) -> None:
    @memoize
    def an_expensive_function():
        an_expensive_function.counter += 1
        return an_expensive_function.counter

    an_expensive_function.counter = 0

    @app.route("/")
    def view():
        return str(an_expensive_function())

    resp1 = app.test_client().get("/")
    assert resp1.status_code == 200
    assert resp1.data == b"1"

    # By deafult, we shouldn't have memoized anything (because redis isn't configured)
    resp2 = app.test_client().get("/")
    assert resp2.status_code == 200
    assert resp2.data == b"2"


def test_memoize_null_cache_by_default(app: Flask) -> None:
    configure_flask_cache(app)

    @memoize
    def an_expensive_function():
        an_expensive_function.counter += 1
        return an_expensive_function.counter

    an_expensive_function.counter = 0

    @app.route("/")
    def view():
        return str(an_expensive_function())

    resp1 = app.test_client().get("/")
    assert resp1.status_code == 200
    assert resp1.data == b"1"

    # By deafult, we shouldn't have memoized anything (because redis isn't configured)
    resp2 = app.test_client().get("/")
    assert resp2.status_code == 200
    assert resp2.data == b"2"


def test_memoize_with_redis(app: Flask, monkeypatch: MonkeyPatch) -> None:
    fake_redis = FakeRedis()
    monkeypatch.setattr(RedisClient, "get", MagicMock(return_value=fake_redis))
    configure_flask_cache(app)

    @memoize
    def an_expensive_function():
        an_expensive_function.counter += 1
        return an_expensive_function.counter

    an_expensive_function.counter = 0

    @app.route("/")
    def view():
        return str(an_expensive_function())

    resp1 = app.test_client().get("/")
    assert resp1.status_code == 200
    assert resp1.data == b"1"

    # The second time we call the function, we should have cached the result
    resp2 = app.test_client().get("/")
    assert resp2.status_code == 200
    assert resp2.data == b"1"


def test_memoize_with_redis_after_timeout(app: Flask, monkeypatch: MonkeyPatch) -> None:
    fake_redis = FakeRedis()
    monkeypatch.setattr(RedisClient, "get", MagicMock(return_value=fake_redis))
    configure_flask_cache(app)

    @memoize(timeout=10)
    def an_expensive_function():
        an_expensive_function.counter += 1
        return an_expensive_function.counter

    an_expensive_function.counter = 0

    @app.route("/")
    def view():
        return str(an_expensive_function())

    with freeze_time() as frozen_time:
        resp1 = app.test_client().get("/")
        assert resp1.status_code == 200
        assert resp1.data == b"1"

        # Tick past the expiration, so the next get should return None
        frozen_time.tick(delta=datetime.timedelta(seconds=15))

        # If we call again, after the TTL, we should re-run the function
        resp2 = app.test_client().get("/")
        assert resp2.status_code == 200
        assert resp2.data == b"2"
