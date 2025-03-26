#!/bin/bash
set -e

EXPERIMENT_COMMAND="$1"           # The command which runs the experiment.
PROCESS_NAME="${2:-EXPERIMENT}"  # The name of the experiment process.
LOG_OUTPUT_PATH="$3"             # The output file path for the log.

# Check if the experiment command is provided
if [ -z "$EXPERIMENT_COMMAND" ]; then
  echo "Error: Missing experiment command (First parameter)."
  exit 1
fi

# Shift the positional parameters to process additional arguments
shift 3

# Run the experiment
if [ -z "$LOG_OUTPUT_PATH" ]; then
  echo "Running, under the name '$PROCESS_NAME', the experiment '$EXPERIMENT_COMMAND' with arguments '$@'"
  exec -a "$PROCESS_NAME" nohup "$EXPERIMENT_COMMAND" "$@" > /dev/null 2>&1 &
else
  echo "Running, under the name '$PROCESS_NAME' and logging to '$LOG_OUTPUT_PATH', the experiment '$EXPERIMENT_COMMAND' with arguments '$@'"
  exec -a "$PROCESS_NAME" nohup "$EXPERIMENT_COMMAND" "$@" > "$LOG_OUTPUT_PATH" 2>&1 &
fi
