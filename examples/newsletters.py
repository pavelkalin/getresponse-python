import os
import json

from getresponse.getresponsev3 import Newsletters

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = Newsletters(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

newsletters = getresponse.get_newsletters(sort='asc')
print('List of all newsletters is: \n {}'.format(newsletters))

newsletter = getresponse.get_newsletter('d')
print('Newsletter with id {} is: \n {}'.format('d', newsletter))
newsletter_stats = getresponse.get_newsletters_statistics(['newsletterId=d'])
print('Newsletter stats of id {} is: \n {}'.format('d', newsletter_stats))