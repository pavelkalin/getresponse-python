import json
import os
import unittest
from unittest import TestCase, skipIf
import nose
from collections import defaultdict

from mock import patch, MagicMock

from getresponse.getresponsev3 import Campaigns, FromFields, CustomFields, Newsletters

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

@skipIf(not API_ENDPOINT and not API_KEY, 'No credentials provided')
class TestNewsletters(TestCase):
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
        cls.getresponse = Newsletters(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()

    @staticmethod
    def _get_test_data_path(filename):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        test_data_dir = os.path.join(directory, 'testdata/newsletters')
        return os.path.join(test_data_dir, filename)

    @staticmethod
    def _open_test_data(filename):
        with open(TestNewsletters._get_test_data_path(filename + '.json')) as f:
            return json.load(f)

    @staticmethod
    def _open_test_data_html(filename):
        with open(TestNewsletters._get_test_data_path(filename + '.html')) as f:
            return f.read()

    def test_get_newsletters(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestNewsletters._open_test_data('get_newsletters')
        data = json.loads(json.dumps([{'type': 'broadcast', 'flags': 'openrate,clicktrack', 'campaign': {'campaignId': 'O', 'href': 'https://api3.getresponse360.pl/v3/campaigns/O', 'name': 'nikolaysemenov'}, 'sendOn': '2017-03-13T19:36:24+0000', 'name': 'vip_time_club_test', 'sendMetrics': {'total': '5', 'status': 'finished', 'sent': '5'}, 'editor': 'getresponse', 'status': 'enabled', 'createdOn': '2017-03-13T19:33:03+0000', 'sendSettings': {'timeTravel': 'false', 'perfectTiming': 'false'}, 'subject': 'Hi from VIP Time Club!', 'href': 'https://api3.getresponse360.pl/v3/newsletters/d', 'newsletterId': 'd'}]
))

        response = self.getresponse.get_newsletters()
        self.assertListEqual(response, data)

    def test_get_newsletter(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestNewsletters._open_test_data('get_newsletter')
        data = json.loads(json.dumps({'replyTo': {'href': 'https://api3.getresponse360.pl/v3/from-fields/3', 'fromFieldId': '3'}, 'href': 'https://api3.getresponse360.pl/v3/newsletters/d', 'subject': 'Hi from VIP Time Club!', 'content': {'plain': '', 'html': '<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\r\n<!--[if !mso]><!-->\r\n<meta http-equiv="X-UA-Compatible" content="IE=edge" />\r\n<!--<![endif]--> \r\n<meta name="viewport" content="width=device-width, initial-scale=1" />\r\n<meta name="x-apple-disable-message-reformatting" />\r\n<!--[if gte mso 9]>\r\n<xml>\r\n<o:OfficeDocumentSettings>\r\n<o:AllowPNG/>\r\n<o:PixelsPerInch>96</o:PixelsPerInch>\r\n</o:OfficeDocumentSettings>\r\n</xml>\r\n<![endif]-->\r\n<title></title>\r\n<style type="text/css">\r\n<!--\r\n#outlook a { padding: 0; }\r\n.ReadMsgBody { width: 100%; background-color: #ebebeb }\r\n.ExternalClass { width: 100%; background-color: #ebebeb }\r\n.ExternalClass * { line-height: 100% !important; }\r\nhtml, body { margin: 0 auto !important; padding: 0 !important; height: 100% !important; width: 100% !important; background-color: #ebebeb; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; transform: scale(1, 1); zoom: 1; }\r\n* { -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; }\r\ndiv[style*="margin: 16px 0"] { margin: 0 !important; }\r\n.wrap { table-layout: fixed; width: 100% !important; padding: 0px; margin: 0px; }\r\nimg {display: block;-ms-interpolation-mode: bicubic;margin: 0 !important;padding: 0 !important;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}\r\ntable font {background-color: inherit;}\r\ntable {border-collapse: collapse;border-spacing: 0px;padding: 0px;empty-cells: hide;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-webkit-font-smoothing: antialiased;-moz-osx-font-smoothing: grayscale;}\r\ntable * {-webkit-font-smoothing: antialiased;-moz-osx-font-smoothing: grayscale;}\r\ntr {border-collapse: collapse;border-spacing: 0px;}\r\ntd {display: table-cell !important;border-collapse: collapse;border-spacing: 0px;}\r\ntd.column {display: table-cell !important;min-width: auto;max-width: auto;float: none !important;}\r\ntd.tdBlock {display: inline-block !important;}\r\nbody[data-getresponse] td[class="column"] {display: table-cell !important;float: none !important;min-width: auto;max-width: auto;}\r\n@media all and (max-width: 480px) {\r\ndiv.wrap > div {width: 100% !important;}body {-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}\r\ntable {-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}\r\ntable[class="column-full-width"] { width: 100% !important; }table td {-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}\r\ndiv[class="WRAPPER"] {max-width: 100% !important;width: 100% !important;}\r\ntable td[class="column"] {display: block;max-width: 100% !important;width: auto !important;}\r\ntable[data-editable="rss"] table { padding: 5px 10px !important; }\r\ntable[class="wrapper"] {width: 100% !important;max-width: 100% !important;}\r\ntable[data-mobile-width="1"] {max-width: 100% !important;width: 100% !important;}\r\ntable[data-mobile-width="0"] {max-width: 100% !important;}\r\ntable[data-mobile-width="0"] td {padding-left: 10px !important;padding-right: 10px !important;}\r\ntable[data-editable="image"] img {width: 100%;max-width: 100% !important;height: auto !important;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}\r\ntable[data-editable="image"][align="center"], table[data-editable="button"][align="center"] {margin-left: auto !important;margin-right: auto !important;}\r\ntable[data-editable="image"][align="right"], table[data-editable="button"][align="right"] {margin-left: auto !important;margin-right: 0px !important;}\r\ntable[data-mobile-width="1"] {width: 100% !important;}\r\ntable[data-mobile-width="1"] img {width: 100% !important;max-width: 100% !important;height: auto !important;}\r\nbody[data-getresponse] table td {display: block !important;width: 100% !important;height: auto !important;}\r\nbody[data-getresponse] td[class="column"] {display: block !important;max-width: 100% !important;}\r\nbody[data-getresponse] table td[data-disabled] {display: none !important;}\r\ntable[data-editable="text"] table[data-editable="button"] {float: none;}\r\ntable[data-mobile-width="1"] td {padding-left: 0 !important; padding-right: 0 !important;}\r\ntable[data-editable="text"] td {padding-left: 10px !important;padding-right: 10px !important;}\r\ntable[data-editable="button"][align="left"] td {margin-left: 10px !important;}\r\ntable[data-editable="button"][align="right"] td {margin-right: 10px !important;}\r\ntable[data-editable="text"] table[data-editable="image"] {max-width: 100% !important;margin: 0px;}\r\ntable[data-editable="text"] table[data-mobile-width] td {padding: 0 !important;padding-bottom: 10px !important;}\r\ntable[data-editable="socialmedia"] table {text-align: center !important;}\r\ntr[data-columns="no"] { text-align: center; }\r\ntr[data-columns="no"] > td {display: inline-block !important;width: auto !important;margin: auto;padding: 5px;}\r\ntable[data-editable="menu"] tr[data-columns="no"] > td { display: table-cell !important; }\r\nbody[data-getresponse] table[class="nowrap"] td {display: table-cell !important;width: auto !important;}\r\ntfoot .wrapper table {float: none !important;margin: auto !important;width: 100% !important;}\r\ntfoot .wrapper table td {display: inline-block;width: 100%;text-align: center !important;}\r\ntfoot .wrapper table td img {margin: auto !important;}\r\n.pl_image {width: 100% !important;}\r\nbody[data-getresponse] tr[data-columns="no"] > td {display: inline-block !important;width: auto !important;margin: auto !important;padding: 5px;}body[data-getresponse] table[data-editable="menu"] tr[data-columns="no"] > td { display: table-cell !important; padding: 0; }\r\n\r\ntable[class="column-full-width"] > td, td[class="column"] td { border-left: none !important; border-right: none !important; }\r\ndiv[class="column"] { width: 100% !important; max-width: 100% !important; }\r\n.column { display: block !important; width: 100% !important; max-width: 100% !important; }}\r\n.pl_image, .outline .editable .imagemask div {vertical-align: middle;text-align: center;font-family: Arial,Helvetica,sans-serif;color: #ffffff;font-size: 20px;-webkit-border-radius: 6px;-moz-border-radius: 6px;border-radius: 6px;background: #dedede url(https://www.getresponse.com/images/common/templates/messages/elements/placeholders/image.png) no-repeat 50% 50%;width: 100%;height: 100%;overflow: hidden;}\r\n--></style>\r\n<!--[if gte mso 9]><style type="text/css">\r\n* { mso-line-height-rule: exactly; }\r\ntable {border-collapse: collapse;}\r\ntable tr td {line-height: 100%; mso-line-height-rule: exactly; }\r\ndiv[class="WRAPPER"] {display: inline-block !important;}\r\n.lh-1 { line-height: 115% !important; }\r\n.lh-2 { line-height: 125% !important; }\r\n.lh-3 { line-height: 135% !important; }\r\n.lh-4 { line-height: 145% !important; }\r\n.lh-5 { line-height: 155% !important; }\r\n.lh-6 { line-height: 165% !important; }\r\n.lh-7 { line-height: 175% !important; }\r\n.lh-8 { line-height: 185% !important; }\r\n.lh-9 { line-height: 195% !important; }\r\n.lh-10 { line-height: 205% !important; }\r\n</style><![endif]--></head>\r\n<body data-getresponse="true" style="margin: 0; padding: 0;">\r\n<div class="wrap" style="width: 100%; min-width: 320px; table-layout: fixed; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"><style type="text/css"><!-- table[class="wrapper"] {width: undefinedpx;max-width: undefinedpx !important;font-size: 16px;}\r\ntd[class="column"] { min-width: 0 !important; } \r\nbody[data-getresponse] td[class="column"] { float: none !important; }body[xx-iframe] td[class="column"] { display: table-cell !important; float: none !important; }--></style>\r\n<table align="center" width="100%" cellpadding="0" cellspacing="0" border="0" data-mobile="true" dir="ltr" data-width="600" style="font-size: 16px; background-color: rgb(235, 235, 235);">\r\n    <tbody><tr>\r\n        <td align="center" valign="top" style="margin:0;padding:0 0 130px;">\r\n            <table align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff" width="600" class="wrapper" style="width: 600px;">\r\n                <tbody><tr>\r\n                    <td align="center" valign="top" bgcolor="#ebebeb" style="margin:0;padding:0 50px;">\r\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" width="223">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="center" style="margin: 0px; padding: 32px 0px 24px; display: inline-block; background-color: rgb(235, 235, 235);" class="tdBlock"><a href=""><img src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png" alt="" width="223" height="23" border="0" data-origsrc="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png" data-src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png|223|23|223|23|0|0|1" style="border: 0px none transparent; display: block;"></a></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0;padding:0;">\r\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="1" width="100%" style="max-width: 100% !important;">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://multimedia.email.v-t-club.ru/viptimeclub/2/2/photos/1.png?img1489433652937" alt="" width="600" border="0" style="border: 0px none transparent; display: block; width: 100%; max-width: 100% !important;" data-src="http://multimedia.email.v-t-club.ru/viptimeclub/2/2/photos/1.png|600|280|600|280|0|0|1" data-origsrc="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_02.png"></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" bgcolor="#00b0ff" style="margin:0; padding:0;background-color:#00b0ff;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-0" style="margin: 0px; padding: 20px 0px; line-height: 1.05; background-color: rgb(0, 176, 255); font-size: 16px; font-family: \'Times New Roman\', Times, serif;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#ffffff;font-size:44px;">\r\n                                        <span style="font-size:90px;white-space: nowrap;">Only 15</span><br> apartments left\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td valign="top" align="left" style="padding:0;margin:0;">\r\n                        <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="left" class="lh-2" style="padding: 40px 50px 15px; margin: 0px; line-height: 1.25; font-size: 16px; font-family: \'Times New Roman\', Times, serif;">\r\n                                    <span style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;color:#000000; line-height:1.2;"><a href="http://www.v-t-club.ru/actions/" target="_blank" title="">\r\n                                        Now’s the time to hurry! Some time ago, you signed up to our email list, so we thought you might be interested in hearing the latest news.</a></span><div><span style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;color:#000000; line-height:1.2;"><br></span></div><div><span style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;color:#000000; line-height:1.2;"><br>    random 123: {{RANDOM "1" "2" "3"}}<br><br><br>    Привет&nbsp;[[firstname]]<br>    Твой возраст -&nbsp;[[exact_age]]<br>    Ссылка отписаться -&nbsp;[[remove]]<br>    Ссылка миррор -&nbsp;[[view]]<br><br>    Динамический контент&nbsp;[[exact_age]]<br><br>    дата&nbsp;[[date format="eu2" shift="+2 day"]]<br><br>    [[pre hello]]<br>\r\n                                        <br>\r\n                                        <span style="font-weight:400;">As of today, we have only 15 apartments left!</span>\r\n                                    </span>\r\n                                </div></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0; padding:0;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 15px 50px 5px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:30px;">\r\n                                        See what we offer:\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0;padding:0;">\r\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 524px;">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png" alt="" width="524" height="397" border="0" data-origsrc="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png" data-src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png|524|397|524|397|0|0|1" style="border: 0px none transparent; display: block;"></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0; padding:0;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\r\n                                        Spacious living room\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0;padding:0;">\r\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 523px;">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png" alt="" width="523" height="396" border="0" data-origsrc="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png" data-src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png|523|396|523|396|0|0|1" style="border: 0px none transparent; display: block;"></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0; padding:0;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\r\n                                        Modern kitchen\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0;padding:0;">\r\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 523px;">\r\n                            <tbody><tr>\r\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png" alt="" width="523" height="396" border="0" data-origsrc="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png" data-src="http://www.email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png|523|396|523|396|0|0|1" style="border: 0px none transparent; display: block;"></td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0; padding:0;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\r\n                                        Elegant bathroom\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td align="center" valign="top" style="margin:0; padding:0;">\r\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\r\n                            <tbody><tr>\r\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 25px 50px 20px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\r\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:30px;">\r\n                                        Step into modern living.\r\n                                    </span>\r\n                                </td>\r\n                            </tr>\r\n                        </tbody></table>\r\n                    </td>\r\n                </tr>\r\n                <tr>\r\n                    <td valign="top" align="center" style="padding:0 0 50px;margin:0;">\r\n                        <div data-box="button" style="width: 100%; margin-top: 0px; margin-bottom: 0px; text-align: center;"><table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="button" style="margin: 0px auto;">\r\n                                <tbody><tr>\r\n                                    <td valign="middle" align="center" class="tdBlock" style="display: inline-block; padding: 15px 28px 14px; margin: 0px; border-top-left-radius: 6px; border-top-right-radius: 6px; border-bottom-right-radius: 6px; border-bottom-left-radius: 6px; background-color: rgb(0, 176, 255);"><a href="" style="font-family:Helvetica,Arial,sans-serif;color:#ffffff;font-size:20px;font-weight:600;text-decoration:none;">\r\n                                            Book a visit\r\n                                        </a></td>\r\n                                </tr>\r\n                            </tbody></table></div>\r\n                    </td>\r\n                </tr>\r\n            </tbody></table>\r\n        </td>\r\n    </tr>\r\n</tbody><tfoot><tr><td align="center" style="margin: 0px; padding: 0px;"><table cellspacing="0" cellpadding="0" align="center" border="0" class="wrapper" width="600" style="width: 600px;"><tbody><tr><td valign="top" align="center" style="background-color: #fff;">[[internal_footer]]</td></tr></tbody></table></td></tr></tfoot></table>\r\n</div></body>\r\n</html>'}, 'createdOn': '2017-03-13T19:33:03+0000', 'sendMetrics': {'status': 'finished', 'total': '5', 'sent': '5'}, 'editor': 'getresponse', 'campaign': {'name': 'nikolaysemenov', 'href': 'https://api3.getresponse360.pl/v3/campaigns/O', 'campaignId': 'O'}, 'name': 'vip_time_club_test', 'sendSettings': {'selectedSuppresions': [], 'timeTravel': 'false', 'excludedSegments': [], 'excludedCampaigns': [], 'selectedContacts': [], 'selectedSegments': [], 'selectedCampaigns': ['O'], 'selectedSuppressions': [], 'perfectTiming': 'false'}, 'flags': ['openrate', 'clicktrack'], 'newsletterId': 'd', 'status': 'enabled', 'clickTracks': [{'name': 'http://www.v-t-club.ru/actions/', 'amount': '3', 'url': 'http://www.v-t-club.ru/actions/', 'clickTrackId': 'd'}], 'sendOn': '2017-03-13T19:36:24+0000', 'fromField': {'href': 'https://api3.getresponse360.pl/v3/from-fields/e', 'fromFieldId': 'e'}, 'type': 'broadcast', 'attachments': []}
))

        response = self.getresponse.get_newsletter('d')
        self.assertEqual(response, data)
        self.assertEqual(response['newsletterId'], data['newsletterId'])

    def test_get_newsletters_statistics(self):
        self.mock_get.return_value.ok = True
        self.mock_get.return_value = MagicMock()
        self.mock_get.return_value.json.return_value = TestNewsletters._open_test_data('get_newsletters_statistics')
        data = json.loads(json.dumps([{'goals': '0', 'totalClicked': '3', 'unsubscribed': '1', 'forwarded': '0', 'uniqueOpened': '4', 'uniqueGoals': '0', 'totalOpened': '5', 'bounced': '1', 'uniqueClicked': '3', 'complaints': '0', 'sent': '5', 'timeInterval': '2017-03-13T00:00:00+0000/P15DT11H0M0S'}]
))

        response = self.getresponse.get_newsletters_statistics((['newsletterId=d']))
        self.assertListEqual(response, data)

    def test_post_newsletters(self):
        self.mock_post.return_value.ok = True
        self.mock_post.return_value = MagicMock()
        self.mock_post.return_value.json.return_value = TestNewsletters._open_test_data('post_newsletters')
        data = json.loads(json.dumps({'status': 'enabled', 'flags': ['openrate', 'clicktrack'], 'editor': 'custom', 'clickTracks': [], 'newsletterId': 'Y', 'campaign': {'name': 'test_camp', 'campaignId': 'e', 'href': 'https://api3.getresponse360.pl/v3/campaigns/e'}, 'attachments': [], 'sendSettings': {'perfectTiming': 'false', 'excludedSegments': [], 'selectedSegments': [], 'selectedSuppressions': [], 'selectedCampaigns': ['e'], 'excludedCampaigns': [], 'selectedContacts': [], 'selectedSuppresions': [], 'timeTravel': 'false'}, 'href': 'https://api3.getresponse360.pl/v3/newsletters/Y', 'createdOn': '2017-04-06T10:52:45+0000', 'sendOn': '2017-04-06T10:52:45+0000', 'type': 'broadcast', 'name': 'test', 'fromField': {'fromFieldId': '3', 'href': 'https://api3.getresponse360.pl/v3/from-fields/3'}, 'subject': 'test auch', 'replyTo': {'fromFieldId': None, 'href': 'https://api3.getresponse360.pl/v3/from-fields'}, 'sendMetrics': {'total': '0', 'status': 'in_progress', 'sent': '0'}, 'content': {'plain': '', 'html': '<table align="center" width="100%" cellpadding="0" cellspacing="0" border="0" data-mobile="true" dir="ltr" data-width="600" style="font-size: 16px; background-color: rgb(235, 235, 235);">\n    <tbody><tr>\n        <td align="center" valign="top" style="margin:0;padding:0 0 130px;">\n            <table align="center" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff" width="600" class="wrapper" style="width: 600px;">\n                <tbody><tr>\n                    <td align="center" valign="top" bgcolor="#ebebeb" style="margin:0;padding:0 50px;">\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" width="223">\n                            <tbody><tr>\n                                <td valign="top" align="center" style="margin: 0px; padding: 32px 0px 24px; display: inline-block; background-color: rgb(235, 235, 235);" class="tdBlock"><a href=""><img src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png" alt="" width="223" height="23" border="0" data-origsrc="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png" data-src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_01.png|223|23|223|23|0|0|1" style="border: 0px none transparent; display: block;"></a></td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0;padding:0;">\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="1" width="100%" style="max-width: 100% !important;">\n                            <tbody><tr>\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_02.png" alt="" width="600" border="0" data-origsrc="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_02.png" data-src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_02.png|600|280|600|280|0|0|1" style="border: 0px none transparent; display: block; width: 100%; max-width: 100% !important;"></td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" bgcolor="#00b0ff" style="margin:0; padding:0;background-color:#00b0ff;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-0" style="margin: 0px; padding: 20px 0px; line-height: 1.05; background-color: rgb(0, 176, 255); font-size: 16px; font-family: \'Times New Roman\', Times, serif;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#ffffff;font-size:44px;">\n                                        <span style="font-size:90px;white-space: nowrap;">Only 15</span><br> apartments left\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td valign="top" align="left" style="padding:0;margin:0;">\n                        <table align="center" width="100%" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td valign="top" align="left" class="lh-2" style="padding: 40px 50px 15px; margin: 0px; line-height: 1.25; font-size: 16px; font-family: \'Times New Roman\', Times, serif;">\n                                    <span style="font-family:Helvetica,Arial,sans-serif;font-size:20px;font-weight:300;color:#000000; line-height:1.2;">\n                                        Now’s the time to hurry! Some time ago, you signed up to our email list, so we thought you might be interested in hearing the latest news.<br>\n                                        <br>\n                                        <span style="font-weight:400;">As of today, we have only 15 apartments left!</span>\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0; padding:0;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 15px 50px 5px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:30px;">\n                                        See what we offer:\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0;padding:0;">\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 524px;">\n                            <tbody><tr>\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png" alt="" width="524" height="397" border="0" data-origsrc="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png" data-src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_03.png|524|397|524|397|0|0|1" style="border: 0px none transparent; display: block;"></td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0; padding:0;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\n                                        Spacious living room\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0;padding:0;">\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 523px;">\n                            <tbody><tr>\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png" alt="" width="523" height="396" border="0" data-origsrc="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png" data-src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_04.png|523|396|523|396|0|0|1" style="border: 0px none transparent; display: block;"></td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0; padding:0;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\n                                        Modern kitchen\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0;padding:0;">\n                        <table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="image" data-mobile-width="0" style="max-width: 523px;">\n                            <tbody><tr>\n                                <td valign="top" align="center" style="margin: 0px; padding: 0px; display: inline-block;" class="tdBlock"><img src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png" alt="" width="523" height="396" border="0" data-origsrc="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png" data-src="http://email.v-t-club.ru/images/common/templates/messages/1054/1/img/1054_05.png|523|396|523|396|0|0|1" style="border: 0px none transparent; display: block;"></td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0; padding:0;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 0px 0px 8px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:24px;">\n                                        Elegant bathroom\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td align="center" valign="top" style="margin:0; padding:0;">\n                        <table width="100%" align="center" border="0" cellpadding="0" cellspacing="0" data-editable="text">\n                            <tbody><tr>\n                                <td align="center" valign="top" class="lh-1" style="margin: 0px; padding: 25px 50px 20px; font-size: 16px; font-family: \'Times New Roman\', Times, serif; line-height: 1.15;">\n                                    <span style="padding:0;font-family:Helvetica,Arial,sans-serif;font-weight:300;color:#000000;font-size:30px;">\n                                        Step into modern living.\n                                    </span>\n                                </td>\n                            </tr>\n                        </tbody></table>\n                    </td>\n                </tr>\n                <tr>\n                    <td valign="top" align="center" style="padding:0 0 50px;margin:0;">\n                        <div data-box="button" style="width: 100%; margin-top: 0px; margin-bottom: 0px; text-align: center;"><table border="0" cellpadding="0" cellspacing="0" align="center" data-editable="button" style="margin: 0px auto;">\n                                <tbody><tr>\n                                    <td valign="middle" align="center" class="tdBlock" style="display: inline-block; padding: 15px 28px 14px; margin: 0px; border-top-left-radius: 6px; border-top-right-radius: 6px; border-bottom-right-radius: 6px; border-bottom-left-radius: 6px; background-color: rgb(0, 176, 255);"><a href="" style="font-family:Helvetica,Arial,sans-serif;color:#ffffff;font-size:20px;font-weight:600;text-decoration:none;">\n                                            Book a visit\n                                        </a></td>\n                                </tr>\n                            </tbody></table></div>\n                    </td>\n                </tr>\n            </tbody></table>\n        </td>\n    </tr>\n</tbody></table>'}}
                                     ))

        newsletter_campaign = {'campaignId': 'e'}
        newsletter_from = {'fromFieldId': '3'}
        html = TestNewsletters._open_test_data_html('newsletter')
        newsletter_content = Newsletters.prepare_content(html, '')


        response = self.getresponse.post_newsletters('test', 'test auch', newsletter_from, newsletter_campaign,
                                                         newsletter_content, Newsletters.prepare_send_settings(selected_campaigns=['e']))
        self.assertEqual(response, data)
    
if __name__ == '__main__':
    nose.run()
