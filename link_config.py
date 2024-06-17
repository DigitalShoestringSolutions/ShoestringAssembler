# link_config.py

# Creates Unix hard links (non-symbolic) between parts of the UserConfig directory and parts of the ServiceModules directory.
# If the UserConfig contains the subdir MyServiceModule and MyServiceModule is sucessfully downloaded via recipe.txt, 
# then the contents of UserConfig/MyServiceModule/ will be hard linked into ServiceModules/MyServiceModule/config/.


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

# Assume this file is <solution_files>/ServiceModules/Assembly/ShoestringAssembler/link_config.py
ServiceModules = Path(__file__).parents[2]
UserConfig = Path(__file__).parents[3].joinpath("UserConfig")

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

print("Linking UserConfig to Service Modules...")
print("UserConfig path:", UserConfig)
print("ServiceModules path:", ServiceModules)

for SMDir in UserConfig.glob('*'): # SMDir is a full path. Get SM name from SMDir.relative_to(UserConfig) below.
    for configitem in SMDir.rglob('*'):
        dest_path = ServiceModules.joinpath(SMDir.relative_to(UserConfig), "config", configitem.relative_to(SMDir))
        
        if configitem.is_dir():
            os.mkdir(dest_path)
        
        else:
            print("linking", configitem, " to ", dest_path)
            # Note how below both "paths are in quotes" to support names with whitespace
            os.system('ln "' + str(configitem) + '" "' + str(dest_path) + '"')