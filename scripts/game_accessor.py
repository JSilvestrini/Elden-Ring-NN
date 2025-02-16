from scripts.build import AOBScanner
import struct

bases = {
    "WorldChrMan": {"aob": "48 8B 05 00 00 00 00 48 85 C0 74 0F 48 39 88", "mask": "xxx????xxxxxxxx", "offset": 3, "additional": 7},
    "WorldChrManAlt": {"aob": "0F 10 00 0F 11 44 24 70 0F 10 48 10 0F 11 4D 80 48 83 3D", "mask": "xxxxxxxxxxxxxxxxxxx", "offset": 19, "additional": 24},
    "GameDataMan": {"aob": "48 8B 05 00 00 00 00 48 85 C0 74 05 48 8B 40 58 C3 C3", "mask": "xxx????xxxxxxxxxxx", "offset": 3, "additional": 7},
    "NetManImp": {"aob": "48 8B 05 00 00 00 00 80 78 00 00 00 00 48 8D 9F 00 00 00 00 48 8B 03", "mask": "xxx????xx?x??xxx????xxx", "offset": 3, "additional": 7},
    "EventFlagMan": {"aob":"48 8B 3D 00 00 00 00 48 85 FF 00 00 32 C0 E9", "mask": "xxx????xxx??xxx", "offset": 3, "additional": 7},
    "FieldArea": {"aob":"48 8B 0D 00 00 00 00 48 00 00 00 44 0F B6 61 00 E8 00 00 00 00 48 63 87 00 00 00 00 48 00 00 00 48 85 C0", "mask": "xxx????x???xxxx?x????xxx????x???xxx", "offset": 3, "additional": 7},
}

# NoDead            world, localPLayer, 0, 190, 0, 119b, bit 0
# NoDamage          dhfajkdhfkajhdfkjahdkjfhadkljfhakl   bit 1
# InfiniteFP        jkahdsfkjhakjdfhakjdfhkajdhfkljahd   bit 2
# InfiniteStamina   asdjkhfkjahdfkljahldjkfhlakjdfhkaj   bit 3
# InfiniteGoods     world, 1e508, 0, 522                 bit 0

player_addrs_loc = {
    "playerDead": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x1c5]},
    "playerHealth": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x138]},
    "playerMaxHealth": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x13c]},
    "playerFP": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x148]},
    "playerMaxFP": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x14c]},
    "playerStamina": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x154]},
    "playerMaxStamina": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x0, 0x158]},
    "playerAnimation": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x80, 0x90]},
    "playerAnimationSpeed": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x28, 0x17C8]},
    "playerX": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x70]},
    "playerY": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x74]},
    "playerZ": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x78]},
    "playerCos": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x54]},
    "playerSin": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x5c]},
    "playerGravity": {"base" : "WorldChrMan", "offsets" : [0x10ef8, 0x0, 0x190, 0x68, 0x1d3]},
    "cutsceneLoading": {"base" : "EventFlagMan", "offsets" : [0x28, 0x113]}, # bit 7, true means cutscene
    "loadingScreen2": {"base": "EventFlagMan", "offsets": [0x28, 0x15195B]}, # bit 3, false means loading
    "healingFlask": {"base": "GameDataMan", "offsets": [0x8, 0x101]},
    "FPFlask": {"base": "GameDataMan", "offsets": [0x8, 0x102]},
    "leftItem": {"base": "GameDataMan", "offsets": [0x8, 0x399]},
    "rightItem": {"base": "GameDataMan", "offsets": [0x8, 0x39C]},
    "leftItem2": {"base": "GameDataMan", "offsets": [0x8, 0x3A0]},
    "rightItem2": {"base": "GameDataMan", "offsets": [0x8, 0x3A4]},
    "leftItem3": {"base": "GameDataMan", "offsets": [0x8, 0x3A8]},
    "rightItem3": {"base": "GameDataMan", "offsets": [0x8, 0x3AC]},
    "helmet": {"base": "GameDataMan", "offsets": [0x8, 0x3C8]},
    "chest": {"base": "GameDataMan", "offsets": [0x8, 0x3CC]},
    "arms": {"base": "GameDataMan", "offsets": [0x8, 0x3D0]},
    "leggings": {"base": "GameDataMan", "offsets": [0x8, 0x3D4]}
}

enemy_addrs_loc = {
    "ID": {"offsets": [0x28, 0x124]},
    "globalID": {"offsets": [0x74]},
    "paramID": {"offsets": [0x60]},
    "health": {"offsets": [0x190, 0x0, 0x138]},
    "maxHealth": {"offsets": [0x190, 0x0, 0x13c]},
    "animation": {"offsets": [0x190, 0x18, 0x40]},
    "animationSpeed": {"offsets": [0x190, 0x28, 0x17C8]},
    "x": {"offsets": [0x190, 0x68, 0x70]},
    "y": {"offsets": [0x190, 0x68, 0x74]},
    "z": {"offsets": [0x190, 0x68, 0x78]},
    "isDead": {"offsets": [0x58, 0xc8, 0x24]},
}

