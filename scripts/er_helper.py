import win32gui
import time
import pydirectinput
import numpy as np
import os
import json

PREV_ACTION = []

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
    win32gui.MoveWindow(hwnd, 0, 0, 800 + 24, 450 + 64, True)
    return win32gui.GetClientRect(hwnd)

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

def clean_keys() -> None:
    """
    'Lifts' each key that was pressed previously.

    Args:
        None

    Returns:
        None
    """
    try:
        for i in PREV_ACTION:
            pydirectinput.keyUp(i, _pause=False)
        PREV_ACTION.clear()
    except:
        print("Error in clean_keys()")

def press_combos(keys: list) -> None:
    """
    Function used to 'press' down multiple keys at the same time

    Args:
        key: the list of keys to press

    Returns:
        None
    """
    clean_keys()
    for i in keys:
        pydirectinput.keyDown(i, _pause=False)
        PREV_ACTION.append(i)

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

def enter_boss(t: float = 1) -> None:
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