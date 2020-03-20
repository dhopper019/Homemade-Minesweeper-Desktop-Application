import math
import time
import random
from Square import Square
from colorama import Fore, Back, Style

class MineSweeper():
    '''
    Constructor method to set up the game with the specified coordinates and the specified amount of mines
	@param self - points the instance the method is called
    @param height - the height of the field
    @param width - the width of the field
    @param mines - the number of mines in the field
    '''
    #Set up the game with the specified coordinates and the specified amount of mines
    def __init__(self, height, width, mines):
        self.fieldCoordinates = [height, width]
        #A constant variable telling how many mines there are in the game
        self.numberOfMines = mines
        #A variable that changes based on the number of flags set
        self.mineCounter = mines
        #Set up an empty field, then expand it to meet the size specified by the coordinates and assign a Square object to each coordinate
        self.field = []
        for row in range(self.fieldCoordinates[0]):
            self.field.append([])
            for column in range(self.fieldCoordinates[1]):
                self.field[row].append(Square())

    '''
    Populate some of the squares with the number of mines specified	
    @param self - points the instance the method is called
    '''
    def SetMines(self):
        randomCoordinates = [-1, -1]
        n = 0
        while (n < self.numberOfMines):
            randomCoordinates[0] = math.floor(random.random()*self.fieldCoordinates[1])
            randomCoordinates[1] = math.floor(random.random()*self.fieldCoordinates[0])
            #Check if there isn't a mine already assigned in the random coordinate, if not then assign one
            if (self.field[randomCoordinates[1]][randomCoordinates[0]].getIsMine() == False and self.field[randomCoordinates[1]][randomCoordinates[0]].getIsFirst() == False):
                self.field[randomCoordinates[1]][randomCoordinates[0]].setIsMine()
                n += 1
        #Finally, assign the number of adjacent mines to each square, so that the number of adjacent mines appears on each square that is not a mine, if there are any adjacent mines
        for row in range(len(self.field)):
            for column in range(len(self.field[0])):
                self.DetermineAdjacentMines(self.field[row][column], column, row)

    '''
    Determine the number of mines adjacent to the square by checking each of the adjacent squares, and then calling the incrementAdjacentMines method
    @param self - points the instance the method is called
    @param square - the square or coordinate that is being checked for the number of adjacent mines
    @param xCoordinate - the horizontal position/location of the square
    @param yCoordinate - the vertical position/location of the square
    '''
    def DetermineAdjacentMines(self, square, xCoordinate, yCoordinate):
        #Check the square to the top of the provided square
        if ((yCoordinate - 1) >= 0):
            if (self.field[(yCoordinate - 1)][(xCoordinate)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the top-right of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate + 1) < self.fieldCoordinates[1]):
            if (self.field[(yCoordinate - 1)][(xCoordinate + 1)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the right of the provided square
        if ((xCoordinate + 1) < self.fieldCoordinates[1]):
            if (self.field[(yCoordinate)][(xCoordinate + 1)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the bottom-right of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate + 1) < self.fieldCoordinates[1]):
            if (self.field[(yCoordinate + 1)][(xCoordinate + 1)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the bottom of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0]):
            if (self.field[(yCoordinate + 1)][(xCoordinate)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the bottom-left of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate - 1) >= 0):
            if (self.field[(yCoordinate + 1)][(xCoordinate - 1)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the left of the provided square
        if ((xCoordinate - 1) >= 0):
            if (self.field[(yCoordinate)][(xCoordinate - 1)].getIsMine()):
                square.incrementAdjacentMines()
        #Check the square to the top-left of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate - 1) >= 0):
            if (self.field[(yCoordinate - 1)][(xCoordinate - 1)].getIsMine()):
                square.incrementAdjacentMines()

    '''
    Changes the appearance of a square based on the game progress and whether the square is revealed
    @param self - points the instance the method is called
    @param gameProgress - states whether the game is still going ("in-session"), lost, or won
    @param square - the square whose appearance is to be changed
    '''
    def PrintButton(self, gameProgress, square):
        #First, give the default parameters for a square that isn't revealed
        symbol = "  "
        color = "black"
        background = "gray95"
        relief = "ridge"
        #if the square is revealed, impress it
        if (square.getIsRevealed() == True and square.getIsMine() == False):
            relief = "sunken"
            #Determine the number and the color of the number based on the amount of mines
            if (square.getAdjacentMines() == 0):
                symbol = "  "
            elif (square.getAdjacentMines() == 1):
                symbol = "1"
                color = "blue"
            elif (square.getAdjacentMines() == 2):
                symbol = "2"
                color = "green"
            elif (square.getAdjacentMines() == 3):
                symbol = "3"
                color = "red"
            elif (square.getAdjacentMines() == 4):
                symbol = "4"
                color = "cyan"
            elif (square.getAdjacentMines() == 5):
                symbol = "5"
                color = "brown"
            elif (square.getAdjacentMines() == 6):
                symbol = "6"
                color = "magenta"
            elif (square.getAdjacentMines() == 7):
                symbol = "7"
                color = "black"
            elif (square.getAdjacentMines() == 8):
                symbol = "8"
                color = "gray"
        #Else if the square is flagged - or is truly a mine and the game is won - or if the game is lost and it's flagged and it is a mine, print an 'f'
        elif ((square.getIsFlagged() == True and gameProgress == "in_session") or (square.getIsMine() == True and gameProgress == "won") or (square.getIsMine() == True and square.getIsFlagged() == True and gameProgress == "lost")):
            symbol = "f"
        #Else if print nothing, if the square hasn't been revealed and the game is in progress - or the square hasn't been revealed, isn't a mine, isn't flagged, and the game is lost
        elif ((square.getIsRevealed() == False and gameProgress == "in_session") or (square.getIsRevealed() == False and square.getIsMine() == False and square.getIsFlagged() == False and gameProgress == "lost")):
            symbol = "  "
        #Else if the square is flagged and is not a mine and the game is lost, print a red 'f'
        elif (square.getIsFlagged() == True and square.getIsMine() == False and gameProgress == "lost"):
            symbol = "f"
            color = "red"
        #Else if the square is a mine, isn't revealed, isn't flagged, and the game is lost, print an 'X' and impress the square
        elif (square.getIsMine() == True and square.getIsRevealed() == False and square.getIsFlagged() == False and gameProgress == "lost"): #NOTE: this happens when the game progress is lost and the square is NOT revealed
            symbol = "X"
            relief = "sunken"
        #Else if the square is a mine, is revealed, and the game is lost, print a red 'X' and impress the square
        elif (square.getIsMine() == True and square.getIsRevealed() == True and gameProgress == "lost"):
            symbol = "X"
            background = "red"
            relief = "sunken"
        return [symbol, color, background, relief]

    '''
    Recursive function that reveals multiple squares when needed
    @param self - points the instance the method is called
    @param square - the square or coordinate that is being revealed
    @param xCoordinate - the horizontal position/location of the square
    @param yCoordinate - the vertical position/location of the square
    '''
    def RevealMultipleSquares(self, square, xCoordinate, yCoordinate):
        '''
        Check if each square adjacent to the square given as a parameter exists on the field and has no adjacent mines and is not revealed or flagged
        If an adjacent square meets the condition above, reveal that square and make a recursive function call (RevealMultipleSquares) on it
        If an adjacent square doesn't have adjacent mines, but it has not been revealed or flagged, just reveal it
        Otherwise, move on to the next adjacent square without doing anything to the square being checked 
        '''
        #Check the square to the top of the provided square
        if ((yCoordinate - 1) >= 0):
            #print("Top: ")
            if (self.field[(yCoordinate - 1)][(xCoordinate)].getAdjacentMines() == 0 and self.field[(yCoordinate - 1)][(xCoordinate)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate - 1)][(xCoordinate)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate - 1)][(xCoordinate)], xCoordinate, (yCoordinate - 1))
            elif (self.field[(yCoordinate - 1)][(xCoordinate)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate - 1)][(xCoordinate)].setIsRevealed()
            else:
                pass
        #Check the square to the top-right of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate + 1) < self.fieldCoordinates[1]):
            #print("Top-right: ")
            if (self.field[(yCoordinate - 1)][(xCoordinate + 1)].getAdjacentMines() == 0 and self.field[(yCoordinate - 1)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate - 1)][(xCoordinate + 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate - 1)][(xCoordinate + 1)], (xCoordinate + 1), (yCoordinate - 1))
            elif (self.field[(yCoordinate - 1)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate - 1)][(xCoordinate + 1)].setIsRevealed()
            else:
                pass
        #Check the square to the right of the provided square
        if ((xCoordinate + 1) < self.fieldCoordinates[1]):
            #print("Right: ")
            if (self.field[(yCoordinate)][(xCoordinate + 1)].getAdjacentMines() == 0 and self.field[(yCoordinate)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate)][(xCoordinate + 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate)][(xCoordinate + 1)], (xCoordinate + 1), (yCoordinate))
            elif (self.field[(yCoordinate)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate)][(xCoordinate + 1)].setIsRevealed()
            else:
                pass
        #Check the square to the bottom-right of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate + 1) < self.fieldCoordinates[1]):
            #print("Bottom-right: ")
            if (self.field[(yCoordinate + 1)][(xCoordinate + 1)].getAdjacentMines() == 0 and self.field[(yCoordinate + 1)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate + 1)][(xCoordinate + 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate + 1)][(xCoordinate + 1)], (xCoordinate + 1), (yCoordinate + 1))
            elif (self.field[(yCoordinate + 1)][(xCoordinate + 1)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate + 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate + 1)][(xCoordinate + 1)].setIsRevealed()
            else:
                pass
        #Check the square to the bottom of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0]):
            #print("Bottom: ")
            if (self.field[(yCoordinate + 1)][(xCoordinate)].getAdjacentMines() == 0 and self.field[(yCoordinate + 1)][(xCoordinate)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate + 1)][(xCoordinate)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate + 1)][(xCoordinate)], (xCoordinate), (yCoordinate + 1))
            elif (self.field[(yCoordinate + 1)][(xCoordinate)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate + 1)][(xCoordinate)].setIsRevealed()
            else:
                pass
        #Check the square to the bottom-left of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate - 1) >= 0):
            #print("Bottom-left: ")
            if (self.field[(yCoordinate + 1)][(xCoordinate - 1)].getAdjacentMines() == 0 and self.field[(yCoordinate + 1)][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate + 1)][(xCoordinate - 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate + 1)][(xCoordinate - 1)], (xCoordinate - 1), (yCoordinate + 1))
            elif (self.field[(yCoordinate + 1)][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate + 1)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate + 1)][(xCoordinate - 1)].setIsRevealed()
            else:
                pass
        #Check the square to the left of the provided square
        if ((xCoordinate - 1) >= 0):
            #print("Left: ")
            if (self.field[(yCoordinate)][(xCoordinate - 1)].getAdjacentMines() == 0 and self.field[(yCoordinate)][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate)][(xCoordinate - 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate)][(xCoordinate - 1)], (xCoordinate - 1), (yCoordinate))
            elif (self.field[(yCoordinate )][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate)][(xCoordinate - 1)].setIsRevealed()
            else:
                pass
        #Check the square to the top-left of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate - 1) >= 0):
            #print("Top-left: ")
            if (self.field[(yCoordinate - 1)][(xCoordinate - 1)].getAdjacentMines() == 0 and self.field[(yCoordinate - 1)][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("If executes:")
                self.field[(yCoordinate - 1)][(xCoordinate - 1)].setIsRevealed()
                self.RevealMultipleSquares(self.field[(yCoordinate - 1)][(xCoordinate - 1)], (xCoordinate - 1), (yCoordinate - 1))
            elif (self.field[(yCoordinate - 1)][(xCoordinate - 1)].getIsRevealed() == False and self.field[(yCoordinate - 1)][(xCoordinate - 1)].getIsFlagged() == False):
                #print("Elif executes:")
                self.field[(yCoordinate - 1)][(xCoordinate - 1)].setIsRevealed()
            else:
                pass
    
    '''
    Marks the first square clicked and all its adjacent squares, so that the player doesn't lose the game on the first move and the player has at least all the marked squares revealed
    @param self - points the instance the method is called
    @param square - the first square or coordinate that is being revealed
    @param xCoordinate - the horizontal position/location of the first revealed square
    @param yCoordinate - the vertical position/location of the first revealed square
    '''
    def MarkFirstInputSquares(self, square, xCoordinate, yCoordinate):
        self.field[(yCoordinate)][(xCoordinate)].setIsFirst()
        #Check each adjacent to ensure it exists on the field, if it does, mark it
        #Check the square to the top of the provided square
        if ((yCoordinate - 1) >= 0):
            self.field[(yCoordinate - 1)][(xCoordinate)].setIsFirst()
        #Check the square to the top-right of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate + 1) < self.fieldCoordinates[1]):
            self.field[(yCoordinate - 1)][(xCoordinate + 1)].setIsFirst()
        #Check the square to the right of the provided square
        if ((xCoordinate + 1) < self.fieldCoordinates[1]):
            self.field[(yCoordinate)][(xCoordinate + 1)].setIsFirst()
        #Check the square to the bottom-right of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate + 1) < self.fieldCoordinates[1]):
            self.field[(yCoordinate + 1)][(xCoordinate + 1)].setIsFirst()
        #Check the square to the bottom of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0]):
            self.field[(yCoordinate + 1)][(xCoordinate)].setIsFirst()
        #Check the square to the bottom-left of the provided square
        if ((yCoordinate + 1) < self.fieldCoordinates[0] and (xCoordinate - 1) >= 0):
            self.field[(yCoordinate + 1)][(xCoordinate - 1)].setIsFirst()
        #Check the square to the left of the provided square
        if ((xCoordinate - 1) >= 0):
            self.field[(yCoordinate)][(xCoordinate - 1)].setIsFirst()
        #Check the square to the top-left of the provided square
        if ((yCoordinate - 1) >= 0 and (xCoordinate - 1) >= 0):
            self.field[(yCoordinate - 1)][(xCoordinate - 1)].setIsFirst()

    '''
    Check to see if the player has won the game
    @param self - points the instance the method is called
    '''
    def CheckWinningConditions(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if (self.field[i][j].getIsRevealed() == False and self.field[i][j].getIsMine() == False):
                    return False
        return True

    '''
    Check to see if the player has lost the game
    @param self - points the instance the method is called
    '''
    def CheckLosingConditions(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if (self.field[i][j].getIsRevealed() == True and self.field[i][j].getIsMine() == True):
                    return True
        return False

    '''
    Getter method for the entire field
    @param self - points the instance the method is called
    '''
    def getField(self):
        return self.field

    '''
    Increments or decrements the mine counter whenever a flag is placed or removed
    @param self - points the instance the method is called
    @param flag - boolean value to check whether the square is flagged
    '''
    def crementMineCounter(self, flag):
        #If a flag has been placed on the square, increment the mine counter, otherwise a flag was removed, so in that case decrement the mine counter
        if (flag):
            self.mineCounter -= 1
        else:
            self.mineCounter += 1

    '''
    Getter method for the mine counter
    @param self - points the instance the method is called
    '''
    def getMineCounter(self):
        return self.mineCounter


#mSweeper = MineSweeper()
#mSweeper.PlayGame()

