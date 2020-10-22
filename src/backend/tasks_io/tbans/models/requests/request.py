import logging


class Request:
    """ Base class used for requests to represent a notification payload.

    Attributes:
        notification (Notification): The Notification to send.
    """

    def __init__(self, notification: Notification) -> None:
        """
        Args:
            notification (Notification): The Notification to send.
        """
        self.notification = notification

    def send(self) -> None:
        """ NotificationRequests should understand how to send themselves to wherever they are going.

        Returns:
            NotificationResponse
        """
        raise NotImplementedError("NotificationRequest subclass must implement send")

    def defer_track_notification(self, num_keys: int) -> None:
        from google.appengine.ext import deferred
        deferred.defer(_track_notification, type(self.notification)._type(), num_keys, _target='backend-tasks', _queue='api-track-call', _url='/_ah/queue/deferred_notification_track_send')


def _track_notification(notification_type_enum: NotificationType, num_keys: int) -> None:
    from backend.common.consts.notification_type import NotificationType
    notification_type_name = NotificationType.type_names[notification_type_enum]

    from backend.common.google_analytics import GoogleAnalytics
    GoogleAnalytics.track_event("tba-notification-tracking", "notification", notification_type_name, num_keys)
