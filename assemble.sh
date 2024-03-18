#!/bin/bash

# Top level of Shoestring Assembler

# Get location of this script
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

python3 $SCRIPT_DIR/SMdownloader.py