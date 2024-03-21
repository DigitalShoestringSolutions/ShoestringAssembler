# init_SMs.py

# Permits Service Modules to request code to be run immediately after download, before compiling
# eg SetupLogging would like setup_logging.sh to be run straight away, 
#       such that during docker compose logs are redirected
# Currently supported files types are .sh
# File types to add: .py

## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#none

# Local imports
#none

## --------------------------------------------------------------------------------

## -- Firm-coded settings ---------------------------------------------------------

ServiceModulesDir = Path(__file__).parents[2] # Assuming this script is in ServiceModules/Assembly/ShoestringAssembler/

## --------------------------------------------------------------------------------

print()
print("Running Service Module init scripts...")

## -- iterate over service module folders -----------------------------------------

for file in ServiceModulesDir.rglob('*'):
    if file.name in ['init_SM.sh']:
        print("    Running init script", file.relative_to(ServiceModulesDir))
        os.system(str(file))    # full abs path

## --------------------------------------------------------------------------------
        
print()