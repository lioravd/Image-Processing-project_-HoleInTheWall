import os, random


class Player:
    def __init__(self, _name, _num_of_players, frame):
        self.name = _name
        self.numOfPlayers = _num_of_players
        self.calibration_image = frame
        self.level = 0
        self.score = 0
        self.life = 3
        self.counter_success = 0
        self._baseDirOfWallsImages = None
        self._setOfWallsImages = []
        self._indexOfMask = 0
        self.speedDim = None

        print(f"Create new Player:\n{self.numOfPlayers} player, name: {self.name}\n")

    def setLevel(self, _level):
        self.level = _level

    def initWallsOfLevel(self, wallsImagesDict):
        path_of_walls = wallsImagesDict[self.numOfPlayers][self.level]
        self._baseDirOfWallsImages = path_of_walls
        self._setOfWallsImages = os.listdir(path_of_walls)
        random.shuffle(self._setOfWallsImages)

    def getNextMaskPath(self):
        next_mask_path = self._setOfWallsImages[self._indexOfMask]
        self._indexOfMask += 1
        return f"{self._baseDirOfWallsImages}/{next_mask_path}"

    def maskImagesIsEmpty(self):
        if self._indexOfMask == len(self._setOfWallsImages):
            return True
        else:
            return False