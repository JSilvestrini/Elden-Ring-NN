import memory_access
from enemies import Enemy
from player import Player
import time
import os.path
import threading

# TODO: Perform Assertions and Raises, Error handling
# TODO: Check all return types
# TODO: Error handling

# TODO: Have certain key presses create the 'NeedTarget' File

class GameAccessor:
    def __init__(self):
        self.__listening = threading.Event()
        self.__enemy_listener = threading.Thread(target=self.check_for_enemies)
        self.reset()

    def reset(self) -> None:
        """
        Resets all the values in the game_accessor after player death or boss death.

        Args:
            None

        Returns:
            None
        """
        self.__is_paused = False
        self.__game_physics_pointer = 0x0
        self.__world_pointer = 0x0
        self.__enemies : list[Enemy] = []
        self.__enemy_pointers = []
        self.__player : Player = None
        self.__listening.set()
        self.__enemy_listener.start()
        self.get_memory_values()

    def begin_reset(self) -> None:
        """
        ...
        """
        self.__listening.clear()
        self.__enemy_listener.join()
        print("thread stopped")
        self.reset()


    def get_player(self) -> Player:
        """
        Returns the player

        Args:
            None

        Returns:
            Player object
        """
        return self.__player

    def get_enemies(self) -> list[Enemy]:
        """
        Returns the enemy list

        Args:
            None

        Returns:
            Enemy list
        """
        return self.__enemies

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
        self.__player = Player(self.__world_pointer)

        os.remove('place_cheat_table_here/DataWritten.txt')
        os.remove('place_cheat_table_here/WorldChrManPointer.txt')
        os.remove('place_cheat_table_here/PausePointer.txt')
        os.remove('place_cheat_table_here/PlayerDead.txt')

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

    def find_game_physics(self) -> None:
        """
        Reads the file that correlates to the pause pointer and sets the game_physics_pointer

        Args:
            None

        Returns:
            None
        """
        self.__game_physics_pointer = memory_access.read_cheat_engine_file('PausePointer.txt')

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

    def check_for_enemies(self) -> None:
        """
        Checks for the enemy file and tries to append it to the enemy list

        Args:
            None

        Returns:
            None
        """
        while self.__listening.is_set():
            potential_pointer = 0
            with open('place_cheat_table_here/NeedTarget.txt', 'w') as file:
                file.write('1')
            while not os.path.isfile('place_cheat_table_here/TargetFound.txt'):
                time.sleep(0.1)

            potential_pointer = memory_access.read_cheat_engine_file('TargetPointer.txt')
            if potential_pointer != 0 and potential_pointer not in self.__enemy_pointers:
                self.__enemy_pointers.append(potential_pointer)
                self.__enemies.append(Enemy(potential_pointer))
            if os.path.isfile('place_cheat_table_here/TargetFound.txt'):
                os.remove('place_cheat_table_here/NeedTarget.txt')
                os.remove('place_cheat_table_here/TargetFound.txt')
                os.remove('place_cheat_table_here/TargetPointer.txt')

if __name__ == "__main__":
    ...