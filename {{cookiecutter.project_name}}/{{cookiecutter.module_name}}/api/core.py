import flask
from flask import jsonify
from flask import request

from {{cookiecutter.module_name}} import exceptions


bp = flask.Blueprint('core', __name__)


@bp.route('/hi')
def say_hi():
    ret = {
        'content': 'hello'
    }
    return jsonify(ret)
