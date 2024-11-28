# Elden-Ring-NN

The following repository contains code that creates a gym-like environment that can be used with stable-baselines3 PPO algorithms, and it aims to compete with previous gym environments for souls games. 

This specific implementation is currently using CNN related policies, though a ground truth version may be made in the future to hopefully create a performance (in terms of computations) increase.

Once the environment is finished and the agent begins training, the repo will be updated with some performance statistics and other tools for watching the training process as it runs.

## Table of Contents

-   [**Dependencies**](#dependencies)
    -   [**Python**](#python)
    -   [**External**](#external)
-   [**Pre-Run Steps**](#pre-run-steps)
-   [**How to Use**](#how-to-use)
-   [**Documentation**](#documentation)
    -   [**er_agent.py**](#er_agentpy)
    -   [**er_environment.py**](#er_environmentpy)
    -   [**er_model.py**](#er_modelpy)
    -   [**game_access.py**](#game_accesspy)
    -   [**logger.py**](#loggerpy)
    -   [**memory_access.py**](#memory_accesspy)
    -   [**webview.py**](#webviewpy)
-   [**References**](#references)

## Dependencies

### Python

-   streamlit
-   json
-   pymem
-   mss
-   pybind11
-   stable_baselines3
-   pytorch
-   numpy
-   ...

### External

**[Elden Ring](https://store.steampowered.com/app/1245620/ELDEN_RING/)**

As this is an environment for training a PPO agent for Elden Ring, you will need the game through either steam or some other service. I do not support or condone pirating, so I will not assist in solving problems that occur on pirated copies.

**[Practice Mod](https://www.nexusmods.com/eldenring/mods/5645)**

This mod makes much of the training much simpler. It makes it so I do not have to perform any complex checks on game logic flags if the PPO agent succeeds, and will automatically revive bosses when they are defeated. This also allows for 'walking back' to bosses to be programmed in with simple button presses since the mod teleports the player directly to the fog wall before the boss. While the mod is not needed to create an environment, it made the creation of it much simpler.

**[CMake](https://cmake.org/download/)**

You need at least version 3.10 of CMake to use the file that is included, but you could most likely get away with changing the minimum required version within CMakeLists.txt, but that is untested on my end.

## Pre-Run Steps

1. Within the **scripts** folder, there is a CMakeLists.txt file, make sure to build it using the following commands.

`cmake -S. Bbuild -Ax64`
`cmake --build build -j`

## How to Use

1. Follow the installation instructions for the practice mod that was linked within the previous section. Once it is installed, launch it through `launchmod_eldenring.bat`. Make sure that you have selected a character, loaded in, and placed your character in front of Gideon.
2. Run ...

## Documentation

Most of the files included in this repo have documentation with information about the function, the arguments taken, and the return type. Below is the specific use case of the file and the reason that it was written.

### data_collection.py

This file is used to gather information of different bosses and enemies, their animation states, how long the animation takes to complete, and stores it in .json format within the animation_files folder that corresponds to the global ID of the entity.

### er_agent.py

### er_environment.py

### er_helper.py

This file contains some of the random functions that would be needed in multiple files, as of now it focuses the window and can perform keyboard presses.

### er_model.py

### enemies.py

This file keeps track of individual enemies for the situations that a fight contains multiple enemies, like Godskin Duo, the fight with the Leonine Misbegotten and Crucible Knight, and others.

### game_access.py

This file is used heavily by the environment to retrieve information about the game state. This file relies on memory_access and communication through files with Cheat Engine. It finds pointers to values that are in Elden Ring's memory and stores those pointers so the environment can use the get functions to retrieve the values at those locations. It also has the ability to pause the game (please note that Elden Ring is normally not able to be paused).

### logger.py

### memory_access.py

This file was made to easily access pointers and memory addresses that were retrieved from Cheat Engine. This is mainly used inside of the **game_access.py** file to read information about the game state as well as edit information about the game state, like the player location, gravity toggle, and logic pause.

### player.py

This file keeps track of individual player pointers. It was made since I was in the process of breaking the **game_access.py** file into multiple parts.

### walk_back.py

This file allows the AI to easily get back to different boss arenas using the Elden Ring Boss Arena mod.

### webview.py

## References

**[Elden Ring FPS](https://github.com/Dasaav-dsv/erfps/tree/master)**

This repository, along with the Hexington Cheat Engine table, gave information over where to find pointers and what AOB to try and search for within the main module. Once I noticed that pymem was failing to find patterns, this repo was the inspiration for utilizing C++ with Python to create a (semi) efficient AOB scanner, though no code was used from the AOB files that are available.

**[SoulsGym](https://github.com/amacati/SoulsGym/tree/master)**

This repository contains a goldmine of information, and pointed me towards one of the most important reference (Elden Ring FPS). While no code was directly used from this repo, it was the original inspiration for creating an Elden Ring environment and using visual information rather than ground truth information.

**[Hexington Cheat Engine](https://www.nexusmods.com/eldenring/mods/48)**

This cheat table contains all AOB searches that I used, as well as information on other locations within memory that I could have never found myself. I used the AOB patterns as well as a modified version of their NPC Selector algorithm that was used to populate a table (in my case I used it to find the proper enemies to track).

This table was an invaluable resource.
<!-- 
Edit the documentation in this file, check removed files, check dependencies


-->