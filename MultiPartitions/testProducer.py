from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
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

# Adding new Topic
# admin = KafkaAdminClient(
#     client_id = "admin",
#     bootstrap_servers = hostname + ":" + str(port)
# )

# topic_name_partitioned = topic_name + "_partitioned"
# topic = NewTopic(name=topic_name_partitioned, num_partitions=2, replication_factor=1)
# admin.create_topics([topic], timeout_ms=10000)

# Send data to partition 0 under the topic "test_partitioned"
producer.send(
    topic_name+"_partitioned",
    key={"id":0},
    value={"name":"Shawn", "temp":36.7},
    partition=0
)

# Send data to partition 1 under the topic "test_partitioned"
producer.send(
    topic_name+"_partitioned",
    key={"id":1},
    value={"name":"test", "temp":37.7},
    partition=1
)

producer.flush()