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
    walk_back.godskin_duo()
    time.sleep(1)
    er_helper.key_press('w', 2)
    er_helper.key_press('4', .5)
    er_helper.key_press('w', .12)
    er_helper.key_press('q', .12)
    game.check_for_enemies()
    er_helper.key_press('3', .12)
    # takes a solid 1 or 2 seconds to grab new enemy ID
    game.check_for_enemies()
    enemy = game.get_enemies()
    print(len(enemy))
    if len(enemy) > 1:
        print(enemy[0].get_health())
        print(enemy[1].get_health())