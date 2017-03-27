import json
import os
import unittest
from unittest import TestCase, skipIf
import nose
from collections import defaultdict

from mock import patch, MagicMock

from getresponse.getresponsev3 import Campaigns, FromFields, CustomFields

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)


@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestCampaigns(TestCase):
    """
    Test campaigns section of API
    """
    maxDiff = None  # to see diff in long texts

    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('getresponse.getresponsev3.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post_patcher = patch('getresponse.getresponsev3.requests.post')
        cls.mock_post = cls.mock_post_patcher.start()
        cls.getresponse = Campaigns(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()

    @staticmethod
    def _get_test_data_path(filename):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        test_data_dir = os.path.join(directory, 'testdata/campaigns')
        return os.path.join(test_data_dir, filename)

    @staticmethod
    def _open_test_data(filename):
        with open(TestCampaigns._get_test_data_path(filename + '.json')) as f:
            return json.load(f)

    def test_get_campaigns(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data('get_campaigns')
        data = json.loads(
            '[{"description": "nikolaysemenov", "href": "https://api3.getresponse360.pl/v3/campaigns/O","campaignId": "O", "name": "nikolaysemenov", "createdOn": "2017-03-13T19:24:59+0000","isDefault": "true", "languageCode": "RU"}]')

        response = self.getresponse.get_campaigns()

        self.assertListEqual(response, data)
        self.assertEqual(response[0]['campaignId'], 'O')

    def test_get_campaign(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data('get_campaign_id')
        data = json.loads(
            '{"name": "nikolaysemenov", "isDefault": "true", "profile": {"description": "", "title": "", "industryTagId": null, "logoLinkUrl": "", "logo": ""}, "createdOn": "2017-03-13T19:24:59+0000", "languageCode": "RU", "campaignId": "O", "postal": {"design": "[[name]], [[address]], [[city]], [[state]] [[zip]], [[country]]", "zipCode": "123456", "state": "NA", "companyName": "GetResponse", "street": "NA", "addPostalToMessages": "true", "city": "NA", "country": "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u0424\u0435\u0434\u0435\u0440\u0430\u0446\u0438\u044f"}, "href": "https://api3.getresponse360.pl/v3/campaigns/O", "optinTypes": {"webform": "double", "email": "double", "import": "single", "api": "double"}, "confirmation": {"mimeType": "text/html", "redirectUrl": null, "subscriptionConfirmationSubjectId": "e1mT", "subscriptionConfirmationBodyId": "e1IM", "redirectType": "hosted", "fromField": {"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}, "replyTo": {"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}}, "subscriptionNotifications": {"status": "enabled", "recipients": [{"href": "https://api3.getresponse360.pl/v3/from-fields/3", "fromFieldId": "3"}]}}')

        response = self.getresponse.get_campaign('O')

        self.assertEqual(response, data)
        self.assertEqual(response['campaignId'], data['campaignId'])

    def test_post_campaign(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestCampaigns._open_test_data('post_campaign')
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
        self.mock_post.return_value.json.return_value = TestCampaigns._open_test_data('update_campaign')
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
                                                    optinTypes=Campaigns._get_option_types(email='single',
                                                                                           import_type='single',
                                                                                           webform='single'))

        self.assertEqual(response, data)
        self.assertEqual(response['campaignId'], data['campaignId'])

    def test_get_campaign_contacts(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data('get_campaign_contacts')
        data = json.loads(json.dumps([{'email': 'xxx@yandex.ru', 'name': 'Yandex', 'contactId': 'F'}]))

        response = self.getresponse.get_campaign_contacts('O', query=['email=ru'], fields='name,email,campaigns')

        self.assertEqual(response, data)
        self.assertEqual(response[0]['contactId'], data[0]['contactId'])

    def test_get_campaign_blacklist(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data('get_campaign_blacklist')
        data = json.loads(json.dumps({'masks': ['spam-spam@gmail.com', 'spam@gmail.com']}))

        response = self.getresponse.get_campaign_blacklist('O', 'gmail.com')

        self.assertEqual(response, data)
        self.assertTrue(str(response).find('gmail.com') > 0)

    def test_post_campaign_blacklist(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestCampaigns._open_test_data('post_campaign_blacklist')
        data = json.loads(json.dumps({'masks': ['spam@sgmail.com', 'spamparam@gmail.com']}))

        response = self.getresponse.post_campaign_blacklist('O', ['spam@sgmail.com', 'spamparam@gmail.com'])

        self.assertEqual(response, data)
        self.assertTrue(str(response).find('gmail.com') > 0)
        self.assertTrue(len(response['masks']) == 2)

    def test_get_campaigns_statistics_list_size(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_list_size')
        data = json.loads(json.dumps([{'totalSubscribers': 3, 'addedSubscribers': 0}]))

        response = self.getresponse.get_campaigns_statistics_list_size(['groupBy=month'], 'O',
                                                                       fields='totalSubscribers,addedSubscribers')  # type: list[dict]

        self.assertEqual(response, data)
        self.assertTrue(len(response[0].keys()) == 2)

    def test_get_campaigns_statistics_locations(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_locations')
        data = json.loads(json.dumps({'RU': {'continentCode': 'EU', 'amount': '3', 'countryCode': 'RU'}}))

        response = self.getresponse.get_campaigns_statistics_locations(['groupBy=month'], 'O')

        self.assertEqual(response, data)

    def test_get_campaigns_statistics_origins(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_origins')
        data = json.loads(
            '[{"2014-12-15":{"import":19,"email":18,"www":19,"panel":19,"leads":6,"sale":6,"api":9,"forward":25,"survey":14,"iphone":22,"copy":17,"landing_page":11,"summary":192},"2015-01-01":{"import":120,"email":126,"www":122,"panel":108,"leads":105,"sale":105,"api":138,"forward":127,"survey":107,"iphone":123,"copy":120,"landing_page":118,"summary":1444}}]')

        response = self.getresponse.get_campaigns_statistics_origins(['groupBy=month'], 'O')

        self.assertEqual(response, data)

    def test_get_campaigns_statistics_removals(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_removals')
        data = json.loads(json.dumps({'3': {'total': {'unsubscribe': 28, 'bounce': 21}}}))

        response = self.getresponse.get_campaigns_statistics_removals(['groupBy=month'], 'O')

        self.assertEqual(response, data)

    def test_get_campaigns_statistics_subscriptions(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_subscriptions')
        data = json.loads(json.dumps({'3': {
            'total': {'mobile': 0, 'survey': 0, 'panel': 0, 'api': 0, 'forward': 0, 'www': 0, 'leads': 0,
                      'import': 9905, 'sale': 0, 'copy': 0, 'landing_page': 0, 'summary': 9905, 'email': 0}}}
        ))

        response = self.getresponse.get_campaigns_statistics_subscriptions(['groupBy=total'], 'O')

        self.assertEqual(response, data)

    def test_get_campaigns_statistics_balance(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_balance')
        data = json.loads(json.dumps({'total': {'removals': {'unsubscribe': 28, 'bounce': 21},
                                                'subscriptions': {'landing_page': 0, 'leads': 0, 'sale': 0, 'survey': 0,
                                                                  'panel': 0, 'api': 0, 'www': 0, 'forward': 0,
                                                                  'copy': 0, 'email': 0, 'summary': 9905,
                                                                  'import': 9905, 'mobile': 0}}}
                                     ))

        response = self.getresponse.get_campaigns_statistics_balance(['groupBy=total'], 'O')

        self.assertEqual(response, data)

    def test_get_campaigns_statistics_summary(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCampaigns._open_test_data(
            'get_campaigns_statistics_summary')
        data = json.loads(json.dumps({'d': {'totalNewsletters': '1', 'totalLandingPages': '0', 'totalTriggers': '0',
                                            'totalWebforms': '0', 'totalSubscribers': '0'},
                                      '3': {'totalNewsletters': '12', 'totalLandingPages': '0', 'totalTriggers': '0',
                                            'totalWebforms': '0', 'totalSubscribers': '9843'}}
                                     ))

        response = self.getresponse.get_campaigns_statistics_summary('3,d')
        self.assertEqual(response, data)


@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestFromFields(TestCase):
    """
    Test From fields section of API
    """

    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('getresponse.getresponsev3.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post_patcher = patch('getresponse.getresponsev3.requests.post')
        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_delete_patcher = patch('getresponse.getresponsev3.requests.delete')
        cls.mock_delete = cls.mock_delete_patcher.start()
        cls.getresponse = FromFields(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()

    @staticmethod
    def _get_test_data_path(filename):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        test_data_dir = os.path.join(directory, 'testdata/from_fields')
        return os.path.join(test_data_dir, filename)

    @staticmethod
    def _open_test_data(filename):
        with open(TestFromFields._get_test_data_path(filename + '.json')) as f:
            return json.load(f)

    def test_get_from_fields(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestFromFields._open_test_data('all')
        data = json.loads(json.dumps([{'createdOn': '2017-03-13T19:32:52+0000', 'name': 'VIP pam',
                                       'email': 'info@domain.com', 'isActive': 'true', 'fromFieldId': 'e',
                                       'isDefault': 'true', 'href': 'https://api3.getresponse360.pl/v3/from-fields/e'},
                                      {'createdOn': '2017-03-13T19:24:59+0000', 'name': 'Nikolay',
                                       'email': 'nikolay@example.ru', 'isActive': 'true', 'fromFieldId': '3',
                                       'isDefault': 'false', 'href': 'https://api3.getresponse360.pl/v3/from-fields/3'}]
                                     ))

        response = self.getresponse.get_from_fields()
        self.assertListEqual(response, data)

    def test_get_from_field(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestFromFields._open_test_data('get_from_field')
        data = json.loads(json.dumps({'name': 'VIP', 'fromFieldId': 'e', 'email': 'info@xxx.ru'}))

        response = self.getresponse.get_from_field('e')
        self.assertEqual(response, data)
        self.assertEqual(response['fromFieldId'], data['fromFieldId'])

    def test_post_from_field(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestFromFields._open_test_data('post_from_field')
        data = json.loads(json.dumps(
            {'fromFieldId': 'V', 'href': 'https://api3.getresponse360.pl/v3/from-fields/V', 'isDefault': 'false',
             'isActive': 'false', 'name': 'Test', 'createdOn': '2017-03-25T15:08:43+0000', 'email': 'pavel@mail.ru'}
        ))

        response = self.getresponse.post_from_field('Test', 'pavel@mail.ru')
        self.assertEqual(response, data)

    def test_delete_or_replace_from_field(self):
        self.mock_delete.return_value.ok = True
        self.mock_delete.return_value = MagicMock()
        self.mock_delete.return_value.json.return_value = TestFromFields._open_test_data('delete_or_replace_from_field')
        self.mock_delete.return_value.text = TestFromFields._open_test_data('delete_or_replace_from_field')
        data = json.loads(json.dumps({}))

        response = self.getresponse.delete_or_replace_from_field('3')
        self.assertEqual(response, data)

    def test_make_default(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestFromFields._open_test_data('make_default')
        data = json.loads(json.dumps(
            {'email': 'info@mail.ru', 'createdOn': '2017-03-13T19:24:59+0000', 'fromFieldId': '3', 'isDefault': 'true',
             'isActive': 'true', 'name': 'XXX', 'href': 'https://api3.getresponse360.pl/v3/from-fields/3'}
        ))

        response = self.getresponse.make_default('v')
        self.assertEqual(response, data)


@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestCustomFields(TestCase):
    """
    Test Custom Fields section of API
    """
    maxDiff = None  # to see diff in long texts

    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('getresponse.getresponsev3.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post_patcher = patch('getresponse.getresponsev3.requests.post')
        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_delete_patcher = patch('getresponse.getresponsev3.requests.delete')
        cls.mock_delete = cls.mock_delete_patcher.start()
        cls.getresponse = CustomFields(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()

    @staticmethod
    def _get_test_data_path(filename):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        test_data_dir = os.path.join(directory, 'testdata/custom_fields')
        return os.path.join(test_data_dir, filename)

    @staticmethod
    def _open_test_data(filename):
        with open(TestCustomFields._get_test_data_path(filename + '.json')) as f:
            return json.load(f)

    def test_get_custom_fields(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCustomFields._open_test_data('get_custom_fields')
        data = json.loads(json.dumps([{'type': 'text', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/g',
                                       'fieldType': 'text', 'values': ['tedt'], 'customFieldId': 'g',
                                       'valueType': 'string', 'name': 'aba', 'hidden': 'true'},
                                      {'type': 'single_select',
                                       'href': 'https://api3.getresponse360.pl/v3/custom-fields/K',
                                       'fieldType': 'single_select',
                                       'values': ['18-29', '30-44', '45-59', '60+', '<18'], 'customFieldId': 'K',
                                       'valueType': 'string', 'name': 'age', 'hidden': 'false'},
                                      {'type': 'date', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/s',
                                       'fieldType': 'text', 'values': [], 'customFieldId': 's', 'valueType': 'date',
                                       'name': 'birthdate', 'hidden': 'false'},
                                      {'type': 'text', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/P',
                                       'fieldType': 'text', 'values': [], 'customFieldId': 'P', 'valueType': 'string',
                                       'name': 'city', 'hidden': 'false'},
                                      {'type': 'textarea', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/n',
                                       'fieldType': 'textarea', 'values': [], 'customFieldId': 'n',
                                       'valueType': 'string', 'name': 'comment', 'hidden': 'false'},
                                      {'type': 'text', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/E',
                                       'fieldType': 'text', 'values': [], 'customFieldId': 'E', 'valueType': 'string',
                                       'name': 'company', 'hidden': 'false'}]))

        response = self.getresponse.get_custom_fields()
        self.assertListEqual(response, data)

    def test_get_custom_field(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestCustomFields._open_test_data('get_custom_field')
        data = json.loads(json.dumps({'values': ['tedt'], 'type': 'text', 'fieldType': 'text',
                                      'href': 'https://api3.getresponse360.pl/v3/custom-fields/g',
                                      'valueType': 'string', 'name': 'aba', 'customFieldId': 'g', 'hidden': 'true'}
                                     ))

        response = self.getresponse.get_custom_field('g')
        self.assertEqual(response, data)

    def test_post_custom_field(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestCustomFields._open_test_data('post_custom_field')
        data = json.loads(json.dumps(
            {'name': 'qwer', 'customFieldId': 'b', 'valueType': 'string', 'hidden': 'false', 'type': 'text',
             'values': ['qwe'], 'fieldType': 'text', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/b'}
            ))

        response = self.getresponse.post_custom_field('qwer', 'text', False, ['qwe'])
        self.assertEqual(response, data)

    def test_delete_custom_field(self):
        self.mock_delete.return_value.ok = True
        self.mock_delete.return_value = MagicMock()
        self.mock_delete.return_value.json.return_value = TestCustomFields._open_test_data('delete_custom_field')
        self.mock_delete.return_value.text = TestCustomFields._open_test_data('delete_custom_field')
        data = json.loads(json.dumps({}))

        response = self.getresponse.delete_custom_field('3')
        self.assertEqual(response, data)

    def test_update_custom_field(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestCustomFields._open_test_data('update_custom_field')
        data = json.loads(json.dumps(
            {'customFieldId': 'i', 'hidden': 'false', 'href': 'https://api3.getresponse360.pl/v3/custom-fields/i',
             'valueType': 'string', 'type': 'text', 'name': 'zzz', 'values': ['z'], 'fieldType': 'text'}
            ))

        response = self.getresponse.update_custom_field('i', False)
        self.assertEqual(response, data)


if __name__ == '__main__':
    nose.run()
