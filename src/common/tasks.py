import os

from common import env


def TaskApp():

     def __init__(self):
         if env.is_debug:
            from redis import Redis
            redis_conn = Redis()
         else:
             from google.cloud import tasks_v2
             client = tasks_v2.CloudTasksClient()

     def queue(self) -> bool:
        from rq import Queue
        q = Queue(connection=redis_conn)  # no args implies the default queue


# TODO: Some return
def queue(queue_name: str):
    else:
        from google.cloud import tasks_v2
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'tba-dev') # TODO: Some smart default here
        location = app_engine_information.get('locationId', 'us-central') # TODO: Some smart default here

    from common import app_engine
    app_engine_information = app_engine.default_information()

    # {
    #   "name": "apps/tbatv-prod-hrd",
    #   "id": "tbatv-prod-hrd",
    #   "dispatchRules": [
    #     {
    #       "domain": "py3.thebluealliance.com",
    #       "path": "/api/*",
    #       "service": "py3-api"
    #     },
    #     {
    #       "domain": "py3.thebluealliance.com",
    #       "path": "/*",
    #       "service": "py3-web"
    #     },
    #     {
    #       "domain": "beta.thebluealliance.com",
    #       "path": "/*",
    #       "service": "pwa-ssr"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/api/v3/*",
    #       "service": "api"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/backend-tasks/*",
    #       "service": "backend-tasks"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/backend-tasks-b2/*",
    #       "service": "backend-tasks-b2"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/clientapi/*",
    #       "service": "clientapi"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/tasks/*",
    #       "service": "tasks"
    #     },
    #     {
    #       "domain": "*",
    #       "path": "/",
    #       "service": "default"
    #     }
    #   ],
    #   "authDomain": "gmail.com",
    #   "locationId": "us-central",
    #   "codeBucket": "staging.tbatv-prod-hrd.appspot.com",
    #   "defaultCookieExpiration": "1209600s",
    #   "servingStatus": "SERVING",
    #   "defaultHostname": "tbatv-prod-hrd.appspot.com",
    #   "defaultBucket": "tbatv-prod-hrd.appspot.com",
    #   "gcrDomain": "us.gcr.io",
    #   "databaseType": "CLOUD_DATASTORE"
    # }
