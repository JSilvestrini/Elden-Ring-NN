from scripts.game_access import GameAccessor
from scripts import er_helper
from scripts.enemies import Enemy
from scripts.player import Player
from scripts import walk_back
import dxcam
import time
import numpy as np

# TODO: Make game access save previous enemy pointers to ensure old pointer is replaced

action_space = {
    0: ['w'],
    1: ['a'],
    2: ['s'],
    3: ['d'],
    4: ['space'],
    5: ['f'],
    6: ['x'],
    7: ['q'],
    8: ['3'],
    9: ['4'],
    10: ['up'],
    11: ['left'],
    12: ['right'],
    13: ['down'],
    14: ['m'],
    15: ['l'],
    16: ['k'],
    17: ['n'],
    18: ['r'],
}

class EldenRing:
    def __init__(self):
        self.__game = GameAccessor()
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        self.__region = (left, top, right, bottom)
        print(self.__region)
        self.reset()

    def reset(self) -> None:
        # player
        if self.__game.is_ready():
            self.__player = self.__game.get_player()
            self.player_health = self.__player.get_health()
            self.player_max_health = self.__player.get_max_health()
            self.player_health_prev = self.player_health
            self.player_stamina = self.__player.get_stamina()
            self.player_max_stamina = self.__player.get_max_stamina()
            self.player_stamina_prev = self.player_stamina
            self.player_fp = self.__player.get_fp()
            self.player_max_fp = self.__player.get_max_fp()
            self.player_prev_fp = self.player_fp
            self.player_coords = np.array(self.__player.get_coords())
            self.player_coords_prev = self.player_coords
            self.player_animation = self.__player.get_animation()
        # list of enemies
        self.enemies = []
        self.boss_health = []
        self.boss_max_health = []
        self.boss_health_prev = []
        self.boss_coords = []
        self.boss_coords_prev = []
        self.distance_from_player = []
        self.direction_from_player = []
        self.boss_animation = []
        # reward
        self.reward = 0
        # frame queue
        self.frame_stack = []
        # screenshot bool
        self.screenshot_check = True
        # player dead
        self.player_dead = False
        # boss (or bosses) dead
        self.boss_dead = []
        # walk_back function
        ...

    def full_reset(self) -> None:
        self.__game.begin_reset()
        self.reset()

    def perform_action(self, action) -> None:
        # check key bindings in game, perform action based on 1 hot encoded array
        index = np.nonzero(action)[0]
        index = index[0]
        print(action_space[index])
        er_helper.key_press(action_space[index])

    def updates(self) -> None:
        self.__game.check()
        self.player_health_prev = self.player_health
        self.player_stamina_prev = self.player_stamina
        self.player_prev_fp = self.player_fp
        self.player_coords_prev = self.player_coords
        self.player_health = self.__player.get_health()
        self.player_stamina = self.__player.get_stamina()
        self.player_fp = self.__player.get_fp()
        self.player_coords = np.array(self.__player.get_coords())
        self.player_animation = self.__player.get_animation()
        self.player_dead = self.player_health <= 0

        self.enemies = self.__game.get_enemies()

        self.boss_health_prev = self.boss_health
        self.boss_coords_prev = self.boss_coords

        for i in range(0, len(self.enemies)):
            self.boss_health[i] = self.enemies[i].get_health()
            self.boss_max_health[i] = self.enemies[i].get_max_health()
            self.boss_coords[i] = np.array(self.enemies[i].get_coords())
            self.boss_animation[i] = self.enemies[i].get_animation()
            self.boss_dead[i] = self.boss_health[i] <= 0
        self.distance_from_player = np.linalg.norm(self.boss_coords - self.player_coords, axis=1)
        self.direction_from_player = np.arctan2(self.boss_coords[:, 1] - self.player_coords[1], self.boss_coords[:, 0] - self.player_coords[0]) * 180 / np.pi

        self.screenshot()

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        if self.screenshot_check:
            self.frame_stack.append(self.__camera.grab(region = self.__region))
            if len(self.frame_stack) > 5:
                self.frame_stack.pop(0)
        self.screenshot_check = not self.screenshot_check

    def get_state(self) -> dict:
        # dictionary of all states
        ...
    def rewards(self) -> None:
        # calculate reward
        ...

    def done(self) -> bool:
        pd = self.player_dead
        bd = True
        for i in self.boss_dead:
            if not i:
                bd = False
                break
        return (pd or bd)

    def step(self, action):
        # use other functions, check if reset needs to be called
        self.perform_action(action)
        self.updates()
        self.reward = self.rewards()
        new_state = self.get_state()
        done = self.done()
        return new_state, self.reward, done

if __name__ == "__main__":
    er = EldenRing()