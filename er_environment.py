from scripts.game_accessor import GameAccessor
from scripts import er_helper
from scripts import database_helper
from scripts import walk_back
from scripts import speedhack
import sqlite3
import dxcam
import time
import numpy as np
import cv2
import gymnasium
import random

'''
forward             - w
left                - a
back                - s
right               - d
jump                - f
dodge               - space
change target up    - 1
change target down  - 2
change target left  - 3
change target right - 4
switch spell        - up
switch item         - down
attack right        - m
strong attack       - l
block               - k
ash of war          - n
use item            - r
crouch              - x
'''

simple_action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['f'],           # jump
    9: ['3'],           # switch target left
    10: ['4'],          # switch target right
    11: ['down'],       # switch item
    12: ['m'],          # attack
    13: ['l'],          # strong attack
    14: ['k'],          # block
    15: ['n'],          # use skill
    16: ['r'],          # use item
}

simple_no_switch_action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['f'],           # jump
    9: ['3'],           # switch target left
    10: ['4'],          # switch target right
    11: ['m'],          # attack
    12: ['l'],          # strong attack
    13: ['k'],          # block
    14: ['n'],          # use skill
    15: ['r'],          # use item
}

'''Adds more movement options for jumping'''
mid_action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
    14: ['w', 'f', 'l'],# forward jump + strong attack
    15: ['x'],          # crouch
    16: ['3'],          # switch target left
    17: ['4'],          # switch target right
    18: ['down'],       # switch item
    19: ['m'],          # attack
    20: ['l'],          # strong attack
    21: ['k'],          # block
    22: ['n'],          # use skill
    23: ['r'],          # use item
}

mid_no_switch_action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
    14: ['w', 'f', 'l'],# forward jump + strong attack
    15: ['x'],          # crouch
    16: ['3'],          # switch target left
    17: ['4'],          # switch target right
    18: ['m'],          # attack
    19: ['l'],          # strong attack
    20: ['k'],          # block
    21: ['n'],          # use skill
    22: ['r'],          # use item
}

'''Adds lock on and some movement when attacking'''
complex_action_space = {
    0: ['w'],           # forward
    1: ['a'],           # left
    2: ['s'],           # back
    3: ['d'],           # right
    4: ['w', 'space'],  # forward roll
    5: ['a', 'space'],  # left roll
    6: ['s', 'space'],  # back roll
    7: ['d', 'space'],  # right roll
    8: ['space'],       # dodge
    9: ['f'],           # jump
    10: ['w', 'f'],     # forward jump
    11: ['a', 'f'],     # left jump
    12: ['s', 'f'],     # back jump
    13: ['d', 'f'],     # right jump
    14: ['w', 'f', 'l'],# forward jump + strong attack
    15: ['x'],          # crouch
    16: ['q'],          # lock-on
    17: ['3'],          # switch target left
    18: ['4'],          # switch target right
    19: ['down'],       # switch item
    20: ['m'],          # attack
    21: ['w', 'm'],     # forward attack
    22: ['l'],          # strong attack
    23: ['w', 'l'],     # forward strong attack
    24: ['k'],          # block
    25: ['n'],          # use skill
    26: ['r'],          # use item
}

full_walk_backs = { # midra, check both forms [0005, 0006]
    # more will be added, I have these for now
    # since I have screenshots of their arenas
    0: walk_back.godrick,
    1: walk_back.morgott,
    2: walk_back.maliketh,
    3: walk_back.godfrey,
    4: walk_back.leonine_misbegotten,
    5: walk_back.margit,
    6: walk_back.dragonkin_nokstella,
    7: walk_back.red_wolf,
    8: walk_back.loretta,
    9: walk_back.makar,
    10: walk_back.elemer,
    11: walk_back.dragonkin_siofra,
    12: walk_back.mimic_tear,
    13: walk_back.misbegotten_crucible_knight,
    14: walk_back.goldfrey,
    15: walk_back.godskin_noble,
    16: walk_back.mohg,
    17: walk_back.godskin_apostle,
    18: walk_back.gideon,
    19: walk_back.loretta_haligtree,
    20: walk_back.grafted_scion,
    21: walk_back.burial_watchdog,
    22: walk_back.burial_watchdog_duo,
    23: walk_back.crucible_knight_duo,
    24: walk_back.beastman,
    25: walk_back.misbegotten_crusader,
    26: walk_back.dancing_lion,
    27: walk_back.rellana,
    28: walk_back.messmer,
    29: walk_back.midra,
    30: walk_back.romina,
    31: walk_back.consort_radahn,
    32: walk_back.death_knight,
    33: walk_back.ancient_dragon_man,
    34: walk_back.death_knight_rauh
}

