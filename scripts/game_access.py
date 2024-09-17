import time
import os.path
import memory_access

# TODO: Write google function strings
# TODO: Perform Assertions and Raises
# TODO: Check all return types
# TODO: Error handling

# TODO: Update cheat table and check for offsets again
# TODO: XYZ Player
# TODO: XYZ Boss
# TODO: Hardcode some TP Coords

class GameAccessor:
    def __init__(self):
        self.__is_paused = False

        self.__targeted_enemy_pointer = 0x0
        self.__boss_animation_pointer = 0x0
        self.__boss_health_pointer = 0x0
        self.__boss_max_health_pointer = 0x0

        self.__game_physics_pointer = 0x0

        self.__world_pointer = 0x0
        self.__local_player_pointer = 0x0
        self.__player_animation_pointer = 0x0
        self.__player_health_pointer = 0x0
        self.__player_max_health_pointer = 0x0
        self.__player_stamina_pointer = 0x0
        self.__player_max_stamina_pointer = 0x0
        self.__player_fp_pointer = 0x0
        self.__player_max_fp_pointer = 0x0

        self.get_memory_values()

    def get_memory_values(self) -> None:
        """
        Communicates with Cheat Engine and acts as an init function for finding essential pointers.

        Args:
            None

        Returns:
            None
        """

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
        """
        Locates all essential player pointers

        Args:
            None

        Returns:
            None
        """
        self.__local_player_pointer = memory_access.read_memory('eldenring.exe', (self.__world_pointer + 0x10ef8))

        # player stats
        offset1 = memory_access.read_memory('eldenring.exe', self.__local_player_pointer)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x190)
        player = memory_access.read_memory('eldenring.exe', offset2)
        self.__player_health_pointer = player + 0x138
        self.__player_max_health_pointer = player + 0x13c
        self.__player_fp_pointer = player + 0x148
        self.__player_max_fp_pointer = player + 0x14c
        self.__player_stamina_pointer = player + 0x154
        self.__player_max_stamina_pointer = player + 0x158

        # animations
        offset3 = memory_access.read_memory('eldenring.exe', offset1 + 0x58)
        offset4 = memory_access.read_memory('eldenring.exe', offset3 + 0x10)
        offset5 = memory_access.read_memory('eldenring.exe', offset4 + 0x190)
        offset6 = memory_access.read_memory('eldenring.exe', offset5 + 0x18)
        self.__player_animation_pointer = offset6 + 0x40

        # position + rotation
        # TODO

    def set_world_information(self) -> None:
        """
        Locates all essential world pointers.

        Args:
            None

        Returns:
            None
        """
        self.find_game_physics()
        self.find_world_pointer()
        self.find_targeted_enemy()

    def set_boss_information(self) -> None:
        """
        Locates all essential targeted enemy pointers.

        Args:
            None

        Returns:
            None
        """
        # animations
        offset1 = memory_access.read_memory('eldenring.exe', self.__targeted_enemy_pointer + 0x190)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x18)
        self.__boss_animation_pointer = offset2 + 0x40

        # stats
        boss = memory_access.read_memory('eldenring.exe', offset1)
        self.__boss_health_pointer = boss + 0x138
        self.__boss_max_health_pointer = boss + 0x13c

        # position + rotation
        # TODO

    def get_boss_animation(self) -> int:
        """
        Reads boss animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss animation number (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__boss_animation_pointer)

    def get_boss_health(self) -> int:
        """
        Reads boss health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss health (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__boss_health_pointer)

    def get_boss_max_health(self) -> int:
        """
        Reads boss max health and returns the integer at that location

        Args:
            None

        Returns:
            Boss max health (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__boss_max_health_pointer)

    def get_player_animation(self) -> int:
        """
        Reads player animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player animation number (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_animation_pointer)

    def get_player_health(self) -> int:
        """
        Reads player health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player health (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_health_pointer)

    def get_player_stamina(self) -> int:
        """
        Reads player stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player stamina (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_stamina_pointer)

    def get_player_fp(self) -> int:
        """
        Reads player fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player fp (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_fp_pointer)

    def get_player_max_health(self) -> int:
        """
        Reads player max health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max health (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_max_health_pointer)

    def get_player_max_stamina(self) -> int:
        """
        Reads player max stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max stamina (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_max_stamina_pointer)

    def get_player_max_fp(self) -> int:
        """
        Reads player max fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max fp (int)
        """
        return memory_access.read_memory_i('eldenring.exe', self.__player_max_fp_pointer)

    def find_game_physics(self) -> None:
        """
        Reads the file that correlates to the pause pointer and sets the game_physics_pointer

        Args:
            None

        Returns:
            None
        """
        self.__game_physics_pointer = memory_access.read_cheat_engine_file('PausePointer.txt')

    def find_targeted_enemy(self) -> None:
        """
        Reads the file that correlates to the targeted enemy pointer and sets the targeted_enemy_pointer

        Args:
            None

        Returns:
            None
        """
        self.__targeted_enemy_pointer = memory_access.read_cheat_engine_file('TargetPointer.txt')

    def find_world_pointer(self) -> None:
        """
        Reads the file that correlates to the world pointer and sets the world_pointer

        Args:
            None

        Returns:
            None
        """
        self.__world_pointer = memory_access.read_cheat_engine_file('WorldChrManPointer.txt')

    def pause_game(self) -> None:
        """
        Pauses and unpauses the game physics

        Args:
            None

        Returns:
            None
        """
        if self.__game_physics_pointer == None:
            return

        if self.__is_paused:
            memory_access.write_byte('eldenring.exe', self.__game_physics_pointer + 0x6, b'\x00')
        else:
            memory_access.write_byte('eldenring.exe', self.__game_physics_pointer + 0x6, b'\x01')

        self.__is_paused = not self.__is_paused

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    game = GameAccessor()
    print(game.get_player_health())