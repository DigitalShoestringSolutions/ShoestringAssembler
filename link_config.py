# link_config.py

# Creates Unix hard links (non-symbolic) between parts of the Config directory and parts of the Modules directory.
# If the Config contains the subdir MyModule and MyModule is successfully downloaded via recipe.txt, 
# then the contents of Config/MyModule/ will be hard linked into Modules/MyModule/config/.


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

# Assume this file is <solution_files>/Modules/Assembly/ShoestringAssembler/link_config.py
SolutionFiles = Path(__file__).parents[3]
Modules = SolutionFiles.joinpath("Modules")
Config = SolutionFiles.joinpath("Config")

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

print("## -----------------------------------------------------------------------")
print("Linking Config to Modules...")
print("    Config path:    ", Config)
print("    Modules path:", Modules)

# For each subdirectory of Config:
for config_module_dir in Config.glob('*'):
# config_module_dir is a full absolute path. Extract module name only from config_module_dir.relative_to(Config) below.

    for configitem in config_module_dir.rglob('*'):
    # configitem is a full absolute path. 

        # Example configitem: /home/pi/ShoestringSolution/Config/Grafana/dashboards/mydashboard.json
        # The below converts this into:
        # Example dest_path: /home/pi/ShoestringSolution/Modules/Grafana/config/dashboards/mydashboard.json
        dest_path = Modules.joinpath(config_module_dir.relative_to(Config), "config", configitem.relative_to(config_module_dir))

        # For brevity when printing, produce shortend names for configitem and dest_path:
        configitem_short = configitem.relative_to(SolutionFiles)
        dest_path_short = dest_path.relative_to(SolutionFiles)

        # Directories cannot be linked. Detect and handle them separately.
        # As the above search is recursive (rglob), the directory tree will be created in Modules as necessary.
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

            # Hard link from the file in Config to the config folder in the Module
            print("    Linking", configitem_short)
            print("        to ", dest_path_short)
            # Note how below both "paths are in quotes" to support names with whitespace
            os.system('ln "' + str(configitem) + '" "' + str(dest_path) + '"')

print("## -----------------------------------------------------------------------")

## --------------------------------------------------------------------------------
