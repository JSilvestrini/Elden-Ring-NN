import sqlite3

# open connection within environment, commit and close when run is finished, open connection on reset
# If run does not finish, try and close the connection before opening it within reset

sql_create_run_info = """
CREATE TABLE Model_Run_Info (
    Run_Number INTEGER,
    Boss_ID INTEGER,
    Boss_Ending_Health REAL,
    Player_Ending_Health REAL,
    Total_Time REAL,
    Victory BOOLEAN,
    PRIMARY KEY (Run_Number, Boss_ID),
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID)
);
"""

sql_create_detailed_run_info_player = """
CREATE TABLE Detailed_Run_Info_Player (
    Run_Number INTEGER,
    Timestep INTEGER,
    pX REAL,
    pY REAL,
    pZ REAL,
    pHealth REAL,
    pAnimation INTEGER,
    pAction INTEGER,
    pReward REAL,
    PRIMARY KEY (Run_Number, Timestep),
    FOREIGN KEY (Run_Number) REFERENCES Run_Info(Run_Number)
);
"""

sql_create_detailed_run_info_boss = """
CREATE TABLE Detailed_Run_Info_Boss (
    Run_Number INTEGER,
    Timestep INTEGER,
    Boss_ID INTEGER,
    bX REAL,
    bY REAL,
    bZ REAL,
    bHealth REAL,
    bAnimation INTEGER,
    PRIMARY KEY (Run_Number, Timestep, Boss_ID),
    FOREIGN KEY (Run_Number) REFERENCES Run_Info(Run_Number)
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID)
);
"""

sql_create_bosses = """
CREATE TABLE Bosses (
    Boss_ID INTEGER PRIMARY KEY,
    Attempts INTEGER
);
"""

sql_create_animations = """
CREATE TABLE Animations (
    Boss_ID INTEGER,
    Animation_ID INTEGER,
    Total_Usage INTEGER,
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
    PRIMARY KEY (Animation_ID, Run_ID),
    FOREIGN KEY (Boss_ID) REFERENCES Bosses(Boss_ID),
    FOREIGN KEY (Run_ID) REFERENCES Run_Info(Run_Number)
);
"""

table_names = [
    ("Model_Run_Info", sql_create_run_info),
    ("Detailed_Run_Info_Player", sql_create_detailed_run_info_player),
    ("Detailed_Run_Info_Boss", sql_create_detailed_run_info_boss),
    ("Bosses", sql_create_bosses),
    ("Animations", sql_create_animations),
    ("Boss_Animation_Usage", sql_create_boss_animation_usage),
]

def create_database(con: sqlite3.Connection) -> None:
        cur = con.cursor()

        for table_name, create_sql in table_names:
            try:
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                if not cur.fetchone():
                    cur.execute(create_sql)
                    con.commit()
            except sqlite3.Error as e:
                print(f"Error creating table {table_name}: {e}")

def write_to_database_step_player(con: sqlite3.Connection, info: dict) -> None:
    # use info and game to write to detailed run info
    dbstr = f"""
    INSERT INTO Detailed_Run_Info_Player (
    Run_Number,
    Timestep,
    pX,
    pY,
    pZ,
    pHealth,
    pAnimation,
    pAction,
    pReward) VALUES (
    {info["Run_Number"]},
    {info["Timestep"]},
    {info["pX"]},
    {info["pY"]},
    {info["pZ"]},
    {info["pHealth"]},
    {info["pAnimation"]},
    {info["pAction"]},
    {info["pReward"]}
    );
    """

    cur = con.cursor()
    cur.execute(dbstr)

def write_to_database_step_boss(con: sqlite3.Connection,info: dict) -> None:
    dbstr = f"""
    INSERT INTO Detailed_Run_Info_Boss (
    Run_Number,
    Timestep,
    Boss_ID,
    bX,
    bY,
    bZ,
    bHealth,
    bAnimation) VALUES (
    {info["Run_Number"]},
    {info["Timestep"]},
    {info["Boss_ID"]},
    {info["bX"]},
    {info["bY"]},
    {info["bZ"]},
    {info["bHealth"]},
    {info["bAnimation"]}
    );
    """

    cur = con.cursor()
    cur.execute(dbstr)

def write_to_database_run(con: sqlite3.Connection, info: dict) -> None:
    # use info to write to run info
    # also write to bosses and increment attempts
    dbstr = f"""
    INSERT INTO Model_Run_Info (
    Run_Number,
    Boss_ID,
    Boss_Ending_Health,
    Player_Ending_Health,
    Total_Time,
    Victory) VALUES (
    {info["Run_Number"]},
    {info["Boss_ID"]},
    {info["Boss_Ending_Health"]},
    {info["Player_Ending_Health"]},
    {info["Total_Time"]},
    {info["Victory"]}
    );
    """

    cur = con.cursor()
    cur.execute(dbstr)

def increase_attempts(con: sqlite3.Connection, boss_id: int) -> None:
    # use info to write to bosses
    dbstr = f"""
    INSERT INTO Bosses (boss_id, attempts) 
    VALUES ({boss_id}, 1)
    ON CONFLICT(boss_id) DO UPDATE SET attempts = attempts + 1;
    """

    cur = con.cursor()
    cur.execute(dbstr)

def write_to_database_animations(con: sqlite3.Connection, info: dict) -> None:
    dbstr = f"""
    INSERT INTO Boss_Animation_Usage (
    Animation_ID,
    Run_ID,
    Boss_ID,
    Usage) VALUES (
    {info["Animation_ID"]},
    {info["Run_Number"]},
    {info["Boss_ID"]},
    1)
    ON CONFLICT(Animation_ID, Run_ID) DO UPDATE SET Usage = Usage + 1;
    """

    cur = con.cursor()
    cur.execute(dbstr)

    dbstr = f"""
    INSERT INTO Animations (
    Boss_ID,
    Animation_ID,
    Total_Usage) VALUES (
    {info["Boss_ID"]},
    {info["Animation_ID"]},
    1) 
    ON CONFLICT(Boss_ID, Animation_ID) DO UPDATE SET Total_Usage = Total_Usage + 1;
    """

    cur = con.cursor()
    cur.execute(dbstr)

def get_run_number(con: sqlite3.Connection, ) -> int:
    # get the largest run number from run info table
    cur = con.cursor()
    cur.execute("SELECT COALESCE(MAX(Run_Number), 0) FROM Model_Run_Info;")
    run_number = cur.fetchone()[0]
    return run_number

def misc_query(con: sqlite3.Connection, query: str) -> None:
    # can pass in random queries
    cur = con.cursor()
    cur.execute(query)