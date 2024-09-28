from game_access import GameAccessor
import er_helper
from enemies import Enemy
from player import Player
import walk_back
import dxcam

class EldenRing:
    def __init__(self):
        self.__game = GameAccessor()
        self.reset()

    def reset(self) -> None:
        # game access
        self.__game.reset()

        # player
            # player health
            # player health prev
            # player max health
            # player stamina
            # player stamina prev
            # player max stamina
            # player mana
            # player mana prev
            # player max mana
            # player animation
            # player coords
        # list of enemies
            # boss health
            # boss health prev
            # boss max health
            # boss animation
            # enemy coords
        # reward
        # frame queue
        # screenshot bool
        # player dead
        # boss (or bosses) dead
        # walk_back function

    def action(self, arr: list) -> None:
        # check key bindings in game, perform action based on 1 hot encoded array
        ...
    def screenshot(self) -> None:
        # screenshot, append to list, pop front if needed, check if other frame
        ...
    def get_state(self) -> dict:
        # dictionary of all states
        ...
    def rewards(self) -> None:
        # calculate reward
        ...
    def step(self, action) -> None:
        # use other functions, check if reset needs to be called
        ...

if __name__ == "__main__":
    ...