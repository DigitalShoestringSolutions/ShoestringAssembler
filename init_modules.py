# init_modules.py

# Permits Modules to request code to be run immediately after download, before compiling
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

# Assuming this script is in Modules/Assembly/ShoestringAssembler/
ModulesDir = Path(__file__).parents[2]

## --------------------------------------------------------------------------------




## -- Iterate over module folders -----------------------------------------

print("## -----------------------------------------------------------------------")
print("Running Module init scripts...")

# Search recursively through all files in all Modules.
#   Should this instead be limited to only the top level within each module?
for file in ModulesDir.rglob('*'):

    if file.stem in ['init_SM']: # ignore extension.
        # Just init etc was avoided as that could conflict with non-shoestring functionality.
        # Changing the target filename above would be a breaking change not only for the Assembler, but for all the Modules that have used this.
        # So far only used by Docker and SetupLogging - which are modules but not service modules - so renaming to init_shoestring_module would only be making it right.
        
        print("    Running init script", file.relative_to(ModulesDir))

        # Run according to extension
        if file.suffix == '.sh':
            os.system(str(file))

        elif file.suffix == '.py':
            with file.open(mode='r') as f:
                # filthy but it works
                exec(f.read())

print("## -----------------------------------------------------------------------")

## --------------------------------------------------------------------------------
