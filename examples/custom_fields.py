import os
import json

from getresponse.getresponsev3 import CustomFields

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = CustomFields(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

custom_fields = getresponse.get_custom_fields()
print('List of all from fields is: \n {}'.format(custom_fields))
print('List of all from fields is: \n {}'.format(getresponse.get_custom_fields(sort='asc')))
