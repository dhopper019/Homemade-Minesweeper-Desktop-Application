import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import messagebox as mBox
from tkinter import Toplevel
from tkinter.font import Font
from MineSweeperGUIComp import MineSweeper
import time
from threading import Thread

class GUI():
    '''
    Constructor method for the class that sets up a beginner's game right as the application is opened.
	@param self - represents the instance the method is called
    '''
    def __init__(self):
        #Set Up using beginner's game coordinates
        self.gameRad = 0

        # Create instance
        self.setUp(9, 9, 10)

    def setUp(self, height, width, mines):
        # Create instance
        self.win = tk.Tk()           

        # Add row title       
        self.win.title("Minesweeper")   

        self.mSweeper = MineSweeper(height, width, mines)

        self.firstRevealPending = True

        self.gameProgress = "in_session"

        self.createWidgets()

        self.win.resizable(0, 0)

        self.win.wm_minsize(275,0)

        self.win.mainloop()

    def gameClass(self):
        gameWindow = Toplevel(self.win)
        gameWindow.resizable(0, 0)
        gameWindow.grab_set()
        gameWindow.title("Game Settings")
        self.gameRadVar = tk.IntVar(gameWindow)
        self.gameRadVar.set(0)
        self.gameRad = 0
        self.newGameButton.configure(command= lambda continueVar=True: self._quit(continueVar))

        def gameRadCall():
            if self.gameRadVar.get() == 0: self.gameRad = 0
            elif self.gameRadVar.get() == 1: self.gameRad = 1
            elif self.gameRadVar.get() == 2: self.gameRad = 2
            elif self.gameRadVar.get() == 3: self.gameRad = 3            

        def game_quit():
            gameWindow.quit()
            gameWindow.destroy()

        def newGameCommand():
            if (self.gameRadVar.get() == 3):
                if (self.customEntryCheck() == False):
                    gameWindow.withdraw()
                    cGEError = mBox.showerror(title='Custom Game Entry Error', message='Invalid custom entry for setting up a game. Read the Setup Help for details on how to properly set up the game.')
                    gameWindow.deiconify()
                    return
            game_quit()
            self._quit(True)

        def createGameWidgets():
            gameFrame = ttk.LabelFrame(gameWindow)
            gameFrame.grid(column=0, row=0)
            buttonFrame = ttk.LabelFrame(gameWindow)
            buttonFrame.grid(column=0, row=1)

            gameOptions = ["Beginner", "Intermediate", "Expert", "Custom"]

            gameText = [["Height", "Width", "Mines"], [9, 9, 10], [16, 16, 40], [16, 30, 99]]

            for i in range(len(gameText)):
                for j in range(len(gameText[i])):
                    curGameText = tk.Label(gameFrame, text=gameText[i][j])
                    curGameText.grid(column=j+1, row=i, sticky=tk.W)
            
            self.customHeight = tk.StringVar(gameWindow, value="20")
            customHeightEntered = ttk.Entry(gameFrame, width=3, textvariable=self.customHeight)
            customHeightEntered.grid(column=1, row=4, sticky=tk.W)

            self.customWidth = tk.StringVar(gameWindow, value="30")
            customWidthEntered = ttk.Entry(gameFrame, width=3, textvariable=self.customWidth)
            customWidthEntered.grid(column=2, row=4, sticky=tk.W)

            self.customMines = tk.StringVar(gameWindow, value="145")
            customMinesEntered = ttk.Entry(gameFrame, width=3, textvariable=self.customMines)
            customMinesEntered.grid(column=3, row=4, sticky=tk.W)

            newGame = ttk.Button(buttonFrame, text="New Game", command=newGameCommand)
            newGame.grid(column=0, row=0)

            setupHelp = ttk.Button(buttonFrame, text="Setup Help", command=setupHelpClass)
            setupHelp.grid(column=1, row=0)

            # Creating all three Radiobutton widgets within one loop
            for i in range(len(gameOptions)):
                curGameRad = tk.Radiobutton(gameFrame, text=gameOptions[i], variable=self.gameRadVar, value=i, command=gameRadCall)
                curGameRad.grid(column=0, row=i+1, sticky=tk.W)
                if (i == 0):
                    curGameRad.select()
            
        def setupHelpClass():
            setupHelpWindow = Toplevel(gameWindow)
            setupHelpWindow.resizable(0, 0)
            setupHelpWindow.grab_set()
            setupHelpWindow.title("Setup Help")

            def destroySetupHelpWindow():
                gameWindow.grab_set()
                setupHelpWindow.destroy()                
            
            def createSetupHelp():
                introductoryFrame = ttk.LabelFrame(setupHelpWindow)
                introductoryFrame.grid(column=0, row=0)
                gridLayoutFrame = ttk.LabelFrame(setupHelpWindow)
                gridLayoutFrame.grid(column=0, row=1)
                otherRulesFrame = ttk.LabelFrame(setupHelpWindow)
                otherRulesFrame.grid(column=0, row=2)


                introductoryText = tk.Label(introductoryFrame, text="Here are the rules by which you may set up a custom game by:")
                introductoryText.grid(column=0, row=0)
                gridLayoutText = tk.Label(gridLayoutFrame, text="Grid Layout: ")
                gridLayoutText.grid(column=1, row=0)
                minimumText = tk.Label(gridLayoutFrame, text="Minimum:")
                minimumText.grid(column=1, row=1)
                maximumText = tk.Label(gridLayoutFrame, text="Maximum:")
                maximumText.grid(column=2, row=1)
                heightText = tk.Label(gridLayoutFrame, text="Height:")
                heightText.grid(column=0, row=2)
                widthText = tk.Label(gridLayoutFrame, text="Width:")
                widthText.grid(column=0, row=3)
                minesText = tk.Label(gridLayoutFrame, text="Mines:")
                minesText.grid(column=0, row=4)
                minHeightText = tk.Label(gridLayoutFrame, text="4")
                minHeightText.grid(column=1, row=2)
                maxHeightText = tk.Label(gridLayoutFrame, text="30")
                maxHeightText.grid(column=2, row=2)
                minWidthText = tk.Label(gridLayoutFrame, text="4")
                minWidthText.grid(column=1, row=3)
                maxWidthText = tk.Label(gridLayoutFrame, text="30")
                maxWidthText.grid(column=2, row=3)
                minMinesText = tk.Label(gridLayoutFrame, text="3")
                minMinesText.grid(column=1, row=4)
                maxMinesText = tk.Label(gridLayoutFrame, text="300")
                maxMinesText.grid(column=2, row=4)
                thirdRule = tk.Label(otherRulesFrame, text="There must be no more than a third of the grid covered with mines.")
                thirdRule.grid(column=0, row=0)
                digitRule = tk.Label(otherRulesFrame, text="NOTE: All entry boxes must contain digits only.")
                digitRule.grid(column=0, row=1)
            
            createSetupHelp()
            setupHelpWindow.protocol("WM_DELETE_WINDOW", destroySetupHelpWindow)
            #setupHelpWindow.mainloop()

        createGameWidgets()
        #gameWindow.mainloop()

        #self.crementMineCounter(self.field[playerInput[1]][playerInput[0]].getIsFlagged())
    
    def customEntryCheck(self):
    #Causes of errors:
        #1 Non-digit characters
        if ((self.customHeight.get().isdigit() and self.customWidth.get().isdigit() and self.customMines.get().isdigit()) == False):
            return False
        #2 Minimum of 4 in terms of height and width and number of mines must be at least 3
        elif (((int(self.customHeight.get()) >= 4) and (int(self.customWidth.get()) >= 4) and (int(self.customMines.get()) >= 3)) == False):
            return False
        #3 Maximum of 30x30 and maximum of 300 mines
        elif (((int(self.customHeight.get()) <= 30) and (int(self.customWidth.get()) <= 30) and (int(self.customMines.get()) <= 300)) == False):
            return False
        #4 More than a third of the field is made up of mines
        elif ((int(self.customHeight.get()) * int(self.customWidth.get()))/(int(self.customMines.get())) < 3):
            return False
        else:
            return True

    def clickMeConfiguration(self, event, i, j, option):
        x = lambda row=i, column=j: self.clickMe(row, column, "Flag")
        x()

    def clickMe(self, row, column, option):
        if (self.gameProgress == "in_session"):
            if (self.firstRevealPending == True):
                if (option == "Reveal" and self.mSweeper.getField()[row][column].getIsFlagged() == False):
                    self.mSweeper.MarkFirstInputSquares(self.mSweeper.getField()[row][column], column, row)
                    self.mSweeper.SetMines()
                    self.mSweeper.getField()[row][column].setIsRevealed()
                    self.firstRevealPending = False
                    self.t0 = time.time()
                    self.timerThread = Thread(target=self.timerFunction, daemon=True)
                    self.timerThread.start()
                    if (self.mSweeper.getField()[row][column].getAdjacentMines() == 0 and self.mSweeper.getField()[row][column].getIsMine() == False):
                                #print(str(playerInput[0] - 1) + "," + str(playerInput[1] - 1))
                        self.mSweeper.RevealMultipleSquares(self.mSweeper.getField()[row][column], column, row)
                elif (option == "Flag" and self.mSweeper.getField()[row][column].getIsRevealed() == False):
                    self.mSweeper.getField()[row][column].setIsFlagged()
                    self.mSweeper.crementMineCounter(self.mSweeper.getField()[row][column].getIsFlagged())
            else:
                if (option == "Reveal" and self.mSweeper.getField()[row][column].getIsFlagged() == False):
                    self.mSweeper.getField()[row][column].setIsRevealed()
                    if (self.mSweeper.getField()[row][column].getAdjacentMines() == 0 and self.mSweeper.getField()[row][column].getIsMine() == False):
                                #print(str(playerInput[0] - 1) + "," + str(playerInput[1] - 1))
                        self.mSweeper.RevealMultipleSquares(self.mSweeper.getField()[row][column], column, row)
                elif (option == "Flag" and self.mSweeper.getField()[row][column].getIsRevealed() == False):
                    self.mSweeper.getField()[row][column].setIsFlagged()
                    self.mSweeper.crementMineCounter(self.mSweeper.getField()[row][column].getIsFlagged())
            
            self.mineCounterText.configure(text=str(self.mSweeper.getMineCounter()))
        
            if (self.mSweeper.CheckWinningConditions()):
                self.gameProgress = "won"
                self.mineCounterText.configure(text="0")
                self.progressText.configure(text="You Won")

            elif (self.mSweeper.CheckLosingConditions()):
                self.gameProgress = "lost"
                self.progressText.configure(text="You Lost")

            for i in range(len(self.mSweeper.getField())):
                for j in range(len(self.mSweeper.getField()[i])):
                    text = self.mSweeper.PrintButton(self.gameProgress, self.mSweeper.getField()[i][j])
                    self.mSweeper.getField()[i][j].getButton().configure(text=text[0], fg=text[1], bg=text[2], relief=text[3])

    def timerFunction(self):
        while ((self.gameProgress == "in_session") and (self.firstRevealPending == False) and (int(round((time.time() - self.t0), 0)) < 999)):
            time.sleep(1)
            if ((self.gameProgress == "in_session") and (self.firstRevealPending == False)): self.timer.configure(text=str(int(round((time.time() - self.t0), 0))))
        #if (self.firstRevealPending == True):
            #self.timer.configure(text="0")

    def _quit(self, continueVar):
        if (self.gameRad == 3 and continueVar):
            if (self.customEntryCheck() == False):
                cGEError = mBox.showerror(title='Custom Game Entry Error', message='Invalid custom entry for setting up a game. Read the Setup Help for details on how to properly set up the game.')
                return
        self.firstRevealPending = True
        self.win.quit()
        self.win.destroy()
        if (continueVar):
            if self.gameRad == 0: self.setUp(9, 9, 10)
            elif self.gameRad == 1: self.setUp(16, 16, 40)
            elif self.gameRad == 2: self.setUp(16, 30, 99)
            elif (self.gameRad == 3): self.setUp(int(self.customHeight.get()), int(self.customWidth.get()), int(self.customMines.get()))
    
    def createWidgets(self):
        self.HUDContainer = ttk.LabelFrame()
        self.HUDContainer.grid(column=0, row=0)        

        # We are creating row container frame to hold all other widgets
        self.minefieldContainer = ttk.LabelFrame()
        self.minefieldContainer.grid(column=0, row=1)        

        self.controlsContainer = ttk.LabelFrame()
        self.controlsContainer.grid(column=0, row=2)

        self.mineCounterText = tk.Label(self.HUDContainer, text=str(self.mSweeper.getMineCounter()), width=3)
        self.mineCounterText.grid(column=0, row=0)

        self.newGameButton = ttk.Button(self.HUDContainer, text="New Game", command= lambda continueVar=True: self._quit(continueVar))
        self.newGameButton.grid(column=1, row=0)

        '''
        if (self.gameFileAccessed):
            self.newGameButton = ttk.Button(self.HUDContainer, text="New Game", command= lambda continueVar=True, variable=self.gameRadVar.get(): self._quit(continueVar, variable))
            self.newGameButton.grid(column=1, row=0)

        else:
            self.newGameButton = ttk.Button(self.HUDContainer, text="New Game", command= lambda continueVar=True, variable=0: self._quit(continueVar, variable))
            self.newGameButton.grid(column=1, row=0)
        '''

        self.timer = tk.Label(self.HUDContainer, text="0", width=3)
        self.timer.grid(column=2, row=0)

        self.progressText = tk.Label(self.HUDContainer, text="In Progress", width=12)
        self.progressText.grid(column=1, row=1)

        for i in range(len(self.mSweeper.getField())):
            #self.action.append([])
            for j in range(len(self.mSweeper.getField()[i])):
                button = tk.Button(self.minefieldContainer, text=" ", fg="black", command= lambda row=i, column=j: self.clickMe(row, column, "Reveal"), width=1, bd=1, bg="gray95", relief="ridge")
                #def clickMeConfiguration(event):
                    #x = lambda row=i, column=j: self.clickMe(row, column, "Flag")
                    #x(i,j)
                button.bind("<Button-3>", lambda event, row=i, column=j: self.clickMeConfiguration(event, row, column, "Flag"))
                button.grid(column=j, row=i)
                self.mSweeper.getField()[i][j].setButton(button)
                #self.action[i].append(button)

                # Radiobutton list


        '''
        i = 1
        self.action1 = ttk.Button(self.monty, text="?", command= lambda row=i: self.clickMe(1,row))
        self.action1.grid(column=1, row=i)


        i = 2
        self.action2 = ttk.Button(self.monty, text="?", command= lambda row=i: self.clickMe(1,row))
        self.action2.grid(column=1, row=i)
        '''

        # Creating row Menu Bar ==========================================================
        menuBar = Menu()
        self.win.config(menu=menuBar)
        
        # Add menu items
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Game Settings", command=self.gameClass)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command= lambda row=False: self._quit(row))
        menuBar.add_cascade(label="File", menu=fileMenu)

gui = GUI()