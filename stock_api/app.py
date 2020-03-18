from flask import Flask, Blueprint
from flask_migrate import Migrate
from bi_api.database import DBContext, engine
from flask_cors import CORS
from .api import api
from .api.event_type import ns as drawee_event_ns

from healthcheck import HealthCheck, EnvironmentDump


def create_app():
    app = Flask(__name__)

    health = HealthCheck()
    envdump = EnvironmentDump()

    CORS(app)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(drawee_event_ns, '/draweeEvent')
    app.register_blueprint(blueprint)
    app.add_url_rule("/health-check", "healthcheck", view_func=lambda: health.run())
    app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

    db = DBContext(engine).__enter__()
    Migrate(app, db)

    return app


if __name__ == "__main__":
    import os
    app = create_app()
    port = os.environ.get('PORT', '5200')
    host = '0.0.0.0'
    debug = (True if os.environ.get('DEBUG') == 'True' else False)
    app.run(host, port, debug)
