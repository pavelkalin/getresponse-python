"""A library that provides a Python interface to the GetResponse API"""
import requests


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
        :param kwargs: options: search string like ?page=1&perPage=100&sort[name]=asc
                       name: campaign name
        :return: JSON return object
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
