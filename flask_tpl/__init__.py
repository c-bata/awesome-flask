from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate = Migrate(app, db)

    from .views.v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')


    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= app.config['SLOW_DB_QUERY_TIME']:
                app.logger.warning(
                    'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                    % (query.statement, query.parameters, query.duration,
                       query.context)
                )
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        """Return a custom 404 error."""
        return 'Sorry, Nothing at this URL.', 404

    @app.errorhandler(500)
    def page_not_found(e):
        """Return a custom 500 error."""
        return 'Sorry, unexpected error: {}'.format(e), 500

    return app

