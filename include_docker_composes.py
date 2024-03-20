# include_docker_composes.py

# Creates a docker-compose.yml file in the solution files directory.
# Detects docker-compose files in service modules and includes them in the master docker-compose file
# does not use the recipe file directly, as some service modules may not have docker-compose elements (eg SetupLogging)

# There are many approaches to the problem this is trying to solve, including:
# Merging compose files
# Extending compose files
# Building containers separately (result of quick test: dependency service remains undefined)
# Including compose files - this is simply the one I am trying first.

## -- Imports ---------------------------------------------------------------------

# standard imports
from pathlib import Path

# installed imports
#none

# Local imports
#none

## --------------------------------------------------------------------------------

## -- Firm-coded settings ---------------------------------------------------------

DOCKER_COMPOSE_VERSION = 'version: "2"'                                     # for inclusion in the master docker-compose.yml
DOCKER_COMPOSE_FILE_NAMES = ['docker-compose.yml', 'docker-compose.yaml']   # for detecting sub compose files

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <soluton_files>/ServiceModules/Assembly/ShoestringAssembler/include_docker_composes.py
solution_files = Path(__file__).parents[3]
ServiceModulesDir = solution_files.joinpath("ServiceModules")

## --------------------------------------------------------------------------------

## -- iterate over service module folders -----------------------------------------

sub_compose_files = []

# What the below block should do:
# for each servicemodulesdir in servicemoduledirs:
#   if servicemoduledir contains a file with name in DOCKER_COMPOSE_FILE_NAMES:
#       note path relative to solution files eg ServiceModules/MQTT/docker-compose.yml

for file in ServiceModulesDir.rglob('*'):
    if file.name in DOCKER_COMPOSE_FILE_NAMES:
        print("found a compose file!")
        rel_path = file.relative_to(solution_files)
        print(rel_path)
        sub_compose_files.append(str(rel_path))

## --------------------------------------------------------------------------------

## -- Create the master docker-compose.yml ----------------------------------------

with solution_files.joinpath(Path('docker-compose.yml')).open(mode='w') as master_compose_file:

    # Add version line to top of master compose file
    master_compose_file.write(DOCKER_COMPOSE_VERSION + '\n')
    master_compose_file.write('\n')

    # append include lines
    if len(sub_compose_files) > 0:
        master_compose_file.write('include:\n')

        for sub_compose_file in sub_compose_files:
            master_compose_file.write('    - ' + sub_compose_file + '\n')

    # Add the shoestring-internal network declaration to the end of the master compose file:
    master_compose_file.write('\n')
    master_compose_file.writelines(['networks:\n', '     internal:\n', '         name: shoestring-internal\n'])

## --------------------------------------------------------------------------------