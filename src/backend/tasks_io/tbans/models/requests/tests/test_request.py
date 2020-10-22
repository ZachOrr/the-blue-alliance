from google.appengine.api import taskqueue
from google.appengine.ext import testbed

from backend.tasks_io.tbans.models.notifications.requests.request import Request

from tests.mocks.notifications.mock_notification import MockNotification


def test_init(self):
    Request(MockNotification())

def test_send(self):
    request = Request(MockNotification())
    with self.assertRaises(NotImplementedError):
        request.send()

def test_defer_track_notification(self):
    request = Request(MockNotification())
    request.defer_track_notification(2)
    tasks = self.taskqueue_stub.GetTasks('api-track-call')

    self.assertEqual(len(tasks), 1)
    task = tasks[0]
    self.assertEqual(task['url'], '/_ah/queue/deferred_notification_track_send')
    self.assertEqual(task['queue_name'], 'api-track-call')
