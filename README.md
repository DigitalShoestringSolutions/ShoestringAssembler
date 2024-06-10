# A concept for deploying Shoestring Solutions.

Future / WIP. 

The Solution is developed and delivered as a lightweight "recipe" of required Service Modules and configuration files.  
An "assembler" then runs on the recipe and gathers the Service Modules from respective git repos.  

<i>(As the workings of the assembler itself will need development, the assembler will have its own git repo - here. A minimal code snippet to download and run the assembler will be shipped with each solution, dubbed "preassembly.sh") </i>  


## Writing a recipe
The recipe for the solution is a text file called `recipe.txt` in the Solution's root directory.  
Service Modules are added to the Solution by appending their name to the recipe. A list of supported Service Modules can be found in `mirrordirector.py`.  
A particular branch or tag of that Service Module's codebase can be used by adding `=branchname` after the name of the Service Module. If this is not supplied, that Service Module's default branch will be used.

An example `recipe.txt`:
```
Grafana
MQTTBroker=master
Sensing=feature/recipe-lite
```


### Multiple of the same Service Module
Multiple instances of the same Service Module are supported. Simply duplicate the lines in the recipe:
```
Sensing=feature/recipe-lite
Sensing=feature/recipe-lite
```
This will create two Sensing Service Modules in your Solution. They can be on the same or different branches. 
When assembled, the Sensing Service Module will be cloned into `ServiceModules/Sensing` and also `ServiceModules/Sensing2`


## To try it out:

- Clone branch `feature/recipe` of the temperature monitoring solution
- Edit the config file as necessary in `UserConfig/sensor_config.toml`
- run `ServiceModules/Assembly/preassembly.sh` to assemble the solution
- `docker compose build`
- `./start.sh`

Note that you may need to remote into the pi from a computer with access to the private Shoestring repos.  
This repo, and many of the service modules called, are private: a typical pi will not have permissions to access them.  
The longer term plan is to consider making necessary repos public.
