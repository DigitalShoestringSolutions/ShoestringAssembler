# SMDownloader.py

# Given a recipe, downloads Service Modules according to mirrordirector.ServiceModuleURLs

## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#import git # pip install GitPython

# Local imports
from mirrordirector import ServiceModuleURLs as SMURLs

## --------------------------------------------------------------------------------

recipefilename = "recipe.txt"

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <soluton_files>/ServiceModules/Assembly/ShoestringAssembler/SMDownloader.py
solution_files = Path(__file__).parents[3]

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
        SMName = line[0]
        branchname = line[1]

        # Attempt to action recipe line
        if SMName in SMURLs:
            url = SMURLs[SMName]
            download_to = str(solution_files.joinpath(Path("ServiceModules/" + SMName)))
            print("Downloading", SMName, "branch", branchname, "from", url, "to", download_to)
            os.system("git clone " + url + " -b " + branchname + " " + download_to)


        else:
            print("Assembler Error: no Servie Module URL defined for line in recipe", line)