Post current temperature at given UK postcode from metoffice [datahub](https://metoffice.apiconnect.ibmcloud.com/) observations to https://emoncms.org

# Install

```
git clone https://github.com/glynhudson/metoffice-emoncms
```


## Install modules

```
pip3 install postcodes_io_api python-dotenv
```

## Create log file

```
sudo touch /var/log/ambient-temp.log
sudo chmod 777 /var/log/ambient-temp.log
```

## Create .env

`mv example.env .env`

Enter postcode, Emoncms.org API key, Dathub Client ID and Datahub secrete

# Test

`python3 metoffice-emoncms.py`

Example output 

```
Now: 2022-09-22 19:18:05.122926
Ambient temp: 14.38
Last updated: 2022-09-22T17:00Z
Emoncms: ok
```

## Create cron job to run every hour

The current temperature from datahub is only updated every 1hr, so not point making more regular calls to the API 

`crontab -e`

`0 * * * * /usr/bin/python3 /home/pi/metoffice-emoncms/metoffice-emoncms.py >> /var/log/ambient-temp.log`

