from scripts.er_helper import key_press, key_presses, find_activate_window, enter_boss
import pydirectinput
import time
from typing import List

game_speed : float

def talk_to_gideon(slots: list) -> None:
    find_activate_window()
    time.sleep(.2)
    key_press('e', 0.1)
    time.sleep(0.3)
    key_press('e', 0.1)
    time.sleep(0.1)
    for i in slots:
        pydirectinput.keyDown('shift', _pause=False)
        key_presses(['down'] * i)
        pydirectinput.keyUp('shift', _pause=False)
        time.sleep(0.08)
        key_press('e', 0.1)
        time.sleep(0.1)
    time.sleep(12)

def test_func() -> None:
    find_activate_window()
    time.sleep(.2)
    key_press('down', .04)

"""
Most bosses have been implemented.

Dragon based bosses may not function correctly.
Bosses that do not have a fog wall may not function correctly.

Will perform testing later.
"""

def godrick() -> List[int]:
    talk_to_gideon([0, 0])
    return [47500014]

def rennala() -> List[int]:
    talk_to_gideon([0, 1])
    return [20300024, 20300124, 20310024]

def regal_spirit() -> List[int]:
    talk_to_gideon([0, 2])
    return [46700065]

def starscourge_radahn() -> List[int]:
    talk_to_gideon([0, 3])
    return [47300040]

def astel() -> List[int]:
    talk_to_gideon([0, 4])
    return [46200062]

def fortissax() -> List[int]:
    talk_to_gideon([0, 5])
    return [45110066]

def morgott() -> List[int]:
    talk_to_gideon([0, 6])
    return [21300534]

def rykard() -> List[int]:
    talk_to_gideon([0, 7])
    return [47100038, 47101038]

def maliketh() -> List[int]:
    talk_to_gideon([0, 8])
    return [21100072, 21101072]

def fire_giant() -> List[int]:
    talk_to_gideon([0, 9])
    return [47600050, 47601050]

def godfrey() -> List[int]:
    talk_to_gideon([0, 10])
    return [47200070, 47210070]

def placidusax() -> List[int]:
    talk_to_gideon([0, 11])
    return [45200072]

def leonine_misbegotten() -> List[int]:
    talk_to_gideon([1, 0])
    return [34600913]

def margit() -> List[int]:
    talk_to_gideon([1, 1])
    key_press('4', .16)
    key_press('w', .08)
    return [21300014]

def dragonkin_nokstella() -> List[int]:
    talk_to_gideon([1, 2])
    return [46500960]

def dragon_agheel() -> List[int]:
    talk_to_gideon([1, 3])
    return [45000010]

def ancestor_spirit() -> List[int]:
    talk_to_gideon([1, 4])
    return [46700964]

def red_wolf() -> List[int]:
    talk_to_gideon([1, 5])
    return [31811024]

def loretta() -> List[int]:
    talk_to_gideon([1, 6])
    return [32520921]

def makar() -> List[int]:
    talk_to_gideon([1, 7])
    return [49100026]

def elemer() -> List[int]:
    talk_to_gideon([1, 8])
    return [31000931]

def naill() -> List[int]:
    # TODO: wrong param id
    talk_to_gideon([1, 22])
    key_press('w', 1 / game_speed)
    return [30500051, 30107051, 30106051]

def dragonkin_siofra() -> List[int]:
    talk_to_gideon([1, 10])
    return [46500265]

def smarag() -> List[int]:
    talk_to_gideon([1, 11])
    return [45020920]

def mimic_tear() -> List[int]:
    talk_to_gideon([1, 12])
    return [526100965]

def misbegotten_crucible_knight() -> List[int]:
    talk_to_gideon([1, 13])
    key_press('w', 1 / game_speed)
    # misbegotten, knight
    return [34600941, 25000941]

def goldfrey() -> List[int]:
    talk_to_gideon([1, 14])
    return [47200134]

def godskin_noble() -> List[int]:
    talk_to_gideon([1, 15])
    return [35700038]

def sirulia() -> List[int]:
    talk_to_gideon([1, 16])
    key_press('w', 1)
    return [25001066]

def mohg() -> List[int]:
    talk_to_gideon([1, 24])
    return [48001935]

def godskin_apostle() -> List[int]:
    talk_to_gideon([1, 25])
    return [35600042]

