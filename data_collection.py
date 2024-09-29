from scripts.player import Player
from scripts.enemies import Enemy
from scripts.game_access import GameAccessor
from scripts import walk_back
from scripts import er_helper
import time
import json
import threading
import os

def json_write(_animation_number, _min_time_to_finish, _max_time_to_finish, _file_location):
    """
    Writes json files that contain animation information that can be used by the AI

    Args:
        _animation_number: int that represents the animation that played
        _min_time_to_finish: float that is the fastest the animation was completed
        _max_time_to_finish: float that is the slowest the animation was completed
        _file_location: location to save the file

    Returns:
        None
    """
    data = {
        "animation_number": _animation_number,
        "min_time_to_finish": _min_time_to_finish,
        "max_time_to_finish": _max_time_to_finish,
        "animation_name": ''
    }

    with open("{}/{}.json".format(_file_location, _animation_number), 'w') as file:
        json.dump(data, file, indent=4)

def directory_creator(_file_dir):
    """
    Creates directories if they do not exist

    Args:
        _file_dir: path to directory to make

    Returns:
        None
    """
    if not os.path.isdir(_file_dir):
        os.mkdir(_file_dir)

def player_listen(player : Player):
    """
    Listens for the player to perform an animation while their FP is greater than 20
    then records the information from the animation into a json file

    Args:
        player: The player object to be observed

    Returns:
        None
    """
    time.sleep(5)
    old_animation_number = -1
    animation_number = -1
    animation_location = "animation_files/000000"
    directory_creator(animation_location)
    while player.get_fp() >= 20:
        start_time = time.time()

        while old_animation_number == animation_number:
            animation_number = player.get_animation()

        end_time = time.time()
        old_animation_number = animation_number 
        if not os.path.isfile(animation_location + "/{}.json".format(animation_number)):
            print("Unknown Animation")
            json_write(old_animation_number, end_time - start_time, 0,  animation_location)

        with open(animation_location + "/{}.json".format(animation_number), 'r') as file:
            data = json.load(file)
        with open(animation_location + "/{}.json".format(animation_number), 'w+') as file:
            timer = end_time - start_time
            if timer < data['min_time_to_finish']:
                data['min_time_to_finish'] = timer
            if timer > data['max_time_to_finish']:
                data['max_time_to_finish'] = timer
            json.dump(data, file, indent=4)

def enemy_listen(enemy):
    """
    Listens for the enemy to perform an animation while their HP is greater than 0
    then records the information from the animation into a json file

    Args:
        enemy: The enemy object to be observed

    Returns:
        None
    """
    time.sleep(5)
    old_animation_number = -1
    animation_number = -1
    animation_location = "animation_files/{}".format(enemy.get_id())
    directory_creator(animation_location)
    while enemy.get_health() > 0:
        start_time = time.time()

        while old_animation_number == animation_number:
            animation_number = enemy.get_animation()

        end_time = time.time()
        old_animation_number = animation_number 
        if not os.path.isfile(animation_location + "/{}.json".format(animation_number)):
            print("Unknown Animation")
            json_write(old_animation_number, end_time - start_time, 0,  animation_location)

        with open(animation_location + "/{}.json".format(animation_number), 'r') as file:
            data = json.load(file)
        with open(animation_location + "/{}.json".format(animation_number), 'w+') as file:
            timer = end_time - start_time
            if timer < data['min_time_to_finish']:
                data['min_time_to_finish'] = timer
            if timer > data['max_time_to_finish']:
                data['max_time_to_finish'] = timer
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    game = GameAccessor()
    time.sleep(5)
    #walk_back.soldier_of_godrick()
    time.sleep(.4)

    game.check()

    while len(game.get_enemies()) < 1:
        e = game.get_enemies()
        print("Checking for enemies")
        time.sleep(.3)
        game.check()
        time.sleep(.2)

    e = game.get_enemies()

    print(e[0].get_id())
    #player_listen(game.get_player())
    enemy_listen(e[0])
    print("Complete")
    game.off()