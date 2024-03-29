



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

username: YOUR INFLUXDB USERNAME

password: YOUR INFLUXDB PASSWORD

organization: YOUR ORGANIZATION NAME

bucket_name: YOUR BUCKET NAME NAME

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
  token = "YOUR INFLUXDB TOKEN"
  organization = "YOUR ORGANIZATION NAME"
  bucket = "YOUR BUCKET NAME"

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

, once we have all the infrastructure ready, we need to create the data from the sensors (simulate the data from the sensors) on another terminal screen:

```
$ python multiple_publisher.py
```

, and we can check that it is passed to the broker, reading the messages of the broker on another terminal screen with:

```
$ python consumer.py
```

Finally, after all that, we go to **grafana main page** in [http://localhost:3000/](http://localhost:3000/)

admin

admin

In **grafana** first task is adding **influxdb** as datasourse, so we need to go to **Connections > Data Sources > Add data source > influxdb**, and configure influxdb settings inside grafana:

Name: influxdb

Query language: Flux

HTTP URL: http://influxdb:8086

Basic Auth Details User: admin

Basic Auth Details Password: admin

InfluxDB Details Organization: YOUR ORGANIZATION NAME

InfluxDB Details Token: YOUR INFLUXDB TOKEN

InfluxDB Details Default Bucket: YOUR BUCKET NAME

<img src="images/screenshot_grafana_configure_datasource_influxdb.png" alt="InfluxDB configuration in Grafana" width="80%">

, and click **Save & Test** button.

If we have confirmation like this:

<img src="images/screenshot_confirmation_grafana.png" alt="Confirmation of InfluxDB connection with Grafana" width="100%">

, interaction between **influxdb** and **grafana** is configured and we can visualize the **streamed sensor data in grafana**.

For this we need to configure a **grafana Dashboard** or import one already defined.

For this example, we are going to use a previous configured Dashboard, so in the grafana left menu, we choose Dashboards and in the upper menu click on:

**+ > Import Dashboard**

, and upload the **dashboard_workcenter.json** file from our repository.

The final output of the Dashboard is:

<img src="images/grafana_dashboard.png" alt="Workcenter Grafana Dashboard" width="100%">

