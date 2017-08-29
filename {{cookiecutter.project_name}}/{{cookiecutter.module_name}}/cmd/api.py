from {{cookiecutter.module_name}} import cfg
from {{cookiecutter.module_name}} import log
from {{cookiecutter.module_name}}.api import wsgi


def main():
    cfg.load_config()
    log.setup()
    wsgi.run_api()
