import flask
from flask import jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from {{cookiecutter.module_name}}.api import core


class JSONExceptionHandler(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def std_handler(self, error):
        response = jsonify({
            'error': {
                'code': error.code,
                'message': str(error.description),
            }
        })

        if isinstance(error, HTTPException):
            response.status_code = error.code
        else:
            response.status_code = 500
        return response

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code, v in default_exceptions.iteritems():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.errorhandler(exception_or_code)(handler or self.std_handler)


def create_webapp():
    """
    Return an instance of Flask.
    """
    app = flask.Flask('{{cookiecutter.module_name}}-api')
    JSONExceptionHandler(app)

    # register blueprints
    app.register_blueprint(core.bp, url_prefix='/v1')
    return app
