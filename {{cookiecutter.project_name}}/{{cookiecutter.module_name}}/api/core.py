import flask
from flask import jsonify

bp = flask.Blueprint('core', __name__)


@bp.route('/hi')
def say_hi():
    ret = {
        'content': 'hello'
    }
    return jsonify(ret)
