import win32gui
import time
import pydirectinput

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
        key_press(']', 0.12)
        key_press(']', 0.12)
    else:
        "Window Not Found"

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
        time.sleep(.12)
        pydirectinput.keyUp(i, _pause=False)
        time.sleep(.12)

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
    time.sleep(.12)
    for i in keys:
        pydirectinput.keyUp(i, _pause=False)
    time.sleep(.12)

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
    time.sleep(.12)

def enter_boss() -> None:
    """
    General function used to enter the fog wall

    Args:
        None

    Returns:
        None
    """
    key_press('w', 1)
    key_press('e', 0.3)
    time.sleep(2.5)
    key_press('w', .5)
    key_press('q', 0.2)