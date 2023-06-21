# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the subfolder
COPY ElectricApp/requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire directory contents to the container
COPY . .

# Exclude .pyc cache files and .DS_Store files
RUN find . -type f -name "*.pyc" -delete && \
    find . -name ".DS_Store" -delete

# Set the Flask environment variables
ENV FLASK_APP=ElectricApp/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the services directory as the working directory for CMD
WORKDIR /app/ElectricApp

# Copy the entrypoint.sh script to the container
CMD python -m services.hg_accsvc & \
    python -m services.hg_mlsvc & \
    python -m services.amk_accsvc & \
    python -m services.amk_mlsvc & \
    python -m services.jurong_accsvc & \
    python -m services.jurong_mlsvc & \
    python -m flask run --port 5000 --host 0.0.0.0
