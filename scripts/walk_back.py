from er_helper import key_press, key_presses, find_activate_window, enter_boss
import time

def talk_to_gideon(slots: list) -> None:
    find_activate_window()
    time.sleep(.2)
    key_press('e', 0.2)
    for i in slots:
        key_presses(['down'] * i)
        key_press('e', 0.2)
    time.sleep(8)

"""
Below is a list of different walk backs that I have implemented using the Elden Ring Arena Mod.
    - Soldier of Godrick
    - Leonine Misbegotten
    - Crucible Knight Ordovis
    - Pumpkin Head
    - Burial Watchdog
    - Beastman of Farum Azula
    - Elemer of the Briar
    - Rellana
    - Dancing Lion
    - Romina
    - Ancient Dragon Man
    - Grafted Scion
    - Godskin Duo
    - ... More bosses in the future once Cutscenes are worked out
"""
def soldier_of_godrick() -> None:
    talk_to_gideon([3, 3, 0])
    enter_boss()

def leonine_misbegotten() -> None:
    talk_to_gideon([2, 0])
    enter_boss()

def misbegotten_crusader() -> None:
    talk_to_gideon([3, 3, 21])
    enter_boss()

def crucible_knight() -> None:
    talk_to_gideon([3, 2, 20])
    enter_boss()

def pumpkin_head() -> None:
    talk_to_gideon([3, 4, 0])
    enter_boss()

def burial_watchdog() -> None:
    talk_to_gideon([3, 2, 1])
    enter_boss()

def beastman() -> None:
    talk_to_gideon([3, 3, 1])
    enter_boss()

def elemer() -> None:
    talk_to_gideon([2, 8])
    enter_boss()

def rellana() -> None:
    talk_to_gideon([4, 1])
    enter_boss()

def dancing_lion() -> None:
    talk_to_gideon([4, 0])
    enter_boss()

def romina() -> None:
    talk_to_gideon([4, 8])
    enter_boss()

def ancient_dragon_man() -> None:
    talk_to_gideon([5, 6])
    enter_boss()

def grafted_scion() -> None:
    talk_to_gideon([3, 0, 8])
    enter_boss()

def godskin_duo() -> None:
    ...
    talk_to_gideon([2, 28])
    enter_boss()
    # This will need a rework
    # The current game access can only find 1 enemy, I will have to make an array
    # that can hold x pointers and allow the bot to switch between targets
    # I will also need to supply the network all x enemies and their health/ animations

if __name__ == "__main__":
    soldier_of_godrick()