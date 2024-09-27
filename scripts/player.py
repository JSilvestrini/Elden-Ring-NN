import memory_access

class Player:
    def __init__(self, WorldPointer):
        self.__pointer = 0x0
        self.__animation_pointer = 0x0
        self.__health_pointer = 0x0
        self.__max_health_pointer = 0x0
        self.__stamina_pointer = 0x0
        self.__max_stamina_pointer = 0x0
        self.__fp_pointer = 0x0
        self.__max_fp_pointer = 0x0
        self.__x_position_pointer = 0x0
        self.__y_position_pointer = 0x0
        self.__z_position_pointer = 0x0
        self.__cos_pointer = 0x0
        self.__sin_pointer = 0x0
        self.__gravity = True
        self.reset(WorldPointer)

    def reset(self, WorldPointer) -> None:
        """
        Locates all essential player pointers

        Args:
            None

        Returns:
            None
        """
        self.__pointer = memory_access.read_memory('eldenring.exe', (WorldPointer + 0x10ef8))

        # player stats
        offset1 = memory_access.read_memory('eldenring.exe', self.__pointer)
        offset2 = memory_access.read_memory('eldenring.exe', offset1 + 0x190)
        player = memory_access.read_memory('eldenring.exe', offset2)
        self.__health_pointer = player + 0x138
        self.__max_health_pointer = player + 0x13c
        self.__fp_pointer = player + 0x148
        self.__max_fp_pointer = player + 0x14c
        self.__stamina_pointer = player + 0x154
        self.__max_stamina_pointer = player + 0x158

        # animations
        offset3 = memory_access.read_memory('eldenring.exe', offset1 + 0x58)
        offset4 = memory_access.read_memory('eldenring.exe', offset3 + 0x10)
        offset5 = memory_access.read_memory('eldenring.exe', offset4 + 0x190)
        offset6 = memory_access.read_memory('eldenring.exe', offset5 + 0x18)
        self.__animation_pointer = offset6 + 0x40

        # local position + rotation
        offset7 = memory_access.read_memory('eldenring.exe', offset2 + 0x68)
        self.__x_position_pointer = offset7 + 0x70
        self.__y_position_pointer = offset7 + 0x78
        self.__z_position_pointer = offset7 + 0x74
        self.__cos_pointer = offset7 + 0x54
        self.__sin_pointer = offset7 + 0x5c

        # gravity
        self.__gravity_pointer = offset7 + 0x1D3

    def get_animation(self) -> int:
        """
        Reads player animation pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player animation number (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__animation_pointer)

    def get_health(self) -> int:
        """
        Reads player health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__health_pointer)

    def get_stamina(self) -> int:
        """
        Reads player stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player stamina (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__stamina_pointer)

    def get_fp(self) -> int:
        """
        Reads player fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player fp (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__fp_pointer)

    def get_max_health(self) -> int:
        """
        Reads player max health pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max health (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__max_health_pointer)

    def get_max_stamina(self) -> int:
        """
        Reads player max stamina pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max stamina (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__max_stamina_pointer)

    def get_max_fp(self) -> int:
        """
        Reads player max fp pointer and returns the integer at that location

        Args:
            None

        Returns:
            Player max fp (int)
        """
        return memory_access.read_memory_int('eldenring.exe', self.__max_fp_pointer)

    def get_coords(self) -> list:
        """
        Reads player local coordinate pointers and returns those values

        Args:
            None

        Returns:
            Player local coordinates [x, y, z] (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__x_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__y_position_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__z_position_pointer)]
    
    def get_rotations(self) -> list:
        """
        Reads player cos and sin rotation pointers and returns those values

        Args:
            None

        Returns:
            Player [cos, sin] (list<float>)
        """
        return [memory_access.read_memory_float('eldenring.exe', self.__cos_pointer),
                memory_access.read_memory_float('eldenring.exe', self.__sin_pointer)]

    def set_coords(self, coords: list) -> None:
        """
        Allows the teleport function to change the local coordinates of the player

        Args:
            coords (list<floats>): The [x, y, z] coordinates

        Returns:
            None
        """
        memory_access.write_memory_float('eldenring.exe', self.__x_position_pointer, coords[0])
        memory_access.write_memory_float('eldenring.exe', self.__y_position_pointer, coords[1])
        memory_access.write_memory_float('eldenring.exe', self.__z_position_pointer, coords[2])

    def set_rotation(self, cos: float, sin: float) -> None:
        """
        Allows the player to be rotated

        Args:
            Cos (float): This is the cosine of the rotation angle

        Returns:
            None
        """
        memory_access.write_memory_float('eldenring.exe', self.__cos_pointer, cos)
        memory_access.write_memory_float('eldenring.exe', self.__sin_pointer, sin)

    def toggle_gravity(self) -> None:
        """
        Turns the gravity on and off, was originally used to teleport the player

        Args:
            None

        Returns:
            None
        """
        if self.__gravity:
            memory_access.write_memory_int('eldenring.exe', self.__gravity_pointer, 1)
            self.__gravity = False
        else:
            memory_access.write_memory_int('eldenring.exe', self.__gravity_pointer, 0)
            self.__gravity = True
