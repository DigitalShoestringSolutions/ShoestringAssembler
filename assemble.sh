#!/bin/bash

# Top level of Shoestring Assembler

# Get location of this script
SCRIPT_DIR="$(dirname -- "$(realpath -- "$0")")"

# Get location of this script's parent folder
PARENT_DIR="$(dirname -- "$(realpath -- $SCRIPT_DIR)")"

# Download Service Modules into <solutionfiles>/ServiceModules
python3 $SCRIPT_DIR/SMDownloader.py 2>&1 | tee -a $PARENT_DIR/assemblerlog.txt
sleep .1

# Run init files in each service module, if present
python3 $SCRIPT_DIR/init_SMs.py 2>&1 | tee -a $PARENT_DIR/assemblerlog.txt
sleep .1

# Link config files between UserConfig and each Service Module's config dirctory
python3 $SCRIPT_DIR/link_config.py 2>&1 | tee -a $PARENT_DIR/assemblerlog.txt
sleep .1

# Generate a docker-compose file at <solutionfiles>
python3 $SCRIPT_DIR/include_docker_composes.py 2>&1 | tee -a $PARENT_DIR/assemblerlog.txt
sleep .1
