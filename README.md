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

## Create cron every hour

`contab -e`

`0 * * * * /usr/bin/python3 /home/pi/metoffice-emoncms/ambient-temp.py >> /var/log/ambient-temp.log`

