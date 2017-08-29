import unittest
import tempfile
import shutil

from {{cookiecutter.module_name}}.api import app
from {{cookiecutter.module_name}} import cfg
from {{cookiecutter.module_name}}.db import base as dbbase
from {{cookiecutter.module_name}}.db import models


class NoDBTestCase(unittest.TestCase):
    """Testcases that not using database access."""

    @classmethod
    def setUpClass(cls):
        cfg.load_config(default=True)

    def setUp(self):
        super(NoDBTestCase, self).setUp()
        self._tempdir = tempfile.mkdtemp()

    def tearDown(self):
        super(NoDBTestCase, self).tearDown()
        shutil.rmtree(self._tempdir)


class DBTestCase(NoDBTestCase):
    """Testcases that using database access.

    We create a sqlite in memory to speed up testcases.
    """

    _multiprocess_shared_ = True

    def setUp(self):
        super(DBTestCase, self).setUp()
        self._setup_temp_database()

    def tearDown(self):
        self._teardown_temp_databse()
        super(DBTestCase, self).tearDown()

    def _setup_temp_database(self):
        cfg.config('DB')['sql_connection'] = 'sqlite://'
        engine = dbbase.get_engine(cfg.config("DB").get('sql_connection'))
        models.BASE.metadata.create_all(engine)

    def _teardown_temp_databse(self):
        for _, e in dbbase.ENGINES.iteritems():
            e.dispose()

        # Force dbapi using new sql_connection
        dbbase.ENGINES.clear()


class APITestCase(DBTestCase):
    """
    All tests for api based on flask should subclass it
    """

    def setUp(self):
        super(APITestCase, self).setUp()
        self.webapp = app.create_webapp()
        self.webapp.config['SERVER_NAME'] = '127.0.0.1'
        self.webapp.config['TESTING'] = True
        self.app = self.webapp.test_client()
