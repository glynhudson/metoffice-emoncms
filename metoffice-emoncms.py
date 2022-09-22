import http.client
import ast
import requests
import postcodes_io_api
from datetime import datetime

post_code = "LL55 3NR"
emoncms_apikey = 'e85005cdc70bfb218cb56f6ce6ed3630'

conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

headers = {
    'X-IBM-Client-Id': "570c8c5965510686d5e5a033434113f2",
    'X-IBM-Client-Secret': "70a7f96e4af67c6c5540154956d53b2b",
    'accept': "application/json"
    }

# Get longitude and latitude from postcode
postcodes_conn = postcodes_io_api.Api()
postcode = postcodes_conn.get_postcode(post_code)
latitude = str(postcode['result']['latitude'])
longitude = str(postcode['result']['longitude'])

url = "/v0/forecasts/point/hourly?excludeParameterMetadata=true&includeLocationName=false&latitude="+latitude+"&longitude="+longitude

# print(url)

conn.request("GET", url, headers=headers)

res = conn.getresponse()
data = res.read()
# print(data)
a = ast.literal_eval(data.decode('utf-8'))

ambient_temp = a['features'][0]['properties']['timeSeries'][0]['screenTemperature']
last_updated = a['features'][0]['properties']['timeSeries'][0]['time']

print("Now: "+str(datetime.now()))
print("Ambient temp: "+str(ambient_temp))
print("Last updated: "+last_updated)

# Post to Emoncms
if type(ambient_temp) == float:
    payload = {'csv':ambient_temp, 'apikey':emoncms_apikey}
    url_emoncms = 'https://emoncms.org/input/post?node=ambient_temp'
    r = requests.post(url_emoncms, params=(payload))
    print ('Emoncms: '+r.text)