from scripts.game_access import GameAccessor
from scripts import er_helper
from scripts.enemies import EnemyAccess, Enemy
from scripts.player import PlayerAccess, Player
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
    14: ['w', 'f', 'l'],
    15: ['x'],
    16: ['3'],
    17: ['4'],
    18: ['down'],
    19: ['m'],
    20: ['l'],
    21: ['k'],
    22: ['n'],
    23: ['r'],
}

# TODO: Boss as dictionary, each entry is ptr: boss()
# TODO: Each boss() will keep track of its own stuff through update()
# TODO: get_enemies needs to return ptr_list, enemy_list
# TODO: check if ptr is key in dictionary, if not add ptr[i]: enemy(enemy[i])
# TODO: Make frames 4x smaller each
class EldenRing:
    def __init__(self):
        self.__game = GameAccessor()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # might be redundant later
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        self.__region = (left, top, right, bottom)
        self.reset()

    def reset(self) -> None:
        # player
        if self.__game.is_ready():
            self.__player_access = self.__game.get_player()
            self.player = Player(self.__player_access)
        # list of enemies
        self.enemies = {}
        # reward
        self.reward = 0
        # frame queue
        self.frame_stack = []
        # screenshot bool
        self.screenshot_check = True
        # walk_back function
        time.sleep(1)
        walk_back.leonine_misbegotten()
        #self.fill_screenshots()
        self.__game.check()
        time.sleep(.23)
        ptrs, enemies = self.__game.get_enemies()
        for i, j in zip(ptrs, enemies):
            self.enemies[i] = Enemy(j, self.player)
        self.begin_time = time.time()

    def full_reset(self) -> None:
        time.sleep(20)
        self.__game.begin_reset()
        self.reset()

    def perform_action(self, action) -> None:
        # check key bindings in game, perform action based on 1 hot encoded array
        index = np.nonzero(action)[0]
        index = index[0]
        #print(action_space[index])
        if index in [15, 16]:
            self.__game.check()
        er_helper.key_presses(action_space[index])

    def updates(self) -> None:
        self.player.update()

        ptrs, enemies = self.__game.get_enemies()
        for i, j in zip(ptrs, enemies):
            if i not in self.enemies:
                self.enemies[i] = Enemy(j)

        for i in self.enemies:
            self.enemies[i].update(self.player)

        #self.screenshot()

    def fill_screenshots(self) -> None:
        for i in range(0, 3):
            self.frame_stack.append(np.array(self.__camera.grab(region = self.__region)))

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        if self.screenshot_check:
            self.frame_stack.append(np.array(self.__camera.grab(region = self.__region)))
            if len(self.frame_stack) > 3:
                self.frame_stack.pop(0)
        self.screenshot_check = not self.screenshot_check

    def get_state(self):
        player_tensor = torch.tensor(self.player.state()).to(self.device)

        tensor_list = []
        for i in self.enemies:
            tensor_list.append(torch.tensor(self.enemies[i].state()).to(self.device))

        enemy_tensor = torch.cat(tensor_list, dim = 0)
        enemy_tensor = enemy_tensor.to(self.device)
        #frame_tensor = torch.tensor(self.frame_stack, dtype=torch.float32).to(self.device)

        # Combine tensors and return
        #combined_tensor = torch.cat([player_tensor.flatten(), enemy_tensor.flatten(), frame_tensor.flatten()], dim=0).to(self.device)
        combined_tensor = torch.cat([player_tensor.flatten(), enemy_tensor.flatten()], dim=0)
        return combined_tensor

    def rewards(self) -> None:
        self.reward = 0
        if len(self.enemies) > 0:
            for i in self.enemies:
                self.reward += ((self.enemies[i].health_prev - self.enemies[i].health) + 1) / self.enemies[i].max_health
        self.reward -= ((self.player.health_prev - self.player.health) + (self.player.max_health * 0.1)) / self.player.max_health
        if self.player.stamina < (0.15 * self.player.max_stamina):
            self.reward -= self.player.stamina / self.player.max_stamina
        self.reward /= (time.time() - self.begin_time / 5)

    def done(self) -> bool:
        pd = self.player.is_dead
        bd = True
        for i in self.enemies:
            if not self.enemies[i].is_dead:
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

        if done:
            if self.player.is_dead:
                self.reward -= 3
            else:
                self.reward += 3

        return new_state, self.reward, done

if __name__ == "__main__":
    ...