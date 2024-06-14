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

for SMDir in UserConfig: # will SMDir be a short string dir name or a full path? Need both  - either way will need to convert.
    for configitem in SMDir.rglob('*'):
        dest_path = ServiceModules.joinpath(SMDir, "config", configitem.relative_to(UserConfig.joinpath(SMDir)))
        if configitem.is_dir():
            os.mkdir(dest_path)
        
        else:
            # create link from (configitemabspath) to (dest_path)
            os.system('ln "' + str(configitem) + '" "' + str(dest_path) + '"')
            


## --------------------------------------------------------------------------------
# Below copied from Grafana's old init_SM.py. TBD: make it iterate over all Service Modules. 

# config_dashboards_dir_abs = Path(__file__).parents[3].joinpath("UserConfig/dashboards")
# SM_dashboards_dir_abs = Path(__file__).parents[2].joinpath("Grafana/dashboard_ui/config/dashboards")

# for dashboard in config_dashboards_dir_abs.rglob('*'):
#     dest_path = SM_dashboards_dir_abs.joinpath(dashboard.relative_to(config_dashboards_dir_abs))
    
#     if dashboard.is_dir():
#         # Directory names with spaces are natively supported
#         os.mkdir(dest_path)
    
#     else:
#         # Note how both "paths are in quotes" to support names with whitespace
#         os.system('ln "' + str(dashboard) + '" "' + str(dest_path) + '"')

# ## --------------------------------------------------------------------------------
# # the simple version from timeseries:

# from pathlib import Path
# import os

# # Note that due to the dubious exec(f.read()) that actually runs this script, 
# #   Path(__file__) returns the Assembly/ShoestringAssembler location!

# link_from_abs = Path(__file__).parents[3].joinpath("UserConfig/telegraf.conf")
# link_to_abs = Path(__file__).parents[2].joinpath("Timeseries/timeseries_sds/config/telegraf.conf")

# os.system("ln " + str(link_from_abs) + " " + str(link_to_abs))