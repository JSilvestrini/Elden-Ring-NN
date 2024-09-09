import time
import os.path
import memory_access

class GameAccessor:
    def __init__(self):
        self.__isPaused = False

        self.__targetedEnemyPointer = 0x0
        self.__bossAnimationPointer = 0x0
        self.__bossHealthPointer = 0x0
        self.__bossMaxHealthPointer = 0x0

        self.__gamePhysicsPointer = 0x0

        self.__worldPointer = 0x0
        self.__localPlayerPointer = 0x0
        self.__playerAnimationPointer = 0x0
        self.__playerHealthPointer = 0x0
        self.__playerMaxHealthPointer = 0x0
        self.__playerStaminaPointer = 0x0
        self.__playerMaxStaminaPointer = 0x0
        self.__playerFPPointer = 0x0
        self.__playerMaxFPPointer = 0x0

        self.get_memory_values()

    def get_memory_values(self):

        with open('place_cheat_table_here/PlayerDead.txt', 'w') as file:
            file.write('1')

        while not os.path.isfile('place_cheat_table_here/DataWritten.txt'):
            time.sleep(1.0)
            print("Waiting")

        self.findGamePhysics()
        self.findWorldPointer()
        self.findTargetedEnemy()

        self.__localPlayerPointer = memory_access.read_memory('eldenring.exe', (self.__worldPointer + 0x10ef8))

        zeroXten = memory_access.read_memory('eldenring.exe', self.__localPlayerPointer)
        oneninety = memory_access.read_memory('eldenring.exe', zeroXten + 0x190)
        zero = memory_access.read_memory('eldenring.exe', oneninety)
        self.__playerHealthPointer = zero + 0x138
        self.__playerMaxHealthPointer = zero + 0x13c
        self.__playerFPPointer = zero + 0x148
        self.__playerMaxFPPointer = zero + 0x14c
        self.__playerStaminaPointer = zero + 0x154
        self.__playerMaxStaminaPointer = zero + 0x158

        fiveeight = memory_access.read_memory('eldenring.exe', zeroXten + 0x58)
        ten = memory_access.read_memory('eldenring.exe', fiveeight + 0x10)
        onenine = memory_access.read_memory('eldenring.exe', ten + 0x190)
        eighteen = memory_access.read_memory('eldenring.exe', onenine + 0x18)
        self.__playerAnimationPointer = eighteen + 0x40

        # boss
        # animation
        a = memory_access.read_memory('eldenring.exe', self.__targetedEnemyPointer + 0x190)
        b = memory_access.read_memory('eldenring.exe', a + 0x18)
        self.__bossAnimationPointer = b + 0x40

        # health
        c = memory_access.read_memory('eldenring.exe', a)
        self.__bossHealthPointer = c + 0x138

        # max health
        self.__bossMaxHealthPointer = c + 0x13c

        os.remove('place_cheat_table_here/DataWritten.txt')
        os.remove('place_cheat_table_here/TargetPointer.txt')
        os.remove('place_cheat_table_here/WorldChrManPointer.txt')
        os.remove('place_cheat_table_here/PausePointer.txt')
        os.remove('place_cheat_table_here/PlayerDead.txt')

    def bossAnimationAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__bossAnimationPointer)

    def bossHealthAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__bossHealthPointer)

    def bossMaxHealthAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__bossMaxHealthPointer)

    def playerAnimationAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerAnimationPointer)

    def playerHealthAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerHealthPointer)

    def playerStaminaAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerStaminaPointer)

    def playerFPAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerFPPointer)

    def playerMaxHealthAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxHealthPointer)

    def playerMaxStaminaAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxStaminaPointer)

    def playerMaxFPAccess(self):
        return memory_access.read_memory_i('eldenring.exe', self.__playerMaxFPPointer)

    def findGamePhysics(self):
        self.__gamePhysicsPointer = memory_access.read_cheat_engine_file('PausePointer.txt')

    def findTargetedEnemy(self):
        self.__targetedEnemyPointer = memory_access.read_cheat_engine_file('TargetPointer.txt')

    def findWorldPointer(self):
        self.__worldPointer = memory_access.read_cheat_engine_file('WorldChrManPointer.txt')

    def PauseGame(self):
        while (self.__gamePhysicsPointer == None):
            self.findGamePhysics()

        if self.__isPaused:
            memory_access.write_byte('eldenring.exe', self.__gamePhysicsPointer + 0x6, b'\x00')
        else:
            memory_access.write_byte('eldenring.exe', self.__gamePhysicsPointer + 0x6, b'\x01')

        self.__isPaused = not self.__isPaused

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    game = GameAccessor()
    print(game.bossAnimationAccess())
    print(game.bossMaxHealthAccess())