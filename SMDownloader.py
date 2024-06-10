# SMDownloader.py

# Given a recipe, downloads Service Modules according to mirrordirector.ServiceModuleURLs

## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#none

# Local imports
from mirrordirector import ServiceModuleURLs

## --------------------------------------------------------------------------------



## -- Settings --------------------------------------------------------------------

recipefilename = "recipe.txt"

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <soluton_files>/ServiceModules/Assembly/ShoestringAssembler/SMDownloader.py
solution_files = Path(__file__).parents[3]

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

# Keep a list of the instance names of service modules that have been downloaded, to manage duplicates.
_downloaded_service_modules = []

# Look for a recipe
with solution_files.joinpath(Path(recipefilename)).open(mode='r') as recipefile:

    for line in recipefile:

        # Force reset - lest any be set in a previous loop, fail to update and are reused.
        sm_base_name = None
        url = None
        branch_name = None      # Also supports not supplying a branch name and using SM repo default.
        _download_command = ""

        # Skip line if blank or commented out python style
        if line[0] in('\n',"#"):
            continue

        # split line into list of components
        line = line.split("=")
        line[-1] = line[-1].split("\n")[0]     # Remove trailing newline from last item.

        # Associate names
        sm_base_name = line[0]
        if len(line) > 1:           # If an = was in the recipe line, try to use what follows as a branch/tab name.
            branch_name = line[1]

        # Attempt to action recipe line
        if sm_base_name in ServiceModuleURLs:
            url = ServiceModuleURLs[sm_base_name]

            # Duplicate management
            sm_instance_name = sm_base_name # First try to use the BaseName as instance name
            i = 1
            while sm_instance_name in _downloaded_service_modules:
                i += 1                                              # If instance name taken, increment count
                sm_instance_name = sm_base_name + str(i)            # and try using name with count eg Sensing2
            _downloaded_service_modules.append(sm_instance_name)    # record final instance name used

            # Download with git clone
            download_to = str(solution_files.joinpath("ServiceModules/" + sm_instance_name))
            print()
            print("Downloading", sm_instance_name, "branch", branch_name, "from", url, "to", download_to)
            _download_command = "git clone " + url
            if branch_name is not None:
                _download_command += " -b " + branch_name
            _download_command += " " + download_to
            os.system(_download_command)


        else:
            print()
            print("Assembler Error: no Servie Module URL defined for line in recipe", line)
            print()

## --------------------------------------------------------------------------------
