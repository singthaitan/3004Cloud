# CSC3004 Cloud and Distributed Computing

## To run project
- Create virtualenv folder to install Python dependencies (*Note: python can be python3 or py or python depending on your Python installation): ```python -m venv venv```
- Run virtualenv (on Windows): ```venv\Scripts\activate```
- Change directory: ```cd ElectricApp```
- Install Python dependencies: ```pip install -r requirements.txt```
- Run Services through 
    - Ang Mo Kio: ```python -m services.amk_accsvc``` and ```python -m services.amk_mlsvc```
    - Hougang: ```python -m services.hg_accsvc``` and ```python -m services.hg_mlsvc```
    - Jurong:```python -m services.jurong_accsvc``` and ```python -m services.jurong_mlsvc```
- Run application: ```python -m flask run```
- Open browser at: ```http://127.0.0.1:5000```
- Register:
    - Password format
        - (Minimum 8 characters)
        - Alphanumeric (At least 1 uppercase, 1 lowercase and 1 digit)
    - Street address, unit number and postal code have to match record in region's household
    - To test register use the following addresses:
      |            | Street Address        | Unit number | Postal Code |
      |------------|-----------------------|-------------|-------------|
      | Hougang    | 245 Hougang Steet 3   |   #10-453   |    530245   |
      | Ang Mo Kio | 55 Ang Mo Kio Street 8|   #06-567   |    560055   |
      | jurong     | 2 Jurong West Street 4|   #12-556   |    640881   |
      
- Login with test credentials: 
    - Ang Mo Kio: ```user: amk_user@gmail.com | password: PassAMK1```
    - Hougang: ```user: hougang_user@gmail.com | password: PassHougang1```
    - Jurong: ```user: jurong_user@gmail.com | password: PassJurong1```

## Installation via Docker
- Ensure DOCKER service is running
- Open terminal
- Run the following to build the docker image
```
docker build -t frontend .
```
- Run the following to start the docker for front end
``` 
docker run -d -p 5000:5000 --name frontend_docker frontend
```
- Run the following to ensure that service ```frontend_docker``` is running
```
docker ps
``` 
- Run app by visiting 
```
http://localhost:5000
```

## To run message queue
### Method 1 (Running on Docker)
1. Open a command terminal and navigate to message_queue folder directory
2. Run the following command to start broker on docker: 
```
docker compose -f kafka-docker.yml up
```
3. Ensure that Zookeeper server is running and at least 1 broker is running on Docker
4. Start all 3 consumers by running the following commands
```
python .\angMoKioConsumer.py
```
```
python .\hougangConsumer.py
```
```
python .\jurongConsumer.py
```
5. Lastly, run the producer code
```
python .\producer.py
```
6. You should see data on the consumers and MongoDB


#### <b>Optional commands that may be useful</b>
1. To view data that are being sent from the producer in a command terminal, use the following command
```
docker exec broker1 kafka-console-consumer --bootstrap-server localhost:29092 --topic electricity_consumption --partition 0
```
2. To view details of a topic in a command terminal, use the following command
```
docker exec broker1 kafka-topics --describe --topic electricity_consumption --bootstrap-server localhost:29092
```

### Method 2 (Running without docker on Windows)
#### The following example is running for a single broker
1. Head to https://kafka.apache.org/downloads to download Apache Kafka onto your computer
2. Extract the files in your desired location
3. Open a command terminal and navigate to your Kafka folder Eg. D:\IDE\codes\csc3004_cloud\kafka
4. Type in the following command
```
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```
5. Open another new command terminal and navigate to your Kafka folder Eg. D:\IDE\codes\csc3004_cloud\kafka
6. Type in the following command
```
bin\windows\kafka-server-start.bat config\server.properties
```
7. Start all 3 consumers by running the following commands
```
python .\angMoKioConsumer.py
```
```
python .\hougangConsumer.py
```
```
python .\jurongConsumer.py
```
8. Lastly, run the producer code
```
python .\producer.py
```
6. You should see data on the consumers and MongoDB


#### <b>Optional commands that may be useful</b>
1. To view data that are being sent from the producer in a command terminal, navigate to windows folder and use the following command
```
consumer kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic <topicName> --from-beginning
```
2. To view details of a topic in a command terminal, use the following command
```
kafka-topics.bat --describe --topic <topicName> --bootstrap-server localhost:9092
```

* Default port number will be 9092. 
* --from-beginning tag allows consumers to retrieve data from the very beginning
