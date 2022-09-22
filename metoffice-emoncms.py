import http.client
import ast
import requests
import postcodes_io_api
from datetime import datetime

post_code = "SW11 7US"
emoncms_apikey = 'xxxxxxxxxxxxxxx'

conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

headers = {
    'X-IBM-Client-Id': "xxxxxxxxxxxxxx",
    'X-IBM-Client-Secret': "xxxxxxxxxxxxxxxxxxx",
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