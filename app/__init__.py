"""
Factory for application
"""

import os
import logging
from flask import Flask, request
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from prometheus_client import Counter
from app.config import ProdConfig, RequestFormatter


metrics = None
error_counter = None

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=ProdConfig):
    """
    Create flask app, init addons, blueprints and setup logging
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    global metrics, error_counter
    if not app.testing and os.getenv("PROMETHEUS_MULTIPROC_DIR"):
        metrics = GunicornInternalPrometheusMetrics.for_app_factory()
        metrics.init_app(app)

        error_counter = Counter(
            'flask_app_errors_total',
            'Total application errors',
            ['status_code', 'endpoint']
        )

    @app.after_request
    def track_errors(response):
        """
        Track errors and increment error counter
        """
        if error_counter and response.status_code >= 400:
            error_counter.labels(
                status_code=str(response.status_code),
                endpoint=request.endpoint or 'unknown'
            ).inc()
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Handle uncaught exceptions and log them
        """
        if error_counter:
            error_counter.labels(
                status_code='500',
                endpoint=request.endpoint or 'unknown'
            ).inc()
        app.logger.error(f"Unhandled exception: {e}", exc_info=True)
        return "Internal Server Error", 500

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)

    #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    #pylint: enable=wrong-import-position, cyclic-import, import-outside-toplevel

    if not app.debug and not app.testing:
        formatter = RequestFormatter(
            '[%(asctime)s %(levelname)s] %(remote_addr)s requested %(url)s\n: %(message)s [in %(module)s:%(lineno)d]'
        )
        default_handler.setFormatter(formatter)
        app.logger.setLevel(logging.INFO)

    return app


from app import models #pylint: disable=wrong-import-position, cyclic-import, import-outside-toplevel