walk_backs = {
    0: walk_back.godrick,
    1: walk_back.morgott,
    2: walk_back.maliketh,
    3: walk_back.godfrey,
    4: walk_back.leonine_misbegotten,
    5: walk_back.dragonkin_nokstella,
    6: walk_back.red_wolf,
    7: walk_back.elemer,
    8: walk_back.dragonkin_siofra,
    9: walk_back.mimic_tear,
    10: walk_back.misbegotten_crucible_knight,
    11: walk_back.mohg,
    12: walk_back.loretta_haligtree,
    13: walk_back.grafted_scion,
    14: walk_back.crucible_knight_duo,
    15: walk_back.beastman,
    16: walk_back.misbegotten_crusader,
    17: walk_back.dancing_lion,
    18: walk_back.rellana,
    19: walk_back.messmer,
    20: walk_back.midra,
    21: walk_back.romina,
    22: walk_back.consort_radahn,
    23: walk_back.ancient_dragon_man
}

action_spaces = [simple_no_switch_action_space, simple_action_space, mid_no_switch_action_space, mid_action_space, complex_action_space]

class EldenRing(gymnasium.Env):
    def __init__(self, action_space = 2, database_writing = False, n_steps = 1024):
        self.__database_writing = database_writing
        self.__game = GameAccessor()
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        # This small offset is for a 4k monitor, might be different for others
        self.__region = (12 + left, 52 + top, 12 + right, 52 + bottom)
        self.obs_type = "rgb"
        self.action_space = gymnasium.spaces.Discrete(len(action_spaces[action_space]))
        self.observation_space = gymnasium.spaces.Box(low=0, high=1, shape=((self.__region[3]- self.__region[1]), (self.__region[2] - self.__region[0]), 3), dtype=np.uint8)

        # can switch action spaces and reward function
        self.key_action_space = action_spaces[action_space]
        self.reward_function = self.complex_reward
        self.games = 0

        # Used for database writing
        self.time_step_run = 0
        self.time_step_total = 0
        self.n_steps = n_steps
        self.begin_time = 0
        self.end_time = 0

        self.speed_hack = speedhack.SpeedHackConnector(self.__game.get_process_id())

        if self.__database_writing:
            self.con = sqlite3.connect("elden_ring.db")
            database_helper.create_database(self.con)
            self.games = database_helper.get_run_number(self.con) if database_helper.get_run_number(self.con) > 0 else 0
            self.con.close()

        self.__game.reset()

    def reset(self, seed=0, options=0) -> None:
        if not self.__game.player_in_roundtable():
            self.__game.kill_player()
            time.sleep(10)
        time.sleep(4)

        self.speed = 1
        self.speed_hack.set_game_speed(self.speed)

        # after n games change the walkback function, maybe 1k then 10k then 100k
        self.reward = 0
        self.time_step_run = 0
        self.games += 1
        print(f"RESET CALLED: GAME {self.games} STARTING...")
        er_helper.clean_keys()
        self.__game.reset() # Reset when entering new area

        #if self.games > 0:
        #    print(f"Actions per Second: {self.time_step / (self.end_time - self.begin_time)}")

        func = walk_backs[random.randint(0, len(walk_backs) - 1)]
        self.enemy_id = func()

        if self.__database_writing:
            for i in range(0, len(self.enemy_id)):
                self.con = sqlite3.connect("elden_ring.db")
                database_helper.increase_attempts(self.con, self.enemy_id[i])

        while self.__game.loading_state():
            time.sleep(0.2)

        self.__game.reset() # Reset when entering new area, just incase

        time.sleep(1)
        er_helper.enter_boss()

        self.speed = 2
        self.speed_hack.set_game_speed(self.speed)

        self.__game.clean()
        while self.__game.enemies == {}:
            time.sleep(0.02)
            self.__game.find_enemies(self.enemy_id.copy())

        self.screenshot()
        self.reset_ground_truth()

        return self.state(), {}
    
    def reset_ground_truth(self) -> None:
        self.begin_time = time.time()
        # used for rewards
        self.deal_damage_timer = time.time()
        self.take_damage_timer = time.time()

        self.player_max_health = self.__game.get_player_max_health()
        self.player_current_health = self.__game.get_player_health()
        self.player_max_stamina = self.__game.get_player_max_stamina()
        self.player_current_stamina = self.__game.get_player_stamina()
        self.player_max_fp = self.__game.get_player_max_fp()
        self.player_current_fp = self.__game.get_player_fp()
        self.boss_max_health = self.__game.get_enemy_max_health()
        self.boss_current_health = self.__game.get_enemy_health()
        self.player_coordinates = self.__game.get_player_coords()
        self.boss_coordinates = self.__game.get_enemy_coords()
        self.player_animation = self.__game.get_player_animation()
        self.boss_animation = self.__game.get_enemy_animation()

        self.player_previous_health = self.player_current_health
        self.player_previous_stamina = self.player_current_stamina
        self.player_previous_fp = self.player_current_fp
        self.boss_previous_health = self.boss_current_health
        self.player_previous_coordinates = self.player_coordinates
        self.boss_previous_coordinates = self.boss_coordinates
        self.player_previous_animation = self.player_animation
        self.boss_previous_animation = self.boss_animation

    def perform_action(self, action) -> None:
        er_helper.press_combos(self.key_action_space[action])

    def screenshot(self) -> None:
        # screenshot, convert to correct color space
        # DXCam boasts high screen capture speed, but will throw
        # an error if the frame does not change since last screenshot
        try:
            m = np.array(self.__camera.grab(region = self.__region))
            m = cv2.cvtColor(m, cv2.COLOR_BGRA2RGB)
            self.__screenshot = m
        except:
            return

    def update(self) -> None:
        # update previous and current values
        # needed for reward and database
        self.player_previous_health = self.player_current_health
        self.player_previous_stamina = self.player_current_stamina
        self.player_previous_fp = self.player_current_fp
        self.boss_previous_health = self.boss_current_health
        self.player_previous_coordinates = self.player_coordinates
        self.boss_previous_coordinates = self.boss_coordinates
        self.player_previous_animation = self.player_animation
        self.boss_previous_animation = self.boss_animation

        self.player_current_health = self.__game.get_player_health()
        self.player_current_stamina = self.__game.get_player_stamina()
        self.player_current_fp = self.__game.get_player_fp()
        self.boss_current_health = self.__game.get_enemy_health()
        self.player_coordinates = self.__game.get_player_coords()
        self.player_animation = self.__game.get_player_animation()
        self.boss_coordinates = self.__game.get_enemy_coords()
        self.boss_animation = self.__game.get_enemy_animation()

        if self.__database_writing:
            if self.player_animation != self.player_previous_animation:
                database_helper.write_to_database_animations(self.con, {"Animation_ID": self.player_animation, "Run_Number": self.games, "Boss_ID": 0})

            for i in range(0, len(self.boss_animation)):
                if self.boss_animation[i] != self.boss_previous_animation[i]:
                    database_helper.write_to_database_animations(self.con, {"Animation_ID": self.boss_animation[i], "Run_Number": self.games, "Boss_ID": self.enemy_id[i]})

    def state(self):
        return self.__screenshot

    def simple_reward(self) -> None:
        self.reward = -1

        for i in range(0, len(self.__game.enemies)):
        # reward for dealing damage
            if self.boss_current_health[i] < self.boss_previous_health[i]:
                self.deal_damage_timer = time.time()
                self.reward += (1 + ((self.boss_previous_health[i] - self.boss_current_health[i]) / self.boss_max_health[i]))

        # punish for taking damage
        if self.player_current_health < self.player_previous_health:
            self.take_damage_timer = time.time()
            self.reward -= (1 + ((self.player_previous_health - self.player_current_health) / self.player_max_health))

        if time.time() - self.deal_damage_timer > (15 / self.speed):
            self.reward -= (1 + (time.time() - self.deal_damage_timer - (15 / self.speed)) / 10)

    def complex_reward(self) -> None:
        self.simple_reward()

        # punish for low stamina
        if self.player_current_stamina < self.player_max_stamina * 0.25:
            self.reward -= (1 + ((self.player_max_stamina * 0.25 - self.player_current_stamina) / self.player_max_stamina))

        if self.player_current_health > self.player_previous_health:
            # reward for healing
            self.reward += (1 + ((self.player_current_health - self.player_previous_health) / self.player_max_health))

            # punish if healing way too early, lvl 1 flask heals 250, so if missing ou
            # on more than 75 potential hp, punish
            # 175 is an arbitrary number in this case
            if self.player_current_health - self.player_previous_health < 175:
                self.reward -= (1 + (250 - (self.player_current_health - self.player_previous_health)) / 175)

        # reward if avoiding damage for more than 15 seconds
        if time.time() - self.take_damage_timer > (15 / self.speed):
            self.reward += (1 + (time.time() - self.take_damage_timer) / (15 / self.speed))

    def done(self) -> bool:
        if self.__game.get_player_dead():
            self.reward -= 10
            return True

        for i in self.__game.get_enemy_dead():
            if not i:
                return False

        self.reward += 10

        return True

    def step(self, action):
        # arbitrary delay to ensure that only 7 or so actions are performed per second
        time.sleep(0.12 / self.speed)
        # while in cut scene, wait, clean enemies, find enemies, need to update for phase 2 bosses
        load = False

        while self.__game.loading_state():
            load = True
            er_helper.key_press('esc', 0.2)
            time.sleep(0.01)

        if load:
            # this will check for the phase 2 enemy
            self.__game.clean()
            self.__game.find_enemies(self.enemy_id.copy())
            print(self.__game.get_enemy_id())
            er_helper.clean_keys()
            er_helper.key_press('q', .1)

        #self.perform_action(action)
        self.update()
        self.screenshot()
        self.reward_function()
        done = self.done()
        truncated = False

        if self.time_step_total % self.n_steps == 0 and self.time_step_total > 1:
            truncated = True
            self.__game.kill_player()
            er_helper.clean_keys()

        if self.__database_writing and self.time_step_run % 4 == 0:
            for i in range(0, len(self.enemy_id)):
                step_info = {
                    "Run_Number": self.games,
                    "Timestep": self.time_step_run,
                    "Boss_ID": self.enemy_id[i],
                    "pX": self.player_coordinates[0],
                    "pY": self.player_coordinates[1],
                    "pZ": self.player_coordinates[2],
                    "pHealth": self.player_current_health,
                    "pAnimation": self.player_animation,
                    "pAction": action,
                    "pReward": self.reward,
                    "bX": self.boss_coordinates[i][0],
                    "bY": self.boss_coordinates[i][1],
                    "bZ": self.boss_coordinates[i][2],
                    "bHealth": self.boss_current_health[i],
                    "bAnimation": self.boss_animation[i]
                }

                database_helper.write_to_database_step_boss(self.con, step_info)
            database_helper.write_to_database_step_player(self.con, step_info)

        if done or truncated:
            er_helper.clean_keys()
            self.end_time = time.time()

            if self.__database_writing:
                for i in range(0, len(self.enemy_id)):
                    run_info = {
                        "Run_Number": self.games,
                        "Boss_ID": self.enemy_id[i],
                        "Boss_Ending_Health": self.boss_current_health[i],
                        "Player_Ending_Health": self.player_current_health,
                        "Total_Time": self.end_time - self.begin_time,
                        "Victory": (self.player_current_health > 0)
                    }

                    database_helper.write_to_database_run(self.con, run_info)
                self.con.commit()
                self.con.close()

            # wait for player to start animation
            time.sleep(4)
            # player dying animations
            # if the player is dying still

            if self.__game.stake_of_marika():
                time.sleep(2)
                er_helper.key_press('right', 0.1)
                er_helper.key_press('e', 0.1)

            while self.__game.get_player_animation() in [17002, 18002]:
                time.sleep(.2)

            time.sleep(2)

            # if player is in loading screen
            while self.__game.loading_state():
                time.sleep(0.2)

        self.time_step_run += 1
        self.time_step_total += 1

        return self.state(), self.reward, done, truncated, {}

    def close(self) -> None:
        pass

if __name__ == "__main__":
    #er = EldenRing(database_writing=True)

    #con = sqlite3.connect("elden_ring.db")
    #cur = con.cursor()
    #cur.execute("SELECT * FROM Detailed_Run_Info_Player;")
    #print(cur.fetchone())
    #con.close()

    er = EldenRing(database_writing=False)
    er.reset(seed = 0)

    while True:
        er.step(0)