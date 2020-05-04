import requests

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
print(send_request.json())
