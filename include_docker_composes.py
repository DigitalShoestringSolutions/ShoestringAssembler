# include_docker_composes.py

# Creates a docker-compose.yml file in the solution files directory.
# Detects docker-compose files in service modules and includes them in the master docker-compose file
# does not use the recipe file directly, as some service modules may not have docker-compose elements (eg SetupLogging)
#     and bespoke service modules using compose may be included with the solution (and hence not in the recipe)




## -- Imports ---------------------------------------------------------------------

# standard imports
from pathlib import Path
import os

# installed imports
#none

# Local imports
#none

## --------------------------------------------------------------------------------




## -- Settings --------------------------------------------------------------------

DOCKER_COMPOSE_FILE_NAMES = ['docker-compose.yml', 'docker-compose.yaml']   # for detecting sub compose files

# Define the solution files folder as 3 levels above this script.
# Typically the stack will be <soluton_files>/ServiceModules/Assembly/ShoestringAssembler/include_docker_composes.py
solution_files = Path(__file__).parents[3]
ServiceModulesDir = solution_files.joinpath("ServiceModules")

## --------------------------------------------------------------------------------




## -- Iterate over service module folders to detect compose files -----------------

print("## -----------------------------------------------------------------------")
print("Searching for docker-compose.yml in Service Modules...")

sub_compose_files = []

# What the below block should do:
# for each servicemodulesdir in servicemoduledirs:
#   if servicemoduledir contains a file with name in DOCKER_COMPOSE_FILE_NAMES:
#       note path relative to solution files eg ServiceModules/MQTT/docker-compose.yml

for file in ServiceModulesDir.rglob('*'):
    if file.name in DOCKER_COMPOSE_FILE_NAMES:
        rel_path = file.relative_to(solution_files)
        print("    Including", rel_path, "in Solution docker-compose.yml")
        sub_compose_files.append(str(rel_path))

## -------------------------------------------------------------------------------




## -- Create the master docker-compose.yml and ./start.sh and ./stop.sh ----------
#  --     iff there are service modules using docker 

if len(sub_compose_files) > 0:
    with solution_files.joinpath(Path('docker-compose.yml')).open(mode='w') as master_compose_file:

        # append include lines
        master_compose_file.write('include:\n')

        for sub_compose_file in sub_compose_files:
            master_compose_file.write('    - ' + sub_compose_file + '\n')

        # Add the shoestring-internal network declaration to the end of the master compose file:
        master_compose_file.write('\n')
        master_compose_file.writelines(['networks:\n', '     internal:\n', '         name: shoestring-internal'])


    # If the solution is using compose, also create ./start.sh if not already present in the solution
    
    start_path = solution_files.joinpath("start.sh")
    print(start_path)
    if not start_path.exists():
        print("    Creating", start_path)

        # Open for exclusive creation. Fail if file already exists, as if block already checked.
        with open(start_path, 'x') as f:
            f.write('CURRENT_UID="$(id -u)" docker compose up -d')

        # Set executable bit. Uses absolute file path.
        os.popen("chmod +x " + str(start_path))

    else:
        print("    start.sh already exists")


print("## -----------------------------------------------------------------------")

## --------------------------------------------------------------------------------
