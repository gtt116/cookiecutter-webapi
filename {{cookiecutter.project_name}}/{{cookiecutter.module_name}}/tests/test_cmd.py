from {{cookiecutter.module_name}} import cfg
from {{cookiecutter.module_name}}.cmd import manage
from {{cookiecutter.module_name}}.tests import base as testbase


class CmdTestCase(testbase.DBTestCase):

    def test_alembic_upgrade_head(self):
        cfg.config("DB")['sql_connection'] = 'sqlite://'
        # no raise here.
        manage.do_alembic_command('upgrade', 'head')
