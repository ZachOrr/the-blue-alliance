# Wrapper around the App Engine Admin API - used in place of the App Identity API
# Authorized user needs at least the App Engine Viewer role

def default_information():
    from common import auth
    credentials, project = auth.default()

    from googleapiclient.discovery import build
    service = build('appengine', 'v1', credentials=credentials)
    # https://cloud.google.com/appengine/docs/admin-api/reference/rest/v1/apps/get
    return service.apps().get(appsId=project).execute()
