"""A library that provides a Python interface to the GetResponse API"""
import requests
from collections import defaultdict
import json


class Api(object):
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

    def get_campaigns(self, **kwargs):
        """
        Get all campaigns within account
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get.all
        :param kwargs: options: search string like page=1&perPage=100&sort[name]=asc
                       name: campaign name
        :return: JSON response
        """
        r = None
        if not kwargs:
            r = requests.get(self.API_ENDPOINT + '/campaigns', headers=self.HEADERS)
        elif 'name' in kwargs.keys():
            if 'options' in kwargs.keys():
                r = requests.get(self.API_ENDPOINT + '/campaigns?query[name]=' + kwargs['name'] + kwargs['options'],
                                 headers=self.HEADERS)
            else:
                r = requests.get(self.API_ENDPOINT + '/campaigns?query[name]=' + kwargs['name'], headers=self.HEADERS)
        return r.json()

    def get_campaign(self, campaign_id: str):
        """
        Get campaign details by id
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get
        :param campaign_id: Id of campaign
        :return: JSON response
        """

        r = requests.get(self.API_ENDPOINT + '/campaigns/' + campaign_id, headers=self.HEADERS)
        return r.json()

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
        r = requests.post(self.API_ENDPOINT + '/campaigns', headers=self.HEADERS, data=json.dumps(data))
        return r.json()

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
        r = requests.post(self.API_ENDPOINT + '/campaigns/' + campaign_id, headers=self.HEADERS, data=json.dumps(data))
        return r.json()

    def get_campaign_contacts(self, campaign_id: str, query: list = None, **kwargs):
        """
        Allows to retrieve all contacts from given campaigns. Standard sorting and filtering apply.
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.contacts.get
        :param campaign_id: Id of given campaign
        :param query: Used to search only resources that meets criteria. Can be:
                                        - email
                                        - name
                                        - createdOn[from]
                                        - createdOn[to]
            Should be passed like this: query = ['email=searched query', ..]
            Examples:
                    query = ['email=@gmail.com','createdOn[from]=2017-03-10']
                    query = ['createdOn[from]=2017-03-10']
        :param kwargs:
            - fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
            - sort: Enable sorting using specified field (set as a key) and order (set as a value).
            multiple fields to sort by can be used.
            - page: Specify which page of results return. :rtype: int
            - perPage: Specify how many results per page should be returned :rtype: int
        :return: JSON response
        """
        q = False  # check whether there was a query in a call
        url = str(self.API_ENDPOINT + '/campaigns/' + campaign_id + '/contacts')
        if query:
            url += '?'
            q = True
            for item in query:
                query_data = str(item).split('=')
                url = url + 'query[' + query_data[0] + ']=' + query_data[1] + '&'
        if kwargs:
            if not q:
                url += '?'
            for key, value in kwargs.items():
                url = url + str(key) + '=' + str(value) + '&'
        url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

    def get_campaign_blacklist(self, campaign_id: str, mask: str):
        """
        This request allows to fetch blacklist for given campaign.
        Blacklist is simple plain collection of email addresses or partial masks (like @gmail.com)
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.blacklists.get
        :param campaign_id: Id of campaign
        :param mask: Blacklist mask to search for
        :return: JSON response
        """
        r = requests.get(self.API_ENDPOINT + '/campaigns/' + campaign_id + '/blacklists?query[mask]=' + mask,
                         headers=self.HEADERS)
        return r.json()

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
        r = requests.post(self.API_ENDPOINT + '/campaigns/' + campaign_id + '/blacklists',
                          headers=self.HEADERS, data=json.dumps(data))
        return r.json()

    @staticmethod
    def _prepare_url_from_query(url: str, query: list, campaign_id: str):
        """
        Method to populate url with query and campaign id
        :param url: str
        :param query: list like this ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/list-size?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/locations?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/origins?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/removals?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/subscriptions?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

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
                        - createdOn[from] Date in YYYY-mm-dd
                        - createdOn[to] Date in YYYY-mm-dd
                      Should be passed like this: query = ['email=searched query', ..]
                      Examples:
                        query = ['createdOn[from]=2017-03-10', 'groupBy=hour' ]
                        query = ['createdOn[from]=2017-03-10']
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :param campaign_id: Id of campaign. For multiple campaigns can be separated by comma like O,323fD,ddeE
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/balance?')
        url = Api._prepare_url_from_query(url, query, campaign_id)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        r = requests.get(url, headers=self.HEADERS)
        return r.json()

    def get_campaigns_statistics_summary(self, campaign_id_list: str, fields: str = None):
        """
        Get summary for found campaigns (i.e. subscriptions and removals)
        http://apidocs.getresponse.com/v3/resources/campaigns#campaigns.get.summary
        :param campaign_id_list: List of campaigns. Fields should be separated by comma
        :param fields: List of fields that should be returned. Id is always returned. Fields should be separated by comma
        :return: JSON response
        """
        url = str(self.API_ENDPOINT + '/campaigns/statistics/summary?')
        url = Api._prepare_url_from_query(url, [], campaign_id_list)
        if fields:
            url += 'fields=' + fields
        else:
            url = url[:-1]  # get rid of last &
        print(url)
        r = requests.get(url, headers=self.HEADERS)
        return r.json()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
