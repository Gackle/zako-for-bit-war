from flask import Flask, redirect, url_for

from .models import db, User, Role
from .controllers.main import main_blueprint
from .controllers.zako.views import zako_blueprint
from .controllers.forum import forum_blueprint
from .extensions import bcrypt
from .filters import datetimeformat


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(zako_blueprint)
    app.register_blueprint(forum_blueprint)

    app.jinja_env.filters['datetimeformat'] = datetimeformat

    return app


if __name__ == "__main__":
    app = create_app()
