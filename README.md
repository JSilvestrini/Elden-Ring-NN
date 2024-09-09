# Elden-Ring-NN

## Table of Contents

-   [**Dependencies**](#dependencies)
-   [**How to Use**](#how-to-use)
-   [**Documentation**](#documentation)

## Dependencies

#### Python

-   streamlit
-   json
-   pymem
-   ...

#### External

-   Cheat Engine <- Link This
-   Hexinton All-in-One Cheat Table <- Link This
-   Elden Ring <- Link This
-   Practice Mod <- Link This

## How to Use

#### Cheat Engine

Inside of the Hexinton Table Add the following under the section shown below:

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

    python_file = io.open("TargetPointer.txt", 'w')
    num = readQword'LastLockOnTarget'
    python_file:write(tostring(num))
    python_file:close()

    python_file2 = io.open("WorldChrManPointer.txt", 'w')
    num2 = getAddress("WorldChrMan")
    python_file2:write(tostring(readQword'num2'))
    python_file2:close()

    python_file3 = io.open("PausePointer.txt", 'w')
    python_file3:write(tostring(pausegame_t))
    python_file3:close()

    ready_file = io.open("DataWritten.txt", 'w')
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
  t.Interval = 1000
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

More discussion of the cheat table is located in the readme that is in the following directory: scripts/place_cheat_table_here/README.md.

#### Elden Ring Initial Setup

## Documentation

Most of the files included in this repo have documentation based on Google's format, with information about the function, the arguments taken, the return type and the expected information returned, as well as potential raises (or in some cases exceptions that will be caught and suppressed).

#### animation_reset.py

#### game_access.py

#### memory_access.py
