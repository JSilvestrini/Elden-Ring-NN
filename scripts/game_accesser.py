import json
from json import decoder

class GameAccessor:
    def __init__(self):
        self._isPaused = False

        self._targetedEnemyPointer = 0x0
        self._bossAnimationPointer = 0x0
        self._bossHealthPointer = 0x0

        self._gamePhysicsPointer = 0x0

        self._worldPointer = 0x0
        self._localPlayerPointer = 0x0
        self._playerAnimationPointer = 0x0
        self._playerHealthPointer = 0x0
        self._playerStaminaPointer = 0x0
        self._playerFPPointer = 0x0

    def BossAnimationAccess(self):
        ...

    def BossHealthAccess(self):
        ...

    def PlayerAnimationAccess(self):
        ...

    def PlayerHealthAccess(self):
        ...

    def PlayerStaminaAccess(self):
        ...

    def PlayerFPAccess(self):
        ...

    def PauseGame(self):
        ...

if __name__ == "__main__":
    # try and find the world pointer and get to player on start
    ...