#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <process_name>"
  exit 1
fi

pkill -f "$1"

if [ $? -eq 0 ]; then
  echo "Process '$1' terminated successfully."
else
  echo "No process named '$1' found."
fi
