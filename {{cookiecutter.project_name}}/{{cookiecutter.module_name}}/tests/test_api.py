import json

import mock

from {{cookiecutter.module_name}}.tests import base as testbase


class CoreAPITests(testbase.APITestCase):

    def test_hi(self):
        resp = self.app.get('/v1/hi',
                             headers={'Content-Type': 'application/json'})
        self.assertEqual(resp.status_code, 200, resp.status)
