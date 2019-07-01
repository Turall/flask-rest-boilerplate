import os

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from prometheus_client import make_wsgi_app

from core.factories import create_app, SettingsError


if os.environ["APP_SETTINGS"]:
    settings_name = os.environ["APP_SETTINGS"]
else:
    raise SettingsError("'APP_SETTINGS' environment " "variable is not defined")
flask_app = create_app(__name__, settings_name)
app = DispatcherMiddleware(flask_app, {"/metrics": make_wsgi_app()})


if __name__ == "__main__":
    run_simple(
        "0.0.0.0", 8080, app, use_reloader=False, use_debugger=flask_app.config["DEBUG"]
    )
