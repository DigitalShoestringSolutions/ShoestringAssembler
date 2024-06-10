# SMDownloader.py

# Given a recipe, downloads Service Modules according to mirrordirector.ServiceModuleURLs

## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#none

# Local imports
from mirrordirector import ServiceModuleURLs as SMURLs

## --------------------------------------------------------------------------------



## -- Settings --------------------------------------------------------------------

recipefilename = "recipe.txt"

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <soluton_files>/ServiceModules/Assembly/ShoestringAssembler/SMDownloader.py
solution_files = Path(__file__).parents[3]

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

# keep a list of the instance names of service modules that have been downloaded, to manage duplicates
_downloaded_service_modules = []

# Look for a recipe
with solution_files.joinpath(Path(recipefilename)).open(mode='r') as recipefile:

    for line in recipefile:

        # Force reset
        url = None # lest url be set in a previous loop, fails to update and is reused

        # Skip line if blank or commented out python style
        if line[0] in('\n',"#"):
            continue

        # split line into list of components
        line = line.split("=")
        line[-1] = line[-1].split("\n")[0]     # remove trailing newline from last item

        # Associate names
        sm_base_name = line[0]
        branch_name = line[1]

        # Attempt to action recipe line
        if sm_base_name in SMURLs:
            url = SMURLs[sm_base_name]

            # Duplicate management
            sm_instance_name = sm_base_name # First try to use the BaseName
            i = 1
            while sm_instance_name in _downloaded_service_modules:
                i += 1
                sm_instance_name = sm_base_name + str(i)
            _downloaded_service_modules.append(sm_instance_name)

            download_to = str(solution_files.joinpath("ServiceModules/" + sm_instance_name))

            print()
            print("Downloading", sm_instance_name, "branch", branch_name, "from", url, "to", download_to)
            os.system("git clone " + url + " -b " + branch_name + " " + download_to)


        else:
            print()
            print("Assembler Error: no Servie Module URL defined for line in recipe", line)

## --------------------------------------------------------------------------------
