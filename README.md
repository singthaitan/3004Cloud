# CSC3004 Cloud and Distributed Computing

## MongoDB connection
- Create your own config.py (in the same folder as app.py) and have this inside:
```MONGO_URI = "mongodb+srv://<username>:<password>@app-cluster.zxcw8od.mongodb.net/"```
Change <username> and <password> to your own mongodb's

## To run project
- Create virtualenv folder to install Python dependencies (*Note: python can be python3 or py or python depending on your Python installation): ```python -m venv venv```
- Run virtualenv (on Windows): ```venv\Scripts\activate```
- Change directory: ```cd ElectricityWebApp```
- Install Python dependencies: ```pip install -r requirements.txt```
- Run Services through ```python -m services.hg_accsvc```
- Run application: ```python -m flask run```
- Open browser at: ```http://127.0.0.1:5000```
- Login with test credentials: ```user: test@gmail.com | password: Pass```
