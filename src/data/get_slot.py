import requests
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
                        'customer_info' : {'account_id' : secret_dict.get('account_id')},
                        'order_info' : {'order_id': "20826667453",
                                        'restricted_item_types': [],
                                        'volume': 0,
                                        'weight': 0,
                                        'sub_total_amount': 0},
                        'service_address' : {'postcode': secret_dict.get('postcode'),
                                            'latitude': secret_dict.get('latitude'),
                                            'longitude': secret_dict.get('longitude')},
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
    account_sid = secret_dict.get('twilio_account_id')
    auth_token  = secret_dict.get('twilio_auth_token')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=secret_dict.get('my_number'),
        from_=secret_dict.get('twilio_number'),
        body="Available delivery slots found: {}".format(available_slots))
    print(message.sid)
else:
    print("No delivery slots are currently available.")