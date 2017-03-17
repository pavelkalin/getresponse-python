import os
import json

from getresponse.getresponsev3 import Api

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = Api(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

campaigns = getresponse.get_campaigns()
print('List of all campaigns is: \n {}'.format(campaigns))

campaign = getresponse.get_campaign(campaigns[0]['campaignId'])
print('Campaign details of 1 campaign from all is: \n {}'.format(campaign))

print('Result of campaign which does not exist is: \n {}'.format(getresponse.get_campaign('dasda')))

print('Result of new campaign addition is: \n {}'.format(getresponse.post_campaign('test_camp', language_code='RU')))
