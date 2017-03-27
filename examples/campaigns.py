import os
import json

from getresponse.getresponsev3 import Campaigns

API_ENDPOINT = os.getenv('API_ENDPOINT', None)
API_KEY = os.getenv('API_KEY', None)
X_DOMAIN = os.getenv('X_DOMAIN', None)
X_TIME_ZONE = os.getenv('X_TIME_ZONE', None)
HEADERS = os.getenv('HEADERS', None)

getresponse = Campaigns(api_endpoint=API_ENDPOINT, api_key=API_KEY, x_domain=X_DOMAIN)

campaigns = getresponse.get_campaigns(sort=['createdOn=asc'])
print('List of all campaigns is: \n {}'.format(campaigns))
#
# campaign = getresponse.get_campaign(campaigns[0]['campaignId'])
# print('Campaign details of 1 campaign from all is: \n {}'.format(campaign))
#
# print('Result of campaign which does not exist is: \n {}'.format(getresponse.get_campaign('dasda')))
#
# print('Result of new campaign addition is: \n {}'.format(getresponse.post_campaign('test_camp3', languageCode='RU')))
#
# # Change campaign option to single instead of double
# print('Result of campaign update is: \n {}'.format(
#     getresponse.update_campaign(campaign_id='e',
#                                 optinTypes=Campaigns._get_option_types(email='single', import_type='single',
#                                                                  webform='single'))))

campaign_id = campaigns[0]['campaignId']
print('Get all contacts from main campaign: \n {}'.format(
    getresponse.get_campaign_contacts(campaign_id, query=['email=com', 'name=а'], fields='name,email,campaigns,createdOn', sort=['email=asc', 'createdOn=desc'])))
#
# print('Get blacklist for given campaign: \n {}'.format(getresponse.get_campaign_blacklist(campaign_id, 'gmail.com')))
#
# print('Update blacklist for given campaign: \n {}'.format(
#     getresponse.post_campaign_blacklist(campaign_id, ['spam@sgmail.com', 'spamparam@gmail.com'])))
#
print('Get campaign list size from main campaign: \n {}'.format(
    getresponse.get_campaigns_statistics_list_size(['groupBy=month', 'createdOn][from]=2017-01-01'], campaign_id,
                                                   fields='totalSubscribers,addedSubscribers')))
#
# print('Get campaign locations from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_locations(['groupBy=total'], campaign_id)))
#
# print('Get campaign origins from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_origins(['groupBy=total'], campaign_id)))
#
# print('Get campaign removals from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_removals(['groupBy=total'], campaign_id)))
#
# print('Get campaign subscriptions from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_subscriptions(['groupBy=total'], campaign_id)))
#
#
# print('Get campaign balance from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_balance(['groupBy=total'], campaign_id)))
#
# print('Get campaign summary from main campaign: \n {}'.format(
#     getresponse.get_campaigns_statistics_summary('3,d')))