import os
import pathlib

from flask import Flask
from tasks_io.datafeed import handlers as datafeed_handlers


def testing():
    print(os.getenv('GAE_ENV', None))
    from common import tasks
    tasks.queue('abc')
    return 200


app = Flask(__name__)
# datafeed routes
app.add_url_rule('/datafeed/test', view_func=testing)
app.add_url_rule('/datafeed/event_list/<int:year>', view_func=datafeed_handlers.event_list)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = f"{pathlib.Path(__file__).parent.absolute()}/service-account-key.json"
    # Need region - GAE_APPLICATION?

    app.run(host='127.0.0.1', port=8080, debug=True)
