import memory_access
import struct

class Enemy:
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