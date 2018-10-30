import os
import json

from getresponse.getresponsev3 import SearchContacts

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = SearchContacts(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

segments = getresponse.get_segments()
print('List of all segments is: \n {}'.format(segments))

# contacts = getresponse.get_contacts('m')
# print('List of all contacts for segment XXX is: \n {}'.format(contacts))
