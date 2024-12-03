from scripts.er_helper import key_press, key_presses, find_activate_window, enter_boss
import time

def talk_to_gideon(slots: list) -> None:
    find_activate_window()
    time.sleep(.2)
    key_press('e', 0.3)
    time.sleep(0.3)
    key_press('e', 0.3)
    time.sleep(0.1)
    for i in slots:
        key_presses(['down'] * i)
        time.sleep(0.08)
        key_press('e', 0.2)
        time.sleep(0.1)
    time.sleep(8)

def test_func() -> None:
    find_activate_window()
    time.sleep(.2)
    key_press('down', .04)

"""
Below is a list of different walk backs that I have implemented using the Elden Ring Arena Mod.
    - Soldier of Godrick
    - Leonine Misbegotten*
    - Margit
    - Morgott
    - Godfrey
    - Misbegotten Crusader
    - Crucible Knight Ordovis
    - Pumpkin Head
    - Burial Watchdog
    - Beastman of Farum Azula
    - Elemer of the Briar
    - Rellana
    - Dancing Lion
    - Messmer
    - Midra
    - Consort Radahn
    - Romina
    - Ancient Dragon Man
    - Grafted Scion
    - Godskin Duo
    - ... More bosses in the future once Cutscenes are worked out
    - Some bosses may not work yet due to phase 2 having a different Global ID
        - Currently in the works
"""
def soldier_of_godrick() -> None:
    talk_to_gideon([2, 3, 0])

def leonine_misbegotten() -> None:
    talk_to_gideon([1, 0])

def margit() -> None:
    talk_to_gideon([1, 1])

def morgott() -> None:
    talk_to_gideon([0, 6])

def godfrey() -> None:
    talk_to_gideon([0, 10])

def misbegotten_crusader() -> None:
    talk_to_gideon([2, 3, 21])

def crucible_knight() -> None:
    talk_to_gideon([2, 2, 20])

def pumpkin_head() -> None:
    talk_to_gideon([2, 4, 0])

def burial_watchdog() -> None:
    talk_to_gideon([2, 2, 1])

def beastman() -> None:
    talk_to_gideon([2, 3, 1])

def elemer() -> None:
    talk_to_gideon([1, 8])

def rellana() -> None:
    talk_to_gideon([3, 1])

def messmer() -> None:
    talk_to_gideon([3, 6])

def midra() -> None:
    talk_to_gideon([3, 7])

def consort_radahn() -> None:
    talk_to_gideon([3, 10])

def dancing_lion() -> None:
    talk_to_gideon([3, 0])

def romina() -> None:
    talk_to_gideon([3, 8])

def ancient_dragon_man() -> None:
    talk_to_gideon([4, 6])

def grafted_scion() -> None:
    talk_to_gideon([2, 0, 8])

def godskin_duo() -> None:
    talk_to_gideon([1, 28])

if __name__ == "__main__":
    ...