# A concept for deploying Shoestring Solutions.

Future / WIP. 

The Solution is developed and delivered as a lightweight "recipe" of required Service Modules and configuration files.  
An "assembler" then runs on the recipe and gathers the Service Modules from respective git repos.  

<i>(As the workings of the assembler itself will need development, the assembler will have its own git repo - here. A minimal code snippet to download and run the assembler will be shipped with each solution, dubbed "preassembly.sh") </i>

The assembler unites the config files with relevant Service Modules.  

## To try it out:

- Clone branch `feature/recipe` of the temperature monitoring solution
- Edit the config file as necessary in `UserConfig/sensor_config.toml`
- run `ServiceModules/Assembly/preassembly.sh` to assemble the solution
- `docker compose build`
- `./start.sh`

Note that you may need to remote into the pi from a computer with access to the private Shoestring repos.  
This repo, and many of the service modules called, are private: a typical pi will not have permissions to access them.  
The longer term plan is to consider making necessary repos public.