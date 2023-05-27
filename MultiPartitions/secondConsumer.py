from kafka import KafkaConsumer, TopicPartition
import json

# Setup
hostname = "localhost"
port = "9092"
topic_name = "test"

consumer = KafkaConsumer(
    client_id = "client2",
    bootstrap_servers = hostname + ":" + str(port),
    value_deserializer = lambda v: json.loads(v.decode('ascii')),
    key_deserializer = lambda v: json.loads(v.decode('ascii')),
    max_poll_records = 10
)

# consumer.topics()

# consumer.subscribe(topics=[topic_name+"_partitioned"])
# consumer.subscription()

# First consumer reads only from partition 1
consumer.assign([TopicPartition(topic_name+"_partitioned", 1)])

# Printing received messages
for message in consumer:
    print(str(message.partition) + ":" + str(message.offset) + ":" + " k=" + str(message.key)
          + " v=" + str(message.value))
    
