#!/bin/bash

# Top level of Shoestring Assembler

# Save some file paths as constants
# Get the parent dir of this script
SCRIPT_DIR="$(dirname -- "$(realpath -- "$0")")"

# Get the parent dir of SCRIPT_DIR
SCRIPT_DIR_DIR="$(dirname -- "$(realpath -- $SCRIPT_DIR)")"

# Define once the log file name, as a full path
LOG_FILE=$SCRIPT_DIR_DIR/assemblerlog.txt



# Print the version of the Solution and Assembler being used
echo "Solution hash:" 2>&1 | tee -a $LOG_FILE
git rev-parse --short HEAD 2>&1 | tee -a $LOG_FILE

echo "Assembler hash:" 2>&1 | tee -a $LOG_FILE
git -C $SCRIPT_DIR rev-parse --short HEAD 2>&1 | tee -a $LOG_FILE



# Run the Assembler!
# Download Service Modules into <solutionfiles>/ServiceModules
python3 $SCRIPT_DIR/SMDownloader.py 2>&1 | tee -a $LOG_FILE

# Run init files in each service module, if present
python3 $SCRIPT_DIR/init_SMs.py 2>&1 | tee -a $LOG_FILE

# Link config files between UserConfig and each Service Module's config dirctory
python3 $SCRIPT_DIR/link_config.py 2>&1 | tee -a $LOG_FILE

# Generate a docker-compose file at <solutionfiles>
python3 $SCRIPT_DIR/include_docker_composes.py 2>&1 | tee -a $LOG_FILE