def godskin_duo() -> List[int]:
    talk_to_gideon([1, 28])
    # boss bar, noble, apostle
    return [35600972, 35700172, 35600172]

def gideon() -> List[int]:
    talk_to_gideon([1, 29])
    return [523240070]

def loretta_haligtree() -> List[int]:
    talk_to_gideon([1, 31])
    key_press('w', 1)
    return [32520054]

def tree_sentinel() -> List[int]:
    talk_to_gideon([2, 0, 3])
    return [32510010]

def grafted_scion() -> List[int]:
    talk_to_gideon([2, 0, 8])
    key_press('w', 1)
    return [46900008]

def tree_sentinel_duo() -> List[int]:
    talk_to_gideon([2, 0, 26])
    return [32511030, 32510030]

def draconic_tree_sentinel() -> List[int]:
    talk_to_gideon([2, 0, 30])
    return [32500033]

def black_knife_assassin() -> List[int]:
    talk_to_gideon([2, 2, 0])
    return [21001010]

def burial_watchdog() -> List[int]:
    talk_to_gideon([2, 2, 1])
    return [42600110]

def grave_warden_duelist() -> List[int]:
    talk_to_gideon([2, 2, 2])
    return [34001110]

def cemetery_shade() -> List[int]:
    talk_to_gideon([2, 2, 3])
    return [36640012]

def burial_watchdog_duo() -> List[int]:
    talk_to_gideon([2, 2, 11])
    return [42600940, 42601940]

def crucible_knight_duo() -> List[int]:
    talk_to_gideon([2, 2, 20])
    return [25001933, 25000933]

def soldier_godrick() -> List[int]:
    talk_to_gideon([2, 3, 0])
    return [43113906]

def beastman() -> List[int]:
    talk_to_gideon([2, 3, 1])
    return [39701910]

def golem() -> List[int]:
    talk_to_gideon([2, 3, 2])
    return [46600910]

def runebbear() -> List[int]:
    talk_to_gideon([2, 3, 6])
    return [46300912]

def bloodhound_knight() -> List[int]:
    talk_to_gideon([2, 3, 7])
    return [42900920]

def cleanrot_knight() -> List[int]:
    talk_to_gideon([2, 3, 8])
    return [38000920]

def misbegotten_crusader() -> List[int]:
    talk_to_gideon([2, 3, 21])
    return [34601952]

def pumpkin_head() -> List[int]:
    talk_to_gideon([2, 4, 0])
    return [43400910]

def troll() -> List[int]:
    talk_to_gideon([2, 4, 1])
    return [46030910]

def scaly_misbegotten() -> List[int]:
    talk_to_gideon([2, 4, 2])
    return [34510912]

def crystalian() -> List[int]:
    talk_to_gideon([2, 4, 3])
    return [33500920]

def pumpkin_head_duo() -> List[int]:
    talk_to_gideon([2, 4, 6])
    return [43401940, 43400940]

def crystalian_duo() -> List[int]:
    talk_to_gideon([2, 4, 11])
    return [33501930, 33500930]

def onyx_lord() -> List[int]:
    talk_to_gideon([2, 4, 12])
    return [36001933]

def dancing_lion() -> List[int]: 
    talk_to_gideon([3, 0])
    return [52100088]

def rellana() -> List[int]:
    talk_to_gideon([3, 1])
    return [53000082]

def putrescent_knight() -> List[int]:
    talk_to_gideon([3, 3])
    return [50200087, 50200187]

def messmer() -> List[int]:
    talk_to_gideon([3, 6])
    return [51300099, 51301099]

def midra() -> List[int]:
    talk_to_gideon([3, 7])
    key_press('w', 1)
    return [50500086, 50510086]

def romina() -> List[int]:
    talk_to_gideon([3, 8])
    return [50300094]

def consort_radahn() -> List[int]:
    talk_to_gideon([3, 10])
    return [52200089, 52201089]

def death_knight() -> List[int]:
    talk_to_gideon([4, 5])
    return [50700081]

def ancient_dragon_man() -> List[int]:
    talk_to_gideon([4, 6])
    return [524070081]

def death_knight_rauh() -> List[int]:
    talk_to_gideon([4, 14])
    return [50701095]

if __name__ == "__main__":
    ...