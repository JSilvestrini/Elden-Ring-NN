import time
import os.path
import memory_access

# TODO: Perform Assertions and Raises, Error handling
# TODO: Check all return types
# TODO: Error handling

# TODO: Update cheat table and check for offsets again
# TODO: XYZ Player
    # Local:
        # x: (((local player + 0) + 190) + 68) + 70
        # y: (((local player + 0) + 190) + 68) + 78
        # z: (((local player + 0) + 190) + 68) + 74
    # Rotation:
        # cos: (((local player + 0) + 190) + 68) + 54
        # sin: (((local player + 0) + 190) + 68) + 5C
# TODO: XYZ Boss
        # x: ((target + 190) + 68) + 0
        # y: ((target + 190) + 68) + 8
        # z: ((target + 190) + 68) + 4
# TODO: Hardcode some TP Coords?
    # TODO: Soldier of Godrick
    # TODO: Lionine Misbegotten
# TODO: TP Function:
# TODO: Add new file to lua for NetManImp
'''
-- Find address!
local x = readFloat("TPData") <- where to teleport
local z = readFloat("TPData+4")
local y = readFloat("TPData+8")

# local coords
local xPtrTp = "[[[[[WorldChrMan]+10EF8]+0]+190]+68]+70"
local zPtrTp = "[[[[[WorldChrMan]+10EF8]+0]+190]+68]+74"
local yPtrTp = "[[[[[WorldChrMan]+10EF8]+0]+190]+68]+78"

# global coords
local xGlobalPtr = "[[[[[[NetManImp]+ 80]+ E0] + 80] + 20] + 98] + 28"
local zGlobalPtr = "[[[[[[NetManImp]+ 80]+ E0] + 80] + 20] + 98] + 1C"
local yGlobalPtr = "[[[[[[NetManImp]+ 80]+ E0] + 80] + 20] + 98] + 2C"

local gravityPtr = "[[[[[WorldChrMan]+10EF8]+0]+190]+68]+1D3" -- Nogravity
writeInteger(gravityPtr, 1)

-- Calculate
xNew = x - (readFloat(xGlobalPtr) - readFloat(xPtrTp))
zNew = z - (readFloat(zGlobalPtr) - readFloat(zPtrTp))
yNew = (y - (readFloat(yGlobalPtr) + readFloat(yPtrTp))) * -1

writeFloat(xPtrTp, xNew)
writeFloat(zPtrTp, zNew)
writeFloat(yPtrTp, yNew)
'''

# create NeedTarget.txt
# Read TargetPointer.txt when TargetFound.txt exists


class GameAccessor:
    def __init__(self):
        self.__is_paused = False

        self.__targeted_enemy_pointer = 0x0
        self.__boss_animation_pointer = 0x0
        self.__boss_health_pointer = 0x0
        self.__boss_max_health_pointer = 0x0
        self.__boss_x_position_pointer = 0x0
        self.__boss_y_position_pointer = 0x0
        self.__boss_z_position_pointer = 0x0
        self.__boss_rotation_position_pointer = 0x0


        self.__game_physics_pointer = 0x0

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

        # global position Pointer
        g_offset1 = memory_access.read_memory('eldenring.exe', self.__netmanimp_pointer)
        g_offset2 = memory_access.read_memory('eldenring.exe', g_offset1 + 0x80)
        g_offset3 = memory_access.read_memory('eldenring.exe', g_offset2 + 0xe0)
        g_offset4 = memory_access.read_memory('eldenring.exe', g_offset3 + 0x80)
        g_offset5 = memory_access.read_memory('eldenring.exe', g_offset4 + 0x20)
        g_offset6 = memory_access.read_memory('eldenring.exe', g_offset5 + 0x98)
        self.__player_global_x_position_pointer = g_offset6 + 0x28
        self.__player_global_y_position_pointer = g_offset6 + 0x2c
        self.__player_global_z_position_pointer = g_offset6 + 0x1c

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

    def get_player_local_coords(self) -> list:
        """
        Reads player local coordinate pointers and returns those values

        Args:
            None

        Returns:
            Player local coordinates (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__player_local_x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_local_y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_local_z_position_pointer)]
    
    def get_player_rotations(self) -> list:
        # TODO: is this a float or is it bigger?
        return [memory_access.read_memory_float('eldenring.exe', self.__player_cos_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_sin_pointer)]

    def get_player_global_coords(self) -> list:
        """
        Reads player global coordinate pointers and returns those values

        Args:
            None

        Returns:
            Player global coordinates (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__player_global_x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_global_y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__player_global_z_position_pointer)]

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
        if not os.path.isfile('TargetPointer.txt'):
            with open('place_cheat_table_here/NeedTarget.txt', 'w') as file:
                file.write('1')
        while not os.path.isfile('TargetFound.txt'):
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

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    game = GameAccessor()
    print(game.get_player_health())
    print(game.get_player_fp())
    print(game.get_player_max_fp())