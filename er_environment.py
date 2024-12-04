from scripts.game_accessor import GameAccessor
from scripts import er_helper
from scripts import database_helper
from scripts import walk_back
import dxcam
import time
import numpy as np
from PIL import Image
import cv2
import gymnasium
import sqlite3

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

walk_backs = { # midra, check both forms [0005, 0006]
    # more will be added, I have these for now
    # since I have screenshots of their arenas
    0: ([0x980A], walk_back.leonine_misbegotten),
    1: ([0xC834], walk_back.dancing_lion),
    2: ([0x9807], walk_back.rellana),
    3: ([0xE016], walk_back.messmer), # does form 2 have different ID?
    4: ([0x9805], walk_back.romina),
    5: ([0x1019], walk_back.morgott),
    6: ([0x0018], walk_back.margit),
    7: ([0x1825], walk_back.godfrey) # does form 2 have different ID?
}

action_spaces = [simple_action_space, mid_action_space, complex_action_space]

class EldenRing(gymnasium.Env):
    def __init__(self, action_space = 1, database_writing = False):
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
        # needed for reset to view speed of PPO
        self.time_step = 0
        self.begin_time = 0
        self.end_time = 0

        if self.__database_writing:
            database_helper.create_database()
            self.games = database_helper.get_run_number() if database_helper.get_run_number() > 0 else 0

        self.__game.reset()

    def reset(self, seed=0, options=0) -> None:
        er_helper.clean_keys()
        self.__game.reset() # Reset when entering new area

        if self.games > 0:
            print(f"Actions per Second: {self.time_step / (self.end_time - self.begin_time)}")

        # wait for player to start animation
        time.sleep(4)

        # player dying animations
        while self.__game.get_player_animation() in [17002, 18002]:
            time.sleep(0.2)

        time.sleep(2)

        while self.__game.loading_state():
            time.sleep(0.2)

        # wait for stand up animation to finish after respawn
        time.sleep(5)

        self.reward = 0
        self.time_step = 0
        self.games += 1

        self.enemy_id, func = walk_backs[0]
        func()

        if self.__database_writing:
            for i in range(0, len(self.enemy_id)):
                database_helper.increase_attempts(self.enemy_id[i])

        while self.__game.loading_state():
            time.sleep(0.2)

        self.__game.reset() # Reset when entering new area, just incase

        time.sleep(1)
        er_helper.enter_boss()

        self.__game.clean()
        while self.__game.enemies == {}:
            time.sleep(0.02)
            self.__game.find_enemies(self.enemy_id.copy())

        self.screenshot()
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

        return self.state(), {}

    def perform_action(self, action) -> None:
        er_helper.press_combos(self.key_action_space[action])

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        try:
            m = np.array(self.__camera.grab(region = self.__region))
            m = cv2.cvtColor(m, cv2.COLOR_BGRA2RGB)
            self.__screenshot = m
            #im = Image.fromarray(m)
            #im.save("screenshot.png")
            #self.__screenshot = np.array(im.resize(((self.__region[2]- self.__region[0]) // 4, (self.__region[3] - self.__region[1]) // 4), Image.Resampling.BILINEAR)) # im.reduce(4)
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
                database_helper.write_to_database_animations({"Animation_ID": self.player_animation, "Run_Number": self.games, "Boss_ID": 0})

            for i in range(0, len(self.boss_animation)):
                if self.boss_animation[i] != self.boss_previous_animation[i]:
                    database_helper.write_to_database_animations({"Animation_ID": self.boss_animation[i], "Run_Number": self.games, "Boss_ID": self.enemy_id[i]})

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

        if time.time() - self.deal_damage_timer > 15:
            self.reward -= (1 + (time.time() - self.deal_damage_timer - 15) / 10)

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
            if self.player_current_health - self.player_previous_health < 175:
                self.reward -= (1 + (250 - (self.player_current_health - self.player_previous_health)) / 250)

        # reward if avoiding damage for more than 15 seconds
        if time.time() - self.take_damage_timer > 15:
            self.reward += (1 + (time.time() - self.take_damage_timer) / 15)

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
        # while in cutscene, wait, clean enemies, find enemies, need to update for phase 2 bosses
        load = False
        while self.__game.loading_state():
            load = True
            time.sleep(0.2)

        if load:
            self.__game.clean_enemies()
            self.__game.find_enemies()

        self.time_step += 1
        self.perform_action(action)
        self.update()
        self.screenshot()
        self.reward_function()
        done = self.done()
        truncated = False

        print(f"Player Health: {self.player_current_health}")
        print(f"Player Dead: {self.__game.get_player_dead()}")
        for i in range(0, len(self.boss_current_health)):
            print(f"Boss {i} Health: {self.boss_current_health[i]}")

        if time.time() - self.begin_time >= 60:
            truncated = True
            self.__game.kill_player()

        '''
        print(f"Reward: {self.reward}")
        print(f"Time Step: {self.time_step}")
        print("PLAYER INFORMATION")
        print(f"Health: {self.player_current_health}")
        print(f"Stamina: {self.player_current_stamina}")
        print(f"FP: {self.player_current_fp}")
        print(f"Animation: {self.player_animation}")
        print("BOSS INFORMATION")
        for i in range(0, len(self.boss_current_health)):
            print(f"Boss {i} Health: {self.boss_current_health[i]}")
        '''

        if self.__database_writing and self.time_step % 4 == 0:
            for i in range(0, len(self.enemy_id)):
                step_info = {
                    "Run_Number": self.games,
                    "Timestep": self.time_step,
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

                database_helper.write_to_database_step_boss(step_info)
            database_helper.write_to_database_step_player(step_info)

        if done or truncated:
            er_helper.clean_keys()
            self.end_time = time.time()
            print(f"Run {self.games} ended in {self.end_time - self.begin_time} seconds")
            print(f"Done: {done}, Truncated: {truncated}")
            #print(f"Enemies: {self.enemy_id}")

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

                    database_helper.write_to_database_run(run_info)

        return self.state(), self.reward, done, truncated, {}

if __name__ == "__main__":
    #er = EldenRing(database_writing=True)

    #con = sqlite3.connect("elden_ring.db")
    #cur = con.cursor()
    #cur.execute("SELECT * FROM Detailed_Run_Info_Player;")
    #print(cur.fetchone())
    #con.close()
    ...