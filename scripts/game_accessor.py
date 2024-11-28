import memory_access as mm
from build import AOBScanner
import pymem
import pymem.process
from bitstring import BitArray
import struct

bases = {
    "WorldChrMan": {"aob": "48 8B 05 00 00 00 00 48 85 C0 74 0F 48 39 88", "mask": "xxx????xxxxxxxx", "offset": 3, "additional": 7},
    "WorldChrManAlt": {"aob": "0F 10 00 0F 11 44 24 70 0F 10 48 10 0F 11 4D 80 48 83 3D", "mask": "xxxxxxxxxxxxxxxxxxx", "offset": 19, "additional": 24},
    "GameDataMan": {"aob": "48 8B 05 00 00 00 00 48 85 C0 74 05 48 8B 40 58 C3 C3", "mask": "xxx????xxxxxxxxxxx", "offset": 3, "additional": 7},
    "NetManImp": {"aob": "48 8B 05 00 00 00 00 80 78 00 00 00 00 48 8D 9F 00 00 00 00 48 8B 03", "mask": "xxx????xx?x??xxx????xxx", "offset": 3, "additional": 7},
    "EventFlagMan": {"aob":"48 8B 3D 00 00 00 00 48 85 FF 00 00 32 C0 E9", "mask": "xxx????xxx??xxx", "offset": 3, "additional": 7},
}

player_addrs_loc = {
    "playerDead": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x1c5]},
    "playerHealth": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x138]},
    "playerMaxHealth": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x13c]},
    "playerFP": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x148]},
    "playerMaxFP": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x14c]},
    "playerStamina": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x154]},
    "playerMaxStamina": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x158]},
    "playerAnimation": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x58, 0x10, 0x190, 0x18, 0x40]},
    "playerX": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x70]},
    "playerY": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x78]},
    "playerZ": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x74]},
    "playerCos": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x54]},
    "playerSin": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x5c]},
    "playerGravity": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x1d3]},
    "cutsceneLoading": {"base" : "EventFlagMan", "offsets" : [0x28, 0x113]}, # may or maynot need to prepend 0x0, != 0 means not controllable
}

enemy_addrs_loc = {
    "ID": {"offsets": [0x28, 0x124]},
    "globalID": {"offsets": [0x74]},
    "health": {"offsets": [0x190, 0x0, 0x138]},
    "maxHealth": {"offsets": [0x190, 0x0, 0x13c]},
    "animation": {"offsets": [0x190, 0x18, 0x40]},
    "x": {"offsets": [0x190, 0x68, 0x70]},
    "y": {"offsets": [0x190, 0x68, 0x78]},
    "z": {"offsets": [0x190, 0x68, 0x74]},
    "isDead": {"offsets": [0x58, 0xc8, 0x24]},
}

