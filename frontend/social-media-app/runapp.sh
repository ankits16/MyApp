#!/bin/bash

# Find the process ID using port 3000
PID=$(lsof -ti :3000)

# Check if a process is found
if [[ -n $PID ]]; then
  # Kill the process
  echo "Killing the React app running on port 3000..."
  kill -9 $PID
else
  echo "No React app found running on port 3000."
fi
npm start