from scripts.game_accessor import GameAccessor
from scripts import er_helper
from scripts import walk_back
import dxcam
import time
import numpy as np
import torch
from PIL import Image
import cv2
import gymnasium

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

action_spaces = [simple_action_space, mid_action_space, complex_action_space]

class EldenRing(gymnasium.Env):
    def __init__(self, action_space = 1):
        self.__game = GameAccessor()
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        # This small offset is for a 4k monitor, might be different for others
        self.__region = (12 + left, 52 + top, 12 + right, 52 + bottom)
        self.obs_type = "rgb"
        self.observation_space = gymnasium.spaces.Box(low=0, high=1, shape=(self.__region[2]- self.__region[0], self.__region[3] - self.__region[1], 3), dtype=np.uint8)
        self.action_space = action_spaces[action_space]
        self.games = 0
        self.reset()

    def reset(self, seed=0, options=0) -> None:
        # kill the player?
        #self.__game.kill_player()
        self.reward = 0
        self.time_step = 0
        self.games += 1
        # walk_back function
        time.sleep(1)
        walk_back.leonine_misbegotten()
        self.__game.find_enemies()
        self.screenshot()
        self.begin_time = time.time()
        # used for rewards
        self.deal_damage_timer = time.time()
        self.take_damage_timer = time.time()
        self.updates()

    def perform_action(self, action) -> None:
        er_helper.press_combos(self.action_space[action])

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        try:
            m = np.array(self.__camera.grab(region = self.__region))
            m = cv2.cvtColor(m, cv2.COLOR_BGRA2RGB)
            im = Image.fromarray(m)
            self.__screenshot = np.array(im) # im.reduce(4)
        except:
            return

    def state(self):
        return self.__screenshot

    def simple_reward(self) -> None:
        # focus on dealing damage and not taking damage
        # negative reward for surviving without doing damage
            # use a timer, if > 10 seconds, negative reward
            # reset timer on hit
        pass

    def complex_reward(self) -> None:
        # simple + incentive for healing, more healed more reward
            # check max healing for level 0 flask
        # incentive for maintaining at least 25% stamina
        # add on incentive for not getting hit for a while
        pass

    def survival_reward(self) -> None:
        # focus on surviving as long as possible
        # incentive for no damage, healing
            # use timer like simple, but for time not hit
            # every 15 seconds, increase reward even more
                # 0-14, 15-29, 29-44 ...
                # +0.5, +1.0, +1.5 ...
        pass

    def done(self) -> bool:
        # check if player dead or all enemy dead
        pass

    def step(self, action):
        self.time_step += 1
        start = time.time()
        self.perform_action(action)
        self.screenshot()
        reward = self.rewards()
        # check for done, player dead, bosses dead
        # check for truncated
        #return self.state(), reward, done, truncated, {}

if __name__ == "__main__":
    er = EldenRing()