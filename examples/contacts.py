import os
import json

from getresponse.getresponsev3 import Contacts, CustomFields
from datetime import datetime

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)
CAMPAIGN_ID = 'O'

getresponse = Contacts(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

contacts = getresponse.get_contacts(query=['campaignId=' + CAMPAIGN_ID], additionalFlags='exactMatch')
print('List of all contacts  is: \n {}'.format(contacts))

# add_contact = getresponse.post_contacts(email='test@gmail.com', campaign_id=CAMPAIGN_IG, name='Павел')
# print(add_contact)
#
# contacts = getresponse.get_contacts(query=['campaignId=O'], additionalFlags='exactMatch')
# print('List of all contacts of CampaignId O is: \n {}'.format(contacts))

customs = CustomFields(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)
updated = datetime.now().strftime('%Y%m%d%H%M%S')
print(updated)
custom_fields = {'customFieldValues': [{'customFieldId': 'GBaeF', 'value': ['5']}, {'customFieldId': 'GBP0L', 'value': [updated]}]}
print(customs.get_custom_fields())
getresponse.update_contact_customs('O1Ultv', custom_fields)