class GameAccessor:
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.__process = pymem.Pymem("eldenring.exe")
        self.__process_id = self.__process.process_id
        self.__process_base = self.__process.base_address
        self.__physics_pointer = 0x0
        self.__is_paused = False
        self.__gravity = True
        self.enemies = {}

    def find_bases(self) -> None:
        """
        Finds all essential base pointers in the game.

        Args:
            None

        Returns:
            None
        """
        for key in bases.keys():
            pattern = [int(x, 16) for x in bases[key]["aob"].split(" ")]
            mask = bases[key]["mask"]
            addr = AOBScanner.FindPattern(self.__process_id, 'eldenring.exe', self.__process_base, pattern, mask, 0, 0)
            offset = mm.read_memory_int(self.__process, addr + bases[key]["offset"])
            address = mm.read_memory(self.__process, addr + offset + bases[key]["additional"])
            bases[key]["address"] = address

        pattern = [int(x, 16) for x in "80 BB 28 01 00 00 00 0F 84".split()]
        mask = "xxxxxxxxx"
        self.__physics_pointer = AOBScanner.FindPattern(self.__process_id, 'eldenring.exe', self.__process_base, pattern, mask, 0, 0)

    def find_player_addrs(self) -> None:
        """
        Finds all player addresses.

        Args:
            None

        Returns:
            None
        """
        for key in player_addrs_loc.keys():
            base_addr = player_addrs_loc[key]["base"]
            offsets = player_addrs_loc[key]["offsets"]
            addr = bases[base_addr]["address"]
            for offset in range(len(offsets) - 1):
                addr = mm.read_memory(self.__process, addr + offsets[offset])
            player_addrs_loc[key]["address"] = addr + offsets[-1]

    def get_player_dead(self) -> bool:
        c = str(mm.read_memory_bytes(self.__process, player_addrs_loc["playerDead"]["address"], 1))
        c = '0'+ c[3:-1]
        h = BitArray(hex=c)
        return h.bin

    def get_player_health(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerHealth"]["address"])

    def get_player_max_health(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerMaxHealth"]["address"])

    def get_player_fp(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerFP"]["address"])

    def get_player_max_fp(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerMaxFP"]["address"])

    def get_player_stamina(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerStamina"]["address"])

    def get_player_max_stamina(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerMaxStamina"]["address"])

    def get_player_coords(self) -> tuple:
        x = mm.read_memory_float(self.__process, player_addrs_loc["playerX"]["address"])
        y = mm.read_memory_float(self.__process, player_addrs_loc["playerY"]["address"])
        z = mm.read_memory_float(self.__process, player_addrs_loc["playerZ"]["address"])
        return (x, y, z)

    def get_player_rotation(self) -> tuple:
        cos = mm.read_memory_float(self.__process, player_addrs_loc["playerCos"]["address"])
        sin = mm.read_memory_float(self.__process, player_addrs_loc["playerSin"]["address"])
        return (cos, sin)

    def get_player_animation(self) -> int:
        return mm.read_memory_int(self.__process, player_addrs_loc["playerAnimation"]["address"])

    def toggle_gravity(self) -> None:
        """
        Toggles gravity for the player, used for teleporting.

        Args:
            None

        Returns:
            None
        """
        if self.__gravity:
            mm.write_memory_int(self.__process, player_addrs_loc["playerGravity"]["address"], 1)
            self.__gravity = False
        else:
            mm.write_memory_int(self.__process, player_addrs_loc["playerGravity"]["address"], 0)
            self.__gravity = True

    def loading_state(self) -> bool:
        """
        Reads the cutsceneLoading pointer and returns True if the game is in a cutscene/loading state

        Args:
            None

        Returns:
            True if game is in cutscene/loading state, False otherwise (bool)
        """
        return (mm.read_memory_bytes(self.__process, player_addrs_loc["cutsceneLoading"]["address"], 1, True) != 0)

    def pause_game(self) -> None:
        """
        Pauses and unpauses the game physics

        Args:
            None

        Returns:
            None
        """

        if self.__is_paused:
            mm.write_byte(self.__process, self.__physics_pointer + 0x6, b'\x00')
        else:
            mm.write_byte(self.__process, self.__physics_pointer + 0x6, b'\x01')

        self.__is_paused = not self.__is_paused

    def find_enemies(self) -> None:
        p = bases["WorldChrManAlt"]["address"]
        begin = mm.read_memory(self.__process, p + 0x1f1b8)
        end = mm.read_memory(self.__process, p + 0x1f1c0)
        characters = (end - begin) // 8

        for i in range(characters):
            addr = mm.read_memory(self.__process, begin + i * 8)
            tb = mm.read_memory_bytes(self.__process, addr + 0x74, 2)
            gid = int(struct.unpack('>H', tb)[0].to_bytes(2, byteorder='little').hex(), 16)

            if gid == 0xB026:
                print("Found Enemy")
                self.find_enemy_addrs(addr)
                return

    def find_enemy_addrs(self, base) -> None:
        self.enemies[base] = {}
        for key in enemy_addrs_loc.keys():
            offsets = enemy_addrs_loc[key]["offsets"]
            addr = base
            for offset in range(len(offsets) - 1):
                addr = mm.read_memory(self.__process, addr + offsets[offset])
            self.enemies[base][key] = addr + offsets[-1]
            print(f"Found {key}: {hex(addr + offsets[-1])}")

    def get_enemy_health(self) -> list:
        health = []
        for key in self.enemies.keys():
            health.append(mm.read_memory_int(self.__process, self.enemies[key]["health"]))
        return health

    def get_enemy_max_health(self) -> list:
        health = []
        for key in self.enemies.keys():
            health.append(mm.read_memory_int(self.__process, self.enemies[key]["maxHealth"]))
        return health

    def get_enemy_id(self) -> list:
        id = []
        for key in self.enemies.keys():
            id.append(mm.read_memory_int(self.__process, self.enemies[key]["ID"]))
        return id

    def get_global_id(self, integer: bool = False) -> list:
        id = []
        for key in self.enemies.keys():
            tb = mm.read_memory_bytes(self.__process, self.enemies[key]["globalID"], 2)
            if integer:
                id.append(int(struct.unpack('>H', tb)[0].to_bytes(2, byteorder='little').hex(), 16))
            else:
                id.append(struct.unpack('>H', tb)[0].to_bytes(2, byteorder='little').hex())
        return id

    def get_enemy_animation(self) -> list:
        animation = []
        for key in self.enemies.keys():
            animation.append(mm.read_memory_int(self.__process, self.enemies[key]["animation"]))
        return animation

    def get_enemy_coords(self) -> list:
        coords = []
        for key in self.enemies.keys():
            x = mm.read_memory_int(self.__process, self.enemies[key]["x"])
            y = mm.read_memory_int(self.__process, self.enemies[key]["y"])
            z = mm.read_memory_int(self.__process, self.enemies[key]["z"])
            coords.append([x, y, z])
        return coords

    def get_enemy_dead(self) -> list:
        dead = []
        for key in self.enemies.keys():
            c = mm.read_memory_bytes(self.__process, self.enemies[key]["isDead"], 1, True)
            dead.append(c > 0)
        return dead

if __name__ == "__main__":
    ...