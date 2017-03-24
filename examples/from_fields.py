import os
import json

from getresponse.getresponsev3 import FromFields

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = FromFields(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

from_fields = getresponse.get_from_fields()
print('List of all from fields is: \n {}'.format(from_fields))
