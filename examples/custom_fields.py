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
# print('List of all custom fields is: \n {}'.format(custom_fields))
print('List of all custom fields is: \n {}'.format(getresponse.get_custom_fields(sort='desc', fields='hidden,name')))
# print('List of custom field with id {} is: \n {}'.format(custom_fields[0]['customFieldId'],
#                                                          getresponse.get_custom_field(
#                                                              custom_fields[0]['customFieldId'])))
# print('Result of creation new custom field is: \n {}'.format(
#     getresponse.post_custom_field('qwer', 'text', False, ['qwe'])))


# print('Result of deletion new custom field is: \n {}'.format(getresponse.delete_custom_field('g')))

# print('List of all custom fields is: \n {}'.format(getresponse.get_custom_fields(fields='name')))

print('Result of update custom fields is: \n {}'.format(getresponse.update_custom_field('i', False)))
