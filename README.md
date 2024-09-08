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

Inside of the Hexinton Table Add the following at line 290 inside of the Enable script (The top level script in the cheat table), directly after the `if #failedScans > 0 then` block of code:

```lua
python_file = io.open("WorldChrManPointer.txt", 'w')
python_file:write(tostring(getAddress("WorldChrMan")))
python_file:close()
```

Under the following section do the following:

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

python_file = io.open("TargetPointer.txt", 'w')
num = readQword'[LastLockOnTarget]'
python_file:write(tostring(num))
python_file:close()

end

[ENABLE]

local id = memrec.ID
local t = scriptTimers[id]

if t then
  t.Enabled = true
else
  scriptTimers[id] = createTimer()
  t = scriptTimers[id]
  t.Interval = 10
  t.OnTimer = onTimer
end

[DISABLE]

local t = scriptTimers[memrec.ID]
if t then
  t.Enabled = false
end
```

The above code was found on this forum [post](https://www.cheatengine.org/forum/viewtopic.php?t=618933&sid=ea8d85619a9513450cc63fbe2f1a3443). So credit to that user for the code. This creates a timer that will check to see if there is a locked on target and if the target changes. This is so that target can easily be grabbed each time that the player dies, since this is expected to be a lot. Unlike the WorldChrMan, this value is subject to change very often.

## Documentation

Most of the files included in this repo have documentation based on Google's format, with information about the function, the arguments taken, the return type and the expected information returned, as well as potential raises (or in some cases exceptions that will be caught and suppressed).

#### animation_reset.py

#### game_access.py

#### memory_access.py
