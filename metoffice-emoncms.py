# Post local temperature data to Emoncms
# OpenEnergyMonitor.og

import metoffer
import pprint
import json
import requests
from datetime import datetime

# API keys
datapoint_apikey = 'xxxxxx'
emoncms_apikey = 'xxxxxx'
latitude = 'xx.xxx'
longitude = '-xxx.xx'

# Setup Metoffer
M = metoffer.MetOffer(datapoint_apikey)

# Get data from nearest observation station
latitude_f = float(latitude)
longitude_f = float(longitude)
x = M.nearest_loc_obs(latitude_f,longitude_f)

# y = metoffer.Weather(x)
# pprint.pprint(y.data)

# Create JSON string
a = json.dumps(x)
b = json.loads(a)

# Extract latest temperature
ambient_temp = b['SiteRep']['DV']['Location']['Period'][1]['Rep']['T']
print("Ambient Temp: " + ambient_temp)

# conbert to float
ambient_temp_float=float(ambient_temp)

# Post to Emoncms
if type(ambient_temp_float) == float:
    payload = {'csv':ambient_temp_float, 'apikey':emoncms_apikey}
    url_emoncms = 'https://emoncms.org/input/post?node=ambient_temp'
    r = requests.post(url_emoncms, params=(payload))
    print ('Emoncms: '+r.text)

print(datetime.now())

    
    
    