



### Instalation

Clone the repository

```
git clone https://github.com/PachiCartelle/iot_bigdata_infrastructure.git
```

The code downloaded contains the folder **infra-iot**, so we cd inside it

```
$ cd infra-iot
```

Then, there we have the **grafana-data** and **influxdb-data** folders.

For Grafana working fine, we need to run this code, to have permissions:

```
$ sudo chown -R 472:472 grafana-data

$ sudo chmod -R 775 grafana-data
```

Then, we need to run the mosquitto, telegraf, influxdb and grafana Docker containers, using our **docker-compose.yml** file:

```
$ sudo docker-compose up -d
```

After that, we need to get the **influxdb token**, so we enter in our browser [http://localhost:8086/](http://localhost:8086/)

,and enter our data:

username: pachi_iot

password: pachi_bigdata

organization: pachi

bucket_name: iot_data

, after that, **influxdb** give us our **token**, that we enter in **telegraf.conf** file:

```
[agent]
  interval = "10s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"
  precision = ""
  debug = false
  quiet = false
  logfile = ""
  hostname = ""
  omit_hostname = false

[[outputs.influxdb_v2]] 
  urls = ["http://influxdb:8086"]
  token = "INFLUXDB TOKEN HERE"
  organization = "pachi"
  bucket = "iot_data"

[[outputs.file]]
  files = ["stdout", "/tmp/metrics.out"]

[[inputs.mqtt_consumer]]
  servers = ["tcp://mosquitto:1883"]
  topics = [
    "office/#"
  ]
  data_format = "json"

```

, and then we restart **telegraf**:

```
$ sudo docker-compose restart telegraf
```

, once we have all the infrastructure ready, we need to create the data from the sensors (simulate the data from the sensors):

```
$ python multiple_publisher.py
```

, and we can check that it is passed to the broker, reading the messages of the broker with:

```
$ python consumer.py
```

Finally, after all that, we go to **grafana main page** in [http://localhost:3000/](http://localhost:3000/)

admin

admin

In **grafana** first task is adding **influxdb** as datasourse, so we need to go to Connections > Data Sources > Add data source > influxdb

