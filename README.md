# A deployment tool for Shoestring Solutions

## About
The purpose of this tool is to allow each Shoestring Solution to be developed and delivered in minimal form.  
The aim is to reduce each Solution's repository to the elements that are specific to that Solution.  
The motivation is two-fold:
- To avoid duplicates of Service Module source code, making version control possible.  
- To minimise Solution development time by making reuse of established modules as easy as possible.

A solution needs only to consist of a "recipe" (names of required Service Modules) and configuration files.  
An "assembler" then runs on the recipe and gathers the Service Modules from their respective git repos.  

As the workings of the assembler itself will need development, the assembler will have its own git repo - here. A minimal code snippet to download and run the assembler will be shipped with each solution, dubbed `get_service_modules.sh`. [See the starter solution template.](https://github.com/DigitalShoestringSolutions/starter-solution-template/blob/feature/assembler/ServiceModules/Assembly/get_service_modules.sh)


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
When assembled, the Sensing Service Module will be cloned first into `ServiceModules/Sensing` and then also into `ServiceModules/Sensing2`


## Linking Config

The Assembler can link config files shipped with the solution onto the Service Modules it downloads.  
If the `UserConfig` contains the subdir `MyServiceModule` and `MyServiceModule` is sucessfully downloaded via `recipe.txt`, then the contents of `UserConfig/MyServiceModule/` will be hard linked into `ServiceModules/MyServiceModule/config/`. 


If for example the `UserConfig` dir has the following structure:

```bash
├── UserConfig/
│   ├── Timeseries/
│   │   └── telegraf.conf
│   ├── Grafana/
│   │   └── dashboards/
│   │       │── dashboard1.json
│   │       └── dashboard2.json
│   ├── Sensing
│   │   └── main.py
│   └── Sensing2
│       └── main.py
...
```
Then when ServiceModules is populated:

```bash
├── ServiceModules/
│   ├── Timeseries/
│   │   ├── config/
│   │   │   └── telegraf.conf
│   │   └── ...
│   ├── Grafana
│   │   ├── config/
│   │   │   └── dashboards/
│   │   │       │── dashboard1.json
│   │   │       └── dashboard2.json
│   │   └── ...
│   ├── Sensing
│   │   ├── config/
│   │   │    └── main.py
│   │   └── ...
│   ├── Sensing2
│   │   ├── config/
│   │   │    └── main.py
│   │   └── ...
│   ├── ...
```
Multiples of the same Service Module are supported - the subdirectory name under `UserConfig` must be incremented as above.


## To try it out:

- Follow instructions in the README of [the Humidity Monitoring solution](https://github.com/DigitalShoestringSolutions/HumidityMonitoring)
