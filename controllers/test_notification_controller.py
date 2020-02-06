from consts.client_type import ClientType
from consts.notification_type import NotificationType
from base_controller import LoggedInHandler
from helpers.push_helper import PushHelper
from helpers.tbans_helper import TBANSHelper
from models.district import District
from models.event import Event
from models.match import Match
from models.mobile_client import MobileClient
from models.team import Team

# Converted TBANS Notifications
from models.notifications.awards import AwardsNotification

from notifications.alliance_selections import AllianceSelectionNotification
from notifications.district_points_updated import DistrictPointsUpdatedNotification
from notifications.level_starting import CompLevelStartingNotification
from notifications.match_score import MatchScoreNotification
from notifications.match_video import MatchVideoNotification, EventMatchVideoNotification
from notifications.schedule_updated import ScheduleUpdatedNotification
from notifications.upcoming_match import UpcomingMatchNotification

"""
Send out a static notification of each type to
all of a user's devices. Used to test parsing
incoming notifications
"""


class TestNotificationController(LoggedInHandler):
    def post(self, type):
        self._require_registration('/account/')

        user_id = self.user_bundle.account.key.id()
        messaging_id = self.request.get('webhook')

        event_key = self.request.get('event_key')
        team_key = self.request.get('team_key')
        match_key = self.request.get('match_key')
        district_key = self.request.get('district_key')

        # Ensure that the passed messaging_id belongs to the logged-in user
        clients = MobileClient.query(
            MobileClient.user_id.IN([user_id]),
            MobileClient.client_type == ClientType.WEBHOOK,
            MobileClient.messaging_id == messaging_id,
            MobileClient.verified == True
        ).fetch(1)

        if not clients:
            self.response.out.write("Invalid webhook")
            return
        client = clients[0]

        try:
            type = int(type)
        except ValueError:
            # Not passed a valid int, just stop here
            return

        event = None

        if type != NotificationType.DISTRICT_POINTS_UPDATED:
            if event_key == "":
                self.response.out.write("No event key specified!")
                return

            event = Event.get_by_id(event_key)

            if event is None:
                self.response.out.write("Invalid event key!")
                return

        if type == NotificationType.UPCOMING_MATCH:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = UpcomingMatchNotification(match, event)
        elif type == NotificationType.MATCH_SCORE:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = MatchScoreNotification(match)
        elif type == NotificationType.LEVEL_STARTING:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = CompLevelStartingNotification(match, event)
        elif type == NotificationType.ALLIANCE_SELECTION:
            notification = AllianceSelectionNotification(event)
        elif type == NotificationType.AWARDS:
            team = Team.get_by_id(team_key) if team_key else None
            if team:
                tbans_notification = AwardsNotification(event, team)
            else:
                tbans_notification = AwardsNotification(event)
        elif type == NotificationType.MEDIA_POSTED:
            # Not implemented yet
            pass
        elif type == NotificationType.DISTRICT_POINTS_UPDATED:
            if district_key == "":
                self.response.out.write("No district key specified!")
                return

            district = District.get_by_id(district_key)

            if district is None:
                self.response.out.write("Invalid district key!")
                return
            notification = DistrictPointsUpdatedNotification(district)
        elif type == NotificationType.SCHEDULE_UPDATED:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = ScheduleUpdatedNotification(event, match)
        elif type == NotificationType.FINAL_RESULTS:
            # Not implemented yet
            pass
        elif type == NotificationType.MATCH_VIDEO:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = MatchVideoNotification(match)
        elif type == NotificationType.EVENT_MATCH_VIDEO:
            if match_key == "":
                self.response.out.write("No match key specified!")
                return

            match = Match.get_by_id(match_key)

            if match is None:
                self.response.out.write("Invalid match key!")
                return

            notification = EventMatchVideoNotification(match)
        else:
            # Not passed a valid int, return
            return

        # TODO: Drop support for old-style notifications for webhooks, once we migrate to TBANS
        if tbans_notification:
            TBANSHelper._defer_webhook([client], tbans_notification)
        elif notification:
            keys = PushHelper.get_client_ids_for_clients([client])
            # This page should not push notifications to the firebase queue
            # Nor should its notifications be tracked in analytics
            notification.send(keys, push_firebase=False, track_call=False)

        self.response.out.write("ok")
