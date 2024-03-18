# A concept for deploying Shoestring Solutions.

Future / WIP. 

The Solution is developed and delivered as a lightweight "recipe" of required Service Modules and configuration files.  
An "assembler" then runs on the recipe and gathers the Service Modules from respective git repos.  
As the workings of the assembler itself will need development, the assembler will have its own git repo.  
A minimal code snippet to download and run the assembler will be shipped with each solution. 

The assembler unites the config files with relevant Service Modules.  
docker compose build, ./start.sh and the solution is up. 
