import json
import os
import unittest
from unittest import TestCase, skipIf
from collections import defaultdict

from mock import patch, MagicMock

from getresponse.getresponsev3 import Api

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)


@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestApi(TestCase):
    maxDiff = None

    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('getresponse.getresponsev3.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post_patcher = patch('getresponse.getresponsev3.requests.post')
        cls.mock_post = cls.mock_post_patcher.start()
        cls.getresponse = Api(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()

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
        data = json.loads(
            '[{"description": "nikolaysemenov", "href": "https://api3.getresponse360.pl/v3/campaigns/O","campaignId": "O", "name": "nikolaysemenov", "createdOn": "2017-03-13T19:24:59+0000","isDefault": "true", "languageCode": "RU"}]')

        response = self.getresponse.get_campaigns()

        self.assertListEqual(response, data)
        self.assertEqual(response[0]['campaignId'], 'O')

    def test_get_campaign(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestApi._open_test_data('get_campaign_id')
        data = json.loads(
            '{"name": "nikolaysemenov", "isDefault": "true", "profile": {"description": "", "title": "", "industryTagId": null, "logoLinkUrl": "", "logo": ""}, "createdOn": "2017-03-13T19:24:59+0000", "languageCode": "RU", "campaignId": "O", "postal": {"design": "[[name]], [[address]], [[city]], [[state]] [[zip]], [[country]]", "zipCode": "123456", "state": "NA", "companyName": "GetResponse", "street": "NA", "addPostalToMessages": "true", "city": "NA", "country": "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u0424\u0435\u0434\u0435\u0440\u0430\u0446\u0438\u044f"}, "href": "https://api3.getresponse360.pl/v3/campaigns/O", "optinTypes": {"webform": "double", "email": "double", "import": "single", "api": "double"}, "confirmation": {"mimeType": "text/html", "redirectUrl": null, "subscriptionConfirmationSubjectId": "e1mT", "subscriptionConfirmationBodyId": "e1IM", "redirectType": "hosted", "fromField": {"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}, "replyTo": {"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}}, "subscriptionNotifications": {"status": "enabled", "recipients": [{"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}]}}')

        response = self.getresponse.get_campaign('O')

        self.assertEqual(response, data)
        self.assertEqual(response['campaignId'], data['campaignId'])

    def test_post_campaign(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestApi._open_test_data('post_campaign')
        data = json.loads(json.dumps(
            {'languageCode': 'RU', 'confirmation': {'mimeType': 'text/html', 'replyTo': {'fromFieldId': 'e',
                                                                                         'href': 'https://api3.getresponse360.pl/v3/from-fields/e'},
                                                    'subscriptionConfirmationSubjectId': 'e1mT', 'redirectUrl': '',
                                                    'fromField': {'fromFieldId': 'e',
                                                                  'href': 'https://api3.getresponse360.pl/v3/from-fields/e'},
                                                    'subscriptionConfirmationBodyId': 'e1IM', 'redirectType': 'hosted'},
             'createdOn': '2017-03-17T13:50:32+0000', 'name': 'test_camp', 'isDefault': 'false',
             'profile': {'logo': '', 'industryTagId': '', 'logoLinkUrl': '', 'description': '', 'title': ''},
             'optinTypes': {'email': 'double', 'import': 'double', 'api': 'double', 'webform': 'double'},
             'href': 'https://api3.getresponse360.pl/v3/campaigns/e', 'subscriptionNotifications': {
                'recipients': [{'fromFieldId': 'e', 'href': 'https://api3.getresponse360.pl/v3/from-fields/e'}],
                'status': 'enabled'},
             'postal': {'country': 'Russian Federation', 'companyName': 'GetResponse', 'street': 'NA', 'city': 'NA',
                        'zipCode': '123456', 'state': 'NA',
                        'design': '[[name]], [[address]], [[city]], [[state]] [[zip]], [[country]]',
                        'addPostalToMessages': 'true'}, 'campaignId': 'e'}))

        response = self.getresponse.post_campaign('test_camp', languageCode='RU')

        self.assertEqual(response, data)
        self.assertEqual(response['campaignId'], data['campaignId'])

    def test_update_campaign(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestApi._open_test_data('update_campaign')
        data = json.loads(json.dumps({'confirmation': {'redirectType': 'hosted',
                                                       'subscriptionConfirmationBodyId': 'e1IM',
                                                       'replyTo': {'fromFieldId': 'e',
                                                                   'href': 'https://api3.getresponse360.pl/v3/from-fields/e'},
                                                       'mimeType': 'text/html', 'redirectUrl': None,
                                                       'fromField': {'fromFieldId': 'e',
                                                                     'href': 'https://api3.getresponse360.pl/v3/from-fields/e'},
                                                       'subscriptionConfirmationSubjectId': 'e1mT'},
                                      'postal': {'city': 'NA',
                                                 'design': '[[name]], [[address]], [[city]], [[state]] [[zip]], [[country]]',
                                                 'addPostalToMessages': 'true', 'country': 'Russian Federation',
                                                 'state': 'NA', 'zipCode': '123456', 'street': 'NA',
                                                 'companyName': 'GetResponse'},
                                      'profile': {'logo': '', 'logoLinkUrl': '', 'description': '',
                                                  'industryTagId': None, 'title': ''}, 'name': 'test_camp',
                                      'optinTypes': {'api': 'double', 'import': 'single', 'email': 'single',
                                                     'webform': 'single'}, 'campaignId': 'e', 'languageCode': 'RU',
                                      'isDefault': 'false', 'subscriptionNotifications': {'status': 'enabled',
                                                                                          'recipients': [
                                                                                              {'fromFieldId': 'e',
                                                                                               'href': 'https://api3.getresponse360.pl/v3/from-fields/e'}]},
                                      'href': 'https://api3.getresponse360.pl/v3/campaigns/e',
                                      'createdOn': '2017-03-17T13:50:32+0000'}))

        response = self.getresponse.update_campaign(campaign_id='e',
                                                    optinTypes=Api._get_option_types(email='single',
                                                                                     import_type='single',
                                                                                     webform='single'))

        self.assertEqual(response, data)
        self.assertEqual(response['campaignId'], data['campaignId'])

    def test_get_campaign_contacts(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestApi._open_test_data('get_campaign_contacts')
        data = json.loads(json.dumps([{'email': 'xxx@yandex.ru', 'name': 'Yandex', 'contactId': 'F'}]))

        response = self.getresponse.get_campaign_contacts('O', query='email=ru', fields='name,email,campaigns')

        self.assertEqual(response, data)
        self.assertEqual(response[0]['contactId'], data[0]['contactId'])

    def test_get_campaign_blacklist(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestApi._open_test_data('get_campaign_blacklist')
        data = json.loads(json.dumps({'masks': ['spam-spam@gmail.com', 'spam@gmail.com']}))

        response = self.getresponse.get_campaign_blacklist('O', 'gmail.com')

        self.assertEqual(response, data)
        self.assertTrue(str(response).find('gmail.com') > 0)

if __name__ == '__main__':
    unittest.main()
