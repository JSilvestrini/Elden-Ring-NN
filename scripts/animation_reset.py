import json
from json import decoder
import os
import sys

def format_file(filename : str):
    """
    This function creates the proper format of a file
    It is only called if an exception is raised inside of
    change_times(filename)

    Args:
        filename: The file name + path that is to be edited

    Returns:
        None

    Raises:
        ValueError: Raises an exception if the filename is incorrect
    """
    animation_number = filename[filename.rfind('/') + 1:filename.find('.')]
    try:
        animation_number = int(animation_number)
    except ValueError:
        print("The file name is not correct, it should be an integer, not {}".format(animation_number))
    data = {
            "animation_number": animation_number,
            "min_time_to_finish": 1_000_000_000,
            "max_time_to_finish": -1,
            "animation_name": ''
        }

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def change_times(filename : str):
    """
    This function resets the values of the given file
    File is expected to be in json format
    With min_time_to_finish and max_time_to_finish keys

    Args:
        filename: The file name + path that is to be edited

    Returns:
        None

    Raises:
        JSONDecodeError: Raises an exception if the json has no data,
        KeyError: Raises an exception if the json is missing data
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        with open(filename, 'w+') as file:
            if 'animation_number' not in data:
                raise KeyError
            data['min_time_to_finish'] = 1_000_000_000
            data['max_time_to_finish'] = -1
            data['animation_name'] = data['animation_name'] if 'animation_name' in data else ''
            json.dump(data, file, indent=4)
    except KeyError:
        print("KeyError:\nThe file located at {} is not in proper format.\nWas expecting a json with the following format: \n\n'animation_number': int,\n'min_time_to_finish': int,\n'max_time_to_finish': int,\n'animation_name': string\n".format(filename))
        format_file(filename)
    except decoder.JSONDecodeError:
        print("JSONDecodeError:\nThe file located at {} contains no data.\nWas expecting a json with the following format: \n\n'animation_number': int,\n'min_time_to_finish': int,\n'max_time_to_finish': int,\n'animation_name': string\n".format(filename))
        format_file(filename)

if __name__ == "__main__":
    path_arg = sys.argv[1]
    path_slash = path_arg + '/'
    for file in os.listdir(path_arg):
        if os.path.isfile(path_slash + file):
            change_times(path_slash + file)
            if not file.endswith('.json'):
                os.rename(path_slash + file, path_slash + file + '.json')