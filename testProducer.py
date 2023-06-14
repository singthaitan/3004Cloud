from kafka import KafkaProducer
import json
import random
import threading
import datetime

# Household 1
def household1_thread():
    # Send data every 10 sec (Simulate sending of data every 1 hour)
    threading.Timer(10.0, household1_thread).start()
    timestamp = datetime.datetime.now().replace(minute=0, microsecond=0)
    
    # Data to be sent to broker
    producer.send(
        topic_name,
        key={"household_id":1},
        value={"timestamp": str(timestamp), "electricity_consumption":format(random.uniform(2, 200), ".2f")}
    )

# Household 2
def household2_thread():
    # Send data every 10 sec (Simulate sending of data every 1 hour)
    threading.Timer(10.0, household2_thread).start()
    timestamp = datetime.datetime.now().replace(minute=0, microsecond=0)

    # Data to be sent to broker
    producer.send(
        topic_name,
        key={"household_id":2},
        value={"timestamp": str(timestamp), "electricity_consumption":format(random.uniform(2, 200), ".2f")}
    )

# Setup
hostname = "localhost"
port = "9092"
topic_name = "test"

# Create producer
producer = KafkaProducer(
    bootstrap_servers = hostname + ":" + str(port),
    value_serializer = lambda v: json.dumps(v).encode('ascii'),
    key_serializer = lambda v: json.dumps(v).encode('ascii')
)

# Start both household threads and send them concurrently
thread1 = threading.Thread(target=household1_thread)
thread1.start()

thread2 = threading.Thread(target=household2_thread)
thread2.start()

thread1.join()
thread2.join()

producer.flush()
