# === Backend dockerfile ====

# Uses python version 3.12-slim as our base image
FROM python:3.12-slim

# Goes to the app directory (this container will have app folder)
WORKDIR /app

# Copy requirements.txt and puts it in the cache of the container
COPY requirements.txt ./

# Install app dependencies if not installed and not in cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy code into the container
COPY . . 

# Expose the port (Flask's default port)
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]