#!/bin/bash

# Create a log file with a timestamp
LOG_FILE="/var/log/interp/interp_$(date +'%Y-%m-%d_%H-%M-%S').log"
echo "entrypoint.sh - $(date +'%Y-%m-%d_%H-%M-%S')" | tee -a $LOG_FILE

# Run the app and tee the output
uvicorn src.main:app 2>&1 | tee -a $LOG_FILE