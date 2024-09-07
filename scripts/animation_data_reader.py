import json
import pymem
import pymem.process
import time
import os
import sys

"""
This file is temporary for accessing data from the game, this will later be merged into a logging script and game_accessor.py, along with others
"""


def read_memory(_process, _address):
    pm = pymem.Pymem(_process)
    memory_value = pm.read_int(_address)
    return memory_value

def json_write(_animation_number, min_time_to_finish, max_time_to_finish, _file_location):
    #file_location  -> player/long_sword
    # or maybe      -> boss_name
    data = {
        "animation_number": _animation_number,
        "min_time_to_finish": min_time_to_finish,
        "max_time_to_finish": max_time_to_finish,
        "animation_name": ''
    }

    with open("{}/{}.json".format(_file_location, _animation_number), 'w') as file:
        json.dump(data, file, indent=4)

def animation_checker():
    process = 'eldenring.exe'
    boss_animation_addr = 0x7FF405C23200 # <- boss animation addr
    boss_health_addr = 0x7FF41F1FA988 # <- boss health addr
    file_location = "animation_files/soldier_of_godrick"
    log_file_location = "logs/soldier_of_godrick-{}.txt".format(time.time())
    unknown_animation_location = "animation_files/soldier_of_godrick/unknown_animations"
    old_animation_number = -1   # Old animation, used to check if animation changes
    animation_number = -1       # current animation that is playing
    while read_memory(process, boss_health_addr) > 0:
        start_time = time.time()

        while old_animation_number == animation_number:
            animation_number = read_memory(process, boss_animation_addr)

        end_time = time.time()
        old_animation_number = animation_number 
        if not os.path.isfile(file_location + "/{}.json".format(animation_number)):
            print("Unknown Animation")
            json_write(old_animation_number, end_time - start_time, 0,  file_location)
            json_write(old_animation_number, end_time - start_time, 0,  unknown_animation_location)

        with open(file_location + "/{}.json".format(animation_number), 'r') as file:
            data = json.load(file)
        with open(file_location + "/{}.json".format(animation_number), 'w+') as file:
            timer = end_time - start_time
            if timer < data['min_time_to_finish']:
                data['min_time_to_finish'] = timer
            if timer > data['max_time_to_finish']:
                data['max_time_to_finish'] = timer
            json.dump(data, file, indent=4)
        print("The Boss used {} which is a {}!".format(animation_number, data['animation_name']))
        with open(log_file_location, 'a') as file:
            file.write("The Boss used animation {} which is {}!\n".format(animation_number, data['animation_name']))

if __name__ == "__main__":
    animation_checker()
