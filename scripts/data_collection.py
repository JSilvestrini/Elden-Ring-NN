from player import Player
from enemies import Enemy
from game_access import GameAccessor
import walk_back
import er_helper
import time

if __name__ == "__main__":
    # below is a test for Godskin Duo as requested by a friend
    game = GameAccessor()
    time.sleep(5)
    e = game.get_enemies()
    print(len(e))
    while len(e) < 1:
        time.sleep(.1)
    en = e[0]
    print(en.get_global_id())
    print(en.get_id())
    game.begin_reset()