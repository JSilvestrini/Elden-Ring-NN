# Elden-Ring-NN

## Table of Contents

-   [**Dependencies**](#dependencies)
    -   [**Python**](#python)
    -   [**External**](#external)
-   [**How to Use**](#how-to-use)
    -   [**Cheat Engine**](#cheat-engine)
    -   [**Elden Ring**](#elden-ring-initial-setup)
-   [**Documentation**](#documentation)
    -   [**er_agent.py**](#er_agentpy)
    -   [**er_environment.py**](#er_environmentpy)
    -   [**er_model.py**](#er_modelpy)
    -   [**game_access.py**](#game_accesspy)
    -   [**logger.py**](#loggerpy)
    -   [**memory_access.py**](#memory_accesspy)
    -   [**webview.py**](#webviewpy)

## Dependencies

#### Python

-   streamlit
-   json
-   pymem
-   dxcam
-   ...

#### External

-   Cheat Engine <- Link This
-   Hexinton All-in-One Cheat Table <- Link This
-   Elden Ring <- Link This
-   Practice Mod <- Link This

## How to Use

#### Cheat Engine

Place the Hexinton table inside of `scripts/place_cheat_table_here/` and inside of the Hexinton Table Add the following under the section shown below:

```
Enable
    |___NPC
        |___Targeted Enemy
```

Inside of Targeted Enemy, create a new header that has a script, the easiest (and messiest) way to do this is to copy another section that already has a script on it into this section and then change the script along with removing all the children headers. This should leave you with one final header that has a script. Next, edit the script to match the following:

```lua
{$lua}
if not scriptTimers then scriptTimers = {} end

local function onTimer(timer)

  player_dead_file = io.open('PlayerDead.txt', 'r')

  if player_dead_file ~= nil then
    io.close(player_dead_file)
    pausegame_t=AOBScanModuleUnique("eldenring.exe","80 BB 28 01 00 00 00 0F 84","+X")

    world_file = io.open("WorldChrManPointer.txt", 'w')
    world_ptr = getAddress("WorldChrMan")
    world_file:write(tostring(readQword'world_ptr'))
    world_file:close()

    pause_file = io.open("PausePointer.txt", 'w')
    pause_file:write(tostring(pausegame_t))
    pause_file:close()

    ready_file = io.open("DataWritten.txt", 'w')
    ready_file:close()
  end

  target_needed = io.open('NeedTarget.txt', 'r')

  if target_needed ~= nil then
    io.close(target_needed)

    tar_ptr = readQword'LastLockOnTarget'
    target_file = io.open("TargetPointer.txt", 'w')
    target_file:write(tostring(tar_ptr))
    target_file:close()

    ready_file = io.open("TargetFound.txt", 'w')
    ready_file:close()
  end
end

[ENABLE]

local id = memrec.ID
local t = scriptTimers[id]

if t then
  t.Enabled = true
else
  scriptTimers[id] = createTimer()
  t = scriptTimers[id]
  t.Interval = 20
  t.OnTimer = onTimer
end

[DISABLE]

local t = scriptTimers[memrec.ID]
if t then
  t.Enabled = false
end
```

The above code was found on this forum [post](https://www.cheatengine.org/forum/viewtopic.php?t=618933&sid=ea8d85619a9513450cc63fbe2f1a3443) and edited to fit the needs of this project. So credit to that user for the code. This creates a timer that will check to see if there is a locked on target and if the target changes. This is so that target can easily be grabbed each time that the player dies, since this is expected to be a lot.

For anyone editing the code above, the interval is in milliseconds, and the code you want to change is within the function block called `onTimer`.

More discussion of the cheat table is located in the readme that is in the following directory: scripts/place_cheat_table_here/README.md and there will be a separate lua file that contains the code as well.

#### Elden Ring Initial Setup

https://www.nexusmods.com/eldenring/mods/5645?tab=description

## Documentation

Most of the files included in this repo have documentation with information about the function, the arguments taken, and the return type. Below is the specific use case of the file and the reason that it was written.

#### data_collection.py

This file is used to gather information of different bosses and enemies, their animation states, how long the animation takes to complete, and stores it in .json format within the animation_files folder that corresponds to the global ID of the entity.

#### er_agent.py

#### er_environment.py

#### er_helper.py

This file contains some of the random functions that would be needed in multiple files, as of now it focuses the window and can perform keyboard presses.

#### er_model.py

#### enemies.py

This file keeps track of individual enemies for the situations that a fight contains multiple enemies, like Godskin Duo, the fight with the Leonine Misbegotten and Crucible Knight, and others.

#### game_access.py

This file is used heavily by the environment to retrieve information about the game state. This file relies on memory_access and communication through files with Cheat Engine. It finds pointers to values that are in Elden Ring's memory and stores those pointers so the environment can use the get functions to retrieve the values at those locations. It also has the ability to pause the game (please note that Elden Ring is normally not able to be paused).

#### logger.py

#### memory_access.py

This file was made to easily access pointers and memory addresses that were retrieved from Cheat Engine. This is mainly used inside of the **game_access.py** file to read information about the game state as well as edit information about the game state, like the player location, gravity toggle, and logic pause.

#### player.py

This file keeps track of individual player pointers. It was made since I was in the process of breaking the **game_access.py** file into multiple parts.

#### walk_back.py

This file allows the AI to easily get back to different boss arenas using the Elden Ring Boss Arena mod.

#### webview.py
