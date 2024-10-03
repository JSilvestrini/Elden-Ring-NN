import scripts.memory_access as memory_access
import struct
import numpy as np
import scripts.er_helper as er_helper
import time
from scripts.player import Player
from bitstring import BitArray

class EnemyAccess:
    def __init__(self, pointer) -> None:
        self.__pointer = pointer
        self.__id_pointer = 0x0
        self.__global_id_pointer = 0x0
        self.__health_pointer = 0x0
        self.__max_health_pointer = 0x0
        self.__animation_pointer = 0x0
        self.__x_position_pointer = 0x0
        self.__y_position_pointer = 0x0
        self.__z_position_pointer = 0x0
        self.__is_dead_pointer = 0x0
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

        # id pointers
        # +28] +124
        offset5 = memory_access.read_memory('eldenring.exe', self.__pointer + 0x28)
        self.__id_pointer = offset5 + 0x124
        self.__global_id_pointer = self.__pointer + 0x74

        #[[self.__pointer + x58]+xC8]+x24, 1 byte
        offset6 = memory_access.read_memory('eldenring.exe', self.__pointer + 0x58)
        offset7 = memory_access.read_memory('eldenring.exe', offset6 + 0xc8)
        self.__is_dead_pointer = offset7 + 0x24

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

    def get_id(self) -> int:
        """
        Gets the int ID of the enemy.

        Args:
            None

        Returns:
            Int
        """
        return memory_access.read_memory_int('eldenring.exe', self.__id_pointer)

    def get_global_id(self) -> int:
        """
        Gets the hex ID of the enemy.

        Args:
            None

        Returns:
            Int
        """
        two_bytes = memory_access.read_memory_bytes('eldenring.exe', self.__global_id_pointer, 2)
        return struct.unpack('>H', two_bytes)[0].to_bytes(2, byteorder='little').hex()

    def get_dead(self) -> str:
        """
        Locates the dead flag on the enemy and returns the value

        Args:
            None

        Returns:
            Dead Flag in binary
        """
        c = str(memory_access.read_memory_bytes('eldenring.exe', self.__is_dead_pointer, 1))
        c = '0'+ c[3:-1]
        h = BitArray(hex=c)
        return h.bin

# TODO: Add Dead AF Flag
'''
can't find bullets through the ID of the enemy?
'''
class Enemy:
    def __init__(self, enemy_access, player: Player):
        self.enemy_access = enemy_access
        self.is_dead = False
        self.health = self.enemy_access.get_health()
        self.max_health = self.enemy_access.get_max_health()
        self.health_prev = self.health
        self.coords = np.array(self.enemy_access.get_coords())
        self.coords_prev = self.coords
        self.animation = self.enemy_access.get_animation()
        self.animation_list = er_helper.get_animation_files("animation_files/{}".format(self.enemy_access.get_id()))
        self.animation_list_zero = np.zeros_like(self.animation_list)
        self.animation_timer = time.time()
        self.previous_animation = self.animation
        self.distance_from_player = np.linalg.norm(self.coords - player.coords, axis=0)
        self.direction_from_player = np.arctan2(self.coords[1] - player.coords[1], self.coords[0] - player.coords[0]) * 180 / np.pi
        self.is_dead = (self.enemy_access.get_dead()[0] == 1)

    def encode_animation(self) -> None:
        """
        This locates the animation folder of the enemy and encodes the number of animations into a list of only 0s

        Args:
            None

        Returns:
            None
        """
        index = np.where(self.animation_list == self.animation)
        self.animation_list_zero = np.zeros_like(self.animation_list)
        self.animation_list_zero[index] = 1

    def update(self, player: Player) -> None:
        """
        This performs all the updates that are needed during each step of the environment

        Args:
            Player: This is to find information about the distance and direction of the enemy to the player

        Returns:
            None
        """
        self.health_prev = self.health
        self.coords_prev = self.coords
        self.previous_animation = self.animation

        self.health = self.enemy_access.get_health()
        self.coords = np.array(self.enemy_access.get_coords())
        self.animation = self.enemy_access.get_animation()
        self.is_dead = not (self.health > 0)
        if self.animation != self.previous_animation:
            self.animation_timer = time.time()
            self.encode_animation()
        self.distance_from_player = np.linalg.norm(self.coords - player.coords, axis=0)
        self.direction_from_player = np.arctan2(self.coords[1] - player.coords[1], self.coords[0] - player.coords[0]) * 180 / np.pi

    def state(self) -> np.ndarray:
        """
        This creates an array that describes the state of the enemy

        Args:
            None

        Returns:
            Information about the health, change in health, distance, direction, current animation, and animation completion in array form
        """
        enemy_health = self.health / self.max_health
        enemy_delta_health = (self.health_prev - self.health) / self.max_health
        enemy_animation = self.animation_list_zero
        enemy_distance = self.distance_from_player
        enemy_direction = self.direction_from_player
        enemy_animation_completion = (self.animation_timer - time.time()) / er_helper.max_time("animation_files/{}".format(self.enemy_access.get_id()), self.animation)

        boss_array = np.array([enemy_health, enemy_delta_health, enemy_distance, enemy_direction, enemy_animation_completion])
        combined_array = np.concatenate((boss_array, enemy_animation))
        return combined_array