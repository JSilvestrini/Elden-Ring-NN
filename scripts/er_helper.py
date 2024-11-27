import win32gui
import time
import pydirectinput
import numpy as np
import os
import json

def find_activate_window() -> None:
    """
    Function used to activate the Elden Ring game window

    Args:
        None

    Returns:
        None
    """
    hwnd = win32gui.FindWindow(None, "ELDEN RING™")
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)
        key_presses(['['] * 12)
        time.sleep(.1)
        key_presses(['['] * 12)
    else:
        "Window Not Found"

def client_window_size() -> list:
    hwnd = win32gui.FindWindow(None, "ELDEN RING™")
    return win32gui.GetClientRect(hwnd)

def get_file_count_and_zero_array(folder_path) -> np.ndarray:
    """
    Counts the number of files in a folder and creates a NumPy array of zeros with that size.

    Args:
        folder_path: The path to the folder.

    Returns:
        A NumPy array that contains 0s
    """

    file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    zero_array = np.zeros(file_count)
    return zero_array

def get_animation_files(folder_path) -> np.ndarray:
    """
    Extracts the numeric parts of file names in a folder and returns them as a NumPy array.

    Args:
        folder_path: The path to the folder.

    Returns:
        A NumPy array containing the numeric parts of the file names.
    """

    file_names = os.listdir(folder_path)
    file_numbers = []
    for file_name in file_names:
        if file_name.endswith('.json'):
            file_number = int(file_name[:-5])  # Remove '.json' and convert to int
            file_numbers.append(file_number)
    return np.array(file_numbers)

def max_time(file_path, animation_number : int) -> float:
    data = 10000.0
    if os.path.isfile(file_path + "/{}.json".format(animation_number)):
        with open(file_path + "/{}.json".format(animation_number), 'r') as file:
            data = json.load(file)
            data = data["max_time_to_finish"]
    return data

def key_presses(keys: list) -> None:
    """
    Function used to 'press' down multiple keys in succession

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
        time.sleep(0.08)
        pydirectinput.keyUp(i, _pause=False)
        time.sleep(0.08)

def key_combos(keys: list) -> None:
    """
    Function used to 'press' down multiple keys at the same time

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
    time.sleep(0.08)
    for i in keys:
        pydirectinput.keyUp(i, _pause=False)
    time.sleep(0.08)

def key_press(key: str, t: float) -> None:
    """
    Function used to 'press' key down for period of time

    Args:
        key: the string of the key that is being pressed
        t: the time in seconds to press the key

    Returns:
        None
    """
    pydirectinput.keyDown(key, _pause=False)
    time.sleep(t)
    pydirectinput.keyUp(key, _pause=False)
    time.sleep(0.08)

def enter_boss(t: float = 0.6) -> None:
    """
    General function used to enter the fog wall

    Args:
        None

    Returns:
        None
    """
    key_press('w', 1)
    key_press('e', 0.08)
    time.sleep(2.5)
    key_press('w', t)
    key_press('q', 0.08)