import game_access
import dxcam
import numpy

class EldenRing:
    def __init__(self):
        # game access
        # player health
        # player max health
        # player stamina
        # player max stamina
        # player mana
        # player max mana
        # player animation
        # boss health
        # boss animation
        # reward
        # frame queue
        # screenshot bool
        # player dead
        # boss dead
        ...
    def reset(self) -> None:
        # reset game_access, reset these stats
        ...
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