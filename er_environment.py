from scripts.game_accessor import GameAccessor
from scripts import er_helper
from scripts import walk_back
import dxcam
import time
import numpy as np
import torch
from PIL import Image

# TODO: Make like Mario Environment
# TODO: Simple and Complex Action_space
# TODO: Change DXCam to Something else, DXCam blows
# TODO: Check Walk_back functions
# TODO: Check time to press keys, maybe implement the key cleaning like in Mario
# TODO: Get moving on Streamlit or whatever
# TODO: Turn the scripts folder into a class or something with a BETTER __init__ file
# TODO: Fix Agent File
# TODO: Begin creating logs formats
# TODO: Remove most ground-truth elements, full image based CNN
    # TODO: Create ground-truth version for training for a different PPO?
# TODO: Create more animation stuff, save in csv format or something instead of json
    # TODO: Create sqlite database to store information for data collection, csv for simple collection
    # TODO: Check arena images, map to coordinates, live drawing functions for data viewing and analysis
# TODO: Check out PyQT6 or PySide6 for making the GUI instead of Streamlit

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

class EldenRing:
    def __init__(self):
        self.__game = GameAccessor()
        self.__camera = dxcam.create()
        left, top, right, bottom = er_helper.client_window_size()
        # Thi small offset is for a 4k monitor, might be different for others
        self.__region = (7 + left, 44 + top, 7 + right, 44 + bottom)
        self.reset()

    def reset(self) -> None:
        # player
        while not self.__game.is_ready():
            time.sleep(0.01)
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
        self.fill_screenshots()
        self.__game.check()
        time.sleep(.3)
        
        self.begin_time = time.time()
        self.updates()

    def full_reset(self) -> None:
        # rejoin the thread
        print("updater thread stopped")
        time.sleep(15)
        self.__game.begin_reset()
        self.reset()

    def perform_action(self, action) -> None:
        # check key bindings in game, perform action based on 1 hot encoded array
        index = np.nonzero(action)[0]
        index = index[0]
        #print(action_space[index])
        if index in [15, 16]:
            self.__game.check()
        if index in [4, 5, 6, 7, 10, 11, 12, 13, 14]:
            # combo press
            er_helper.key_combos(action_space[index])
        else:
            er_helper.key_presses(action_space[index])

    def updates(self) -> None:
        self.player.update()

        ptrs, enemies = self.__game.get_enemies()
        for i, j in zip(ptrs, enemies):
            if i not in self.enemies:
                self.enemies[i] = Enemy(j, self.player)

        for i in self.enemies:
            self.enemies[i].update(self.player)

        self.screenshot() #/////////////////////////////////////

    def fill_screenshots(self) -> None:
        # removed the for loop since dxcam returns none if the frame does not change
        m = np.array(self.__camera.grab(region = self.__region))
        im = Image.fromarray(m)
        im = im.reduce(8)
        im = np.array(im)
        self.frame_stack.append(im)
        self.frame_stack.append(im)
        self.frame_stack.append(im)

    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        if self.screenshot_check:
            try:
                m = np.array(self.__camera.grab(region = self.__region))
                im = Image.fromarray(m)
                self.frame_stack.append(np.array(im.reduce(8)))
                if len(self.frame_stack) > 3:
                    self.frame_stack.pop(0)
            except:
                return
        self.screenshot_check = not self.screenshot_check

    def get_state(self):
        player_tensor = torch.tensor(self.player.state())

        tensor_list = []
        for i in self.enemies:
            tensor_list.append(torch.tensor(self.enemies[i].state()))

        enemy_tensor = torch.cat(tensor_list, dim = 0)
        enemy_tensor = enemy_tensor
        frame_tensor = torch.tensor(self.frame_stack, dtype=torch.float32) #////////////////////////////
        frame_tensor = frame_tensor.mean(dim=3)                                           #/////////////////////////////

        # Combine tensors and return
        combined_tensor = torch.cat([player_tensor.flatten(), enemy_tensor.flatten(), frame_tensor.flatten()], dim=0)# //////////////////
        #combined_tensor = torch.cat([player_tensor.flatten(), enemy_tensor.flatten()], dim=0)
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
            else:
                self.enemies[i].dead()
        #print("Player Dead: {}, Enemy dead: {}".format(pd, bd))
        return (pd or bd)

    def step(self, action):
        start = time.time()
        # use other functions, check if reset needs to be called
        self.perform_action(action)
        self.updates()
        self.rewards()
        new_state = self.get_state()
        done = self.done()
        print(f"PLAYER HEALTH: {self.player.health}")
        print(f"PLAYER DEAD: {self.player.is_dead}")

        if done:
            if self.player.is_dead:
                self.reward -= 3
            else:
                self.reward += 3

        print("FPS: {}".format(1/(time.time()-start)))
        return new_state, self.reward, done

if __name__ == "__main__":
    ...