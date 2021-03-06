import re
import unittest2

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from consts.notification_type import NotificationType
from helpers.event.event_test_creator import EventTestCreator
from models.team import Team

from models.notifications.match_video import MatchVideoNotification


class TestMatchVideoNotification(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()  # Prevent data from leaking between tests

        self.testbed.init_taskqueue_stub(root_path=".")

        for team_number in range(6):
            Team(id="frc%s" % team_number,
                 team_number=team_number).put()

        self.event = EventTestCreator.createPresentEvent()
        self.match = self.event.matches[0]
        self.notification = MatchVideoNotification(self.match)

    def tearDown(self):
        self.testbed.deactivate()

    def test_type(self):
        self.assertEqual(MatchVideoNotification._type(), NotificationType.MATCH_VIDEO)

    def test_fcm_notification(self):
        self.assertIsNotNone(self.notification.fcm_notification)
        self.assertEqual(self.notification.fcm_notification.title, 'TESTPRESENT Match Video')
        self.assertEqual(self.notification.fcm_notification.body, 'Video for TESTPRESENT Quals 1 has been posted.')

    def test_fcm_notification_team(self):
        team = Team.get_by_id('frc1')
        notification = MatchVideoNotification(self.match, team)
        self.assertEqual(notification.fcm_notification.title, 'Team 1 Match Video')
        self.assertEqual(notification.fcm_notification.body, 'Video for TESTPRESENT Quals 1 featuring Team 1 has been posted.')

    def test_data_payload(self):
        payload = self.notification.data_payload
        self.assertEqual(len(payload), 2)
        self.assertEqual(payload['event_key'], self.event.key_name)
        self.assertEqual(payload['match_key'], '{}_qm1'.format(self.event.key_name))

    def test_data_payload_team(self):
        team = Team.get_by_id('frc1')
        notification = MatchVideoNotification(self.match, team)
        payload = notification.data_payload
        self.assertEqual(len(payload), 3)
        self.assertEqual(payload['event_key'], self.event.key_name)
        self.assertEqual(payload['match_key'], '{}_qm1'.format(self.event.key_name))
        self.assertEqual(payload['team_key'], 'frc1')

    def test_webhook_message_data(self):
        # Has `event_name`
        payload = self.notification.webhook_message_data
        self.assertEqual(len(payload), 3)
        self.assertEqual(payload['event_key'], self.event.key_name)
        self.assertEqual(payload['event_name'], 'Present Test Event')
        self.assertIsNotNone(payload['match'])

    def test_webhook_message_data_team(self):
        team = Team.get_by_id('frc1')
        notification = MatchVideoNotification(self.match, team)
        payload = notification.webhook_message_data
        self.assertEqual(len(payload), 4)
        self.assertEqual(payload['event_key'], self.event.key_name)
        self.assertEqual(payload['event_name'], 'Present Test Event')
        self.assertEqual(payload['team_key'], 'frc1')
        self.assertIsNotNone(payload['match'])
