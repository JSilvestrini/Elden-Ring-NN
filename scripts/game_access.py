import time
import os.path
import memory_access

# TODO: write google function strings
# TODO: Check Raises from memory_access.py
# TODO: Check all return types
# TODO: Error handling
# TODO: Update cheat table and check for offsets again

class GameAccessor:
    def __init__(self):
        self.__isPaused = False

        self.__targetedEnemyPointer = 0x0
        self.__bossAnimationPointer = 0x0
        self.__bossHealthPointer = 0x0
        self.__bossMaxHealthPointer = 0x0

        self.__gamePhysicsPointer = 0x0

        self.__worldPointer = 0x0
        self.__localPlayerPointer = 0x0
        self.__playerAnimationPointer = 0x0
        self.__playerHealthPointer = 0x0
        self.__playerMaxHealthPointer = 0x0
        self.__playerStaminaPointer = 0x0
        self.__playerMaxStaminaPointer = 0x0
        self.__playerFPPointer = 0x0
        self.__playerMaxFPPointer = 0x0

        self.get_memory_values()

    def get_memory_values(self) -> None:

        with open('place_cheat_table_here/PlayerDead.txt', 'w') as file:
            file.write('1')

        while not os.path.isfile('place_cheat_table_here/DataWritten.txt'):
            time.sleep(1.0)
            print("Waiting")

        self.set_world_information()
        self.set_player_information()
        self.set_boss_information()

        os.remove('place_cheat_table_here/DataWritten.txt')
        os.remove('place_cheat_table_here/TargetPointer.txt')
        os.remove('place_cheat_table_here/WorldChrManPointer.txt')
        os.remove('place_cheat_table_here/PausePointer.txt')
        os.remove('place_cheat_table_here/PlayerDead.txt')

    def set_player_information(self) -> None:
        self.__localPlayerPointer = memory_access.read_memory('eldenring.exe', (self.__worldPointer + 0x10ef8))

        # player stats
        offset1 = memory_access.read_memory('eldenring.exe', self.__localPlayerPointer)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x190)
        player = memory_access.read_memory('eldenring.exe', offset2)
        self.__playerHealthPointer = player + 0x138
        self.__playerMaxHealthPointer = player + 0x13c
        self.__playerFPPointer = player + 0x148
        self.__playerMaxFPPointer = player + 0x14c
        self.__playerStaminaPointer = player + 0x154
        self.__playerMaxStaminaPointer = player + 0x158

        # animations
        offset3 = memory_access.read_memory('eldenring.exe', offset1 + 0x58)
        offset4 = memory_access.read_memory('eldenring.exe', offset3 + 0x10)
        offset5 = memory_access.read_memory('eldenring.exe', offset4 + 0x190)
        offset6 = memory_access.read_memory('eldenring.exe', offset5 + 0x18)
        self.__playerAnimationPointer = offset6 + 0x40

        # position + rotation
        # TODO

    def set_world_information(self) -> None:
        self.find_game_physics()
        self.find_world_pointer()
        self.find_targeted_enemy()

    def set_boss_information(self) -> None:
        # animations
        offset1 = memory_access.read_memory('eldenring.exe', self.__targetedEnemyPointer + 0x190)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x18)
        self.__bossAnimationPointer = offset2 + 0x40

        # stats
        boss = memory_access.read_memory('eldenring.exe', offset1)
        self.__bossHealthPointer = boss + 0x138
        self.__bossMaxHealthPointer = boss + 0x13c

        # position + rotation
        # TODO

    def get_boss_animation(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__bossAnimationPointer)

    def get_boss_health(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__bossHealthPointer)

    def get_boss_max_health(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__bossMaxHealthPointer)

    def get_player_animation(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerAnimationPointer)

    def get_player_health(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerHealthPointer)

    def get_player_stamina(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerStaminaPointer)

    def get_player_fp(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerFPPointer)

    def get_player_max_health(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxHealthPointer)

    def get_player_max_stamina(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxStaminaPointer)

    def get_player_max_fp(self) -> int:
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxFPPointer)

    def find_game_physics(self) -> None:
        self.__gamePhysicsPointer = memory_access.read_cheat_engine_file('PausePointer.txt')

    def find_targeted_enemy(self) -> None:
        self.__targetedEnemyPointer = memory_access.read_cheat_engine_file('TargetPointer.txt')

    def find_world_pointer(self) -> None:
        self.__worldPointer = memory_access.read_cheat_engine_file('WorldChrManPointer.txt')

    def pause_game(self) -> None:
        if self.__gamePhysicsPointer == None:
            return

        if self.__isPaused:
            memory_access.write_byte('eldenring.exe', self.__gamePhysicsPointer + 0x6, b'\x00')
        else:
            memory_access.write_byte('eldenring.exe', self.__gamePhysicsPointer + 0x6, b'\x01')

        self.__isPaused = not self.__isPaused

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    game = GameAccessor()
    print(game.get_player_health())