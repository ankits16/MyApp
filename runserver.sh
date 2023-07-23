#!/bin/bash

# Define the initial port number
port=8000

# Function to check if a port is available
function port_available() {
  netstat -tuln | grep ":$1 " >/dev/null
  return $?
}

# Loop until an available port is found
while port_available $port; do
  ((port++))
done

# Start the Django development server on the available port
python manage.py runserver $port

# to un this script
#chmod +x runserver.sh
# ./runserver.sh
# lsof -i :PORT_NUMBER : kill -9 pid - for maual kill