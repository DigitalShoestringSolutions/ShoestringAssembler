# init_SMs.py

# Permits Service Modules to request code to be run immediately after download, before compiling
# eg SetupLogging would like setup_logging.sh to be run straight away, 
#       such that during docker compose logs are redirected
# Currently supported files types are .sh and .py




## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#none

# Local imports
#none

## --------------------------------------------------------------------------------




## -- Settings --------------------------------------------------------------------

# Assuming this script is in ServiceModules/Assembly/ShoestringAssembler/
ServiceModulesDir = Path(__file__).parents[2]

## --------------------------------------------------------------------------------




## -- Iterate over service module folders -----------------------------------------
print("## -----------------------------------------------------------------------")
print("Running Service Module init scripts...")

for file in ServiceModulesDir.rglob('*'):
    #if file.name in ['init_SM.sh']:
    if file.stem in ['init_SM']:
        print("    Running init script", file.relative_to(ServiceModulesDir))
        if file.suffix == '.sh':
            os.system(str(file))
        elif file.suffix == '.py':
            with file.open(mode='r') as f:
                # filthy but it works
                exec(f.read())

print("## -----------------------------------------------------------------------")
## --------------------------------------------------------------------------------