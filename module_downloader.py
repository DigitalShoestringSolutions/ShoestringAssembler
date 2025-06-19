# module_downloader.py

# Given a recipe, downloads Shoestring Modules according to mirrordirector.ModuleURLs

## -- Imports ---------------------------------------------------------------------

# standard imports
import os
from pathlib import Path

# installed imports
#none

# Local imports
from mirrordirector import ModuleURLs

## --------------------------------------------------------------------------------




## -- Settings --------------------------------------------------------------------

recipefilename = "recipe.txt"

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <solution_files>/Modules/Assembly/ShoestringAssembler/module_downloader.py
solution_files = Path(__file__).parents[3]

## --------------------------------------------------------------------------------




## -- Run -------------------------------------------------------------------------

print("## -----------------------------------------------------------------------")
print("Downloading Modules...")

# Keep a list of the instance names of modules that have been downloaded, to manage duplicates.
_downloaded_modules = []

# Suppress messages about being in 'detached HEAD' state when switching to a tag
os.system("git config --global advice.detachedHead false")

# Look for a recipe
with solution_files.joinpath(Path(recipefilename)).open(mode='r') as recipefile:

    for line in recipefile:

        # Force reset - lest any be set in a previous loop, fail to update and are reused.
        module_base_name = None
        url = None
        version_specifier = None      # Also supports not supplying a branch/tag name and using module repo default.
        _version_specifier_search = None
        _available_branches = None
        _available_long_heads = None
        _available_tags = None
        _available_long_tags = None
        _download_version = None
        _download_hash = None
        _download_command = ""

        # Skip line if blank or commented out python style
        if line[0] in('\n',"#"):
            continue

        # split line into list of components
        line = line.split("=")
        line[-1] = line[-1].split("\n")[0]      # Remove trailing newline from last item.

        # Associate names
        module_base_name = line[0]
        if len(line) > 1:               # If an = was in the recipe line, try to use what follows as a branch/tag name,
            version_specifier = line[1] # else the default value of None will persist

        # Attempt to action recipe line
        if module_base_name in ModuleURLs:
            url = ModuleURLs[module_base_name]

            # Duplicate management: find a unique "instance name" for this line of the recipe
            module_instance_name = module_base_name # First try to use the base name as the instance name
            i = 1
            while module_instance_name in _downloaded_modules:                                  # Check against list of instance names already taken
                i += 1                                                                          # If instance name taken, increment count
                module_instance_name = module_base_name + str(i)                                # and try using name with count eg Sensing2
            _downloaded_modules.append(module_instance_name)                                    # record final instance name used
            instance_dir = str(solution_files.joinpath("Modules/" + module_instance_name))      # Directory to clone into

            # Version management
            # To remove the possibility of ending up with the wrong version downloaded,
            # ensure the target branch or tag is available before attempting clone.

            if version_specifier is not None:

                # Get list of remote branches
                _available_long_heads = os.popen("git ls-remote --heads " + url).read().splitlines()
                _available_branches = []
                for head in _available_long_heads:
                    _available_branches.append(head.split("heads/")[-1])    # Everything after heads/ , ie the name of the branch

                # First attempt to clone an exact match of a branch name:
                if version_specifier in _available_branches:
                    _download_version = version_specifier

                else:
                    # Get list of remote tags, sorted semver highest to lowest.
                    _available_long_tags = os.popen("git ls-remote --tags --sort=-version:refname " + url).read().splitlines()
                    _available_tags = []
                    for tag in _available_long_tags:
                        _available_tags.append(tag.split("tags/")[-1])      # Everything after tags/ , ie the name of the tag

                    # If an exact tag match is available, take it
                    if version_specifier in _available_tags:
                        _download_version = version_specifier

                    # If no exact branch or tag match, search for the tag that is the best semver match.
                    else:
                        # Given that there was not an exact match, an unknown suffix will be found.
                        # It should not begin with a digit (e.g. if I asked for v1.6 I don't want v1.62)
                        # It should not begin with a - (as I desire to exclude prereleases from search, partially because git ls-remote can't get them in the semver order).
                        # Hence, the only acceptable next character is a full stop. Add this to the search term to exclude the above alternatives.
                        _version_specifier_search = version_specifier + '.'

                        for tag in _available_tags:
                            # _available_tags is already sorted by semver M.m.p highest precedence first when created.
                            if tag.startswith(_version_specifier_search):

                                # Ignore prerelease tags
                                # A request for v1.10 could so far pick up v1.10.2-rc3
                                # Furthermore, it could select v1.10.2-rc3 over v1.10.2 due to ls-remote's imperfect ordering.
                                # However, it would be excessive to ignore any tag with a dash in it. lite-v1.2.3 is a desired pickup from specifier lite-v1.2
                                _suffix = tag[len(_version_specifier_search):]
                                if '-' in _suffix:  # if there is a dash in the unspecified part of the tag
                                    continue        # skip and continue search

                                # The first tag tested which starts as required AND does not contain a dash after the search specifier, is the target. Save it and stop searching. 
                                _download_version = tag
                                break

                        # if _download_version is still None, a suitable branch/tag could not be found.
                        if _download_version is None: # not acceptable here as within `if branch_specifier is not None:` far above.
                            print("    ERROR: No suitable branch of", module_base_name, "found for specifier", version_specifier, "Cancelling download of", module_instance_name)
                            continue    # give up on this line of the recipe and move on to next

                # Get the short commit hash from branch or tag name. If no branches or tag match _download_Version, returns empty string
                _download_hash = os.popen("git ls-remote " + url + " " + _download_version).read()[:7]

            
            # Now that the target version has been identified, action this information
            print() # in terminal and logs, give each recipe line a paragraph

            # If no such instance of the module has been downloaded previously, clone a new one:
            if not Path(instance_dir).exists():
                print("    Downloading", module_instance_name, "version", _download_version, "(hash", _download_hash + ")", "from specifier", version_specifier)
                print("        from", url)
                print("        to  ", instance_dir)

                _download_command = "git clone --quiet " + url + " " + instance_dir
                if _download_version is not None:                    # If branch specified in recipe
                    _download_command += " -b " + _download_version  # Insert into the clone command. Else omit.
                os.system(_download_command)                         # Run the string concatenated above

            # If the module instance clone already exists (likely by this script running previously), update that instance
            else:
                # Get information about existing clone
                current_hash = os.popen("git -C " + instance_dir + " log --oneline -1").read()[:7]  # could also use rev parse head etc.
                # Showing current tag is harder. git describe --exact-match --tags/--all is ok but not ideal (if no tags found, fatal message is insuppressible).
                # tag display is not needed anyway when hashes are being compared. Only use is informing the user what the version being replaced was.
                # Hence, do not attempt to display old tag.

                if current_hash == _download_hash:
                    print("    " + module_instance_name, "existing version", _download_version, "(hash", _download_hash + ")", "is already suitable for specifier", version_specifier)

                else: # need to update
                    print("    Updating", module_instance_name, "from hash", current_hash, "to version", _download_version, "(hash", _download_hash + ")", "from specifier", version_specifier)
                    # git checkout or git switch?
                    # Need to stash changes eg replaced requirements files? No - lose them and relink from Config. 
                    #   Nothing should be changed in a module outside of what is linked from Config.
                    # What will cause the checkout to abort? Possible hard reset required.
                    os.system("git -C " + instance_dir + " checkout " + _download_version + " --quiet")

                    # Confirm if the update was successful
                    _post_update_hash = None # In case below line fails, don't let previously stored value persist.
                    _post_update_hash = os.popen("git -C " + instance_dir + " log --oneline -1").read()[:7]  # could also use rev parse head etc.
                    if _post_update_hash == _download_hash:
                        print("        " + module_instance_name, "has been sucessfully updated to", _post_update_hash)

                    else:
                        print("        ERROR: There was an issue during the checkout to", _download_hash + ".", module_instance_name, "is still on hash", _post_update_hash)

        else:
            print("ERROR: no Module URL defined for line in recipe", line)

print("## -----------------------------------------------------------------------")

## --------------------------------------------------------------------------------
