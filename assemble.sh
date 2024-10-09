#!/bin/bash

# Top level of Shoestring Assembler

# Save some file paths as constants
# Get the parent dir of this script
SCRIPT_DIR="$(dirname -- "$(realpath -- "$0")")"

# Get the parent dir of SCRIPT_DIR
SCRIPT_DIR_DIR="$(dirname -- "$(realpath -- $SCRIPT_DIR)")"

# Define once the log file name, as a full path
LOG_FILE=$SCRIPT_DIR_DIR/assemblerlog.txt




# Wrap all commands to redirect IO. Closed in the last line. 
{

# Standard length divider
echo "## -----------------------------------------------------------------------"

# Print the version of the Solution and Assembler being used. echo -n for no newline at end.
echo -n "Solution hash: "
git rev-parse --short HEAD
echo -n "Assembler hash: "
git -C $SCRIPT_DIR rev-parse --short HEAD

echo "## -----------------------------------------------------------------------"




# Assembler functional steps
# Download Service Modules into <solutionfiles>/ServiceModules
python3 $SCRIPT_DIR/SMDownloader.py
echo ""

# Run init files in each service module, if present
python3 $SCRIPT_DIR/init_SMs.py
echo ""

# Link config files between UserConfig and each Service Module's config dirctory
python3 $SCRIPT_DIR/link_config.py
echo ""

# Generate a docker-compose file at <solutionfiles>
python3 $SCRIPT_DIR/include_docker_composes.py




# Wrap all of the above, send stdout & stderr to local log file
} 2>&1 | tee -a $LOG_FILE
