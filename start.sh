
#!/bin/bash

zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties &
kafka-server-start /opt/homebrew/etc/kafka/server.properties &

sleep 10

kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test &
kafka-console-producer --broker-list localhost:9092 --topic test &
kafka-console-consumer --bootstrap-server localhost:9092 --topic test &

python3 app.py
