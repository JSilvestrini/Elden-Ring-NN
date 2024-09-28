from scripts.game_access import GameAccessor
from scripts import er_helper
from scripts.enemies import Enemy
from scripts.player import Player
from scripts import walk_back
import dxcam
import time
import numpy as np
import torch

# TODO: Make game access save previous enemy pointers to ensure old pointer is replaced

action_space = {
    0: ['w'],
    1: ['a'],
    2: ['s'],
    3: ['d'],
    4: ['w', 'space'],
    5: ['a', 'space'],
    6: ['s', 'space'],
    7: ['d', 'space'],
    8: ['space'],
    9: ['f'],
    10: ['w', 'f'],
    11: ['a', 'f'],
    12: ['s', 'f'],
    13: ['d', 'f'],
    14: ['x'],
    15: ['3'],
    16: ['4'],
    17: ['up'],
    18: ['left'],
    19: ['right'],
    20: ['down'],
    21: ['m'],
    22: ['l'],
    23: ['k'],
    24: ['n'],
    25: ['r'],
}

class EldenRing:
    def __init__(self):
        self.__game = GameAccessor()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
            self.player_animation_list = er_helper.get_animation_files("animation_files/000000")
            self.player_animation_list_zero = np.zeros_like(self.player_animation_list)
            self.player_animation_timer = time.time()
            self.player_previous_animation = self.player_animation
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
        self.boss_animation_list = []
        self.boss_animation_list_zero = []
        self.boss_animation_timers = []
        self.boss_previous_animation = []
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
        time.sleep(10)
        walk_back.soldier_of_godrick()
        self.__game.check()
        self.enemies = self.__game.get_enemies()
        self.begin_time = time.time()

    def full_reset(self) -> None:
        self.__game.begin_reset()
        self.reset()

    def perform_action(self, action) -> None:
        # check key bindings in game, perform action based on 1 hot encoded array
        index = np.nonzero(action)[0]
        index = index[0]
        print(action_space[index])
        if index in [15, 16]:
            self.__game.check()
        er_helper.key_press(action_space[index])

    def encode_player_animation(self):
        index = np.where(self.player_animation_list, self.player_animation)
        self.player_animation_list_zero = np.zeros_like(self.player_animation_list)
        self.player_animation_list_zero[index] = 1

    def encode_enemy_animation(self):
        for i in range(len(0, self.enemies)):
            index = np.where(self.boss_animation_list[i], self.boss_animation[i])
            self.boss_animation_list_zero[i] = np.zeros_like(self.boss_animation_list[i])
            self.boss_animation_list_zero[i][index] = 1

    def updates(self) -> None:
        self.player_health_prev = self.player_health
        self.player_stamina_prev = self.player_stamina
        self.player_prev_fp = self.player_fp
        self.player_coords_prev = self.player_coords
        self.player_previous_animation = self.player_animation
        self.player_health = self.__player.get_health()
        self.player_stamina = self.__player.get_stamina()
        self.player_fp = self.__player.get_fp()
        self.player_coords = np.array(self.__player.get_coords())
        self.player_animation = self.__player.get_animation()
        if self.player_animation != self.player_previous_animation:
            self.player_animation_timer = time.time()
        self.encode_player_animation()
        self.player_dead = self.player_health <= 0

        self.enemies = self.__game.get_enemies()

        self.boss_health_prev = self.boss_health
        self.boss_coords_prev = self.boss_coords
        self.boss_previous_animation = self.boss_animation

        for i in range(0, len(self.enemies)):
            self.boss_health[i] = self.enemies[i].get_health()
            self.boss_max_health[i] = self.enemies[i].get_max_health()
            self.boss_coords[i] = np.array(self.enemies[i].get_coords())
            self.boss_animation[i] = self.enemies[i].get_animation()
            self.boss_dead[i] = self.boss_health[i] <= 0
            self.boss_animation_list[i] = er_helper.get_animation_files("animation_files/{}".format(self.enemies[i].get_id()))
            self.boss_animation_list_zero[i] = np.zeros_like(self.boss_animation_list)
            if self.boss_animation[i] != self.boss_previous_animation[i]:
                self.boss_animation_timers[i] = time.time()
        self.encode_enemy_animation()
        self.distance_from_player = np.linalg.norm(self.boss_coords - self.player_coords, axis=1)
        self.direction_from_player = np.arctan2(self.boss_coords[:, 1] - self.player_coords[1], self.boss_coords[:, 0] - self.player_coords[0]) * 180 / np.pi

        self.screenshot()

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        if self.screenshot_check:
            self.frame_stack.append(np.array(self.__camera.grab(region = self.__region)))
            if len(self.frame_stack) > 5:
                self.frame_stack.pop(0)
        self.screenshot_check = not self.screenshot_check

    def get_state(self):
        player_health = self.player_health / self.player_max_health
        player_stamina = self.player_stamina / self.player_max_stamina
        player_fp = self.player_fp / self.player_max_fp
        player_animation = self.player_animation_list_zero
        player_delta_health = (self.player_health_prev - self.player_health) / self.player_max_health
        player_delta_stamina = (self.player_stamina_prev - self.player_stamina) / self.player_max_stamina
        player_delta_fp = (self.player_prev_fp - self.player_fp) / self.player_max_fp
        animation_completion = (self.player_animation_timer - time.time()) / er_helper.max_time("animation_files/000000", self.player_animation)
        player_tensor = torch.tensor([player_health, player_delta_health, player_stamina, player_delta_stamina, 
                                      player_fp, player_delta_fp, player_animation, animation_completion], dtype=torch.float32).to(self.device)

        enemy_health = np.array(self.boss_health) / np.array(self.boss_max_health)
        enemy_delta_health = (np.array(self.boss_health_prev) - np.array(self.boss_health)) / np.array(self.boss_max_health)
        enemy_animation = self.boss_animation_list_zero
        enemy_distance = self.distance_from_player
        enemy_direction = self.direction_from_player
        enemy_animation_completion = []
        for i in range(len(self.enemies)):
            enemy_animation_completion[i] = (self.boss_animation_timers[i] - time.time()) / er_helper.max_time("animation_files/{}".format(self.enemies[i].get_id()), self.boss_animation[i])
        boss_array = np.column_stack(enemy_health, enemy_delta_health, enemy_distance, enemy_direction, enemy_animation, enemy_animation_completion)
        enemy_tensor = torch.tensor(boss_array, dtype=torch.float32).to(self.device)
        frame_tensor = torch.tensor(self.frame_stack, dtype=torch.float32).to(self.device)

        # Combine tensors and return
        combined_tensor = torch.cat([player_tensor.flatten(), enemy_tensor.flatten(), frame_tensor.flatten()], dim=0)
        return combined_tensor

    def rewards(self) -> None:
        self.reward = 0
        if len(self.enemies) > 0:
            for i in range(0, len(self.enemies)):
                self.reward += ((self.boss_health_prev[i] - self.boss_health[i]) + 1) / self.boss_max_health[i]
        self.reward -= ((self.player_health_prev - self.player_health) + (self.player_max_health * 0.1)) / self.player_max_health
        if self.player_stamina < (0.15 * self.player_max_stamina):
            self.reward -= self.player_stamina / self.player_max_stamina
        self.reward /= (time.time() - self.begin_time() / 5)

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
        self.rewards()
        new_state = self.get_state()
        done = self.done()
        return new_state, self.reward, done

if __name__ == "__main__":
    #er = EldenRing()
    ...