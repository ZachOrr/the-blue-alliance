from google.cloud import ndb
from werkzeug.test import Client

from backend.common.consts.auth_type import AuthType
from backend.common.consts.event_type import EventType
from backend.common.models.api_auth_access import ApiAuthAccess
from backend.common.models.event import Event
from backend.common.models.team import Team


def test_not_authenticated(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Team(id="frc254", team_number=254).put()
    resp = api_client.get("/api/v3/team/frc254")
    assert resp.status_code == 401
    assert "required" in resp.json["Error"]


def test_bad_auth(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Team(id="frc254", team_number=254).put()
    resp = api_client.get(
        "/api/v3/team/frc254", headers={"X-TBA-Auth-Key": "bad_auth_key"}
    )
    assert resp.status_code == 401
    assert "invalid" in resp.json["Error"]


def test_authenticated_header(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Team(id="frc254", team_number=254).put()
    resp = api_client.get(
        "/api/v3/team/frc254", headers={"X-TBA-Auth-Key": "test_auth_key"}
    )
    assert resp.status_code == 200


def test_authenticated_urlparam(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Team(id="frc254", team_number=254).put()
    resp = api_client.get("/api/v3/team/frc254?X-TBA-Auth-Key=test_auth_key")
    assert resp.status_code == 200


def test_team_key_invalid(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        Team(id="frc254", team_number=254).put()
    resp = api_client.get(
        "/api/v3/team/254", headers={"X-TBA-Auth-Key": "test_auth_key"}
    )
    assert resp.status_code == 404
    assert resp.json["Error"] == "254 is not a valid team key"


def test_team_key_does_not_exist(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Team(id="frc254", team_number=254).put()
    resp = api_client.get(
        "/api/v3/team/frc604", headers={"X-TBA-Auth-Key": "test_auth_key"}
    )
    assert resp.status_code == 404
    assert resp.json["Error"] == "team key: frc604 does not exist"


def test_event_key_invalid(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        Event(
            id="2019casj",
            year=2019,
            event_short="casj",
            event_type_enum=EventType.REGIONAL,
        ).put()
    resp = api_client.get(
        "/api/v3/event/casj", headers={"X-TBA-Auth-Key": "test_auth_key"}
    )
    assert resp.status_code == 404
    assert resp.json["Error"] == "casj is not a valid event key"


def test_event_key_does_not_exist(ndb_client: ndb.Client, api_client: Client) -> None:
    with ndb_client.context():
        ApiAuthAccess(
            id="test_auth_key",
            auth_types_enum=[AuthType.READ_API],
        ).put()
        Event(
            id="2019casj",
            year=2019,
            event_short="casj",
            event_type_enum=EventType.REGIONAL,
        ).put()
    resp = api_client.get(
        "/api/v3/event/2019casf", headers={"X-TBA-Auth-Key": "test_auth_key"}
    )
    assert resp.status_code == 404
    assert resp.json["Error"] == "event key: 2019casf does not exist"
