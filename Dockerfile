# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /cleanerapp

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Upgrade pip and install other dependencies
RUN pip install --upgrade pip

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the Supervisor configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisor.conf

# Expose any necessary ports (if needed)
# EXPOSE 8000

# Command to start Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisor.conf"]
