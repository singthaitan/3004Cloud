from kafka import KafkaConsumer, TopicPartition
import json
import pymongo
from bson import ObjectId

# Setup for kafka
hostname = "localhost"
port = "9092"
topic_name = "electricity_consumption"
group_id = "hougangConsumer"

# Setup for mongodb

# Local mongodb
# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# mydb = myclient["household_db"]
# collection = mydb["electricity_usage"]

# Mongodb Atlas
myclient = pymongo.MongoClient("mongodb+srv://shawn:shawn@app-cluster.zxcw8od.mongodb.net/")
mydb = myclient["Hougang-Electric"]
collection = mydb["query_elec"]


# Create consumer
consumer = KafkaConsumer(
    client_id = "hougang_client",
    group_id = group_id,
    bootstrap_servers = hostname + ":" + str(port),
    value_deserializer = lambda v: json.loads(v.decode('ascii')),
    key_deserializer = lambda v: json.loads(v.decode('ascii')),
    max_poll_records = 10
)

# Subscribe to the topic "test"
# consumer.subscribe(topics=[topic_name])
# consumer.subscription()

# Reading from a specific offset value
# consumer.assign([TopicPartition(topic_name, 0)])
# consumer.seek(TopicPartition(topic_name, 0), 0)
consumer.assign([TopicPartition(topic_name, 1)])

# Printing received messages
for message in consumer:
    value = message.value
    hour = value['timestamp']
    electricity_consumption = value['electricity_consumption']
    print(str(message.partition) + ":" + str(message.offset) + ":" + " k=" + str(message.key['household_id']['$oid'])
          + " v=" + str(value))
    
    # Combine the household id into value variable
    mongoData = value.copy()
    mongoData.update({"household_id": ObjectId(message.key['household_id']['$oid'])})

    # Insert into mongodb collection
    insert_result = collection.insert_one(mongoData)
    if(insert_result.acknowledged):
        print("Successfully inserted into db" + "\n")
    else:
        print("Failed to store data in db" + "\n")

    
