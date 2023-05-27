from kafka import KafkaProducer
import json

# Setup
hostname = "localhost"
port = "9092"
topic_name = "test"

producer = KafkaProducer(
    bootstrap_servers = hostname + ":" + str(port),
    value_serializer = lambda v: json.dumps(v).encode('ascii'),
    key_serializer = lambda v: json.dumps(v).encode('ascii')
)

# Sending data to topic "test"
producer.send(
    topic_name,
    key={"id":1},
    value={"name":"Shawn", "temp":36.7}
)

producer.flush()
