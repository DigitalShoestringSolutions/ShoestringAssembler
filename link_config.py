# link_config.py

# Creates Unix hard links (non-symbolic) between parts of the UserConfig directory and parts of the ServiceModules directory.
# If the UserConfig contains the subdir MyServiceModule and MyServiceModule is successfully downloaded via recipe.txt, 
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
SolutionFiles = Path(__file__).parents[3]
ServiceModules = SolutionFiles.joinpath("ServiceModules")
UserConfig = SolutionFiles.joinpath("UserConfig")

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

print("## -----------------------------------------------------------------------")
print("Linking UserConfig to Service Modules...")
print("    UserConfig path:    ", UserConfig)
print("    ServiceModules path:", ServiceModules)

# For each subdirectory of UserConfig:
for SMDir in UserConfig.glob('*'):
# SMDir is a full absolute path. Extract SM name only from SMDir.relative_to(UserConfig) below.

    for configitem in SMDir.rglob('*'):
    # configitem is a full absolute path. 

        # Example configitem: /home/pi/ShoestringSolution/UserConfig/Grafana/dashboards/mydashboard.json
        # The below converts this into:
        # Example dest_path: /home/pi/ShoestringSolution/ServiceModules/Grafana/config/dashboards/mydashboard.json
        dest_path = ServiceModules.joinpath(SMDir.relative_to(UserConfig), "config", configitem.relative_to(SMDir))

        # For brevity when printing, produce shortend names for configitem and dest_path:
        configitem_short = configitem.relative_to(SolutionFiles)
        dest_path_short = dest_path.relative_to(SolutionFiles)

        # Directories cannot be linked. Detect and handle them separately.
        # As the above search is recursive (rglob), the directory tree will be created in ServiceModules as necessary.
        if configitem.is_dir():
            # ignore if already exists
            if not dest_path.exists():
                print("    Making directory", dest_path_short)
                os.mkdir(dest_path)

        # if not a directory, it is a file item that can be linked
        else:
            
            # If a file/dir/similar already exists in the destination, delete it to make way for replacement
            if dest_path.exists():
                print("    Deleting default config file at", dest_path_short)
                os.system('rm -r "' + str(dest_path) + '"')

            # Hard link from the file in UserConfig to the config folder in the Service Module
            print("    Linking", configitem_short)
            print("        to ", dest_path_short)
            # Note how below both "paths are in quotes" to support names with whitespace
            os.system('ln "' + str(configitem) + '" "' + str(dest_path) + '"')

print("## -----------------------------------------------------------------------")

## --------------------------------------------------------------------------------
