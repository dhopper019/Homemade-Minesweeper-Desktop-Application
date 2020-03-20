class Square():

    
    def __init__(self):
        self.isMine = False
        self.adjacentMines = 0
        self.isRevealed = False
        self.isFlagged = False
        self.isFirst = False

    def getIsMine(self):
        return self.isMine
    
    def setIsMine(self):
        self.isMine = True

    def incrementAdjacentMines(self):
        self.adjacentMines += 1

    def getAdjacentMines(self):
        return self.adjacentMines

    def setIsRevealed(self):
        self.isRevealed = True
        self.isFlagged = False

    def getIsRevealed(self):
        return self.isRevealed

    def setIsFlagged(self):
        if (self.isFlagged == False):
            self.isFlagged = True
        else:
            self.isFlagged = False

    def getIsFlagged(self):
        return self.isFlagged

    def setIsFirst(self):
        self.isFirst = True

    def getIsFirst(self):
        return self.isFirst

    def setButton(self, button):
        self.button = button

    def getButton(self):
        return self.button