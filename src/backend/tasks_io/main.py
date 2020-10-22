from flask import Flask

from backend.common.logging import configure_logging
from backend.common.middleware import install_middleware
from backend.tasks_io.handlers.tbans import blueprint as tbans_blueprint


configure_logging()

app = Flask(__name__)
install_middleware(app)

app.register_blueprint(tbans_blueprint, url_prefix='/tasks-io/tbans')
