A lightweight sqlite database is going to be used to store data. This will be used to track training progress, and hopefully step through runs to see the location of the player
and boss at any given timestep. This table will also track animation (attack) usage by bosses to find patterns in AI.

tables:
    1. Run Info: Run Number (PK), Boss ID, Boss Ending Health, Player Ending Health, Damage Taken, Start Time, End Time, Total Time, Victory Boolean, Reward Information
        a. Used for plotting information about each individual run
    2. Detailed Run Information: Run Number + Timestep (PK), pX, pY, pZ, pHealth, pAnimation, pAction, pReward, bX, bY, bZ, bHealth, bAnimation
        a. Used to draw over images so a player can view past runs and step through them one step at a time
    3. Bosses: Boss ID (PK), Name, attempts
        a. Just stores data about bosses, can be used for some random stuff
    4. Animations: Boss or Player ID + Animation ID, Total Usage, Minimum execution time, maximum execution time, average execution time
        a. A large list that contains all animations from bosses and players and will contain totals of all usage
    5. Boss Animation Usage: Animation ID + Run ID (PK), BossID, Usage, Distance from Player
        a. Can be used to see boss move preference in a bucket graph or something

Every 2,000 or so runs, archive tables 1, 2, and 5 to prevent large tables. Leave 1 entry incase of automatic increments.
if n % 2000 == 1 and n > 1: archive database tables


- TODO: Multiple Observation Spaces, CNN and Ground Truth
- TODO: Get moving on Streamlit or whatever
- TODO: Fix Agent File, Create a Run file, take user options to choose reward, action, and observation space
- TODO: Begin creating logs formats, make them optional to reduce file space on system (same for database)
- TODO: Create more animation stuff, save in csv format or something instead of json
- TODO: Create sqlite database to store information for data collection, csv for simple collection
- TODO: Check arena images, map to coordinates, live drawing functions for data viewing and analysis
- TODO: Check out PyQT6 or PySide6 for making the GUI instead of Streamlit