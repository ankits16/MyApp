# Dockerfile

# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the Django project code to the container
COPY . /app/

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt



# Expose the port that Django runs on (change this to your Django app port)
EXPOSE 8000

# Command to run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]