import requests
import os
from datetime import datetime
from twilio.rest import Client

# Read in sensitive info from local file
secret_dict = {}
with open('../../secret/secrets.txt') as f:
    for item in f:
        (key, val) = item.split(':')
        secret_dict[key] = val.strip('\n')

# POST request header URL
url = 'https://groceries.asda.com/api/v3/slot/view'

# POST request JSON payload
json_payload = {'requestorigin' : 'gi',
                    'data' : {
                        'customer_info' : {'account_id' : os.environ["ASDA_ACT_ID"]},
                        'order_info' : {'order_id': "20826667453",
                                        'restricted_item_types': [],
                                        'volume': 0,
                                        'weight': 0,
                                        'sub_total_amount': 0},
                        'service_address' : {'postcode': os.environ["HOME_POSTCODE"],
                                            'latitude': os.environ["HOME_LAT"],
                                            'longitude': os.environ["HOME_LON"]},
                        'service_info' : {'fulfillment_type': "DELIVERY",
                                        'enable_express': 'false'}
                    }}
send_request = requests.post(url, json = json_payload)

slot_availability = {}
for slot_day in send_request.json()['data']['slot_days']:
    slot_date = slot_day['slot_date']
    for slot in slot_day['slots']:
        slot_time = slot['slot_info']['start_time']
        # convert time into datetime object
        slot_time = datetime.strptime(slot_time, '%Y-%m-%dT%H:%M:%SZ')
        slot_status = slot['slot_info']['status']

        # write the slot time and the corresponding status to the empty dictionary
        slot_availability[slot_time.strftime('%H:%M:%S %d-%m-%Y')] = slot_status


available_slots = [k for k, v in slot_availability.items() if v != 'UNAVAILABLE']

# if there are available slots, send a text with the slots to my mobile number
if len(available_slots) > 0:
    account_sid = os.environ["TWILIO_ACT_ID"]
    auth_token  = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ["MOBILE_NUM"],
        from_=os.environ["TWILIO_NUM"],
        body="Available delivery slots found: {}".format(available_slots))
    print(message.sid)
else:
    print("No delivery slots are currently available.")