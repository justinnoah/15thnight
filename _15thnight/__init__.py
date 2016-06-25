"""15th Night Flask App."""

from flask import Flask
from flask.ext.login import LoginManager

from _15thnight.api import user_api, alert_api, admin_api
from _15thnight.models import User
from _15thnight import queue


login_manager = LoginManager()


def create_app(testing=False):
    app = Flask(__name__)

    if not testing:
        try:
            app.config.from_object('config')
        except:
            app.config.from_object('configdist')
    else:
        app.config.from_object('configtest')

    app.secret_key = app.config['SECRET_KEY']

    app.register_blueprint(user_api, url_prefix='/api/v1')
    app.register_blueprint(alert_api, url_prefix='/api/v1')
    app.register_blueprint(admin_api, url_prefix='/api/v1')

    queue.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return app


@login_manager.user_loader
def load_user(id):
    """User loading needed by Flask-Login."""
    return User.query.get(int(id))
