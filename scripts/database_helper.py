import sqlite3
from scripts.game_accessor import GameAccessor

sql_create_run_info = """
CREATE TABLE Run_Info (
    Run_Number INTEGER PRIMARY KEY,
    Boss_ID INTEGER,
    Boss_Ending_Health REAL,
    Player_Ending_Health REAL,
    Damage_Taken REAL,
    Start_Time DATETIME,
    End_Time DATETIME,
    Total_Time REAL,
    Victory BOOLEAN,
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID)
);
"""

sql_create_detailed_run_info = """
CREATE TABLE Detailed_Run_Info (
    Run_Number INTEGER,
    Timestep INTEGER,
    pX REAL,
    pY REAL,
    pZ REAL,
    pHealth REAL,
    pAnimation TEXT,
    pAction TEXT,
    pReward REAL,
    bX REAL,
    bY REAL,
    bZ REAL,
    bHealth REAL,
    bAnimation TEXT,
    PRIMARY KEY (Run_Number, Timestep),
    FOREIGN KEY (Run_Number) REFERENCES Run_Info(Run_Number)
);
"""

sql_create_bosses = """
CREATE TABLE Bosses (
    Boss_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Attempts INTEGER
);
"""

sql_create_animations = """
CREATE TABLE Animations (
    Boss_ID INTEGER,
    Animation_ID INTEGER,
    Total_Usage INTEGER,
    Min_Execution_Time REAL,
    Max_Execution_Time REAL,
    Avg_Execution_Time REAL,
    PRIMARY KEY (Boss_ID, Animation_ID),
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID)
);
"""

sql_create_boss_animation_usage = """
CREATE TABLE Boss_Animation_Usage (
    Animation_ID INTEGER,
    Run_ID INTEGER,
    Boss_ID INTEGER,
    Usage INTEGER,
    Distance_From_Player REAL,
    PRIMARY KEY (Animation_ID, Run_ID),
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID),
    FOREIGN KEY (Run_ID) REFERENCES Run_Info(Run_Number)
);
"""

table_names = [
    ("Run_Info", sql_create_run_info),
    ("Detailed_Run_Info", sql_create_detailed_run_info),
    ("Bosses", sql_create_bosses),
    ("Animations", sql_create_animations),
    ("Boss_Animation_Usage", sql_create_boss_animation_usage),
]

def create_database() -> None:
        con = sqlite3.connect("elden_ring.db")
        cur = con.cursor()

        for table_name, create_sql in table_names:
            try:
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if not cur.fetchone():
                    cur.execute(create_sql)
                    con.commit()
            except sqlite3.Error as e:
                print(f"Error creating table {table_name}: {e}")

def write_to_database_step(self, game: GameAccessor, info: dict) -> None:
    # use info and game to write to detailed run info
    ...

def write_to_database_run(game: GameAccessor, info: dict) -> None:
    # use info to write to run info
    # also write to bosses and increment attempts
    ...

def write_to_database_animations(game: GameAccessor, info: dict) -> None:
    # write to both animations tables
    ...

def get_run_number() -> int:
    # get the largest run number from run info table
    ...

def misc_query(query: str) -> None:
    # can pass in random queries
    ...