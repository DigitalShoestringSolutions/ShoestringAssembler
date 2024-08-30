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
# Typically the stack will be <solution_files>/ServiceModules/Assembly/ShoestringAssembler/SMDownloader.py
solution_files = Path(__file__).parents[3]

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------
print("## -----------------------------------------------------------------------")
print("Downloading Service Modules...")

# Keep a list of the instance names of service modules that have been downloaded, to manage duplicates.
_downloaded_service_modules = []

# Suppress messages about being in 'detached HEAD' state when switching to a tag
os.system("git config --global advice.detachedHead false")

# Look for a recipe
with solution_files.joinpath(Path(recipefilename)).open(mode='r') as recipefile:

    for line in recipefile:

        # Force reset - lest any be set in a previous loop, fail to update and are reused.
        sm_base_name = None
        url = None
        branch_specifier = None      # Also supports not supplying a branch name and using SM repo default.
        _branch_specifier_search = None
        _available_branches = None
        _available_long_heads = None
        _available_tags = None
        _available_long_tags = None
        _download_branch = None
        _download_command = ""

        # Skip line if blank or commented out python style
        if line[0] in('\n',"#"):
            continue

        # split line into list of components
        line = line.split("=")
        line[-1] = line[-1].split("\n")[0]     # Remove trailing newline from last item.

        # Associate names
        sm_base_name = line[0]
        if len(line) > 1:           # If an = was in the recipe line, try to use what follows as a branch/tag name.
            branch_specifier = line[1]

        # Attempt to action recipe line
        if sm_base_name in ServiceModuleURLs:
            url = ServiceModuleURLs[sm_base_name]

            # Duplicate management
            sm_instance_name = sm_base_name # First try to use the base name as the instance name
            i = 1
            while sm_instance_name in _downloaded_service_modules:
                i += 1                                              # If instance name taken, increment count
                sm_instance_name = sm_base_name + str(i)            # and try using name with count eg Sensing2
            _downloaded_service_modules.append(sm_instance_name)    # record final instance name used

            # Version management
            # To remove the possibility of ending up with the wrong version downloaded,
            # ensure the target branch or tag is available before attempting clone.

            if branch_specifier is not None:

                # Get list of remote branches
                _available_long_heads = os.popen("git ls-remote --heads " + url).read().splitlines()
                _available_branches = []
                for head in _available_long_heads:
                    _available_branches.append(head.split("heads/")[-1])    # Everything after heads/ , ie the name of the branch

                # First attempt to clone an exact match of a branch name:
                if branch_specifier in _available_branches:
                    _download_branch = branch_specifier

                else:
                    # Get list of remote tags, sorted semver highest to lowest.
                    _available_long_tags = os.popen("git ls-remote --tags --sort=-version:refname " + url).read().splitlines()
                    _available_tags = []
                    for tag in _available_long_tags:
                        _available_tags.append(tag.split("tags/")[-1])      # Everything after tags/ , ie the name of the tag

                    # If an exact tag match is available, take it
                    if branch_specifier in _available_tags:
                        _download_branch = branch_specifier

                    # If no exact branch or tag match, search for the tag that is the best semver match.
                    else:
                        # Given that there was not an exact match, an unknown suffix will be found.
                        # It should not begin with a digit (e.g. if I asked for v1.6 I don't want v1.62)
                        # It should not begin with a - (as I desire to exclude prereleases from search, partially because git ls-remote can't get them in the semver order).
                        # Hence, the only acceptable next character is a full stop. Add this to the search term to exclude the above alternatives.
                        _branch_specifier_search = branch_specifier + '.'

                        for tag in _available_tags:
                            # _available_tags is already sorted by semver M.m.p highest precedence first when created.
                            if tag.startswith(_branch_specifier_search):

                                # Ignore prerelease tags
                                # A request for v1.10 could so far pick up v1.10.2-rc3
                                # Furthermore, it could select v1.10.2-rc3 over v1.10.2 due to ls-remote's imperfect ordering.
                                # However, it would be excessive to ignore any tag with a dash in it. lite-v1.2.3 is a desired pickup from specifier lite-v1.2
                                _suffix = tag[len(_branch_specifier_search):]
                                if '-' in _suffix:  # if there is a dash in the unspecified part of the tag
                                    continue        # skip and continue search

                                _download_branch = tag
                                break

                        # if _download_branch is still None, a suitable branch/tag could not be found.
                        if _download_branch is None: # not acceptable here as within `if branch_specifier is not None:` far above.
                            print("    ERROR: No suitable branch of", sm_base_name, "found for specifier", branch_specifier, "Cancelling download of", sm_instance_name)
                            continue    # give up on this line of the recipe and move on to next

            # Download with git clone
            download_to = str(solution_files.joinpath("ServiceModules/" + sm_instance_name))
            print()
            print("    Downloading", sm_instance_name, "branch", _download_branch, "from specifier", branch_specifier)
            print("        from", url)
            print("        to", download_to)

            _download_command = "git clone --quiet " + url
            if _download_branch is not None:                    # If branch specified in recipe
                _download_command += " -b " + _download_branch  # Insert into the clone command. Else omit.
            _download_command += " " + download_to

            os.system(_download_command)                        # Run the string concatenated above


        else:
            print()
            print("ERROR: no Servie Module URL defined for line in recipe", line)
            print()

print("## -----------------------------------------------------------------------")
## --------------------------------------------------------------------------------
