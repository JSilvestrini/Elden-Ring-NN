import time
import os.path
import memory_access

# TODO: Perform Assertions and Raises, Error handling
# TODO: Check all return types
# TODO: Error handling

# TODO: XYZ Boss
        # x: ((target + 190) + 68) + 0
        # y: ((target + 190) + 68) + 8
        # z: ((target + 190) + 68) + 4
# TODO: Hardcode some TP Coords into json?
    # TODO: Soldier of Godrick
        # local: <-0.9855866432, 5.026652336, 0.9077949524>
        # global: <8.907794952, 77.02664948, 0.6983950138>
    # TODO: Lionine Misbegotten
    # TODO: The map is unloaded, perform some hardcoded actions to talk to Gideon, then TP to fog, then drink flask and enter.
# TODO: Fix global coordinates, something is wrong

class GameAccessor:
    def __init__(self):
        self.__is_paused = False
        self.__gravity = True

        self.__targeted_enemy_pointer = 0x0
        self.__boss_animation_pointer = 0x0
        self.__boss_health_pointer = 0x0
        self.__boss_max_health_pointer = 0x0
        self.__boss_x_position_pointer = 0x0
        self.__boss_y_position_pointer = 0x0
        self.__boss_z_position_pointer = 0x0
        self.__boss_rotation_position_pointer = 0x0

        self.__game_physics_pointer = 0x0
        self.__gravity_pointer = 0x0

        self.__world_pointer = 0x0
        self.__netmanimp_pointer = 0x0
        self.__local_player_pointer = 0x0
        self.__player_animation_pointer = 0x0
        self.__player_health_pointer = 0x0
        self.__player_max_health_pointer = 0x0
        self.__player_stamina_pointer = 0x0
        self.__player_max_stamina_pointer = 0x0
        self.__player_fp_pointer = 0x0
        self.__player_max_fp_pointer = 0x0
        self.__player_local_x_position_pointer = 0x0
        self.__player_local_y_position_pointer = 0x0
        self.__player_local_z_position_pointer = 0x0
        self.__player_global_x_position_pointer = 0x0
        self.__player_global_y_position_pointer = 0x0
        self.__player_global_z_position_pointer = 0x0
        self.__player_cos_pointer = 0x0
        self.__player_sin_pointer = 0x0

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
        os.remove('place_cheat_table_here/NetManImpPointer.txt')
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

        # local position + rotation
        offset7 = memory_access.read_memory('eldenring.exe', offset2 + 0x68)
        self.__player_local_x_position_pointer = offset7 + 0x70
        self.__player_local_y_position_pointer = offset7 + 0x78
        self.__player_local_z_position_pointer = offset7 + 0x74
        self.__player_cos_pointer = offset7 + 0x54
        self.__player_sin_pointer = offset7 + 0x5c

        # gravity
        self.__gravity_pointer = offset7 + 0x1D3

        # global position Pointer
        g_offset1 = memory_access.read_memory('eldenring.exe', self.__local_player_pointer)

        #g_offset1 = memory_access.read_memory('eldenring.exe', self.__netmanimp_pointer)
        #g_offset2 = memory_access.read_memory('eldenring.exe', g_offset1 + 0x80)
        #g_offset3 = memory_access.read_memory('eldenring.exe', g_offset2 + 0xe0)
        #g_offset4 = memory_access.read_memory('eldenring.exe', g_offset3 + 0x80)
        #g_offset5 = memory_access.read_memory('eldenring.exe', g_offset4 + 0x20)
        #g_offset6 = memory_access.read_memory('eldenring.exe', g_offset5 + 0x98)
        self.__player_global_x_position_pointer = g_offset1 + 0x6C4
        self.__player_global_y_position_pointer = g_offset1 + 0x6C8
        self.__player_global_z_position_pointer = g_offset1 + 0x6CC

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
        self.find_netman_pointer()

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

        # l+g position + rotation
        # TODO

    def get_boss_animation(self) -> int:
        """
        Reads boss animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss animation number (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__boss_animation_pointer)

    def get_boss_health(self) -> int:
        """
        Reads boss health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Boss health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__boss_health_pointer)

    def get_boss_max_health(self) -> int:
        """
        Reads boss max health and returns the integer at that location

        Args:
            None

        Returns:
            Boss max health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__boss_max_health_pointer)

    def get_player_animation(self) -> int:
        """
        Reads player animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player animation number (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_animation_pointer)

    def get_player_health(self) -> int:
        """
        Reads player health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_health_pointer)

    def get_player_stamina(self) -> int:
        """
        Reads player stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player stamina (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_stamina_pointer)

    def get_player_fp(self) -> int:
        """
        Reads player fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player fp (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_fp_pointer)

    def get_player_max_health(self) -> int:
        """
        Reads player max health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_max_health_pointer)

    def get_player_max_stamina(self) -> int:
        """
        Reads player max stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max stamina (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_max_stamina_pointer)

    def get_player_max_fp(self) -> int:
        """
        Reads player max fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max fp (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__player_max_fp_pointer)

    def get_player_local_coords(self) -> list:
        """
        Reads player local coordinate pointers and returns those values

        Args:
            None

        Returns:
            Player local coordinates [x, y, z] (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__player_local_x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_local_y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_local_z_position_pointer)]
    
    def get_player_rotations(self) -> list:
        """
        Reads player cos and sin rotation pointers and returns those values

        Args:
            None

        Returns:
            Player [cos, sin] (list<float>)
        """
        # TODO: is this a float or is it bigger?
        return [memory_access.read_memory_float('eldenring.exe', self.__player_cos_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_sin_pointer)]

    def get_player_global_coords(self) -> list:
        """
        Reads player global coordinate pointers and returns those values

        Args:
            None

        Returns:
            Player global coordinates [x, y, z] (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__player_global_x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_global_y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_global_z_position_pointer)]

    def set_player_local_coords(self, coords: list) -> None:
        """
        Allows the teleport function to change the local coordinates of the player

        Args:
            coords (list<floats>): The [x, y, z] coordinates

        Returns:
            None
        """
        memory_access.write_memory_float('eldenring.exe', self.__player_local_x_position_pointer, coords[0])
        memory_access.write_memory_float('eldenring.exe', self.__player_local_y_position_pointer, coords[1])
        memory_access.write_memory_float('eldenring.exe', self.__player_local_z_position_pointer, coords[2])


    def set_player_rotation(self, cos: float) -> None: ...
    """
    Allows the player to be rotated

    Args:
        Cos (float): This is the cosine of the rotation angle

    Returns:
        None
    """

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
        if not os.path.isfile('place_cheat_table_here/TargetPointer.txt'):
            with open('place_cheat_table_here/NeedTarget.txt', 'w') as file:
                file.write('1')
        while not os.path.isfile('place_cheat_table_here/TargetFound.txt'):
            time.sleep(1)
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

    def find_netman_pointer(self) -> None:
        """
        Finds the NetManImp Pointer for using the teleport function

        Args:
            None

        Returns:
            None
        """
        self.__netmanimp_pointer = memory_access.read_cheat_engine_file('NetManImpPointer.txt')

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

    def toggle_gravity(self) -> None:
        if self.__gravity:
            memory_access.write_memory_int('eldenring.exe', self.__gravity_pointer, 1)
            self.__gravity = False
        else:
            self.__gravity = True
            memory_access.write_memory_int('eldenring.exe', self.__gravity_pointer, 0)

    def teleport(self, coords: list) -> None:
        current_local_coords = self.get_player_local_coords()
        current_global_coords = self.get_player_global_coords()
        self.toggle_gravity()
        new_coords = [coords[0] - (current_global_coords[0] - current_local_coords[0]),
                     (coords[1] - (current_global_coords[1] - current_local_coords[1])) * -1,
                      coords[2] - (current_global_coords[2] - current_local_coords[2])]
        print(new_coords)
        self.set_player_local_coords(new_coords)
        self.toggle_gravity()

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    game = GameAccessor()
    print(game.get_player_health())
    print(game.get_player_fp())
    print(game.get_player_max_fp())
    print(game.get_player_local_coords())
    print(game.get_player_global_coords())
    game.teleport([-0.9855866432, 5.026652336, 0.9077949524])