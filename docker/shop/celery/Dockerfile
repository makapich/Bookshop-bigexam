# Use an appropriate base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements/shop/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY backend/shop/ .

# Expose the port that your application will listen on
EXPOSE 8000

# Apply database migrations and start the application
CMD sh -c "sleep 10 && celery -A core worker --beat --loglevel=info"