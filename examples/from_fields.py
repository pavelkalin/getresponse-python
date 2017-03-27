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
print('List of all from fields is: \n {}'.format(getresponse.get_from_fields(sort='asc')))
#
# print('List of all from fields is: \n {}'.format(
#     getresponse.get_from_fields(query=['email=info@mail.ru', 'name=VIP'], fields='email,name,fromFieldId')))
#
# from_fields_id = from_fields[0]['fromFieldId']
# print('List of from field with id {} is: \n {}'.format(from_fields_id,
#                                                        getresponse.get_from_field(from_fields_id,
#                                                                                   'email,name,fromFieldId')))
# new_from_field = getresponse.post_from_field('Test', 'pavel10@mail.ru')
# print('Result of creation of new from field is: \n {}'.format(new_from_field))
#
# new_from_field2 = getresponse.post_from_field('Test', 'pavel7@mail.ru')
# print('Result of creation of new from field is: \n {}'.format(new_from_field2))
#
# print('Result of replacement of new from field is: \n {}'.format(
#     getresponse.delete_or_replace_from_field(new_from_field['fromFieldId'], new_from_field2['fromFieldId'])))

# print('Result of replacement of new from field is: \n {}'.format(
#     getresponse.delete_or_replace_from_field('v')))


# print('List of all from fields is: \n {}'.format(getresponse.get_from_fields()))

# print('Make another active from field as default: \n {}'.format(getresponse.make_default('3')))
