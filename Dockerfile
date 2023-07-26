# Use the official Python image as a base image
FROM python:3.8

# Set environment variables for Python buffering and enable Docker in development mode
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 1

# Set the working directory inside the container
WORKDIR /app

# Install project dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Copy the wait-for-it script to the container
COPY wait-for-it.sh /app/

# Run Django development server using the wait-for-it script
CMD ["./wait-for-it.sh", "db", "--", "./manage.py", "runserver", "0.0.0.0:8000"]