class GameAccessor:
    def __init__(self):
        self.__process_id = AOBScanner.getPID()
        self.__is_paused = False
        self.__gravity = True
        self.reset()

    def reset(self) -> None:
        self.__physics_pointer = 0x0
        self.enemies = {}
        self.find_bases()
        self.find_player_addrs()

    def clean(self) -> None:
        self.enemies = {}

    def get_process_id(self) -> int:
        return self.__process_id

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
            addr = AOBScanner.AOBScan(self.__process_id, 'eldenring.exe', pattern, mask, 0, 0)
            offset = AOBScanner.readInteger(self.__process_id, addr + bases[key]["offset"])
            address = AOBScanner.readLongLong(self.__process_id, addr + offset + bases[key]["additional"])
            bases[key]["address"] = address

        pattern = [int(x, 16) for x in "80 BB 28 01 00 00 00 0F 84".split()]
        mask = "xxxxxxxxx"
        self.__physics_pointer = AOBScanner.AOBScan(self.__process_id, 'eldenring.exe', pattern, mask, 0, 0)

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
                addr = AOBScanner.readLongLong(self.__process_id, addr + offsets[offset])
            player_addrs_loc[key]["address"] = addr + offsets[-1]

    def player_in_roundtable(self) -> bool:
        return (AOBScanner.readInteger(self.__process_id, bases["FieldArea"]["address"] + 0xE4) == 11100)

    def get_player_dead(self) -> bool:
        return self.get_player_health() <= 0

    def get_player_health(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerHealth"]["address"])

    def get_player_max_health(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerMaxHealth"]["address"])

    def kill_player(self) -> None:
        AOBScanner.writeInteger(self.__process_id, player_addrs_loc["playerHealth"]["address"], 0)

    def get_player_fp(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerFP"]["address"])

    def get_player_max_fp(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerMaxFP"]["address"])

    def get_player_stamina(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerStamina"]["address"])

    def get_player_max_stamina(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerMaxStamina"]["address"])

    def get_player_coords(self) -> tuple:
        x = AOBScanner.readFloat(self.__process_id, player_addrs_loc["playerX"]["address"])
        y = AOBScanner.readFloat(self.__process_id, player_addrs_loc["playerY"]["address"])
        z = AOBScanner.readFloat(self.__process_id, player_addrs_loc["playerZ"]["address"])
        return (x, y, z)

    def get_player_rotation(self) -> tuple:
        cos = AOBScanner.readFloat(self.__process_id, player_addrs_loc["playerCos"]["address"])
        sin = AOBScanner.readFloat(self.__process_id, player_addrs_loc["playerSin"]["address"])
        return (cos, sin)

    def get_player_animation(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["playerAnimation"]["address"])

    def get_player_heal_flask(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["healingFlask"]["address"])

    def get_player_fp_flask(self) -> int:
        return AOBScanner.readInteger(self.__process_id, player_addrs_loc["FPFlask"]["address"])

    def get_left_equipment(self) -> list:
        ret = [
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["leftItem"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["leftItem2"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["leftItem3"]["address"])
        ]

        return ret

    def get_right_equipment(self) -> list:
        ret = [
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["rightItem"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["rightItem2"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["rightItem3"]["address"])
        ]

        return ret

    def get_armor(self) -> list:
        ret = [
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["helmet"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["chest"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["arms"]["address"]),
            AOBScanner.readInteger(self.__process_id, player_addrs_loc["leggings"]["address"])
        ]

        return ret

    def toggle_gravity(self) -> None:
        """
        Toggles gravity for the player, used for teleporting.

        Args:
            None

        Returns:
            None
        """
        if self.__gravity:
            AOBScanner.writeInteger(self.__process_id, player_addrs_loc["playerGravity"]["address"], 1)
            self.__gravity = False
        else:
            AOBScanner.writeInteger(self.__process_id, player_addrs_loc["playerGravity"]["address"], 0)
            self.__gravity = True

    def loading_state(self):
        """
        Reads the cutsceneLoading pointer and returns True if the game is in a cutscene/loading state

        Args:
            None

        Returns:
            True if game is in cutscene/loading state, False otherwise (bool)
        """
        return (bin(AOBScanner.readBytes(self.__process_id, player_addrs_loc["loadingScreen2"]["address"], 1)[0]) == '0b0')

    def cutscene_state(self):
        return (bin(AOBScanner.readBytes(self.__process_id, player_addrs_loc["cutsceneLoading"]["address"], 1)[0])[2] == '1')

    def pause_game(self) -> None:
        """
        Pauses and unpauses the game physics

        Args:
            None

        Returns:
            None
        """

        if self.__is_paused:
            AOBScanner.writeBytes(self.__process_id, self.__physics_pointer + 0x6, 1, [int('0', 16)])
        else:
            AOBScanner.writeBytes(self.__process_id, self.__physics_pointer + 0x6, 1, [int('1', 16)])

        self.__is_paused = not self.__is_paused

    def stake_of_marika(self) -> bool:
        offsets =  [0x10ef8, 0x0, 0x178, 0x8]
        addr = bases["WorldChrMan"]["address"]
        for offset in offsets:
            addr = AOBScanner.readLongLong(self.__process_id, addr + offset)

        temp = addr
        try:
            for i in range(0, 15):
                for _ in range(0, i):
                    temp = AOBScanner.readLongLong(self.__process_id, temp + 0x30)
                if AOBScanner.readInteger(self.__process_id, temp + 0x8) == 26:
                    return True
        except:
            return False

    def set_animation_speed(self, speed: float) -> None:
        AOBScanner.writeFloat(self.__process_id, player_addrs_loc["playerAnimationSpeed"]["address"], speed)
        for e in self.enemies:
            AOBScanner.writeFloat(self.__process_id, self.enemies[e]["animationSpeed"], speed)

    def find_enemies(self, ids) -> None:
        #print(f"FINDING ENEMIES: {ids}")
        self.enemies = {} # remove old enemies incase there is a phase 2

        pattern = [int(x, 16) for x in bases["WorldChrManAlt"]["aob"].split(" ")]
        mask = bases["WorldChrManAlt"]["mask"]
        addr = AOBScanner.AOBScan(self.__process_id, 'eldenring.exe', pattern, mask, 0, 0)
        offset = AOBScanner.readInteger(self.__process_id, addr + bases["WorldChrManAlt"]["offset"])
        address = AOBScanner.readLongLong(self.__process_id, addr + offset + bases["WorldChrManAlt"]["additional"])
        bases["WorldChrManAlt"]["address"] = address

        p = bases["WorldChrManAlt"]["address"]
        begin = AOBScanner.readLongLong(self.__process_id, p + 0x1f1b8)
        end = AOBScanner.readLongLong(self.__process_id, p + 0x1f1c0)
        characters = (end - begin) // 8

        for i in range(characters):
            #print(f"Scanning Character {i}")
            addr = AOBScanner.readLongLong(self.__process_id, begin + i * 8)
            tb = AOBScanner.readInteger(self.__process_id, addr + 0x60)

            #print(f"Found GID: {hex(gid)}")
            if tb in ids:
                #print("Found Enemy")
                self.find_enemy_addrs(addr)
                ids.pop(ids.index(tb))

            if len(ids) == 0:
                break

    def find_enemy_addrs(self, base) -> None:
        self.enemies[base] = {}
        for key in enemy_addrs_loc.keys():
            offsets = enemy_addrs_loc[key]["offsets"]
            addr = base
            for offset in range(len(offsets) - 1):
                addr = AOBScanner.readLongLong(self.__process_id, addr + offsets[offset])
            self.enemies[base][key] = addr + offsets[-1]
            #print(f"Found {key}: {hex(addr + offsets[-1])}")

    def get_enemy_health(self) -> list:
        health = []
        for key in self.enemies.keys():
            health.append(AOBScanner.readInteger(self.__process_id, self.enemies[key]["health"]))
        return health

    def get_enemy_max_health(self) -> list:
        health = []
        for key in self.enemies.keys():
            health.append(AOBScanner.readInteger(self.__process_id, self.enemies[key]["maxHealth"]))
        return health

    def get_enemy_id(self) -> list:
        id = []
        for key in self.enemies.keys():
            id.append(AOBScanner.readInteger(self.__process_id, self.enemies[key]["ID"]))
        return id

    def get_global_id(self, integer: bool = False) -> list:
        id = []
        for key in self.enemies.keys():
            tb = bytes(AOBScanner.readBytes(self.__process_id, self.enemies[key]["globalID"], 2))
            if integer:
                id.append(int(struct.unpack('>H', tb)[0].to_bytes(2, byteorder='little').hex(), 16))
            else:
                id.append(struct.unpack('>H', tb)[0].to_bytes(2, byteorder='little').hex())
        return id

    def get_param_id(self) -> list:
        id = []
        for key in self.enemies.keys():
            id.append(AOBScanner.readInteger(self.__process_id, self.enemies[key]["paramID"]))
        return id

    def get_enemy_animation(self) -> list:
        animation = []
        for key in self.enemies.keys():
            animation.append(AOBScanner.readInteger(self.__process_id, self.enemies[key]["animation"]))
        return animation

    def get_enemy_coords(self) -> list:
        coords = []
        for key in self.enemies.keys():
            x = AOBScanner.readFloat(self.__process_id, self.enemies[key]["x"])
            y = AOBScanner.readFloat(self.__process_id, self.enemies[key]["y"])
            z = AOBScanner.readFloat(self.__process_id, self.enemies[key]["z"])
            coords.append([x, y, z])
        return coords

    def get_enemy_dead(self) -> list:
        dead = []
        for key in self.enemies.keys():
            c = AOBScanner.readBytes(self.__process_id, self.enemies[key]["isDead"], 1)[0]
            dead.append(c > 0)
        return dead

if __name__ == "__main__":
    pass