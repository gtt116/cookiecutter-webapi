import json

import mock

from {{cookiecutter.module_name}}.tests import base as testbase


class CoreAPITests(testbase.APITestCase):

    @mock.patch('{{cookiecutter.module_name}}.ocr.api._download_image')
    def test_process_ocr_works(self, mock_download_image):
        mock_download_image.return_value = 'imagecontent'
        data = json.dumps({
            "url": "http://www.baidu.com"
        })
        resp = self.app.post('/v1/ocr',
                             headers={'Content-Type': 'application/json'},
                             data=data)
        self.assertEqual(resp.status_code, 200, resp.status)

    def test_process_ocr_given_invalid_url(self):
        data = json.dumps({
            "url": "invalid url"
        })
        resp = self.app.post('/v1/ocr',
                             headers={'Content-Type': 'application/json'},
                             data=data)
        self.assertEqual(resp.status_code, 400, resp.status)

    def test_not_given_url(self):
        data = "{}"
        resp = self.app.post('/v1/ocr',
                             headers={'Content-Type': 'application/json'},
                             data=data)
        self.assertEqual(resp.status_code, 400, resp.status)
