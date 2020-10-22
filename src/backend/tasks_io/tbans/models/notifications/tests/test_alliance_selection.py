# from helpers.event.event_test_creator import EventTestCreator
# from models.event_details import EventDetails
# from models.team import Team

from backend.common.consts.notification_type import NotificationType
from backend.common.models.event import Event
from backend.common.models.team import Team
from backend.tasks_io.tbans.models.notifications.alliance_selection import AllianceSelectionNotification

class TestAllianceSelection:

    def setup_method(self, method):
        from backend.common.consts.event_type import EventType
        self.event = Event(
            event_short="TEST",
            event_type_enum=EventType.REGIONAL,
            name="Test Event",
        )
        self.notification = AllianceSelectionNotification(self.event)

    # def setUp():
    #     self.testbed = testbed.Testbed()
    #     self.testbed.activate()
    #     self.testbed.init_datastore_v3_stub()
    #     self.testbed.init_memcache_stub()
    #     ndb.get_context().clear_cache()
    #
    #     self.testbed.init_taskqueue_stub(root_path=".")
    #
    #     for team_number in range(7):
    #         Team(id="frc%s" % team_number,
    #              team_number=team_number).put()
    #
    #     self.event = EventTestCreator.createPresentEvent()
    #     self.notification = AllianceSelectionNotification(self.event)
    #
    # def tearDown():
    #     self.testbed.deactivate()

    def test_type(self) -> None:
        assert AllianceSelectionNotification._type() == NotificationType.ALLIANCE_SELECTION

    def test_fcm_notification(self) -> None:
        assert self.notification.fcm_notification is not None
        assert self.notification.fcm_notification.title == "TEST Alliances Updated"
        assert self.notification.fcm_notification.body == "Test Event alliances have been updated."

    def test_fcm_notification_team_captain(self):
        # team = Team(id="frc1", team_number=1)
        # Setup alliance selection information
        EventDetails(
            id=self.event.key_name,
            alliance_selections=[
                {"declines": [], "picks": ["frc1", "frc2", "frc3"]}
            ]
        ).put()

        notification = AllianceSelectionNotification(self.event, team)
        assert notification.fcm_notification is not None
        assert notification.fcm_notification.title == 'TEST Alliances Updated'
        assert notification.fcm_notification.body == 'Test Event alliances have been updated. Team 1 is Captain of Alliance 1 with Team 2 and Team 3.'

    # def test_fcm_notification_team(self):
    #     team = Team.get_by_id('frc1')
    #     # Setup alliance selection information
    #     EventDetails(
    #         id=self.event.key_name,
    #         alliance_selections=[
    #             {"declines": [], "picks": ["frc2", "frc1", "frc3"]}
    #         ]
    #     ).put()
    #
    #     notification = AllianceSelectionNotification(self.event, team)
    #     self.assertIsNotNone(notification.fcm_notification)
    #     assert notification.fcm_notification.title == 'TESTPRESENT Alliances Updated'
    #     assert notification.fcm_notification.body == 'Present Test Event alliances have been updated. Team 1 is on Alliance 1 with Team 2 and Team 3.'
    #
    # def test_fcm_notification_team_four(self):
    #     team = Team.get_by_id('frc1')
    #     # Setup alliance selection information
    #     EventDetails(
    #         id=self.event.key_name,
    #         alliance_selections=[
    #             {"declines": [], "picks": ["frc2", "frc1", "frc3", "frc4"]}
    #         ]
    #     ).put()
    #
    #     notification = AllianceSelectionNotification(self.event, team)
    #     self.assertIsNotNone(notification.fcm_notification)
    #     assert notification.fcm_notification.title == 'TESTPRESENT Alliances Updated'
    #     assert notification.fcm_notification.body == 'Present Test Event alliances have been updated. Team 1 is on Alliance 1 with Team 2, Team 3 and Team 4.'
    #
    # def test_fcm_notification_short_name(self):
    #     self.notification.event.short_name = 'Arizona North'
    #
    #     self.assertIsNotNone(self.notification.fcm_notification)
    #     assert self.notification.fcm_notification.title == 'TESTPRESENT Alliances Updated'
    #     assert self.notification.fcm_notification.body == 'Arizona North Regional alliances have been updated.'
    #
    # def test_data_payload(self):
    #     payload = self.notification.data_payload
    #     assert len(payload) == 1
    #     assert payload['event_key'] == self.event.key_name
    #
    # def test_data_payload_team(self):
    #     team = Team.get_by_id('frc1')
    #     notification = AllianceSelectionNotification(self.event, team)
    #     payload = notification.data_payload
    #     assert len(payload) == 2
    #     assert payload['event_key'] == self.event.key_name
    #     assert payload['team_key'] == team.key_name
    #
    # def test_webhook_message_data(self):
    #     payload = self.notification.webhook_message_data
    #     assert len(payload) == 3
    #     assert payload['event_key'] == self.event.key_name
    #     assert payload['event_name'] == 'Present Test Event'
    #     self.assertIsNotNone(payload['event'])
    #
    # def test_webhook_message_data_team(self):
    #     team = Team.get_by_id('frc1')
    #     notification = AllianceSelectionNotification(self.event, team)
    #     payload = notification.webhook_message_data
    #     assert len(payload), 4)
    #     assert payload['event_key'] == self.event.key_name
    #     assert payload['team_key'] == team.key_name
    #     assert payload['event_name'] == 'Present Test Event'
    #     self.assertIsNotNone(payload['event'])
