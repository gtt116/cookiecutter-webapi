from {{cookiecutter.module_name}}.db import base
from {{cookiecutter.module_name}} import cfg


def get_session():
    maker = base.maker(cfg.config('DB').get('sql_connection'), False)
    return maker()
