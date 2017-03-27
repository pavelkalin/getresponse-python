"""A library that provides a Python interface to the GetResponse API"""
import requests
from collections import defaultdict
import json


class GetresponseClient(object):
    """
    Base class which does requests calls
    """
    API_ENDPOINT = 'https://api.getresponse.com/v3'
    API_KEY = None
    X_DOMAIN = None
    X_TIME_ZONE = None
    HEADERS = None

    def __init__(self, api_endpoint: str, api_key: str, x_domain: str = None, x_time_zone: str = None):
        """
        Initiation of Client object
        :param api_endpoint: API Endpoint - http://apidocs.getresponse.com/v3
        Usually either https://api.getresponse.com/v3 for normal GetResponse account or
        https://api3.getresponse360.[pl|com]/v3 for Getresponse 360
        :param api_key: API key, should be generated here - https://app.getresponse.com/manage_api.html
        :param x_domain: http://apidocs.getresponse.com/v3/configuration
        Account url for GetResponse 360 without http,https and www
        :param x_time_zone: TZ column from https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        The default timezone in response data is UTC
        """
        self.API_ENDPOINT = api_endpoint
        self.API_KEY = api_key
        self.X_DOMAIN = x_domain
        self.X_TIME_ZONE = x_time_zone
        if x_domain:
            self.HEADERS = {'X-Auth-Token': 'api-key ' + self.API_KEY, 'X-DOMAIN': self.X_DOMAIN,
                            'Content-Type': 'application/json'}
        else:
            self.HEADERS = {'X-Auth-Token': 'api-key ' + self.API_KEY, 'Content-Type': 'application/json'}

    def get(self, url: str):
        r = requests.get(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.json()

    def post(self, url: str, data: json):
        r = requests.post(self.API_ENDPOINT + url, data=data, headers=self.HEADERS)
        return r.json()

    def delete(self, url: str, data: json = None):
        if data:
            r = requests.delete(self.API_ENDPOINT + url, data=data, headers=self.HEADERS)
        else:
            r = requests.delete(self.API_ENDPOINT + url, headers=self.HEADERS)
        return r.text


class Campaigns(object):
    """
    Class represents campaigns section of API
    http://apidocs.getresponse.com/v3/resources/campaigns
    """

    def __init__(self, api_endpoint: str, api_key: str, x_domain: str = None, x_time_zone: str = None):
        self._getresponse_client = GetresponseClient(api_endpoint=api_endpoint, api_key=api_key, x_domain=x_domain,
                                                     x_time_zone=x_time_zone)

    def get_campaigns(self, query: list = None, sort: list = None, **kwargs):
        """
        Get all campaigns within account
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get.all
        :param query: Used to search only resources that meets criteria. Can be:
                                        - name
            Should be passed like this: query = ['name=searched query', ..]
            Examples:
                    query = ['name=VIP']
        :param sort: Enable sorting using specified field (set as a key) and order (set as a value).
            multiple fields to sort by can be used. Can be:
                                        - name: asc or desc
                                        - createdOn: asc or desc

            Should be passed like this: sort = ['name=asc', ..]
            Examples:
                    sort = ['name=asc','createdOn=desc']
                    query = ['name=asc']
        :param kwargs:
            - fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
            - page: Specify which page of results return. :type: int
            - perPage: Specify how many results per page should be returned :type: int
        :return: JSON response
        """
        url = str('/campaigns?')
        if query:
            for item in query:
                query_data = str(item).split('=')
                url = url + 'query[' + query_data[0] + ']=' + query_data[1] + '&'
        if sort:
            for item in sort:
                sort_data = str(item).split('=')
                url = url + 'sort[' + sort_data[0] + ']=' + sort_data[1] + '&'
        if kwargs:
            for key, value in kwargs.items():
                url = url + str(key) + '=' + str(value) + '&'
        url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaign(self, campaign_id: str):
        """
        Get campaign details by id
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get
        :param campaign_id: Id of campaign
        :return: JSON response
        """
        r = self._getresponse_client.get('/campaigns/' + campaign_id)
        return r

    @staticmethod
    def _get_confirmation(from_field: dict, reply_to: dict, redirect_type: str, redirect_url: str = None):
        """
        Subscription confirmation email settings
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param from_field: dict {"fromFieldId": 'xxx'} FromFieldId from from-fields resources
        :param reply_to: dict {"fromFieldId": 'xxx'} FromFieldId from from-fields resources
        :param redirect_type: What will happen after confirmation of email. Possible values: hosted (subscriber will stay on GetResponse website), customUrl (subscriber will be redirected to provided url)
        :param redirect_url: Url where subscriber will be redirected if redirectType is set to customUrl
        :return: dict
        """
        if redirect_url:
            response = {"fromField": from_field, "replyTo": reply_to, "redirectType": redirect_type,
                        "redirectUrl": redirect_url}
        else:
            response = {"fromField": from_field, "replyTo": reply_to, "redirectType": redirect_type}
        return response

    @staticmethod
    def _get_profile(industry_tag_id: int, description: str, logo: str, logo_link_url: str, title: str):
        """
        How campaign will be visible for subscribers
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param industry_tag_id: Category of content of campaign
        :param description: Short description of campaign content, length 2-255
        :param logo: Url of image displayed as campaign logo
        :param logo_link_url: Url of link in campaign logo
        :param title: Title of campaign, length 2-64
        :return: dict
        """
        response = {"industryTagId": industry_tag_id, "description": description, "logo": logo,
                    "logoLinkUrl": logo_link_url, "title": title}
        return response

    @staticmethod
    def _get_postal(add_postal_to_messages: str, city: str, company_name: str, design: str, state: str, street: str,
                    zipcode: str):
        """
        Postal address of your company
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param add_postal_to_messages: Should postal address be sent with all messages from campaign. (For US and Canada it's mandatory)
        :param city: City
        :param company_name: Company name
        :param design: How postal address would be designed in emails. Avaiable fields definitions: [[name]], [[address]], [[city]], [[state]] [[zip]], [[country]]
        :param state: State
        :param street: Street
        :param zipcode: Zip code
        :return: dict
        """
        response = {"addPostalToMessages": add_postal_to_messages, "city": city, "companyName": company_name,
                    "design": design, "state": state, "street": street, "zipCode": zipcode}
        return response

    @staticmethod
    def _get_option_types(email: str, import_type: str, webform: str):
        """
        How subscribers will be added to list - with double (with confirmation) or single optin
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param email: Optin type for subscriptions via email. Possible values: single, double
        :param import_type: Optin type for subscriptions via import. Possible values: single, double
        :param webform: Optin type for subscriptions via webforms and landing pages. Possible values: single, double
        :return: dict
        """
        response = {"email": email, "import": import_type, "webform": webform}
        return response

    @staticmethod
    def _get_subscription_notifications(status: str, recipients: list):
        """
        Notifications for each subscribed email to Your list
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param status: Are notifications enabled. Possible values: enabled, disabled
        :param recipients: Emails where to send notifications. They have to be defined in account from fields
        :return: dict
        """
        response = {"status": status, "recipients": recipients}
        return response

    def post_campaign(self, name: str, **kwargs):
        """
        Create new campaign
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.create
        :param name: Campaign name which has to be unique in whole GetResponse platform
        :param kwargs:
                -languageCode: Campaign language code (2 letters format)
                -isDefault: Possible values: true, false. Is campaign default for account. You cannot remove default flag, only reassign it to other campaign.
                -confirmation: Subscription confirmation email settings. Dict from _get_confirmation method
                -profile: How campaign will be visible for subscribers. Dict from _get_profile
                -postal: Postal address of your company. Dict from _get_postal
                -optinTypes: How subscribers will be added to list - with double (with confirmation) or single optin. Dict from  _get_option_types
                -subscriptionNotifications: Notifications for each subscribed email to Your list.  Dict from _get_subscription_notifications
        :return: JSON response
        """
        data = defaultdict()
        data['name'] = name
        for key, value in kwargs.items():
            data[key] = value
        r = self._getresponse_client.post('/campaigns', data=json.dumps(data))
        return r

    def update_campaign(self, campaign_id: str, **kwargs):
        """
        Allows to update campaign prefenrences. Send only those fields that need to be changed.
        The rest of properties will stay the same.
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.update
        :param campaign_id: Id of campaign to update
        :param kwargs:
                -languageCode: Campaign language code (2 letters format)
                -isDefault: Possible values: true, false. Is campaign default for account. You cannot remove default flag, only reassign it to other campaign.
                -confirmation: Subscription confirmation email settings. Dict from _get_confirmation method
                -profile: How campaign will be visible for subscribers. Dict from _get_profile
                -postal: Postal address of your company. Dict from _get_postal
                -optinTypes: How subscribers will be added to list - with double (with confirmation) or single optin. Dict from  _get_option_types
                -subscriptionNotifications: Notifications for each subscribed email to Your list.  Dict from _get_subscription_notifications
        :return: JSON response
        """
        data = defaultdict()
        for key, value in kwargs.items():
            data[key] = value
        r = self._getresponse_client.post('/campaigns/' + campaign_id, data=json.dumps(data))
        return r

    def get_campaign_contacts(self, campaign_id: str, query: list = None, sort: list = None, **kwargs):
        """
        Allows to retrieve all contacts from given campaigns. Standard sorting and filtering apply.
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.contacts.get
        :param campaign_id: Id of given campaign
        :param query: Used to search only resources that meets criteria. Can be:
                                        - email
                                        - name
                                        - createdOn][from]
                                        - createdOn][to]
            Should be passed like this: query = ['email=searched query', ..]
            Examples:
                    query = ['email=@gmail.com','createdOn][from]=2017-03-10']
                    query = ['createdOn][from]=2017-03-10']
        :param sort: Enable sorting using specified field (set as a key) and order (set as a value).
            multiple fields to sort by can be used. Can be:
                                        - email: asc or desc
                                        - name: asc or desc
                                        - createdOn: asc or desc

            Should be passed like this: sort = ['email=asc', ..]
            Examples:
                    sort = ['email=asc','createdOn=desc']
                    query = ['name=asc']
        :param kwargs:
            - fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
            - page: Specify which page of results return. :type: int
            - perPage: Specify how many results per page should be returned :type: int
        :return: JSON response
        """
        url = str('/campaigns/' + campaign_id + '/contacts?')
        if query:
            for item in query:
                query_data = str(item).split('=')
                url = url + 'query[' + query_data[0] + ']=' + query_data[1] + '&'
        if sort:
            for item in sort:
                sort_data = str(item).split('=')
                url = url + 'sort[' + sort_data[0] + ']=' + sort_data[1] + '&'
        if kwargs:
            for key, value in kwargs.items():
                url = url + str(key) + '=' + str(value) + '&'
        url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaign_blacklist(self, campaign_id: str, mask: str):
        """
        This request allows to fetch blacklist for given campaign.
        Blacklist is simple plain collection of email addresses or partial masks (like @gmail.com)
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.blacklists.get
        :param campaign_id: Id of campaign
        :param mask: Blacklist mask to search for
        :return: JSON response
        """
        r = self._getresponse_client.get('/campaigns/' + campaign_id + '/blacklists?query[mask]=' + mask)
        return r

    def post_campaign_blacklist(self, campaign_id: str, mask: list):
        """
        This request allows to update blacklist. Full list is expected.
        This list will replace the present list
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.blacklists.update
        :param campaign_id: Id of campaign
        :param mask: Blacklist mask
        :return: JSON response
        """
        data = {'masks': mask}
        r = self._getresponse_client.post('/campaigns/' + campaign_id + '/blacklists', data=json.dumps(data))
        return r

    @staticmethod
    def _prepare_url_from_query(url: str, query: list, campaign_id: str):
        """
        Method to populate url with query and campaign id
        :param url: str
        :param query: list like this ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
        :param campaign_id: Id of campaign.
        :return:
        """
        url = url + 'query[campaignId]=' + campaign_id + '&'
        for item in query:
            query_data = str(item).split('=')
            url = url + 'query[' + query_data[0] + ']=' + query_data[1] + '&'
        return url

    def get_campaigns_statistics_list_size(self, query: list, campaign_id: str, fields: str = None):
        """
        Get list size for found campaigns
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.statistics.list-size
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/list-size?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_locations(self, query: list, campaign_id: str, fields: str = None):
        """
        Get locations for found campaigns
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.statistics.locations
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/locations?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_origins(self, query: list, campaign_id: str, fields: str = None):
        """
        Get origins for found campaigns
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.statistics.locations
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/origins?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_removals(self, query: list, campaign_id: str, fields: str = None):
        """
        Get removals for found campaigns
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.statistics.removals
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/removals?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_subscriptions(self, query: list, campaign_id: str, fields: str = None):
        """
        Get removals for found campaigns
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.statistics.subscriptions
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/subscriptions?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_balance(self, query: list, campaign_id: str, fields: str = None):
        """
        Get balance for found campaigns (i.e. subscriptions and removals)
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get.balance
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - groupBy String. Can be:
                                            - hour
                                            - day
                                            - month
                                            - total
                        - createdOn][from] Date in YYYY-mm-dd
                        - createdOn][to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn][from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn][from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str('/campaigns/statistics/balance?')
        url = Campaigns._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r

    def get_campaigns_statistics_summary(self, campaign_id_list: str, fields: str = None):
        """
        Get summary for found campaigns (i.e. subscriptions and removals)
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get.summary
        :param campaign_id_list: List of campaigns. Fields should be separated by comma
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :return: JSON response
        """
        url = str('/campaigns/statistics/summary?')
        url = Campaigns._prepare_url_from_query(url, [], campaign_id_list)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = self._getresponse_client.get(url)
        return r


class FromFields(object):
    """
    Class represents From fields section of API
    http://apidocs.getresponse.com/v3/resources/fromfields
    """

    def __init__(self, api_endpoint: str, api_key: str, x_domain: str = None, x_time_zone: str = None):
        self._getresponse_client = GetresponseClient(api_endpoint=api_endpoint, api_key=api_key, x_domain=x_domain,
                                                     x_time_zone=x_time_zone)

    def get_from_fields(self, query: list = None, **kwargs):
        """
        Get all from fields within account
        http://apidocs.getresponse.com/v3/resources/fromfields#fromfields.get.all
        :param query: Used to search only resources that meets criteria.
                      If multiple parameters are specified then it uses AND logic.
                      Can be:
                        - name
                        - email (should be full email as expression is strict equality)
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['name=Test', 'email=info@test.com' ]
                        query = ['name=Test']
        :param kwargs:
                       - fields: :type: str
                       List of fields that should be returned. Fields should be separated by comma
                       - sort: Enable sorting using specified field (set as a key) and order (set as a value).
                               Can be:
                                        - createdOn: - asc
                                                     - desc
                       - perPage: :type: int
                       Number results on page
                       - page: :type: int
                       Page number
        :return: JSON response
        """
        url = '/from-fields?'
        if query:
            for item in query:
                query_data = str(item).split('=')
                url = url + 'query[' + query_data[0] + ']=' + query_data[1] + '&'
        for key, value in kwargs.items():
            if key == 'sort':
                url = url + key + '[createdOn]=' + value + '&'
            else:
                url = url + key + '=' + value + '&'
        url = url[:-1]  # get rid of last & or ?
        r = self._getresponse_client.get(url)
        return r

    def get_from_field(self, field_id: str, fields: str = None):
        """
        This method returns from field by fromfieldId.
        http://apidocs.getresponse.com/v3/resources/fromfields#fromfields.get
        :param field_id: Id of the field to return
        :param fields: List of fields that should be returned. Fields should be separated by comma
        :return: JSON response
        """
        url = '/from-fields/' + field_id
        if fields:
            url += '?fields=' + fields
        r = self._getresponse_client.get(url)
        return r

    def post_from_field(self, name: str, email: str):
        """
        This request will create new from-field
        http://apidocs.getresponse.com/v3/resources/fromfields#fromfields.create
        :param name: Name connected to email address
        :param email: Email
        :return: JSON response
        """
        url = '/from-fields'
        data = {'name': name, 'email': email}
        r = self._getresponse_client.post(url, data=json.dumps(data))
        return r

    def delete_or_replace_from_field(self, from_field_id: str, replace_id: str = None):
        """
        This request removes fromField.
        New fromFieldId could be passed in the body of this request, and it will replace removed from field.
        http://apidocs.getresponse.com/v3/resources/fromfields#fromfields.delete
        :param replace_id: Id of replacement from field
        :return: Empty response or error response
        """
        url = '/from-fields/' + from_field_id
        if replace_id:
            data = {'fromFieldIdToReplaceWith': replace_id}
            r = self._getresponse_client.delete(url, data=json.dumps(data))
        else:
            r = self._getresponse_client.delete(url)
        return r

    def make_default(self, from_field_id: str):
        """
        Make from field default
        http://apidocs.getresponse.com/v3/resources/fromfields#fromfields.default
        :param from_field_id: Id of from field
        Field should be active, i.e. it's 'isActive' property should be set to 'true'
        :return: JSON response
        """
        url = '/from-fields/' + from_field_id + '/default'
        r = self._getresponse_client.post(url, data=None)
        return r


class CustomFields(object):
    """
    Class represents Custom fields section of API
    http://apidocs.getresponse.com/v3/resources/customfields
    """

    def __init__(self, api_endpoint: str, api_key: str, x_domain: str = None, x_time_zone: str = None):
        self._getresponse_client = GetresponseClient(api_endpoint=api_endpoint, api_key=api_key, x_domain=x_domain,
                                                     x_time_zone=x_time_zone)

    def get_custom_fields(self, **kwargs):
        """
        Get custom fields
        http://apidocs.getresponse.com/v3/resources/customfields#customfields.get.all
        :param kwargs:
                - fields: :type: str
                List of fields that should be returned. Fields should be separated by comma
                - sort: Enable sorting using specified field (set as a key) and order (set as a value).
                Can be:
                        - name: - asc
                                - desc
                - perPage: :type: int
                Number results on page
                - page: :type: int
                Page number
        :return:
        """
        url = '/custom-fields?'
        for key, value in kwargs.items():
            if key == 'sort':
                url = url + key + '[name]=' + value + '&'
            else:
                url = url + key + '=' + value + '&'
        url = url[:-1]  # get rid of last & or ?
        r = self._getresponse_client.get(url)
        return r

    def get_custom_field(self, field_id: str, fields: str = None):
        """
        Get custom field by id
        http://apidocs.getresponse.com/v3/resources/customfields#customfields.get
        :param field_id: Id of custom field
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :return: JSON Response
        """
        url = '/custom-fields/' + field_id
        if fields:
            url += '?fields=' + fields
        r = self._getresponse_client.get(url)
        return r

    def post_custom_field(self, name: str, type: str, hidden: bool, values: list):
        """
        Create custom field
        http://apidocs.getresponse.com/v3/resources/customfields#customfields.create
        :param name: Name of the custom field.
        Should be:
        - from 1 to 32 characters long
        - be unique
        - use only lowercase letters, underscores and digits
        - not be equal to one of the merge words used in messages, i.e. name, email, campaign, twitter, facebook, buzz,
          myspace, linkedin, digg, googleplus, pinterest, responder, campaign, change
        :param type: Type of custom field value. Cane be text for example
        :param hidden: Flag if custom field is visible to contact
        :param values: List of assigned values (one or more - depending of customField type)
        :return: JSON Response
        """
        url = '/custom-fields'
        data = {'name': name, 'type': type, 'hidden': hidden, 'values': values}
        r = self._getresponse_client.post(url, data=json.dumps(data))
        return r

    def delete_custom_field(self, field_id: str):
        """
        Delete custom field by id
        http://apidocs.getresponse.com/v3/resources/customfields#customfields.delete
        :param field_id: Id of custom field
        :return Empty response or error response
        """
        url = '/custom-fields/' + field_id
        r = self._getresponse_client.delete(url)
        return r

    def update_custom_field(self, field_id: str, hidden: bool, values: list = None):
        """
        Update custom field
        http://apidocs.getresponse.com/v3/resources/customfields#customfields.update
        :param hidden: Flag if custom field is visible to contact
        :param values: List of assigned values (one or more - depending of customField type)
        :return: JSON Response
        """
        url = '/custom-fields/' + field_id
        if values:
            data = {'hidden': hidden, 'values': values}
        else:
            data = {'hidden': hidden}
        r = self._getresponse_client.post(url, data=json.dumps(data))
        return r


if __name__ == '__main__':
    import doctest

    doctest.testmod()
