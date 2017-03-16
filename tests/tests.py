import json
import os
import unittest
from unittest import TestCase, skipIf

from mock import patch, MagicMock

from getresponse.getresponsev3 import Api

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)


@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestApi(TestCase):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('getresponse.getresponsev3.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.getresponse = Api(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    @staticmethod
    def _get_test_data_path(filename):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        test_data_dir = os.path.join(directory, 'testdata')
        return os.path.join(test_data_dir, filename)

    @staticmethod
    def _open_test_data(filename):
        with open(TestApi._get_test_data_path(filename + '.json')) as f:
            return json.load(f)

    def test_get_campaigns(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestApi._open_test_data('get_campaigns')
        todos = [{"userId": 1,"id": 1,"title": "Make the bed","completed": "False"}]

        response = self.getresponse.get_campaigns()

        self.assertListEqual(response, todos)


if __name__ == '__main__':
    unittest.main()
