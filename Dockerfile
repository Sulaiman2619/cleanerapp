FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /cleanerapp

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install Node.js dependencies if you have any
# RUN npm install

# Collect static files (if applicable)
# RUN python manage.py collectstatic --no-input

# Command to run the Django server and Tailwind CSS
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
