# A deployment tool for Shoestring Solutions

## About
The purpose of this tool is to allow each Shoestring Solution to be developed and delivered in minimal form.  
The aim is to reduce each Solution's repository to the elements that are specific to that Solution.  
The motivation is two-fold:
- To avoid duplicates of the core source code of reusuable Modules, making version control possible.  
- To minimise Solution development time by making reuse of established modules as easy as possible.

A solution needs only to consist of a "recipe" (names of required Modules) and configuration files.  
An "assembler" then runs on the recipe and gathers the Modules from their respective git repos.  

As the workings of the assembler itself will need development, the assembler will have its own git repo - here. A minimal code snippet to download and run the assembler will be shipped with each solution, dubbed `get_modules.sh`. [See the starter solution template.](https://github.com/DigitalShoestringSolutions/starter-solution-template/blob/feature/assembler/Modules/Assembly/get_modules.sh)


## Writing a recipe
The recipe for the solution is a text file called `recipe.txt` in the Solution's root directory.  
Modules are added to the Solution by appending their name to the recipe. Each Module must have its own line in `recipe.txt`.    
A list of supported Modules can be found in `mirrordirector.py`.

### Specifing versions of Modules
A particular branch or tag of that Module's codebase can be specified by adding `=branchname` after the name of the Module. If this is not supplied, that Module's default branch will be used. Release tags can be specified in the same way.  

Semantically versioned release tags can be partially specified. Where an exact branch or tag match is not available, the tag with the highest SemVer precedence that begins as specified will be used.  
Note that prereleases (tags with dashed suffixes) will not be automatically selected.  

An example of a valid `recipe.txt`:
```
Grafana
MQTTBroker=main
Sensing=feature/recipe-lite
Telemetry=v1.2.3
SetupLogging=v1.6
```
Assuming the exact tag `v1.2.3` exists for Telemetry, this will be used.  
Assuming the exact tag `v1.6` does not exist for SetupLogging, `v1.6.2` would be selected over `v1.6.1`, but `v1.6.3-rc4` would be ignored.

### Multiple of the same Module
Multiple instances of the same Module are supported. Simply duplicate the lines in the recipe:
```
Sensing=feature/recipe-lite
Sensing=feature/recipe-lite
```
This will create two Sensing Modules in your Solution. They can be on the same or different branches/tags. 
When assembled, the Sensing Module will be cloned first into `Modules/Sensing` and then also into `Modules/Sensing2`


## Linking Config

The Assembler can link config files shipped with the solution onto the Modules it downloads.  
If the `UserConfig` contains the subdir `MyModule` and `MyModule` is sucessfully downloaded via `recipe.txt`, then the contents of `UserConfig/MyModule/` will be hard linked into `Modules/MyModule/config/`. 


If for example the `UserConfig` dir has the following structure:

```bash
├── UserConfig/
│   ├── InfluxDB/
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
Then when Modules is populated:

```bash
├── Modules/
│   ├── InfluxDB/
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
Multiples of the same Module are supported - the subdirectory name under `UserConfig` must be incremented as above. This approach allows multiple instances of the same Module to be configured differently.


## Logging

During Assembly, status messages are printed to terminal. This includes what versions of Modules have been selected, where config files are being linked between UserConfig and Modules, what `docker-compose` files have been detected etc.  
These (`stdout&stderr`) are also saved to a local text file called `assemblerlog.txt`, which will appear alongside the clone.  
Hence, if the Assembler is downloaded with [the template's `get_modules.sh`](https://github.com/DigitalShoestringSolutions/starter-solution-template/blob/feature/assembler/Modules/Assembly/get_modules.sh) the file `assemblerlog.txt` will appear alongside `get_modules.sh` in `.../Modules/Assembly/`.

## To try it out:

- Follow instructions in the README of [the Humidity Monitoring solution](https://github.com/DigitalShoestringSolutions/HumidityMonitoring)
