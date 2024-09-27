import memory_access

class Enemy:
    def __init__(self, pointer) -> None:
        self.__pointer = pointer
        self.__id_pointer = 0x0
        self.__health_pointer = 0x0
        self.__max_health_pointer = 0x0
        self.__animation_pointer = 0x0
        self.__x_position_pointer = 0x0
        self.__y_position_pointer = 0x0
        self.__z_position_pointer = 0x0
        self.__set_values()

    def __set_values(self) -> None:
        """
        Locates all essential targeted enemy pointers.

        Args:
            None

        Returns:
            None
        """
        # animations
        offset1 = memory_access.read_memory('eldenring.exe', self.__pointer + 0x190)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x18)
        self.__animation_pointer = offset2 + 0x40

        # stats
        boss = memory_access.read_memory('eldenring.exe', offset1)
        self.__health_pointer = boss + 0x138
        self.__max_health_pointer = boss + 0x13c

        # boss coords
        offset4 = memory_access.read_memory('eldenring.exe', offset1 + 0x68)
        self.__x_position_pointer = offset4 + 0x70
        self.__y_position_pointer = offset4 + 0x78
        self.__z_position_pointer = offset4 + 0x74

    def get_pointer(self) -> int:
        """
        Returns the boss' pointer to be compared with other pointers

        Args:
            None

        Returns:
            Boss pointer (int)
        """
        return self.__pointer

    def get_animation(self) -> int:
        """
        Reads boss animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss animation number (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__animation_pointer)

    def get_health(self) -> int:
        """
        Reads boss health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__health_pointer)

    def get_max_health(self) -> int:
        """
        Reads boss max health and returns the integer at that location

        Args:
            None

        Returns:
            Boss max health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__max_health_pointer)

    def get_coords(self) -> list:
        """
        Reads Enemy coordinate pointers and returns those values
        Args:
            None
        Returns:
            Enemy coordinates [x, y, z] (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__z_position_pointer)]

# TODO
    def get_id(self) -> int:
        """
        Gets the hex ID of the enemy.

        Args:
            None

        Returns:
            Int
        """
        return memory_access.read_memory_int('eldenring.exe', self.__id_pointer)

'''
    def find_targeted_enemy(self) -> None:
        """
        Reads the file that correlates to the targeted enemy pointer and sets the targeted_enemy_pointer

        Args:
            None

        Returns:
            None
        """
        target_found = False
        potential_pointer = 0
        with open('place_cheat_table_here/NeedTarget.txt', 'w') as file:
            file.write('1')
        while not target_found:
            print("Waiting for Target Pointer")
            time.sleep(1)
            if os.path.isfile('place_cheat_table_here/TargetFound.txt'):
                potential_pointer = memory_access.read_cheat_engine_file('TargetPointer.txt')
            if (potential_pointer != self.__previous_targeted_enemy_pointer and 
                potential_pointer != 0): # and potential_pointer not in self.current_enemies_pointers
                self.__targeted_enemy_pointer = potential_pointer
                target_found = True
        os.remove('place_cheat_table_here/NeedTarget.txt')
        os.remove('place_cheat_table_here/TargetFound.txt')'''