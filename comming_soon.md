- TODO: Update ReadME Accordingly
    - TODO: Make sure speedhack + .dll is credited to original author                               [ DONE ]
    - TODO: Make sure that AOBs are credited to Cheat Table Makers and FPS ER                       [ DONE ]
    - TODO: Delete old legacy files
    - TODO: Add information about AOBScanner file and contents

- TODO: Refactor Environment
- TODO: Make new file and copy over incrementally
- TODO: Make boss walk backs more boss-specific
    - Could reduce training time by removing excess loading screens
    - TODO: Remove walk_back.py, legacy file

- TODO: Make it so a model fights one boss instead of multiple
    - TODO: Use Stake of Marika then TP to door
    - TODO: No longer use Gideon unless needed
    - Make way for Program to Open Map -> Move to Table -> TP
        - Can do G -> Open List -> Table Shortcut -> Enter

- TODO: Adjust rewards
    - TODO: Bonus for middle arena (Boss-Specific)
    - TODO: Punish for Bad or non-optimal flask use
        - Track flask number (get max during init or restart call)
    - TODO: Adjust rewards for the following 3 training modes
    - TODO: Reward for time alive rather than punish, gradually increase as boss health decreases

- TODO: One-Hit Kill Mode
    - Model will die if hit to ensure defensive play
    - No attacking in action space, no healing in action spaces, dodge, move, and jump only

- TODO: Health Threshold Mode
    - Model will die when below X Health
    - Give the ability to Heal

- TODO: Full Mode
    - Basically what it is now

- TODO: Multiple Observation Spaces, CNN and Ground Truth

- TODO: Work on database-related files (Stretch)
    - TODO: Streamlit or Qt6 application
        - take data, show buckets of information
        - correlate boss animation on distance
        - take map image and show death points
- TODO: Begin training AI more
- TODO: ADD IN A PYTHON DOWNLOAD FILE