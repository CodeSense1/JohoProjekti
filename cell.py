import tkinter as tk


# Could this inherit from tkinter.Button?

# Cell object is basically tkinter Button with couple of extra methods
# Each cell holds data about its state (mine of regular), it's position,
# is the cell revealed and is it marked with a flag
#
# Also each cell is used as a mousepressed event and therefore instances to
# minesweeper and window object are necessary.
# Cell is also responsible for drawing itself to the window, so it needs
# a reference to main window, so it can be drawn
#

class Cell():

    def __init__(self, window, x, y, mineState, master, gameInstance):

        # Reference to main window object
        self.__window = window
        # Reference to minesweeper game object
        self.__gameInstance = gameInstance

        # Reference to window object, where Cells are drawn
        self.__master = master

        # Cell object is basicly Button with extra methods
        # If I knew better what inheritance is, maybe this could be easier
        self.__btn = tk.Button(self.__master, text=" ",
                               width=2, command=self.press)
        self.__btn.grid(row=2 + x, column=1 + y)
        # self.__btn.configure()

        self.__x = x
        self.__y = y
        self.__txt = "0" if not mineState else "X"
        self.__neighbourMines = 0

        self.__mine = mineState
        self.__flag = False
        self.__isRevealed = False

    def __str__(self):
        """ In case you want to print Cell """
        return "x: {}, y: {}, is mine: {}".format(self.__x, self.__y, self.__mine)

    # _____ Getters and Setters _____

    def isFlag(self):
        return self.__flag

    def isRevealed(self):
        return self.__isRevealed

    def isMine(self):
        return self.__mine

    def setState(self, state):
        """ 
        Set wether this Cell should be mine or regular.
        Do not change Cell is already set!

        """
        self.__mine = state

    def setCellNumber(self, num):
        """ Set how many mines surround this Cell """
        self.__neighbourMines = num

        if self.__flag:
            self.__txt = "?"
        elif self.__mine:
            self.__txt = "X"
        else:
            self.__txt = str(num)

    def getCellNumber(self):
        """ Amount of mines that surround this Cell """
        return self.__neighbourMines

    def getText(self):
        """ Get text that is currently written in Cell """
        return self.__txt

    def update(self):
        """ Update this Cell """
        if self.__flag:
            self.__txt = "?"

        elif not self.__flag and not self.__isRevealed:
            self.__txt = " "
        elif self.__mine and self.__isRevealed:
            self.__txt = "X"

        elif self.__isRevealed:
            self.__txt = str(self.__neighbourMines)

            self.__btn.configure(bg="grey63")

        self.__btn.configure(text=self.__txt)

    def press(self):
        """ Behavior that happens when Cell is pressed """
        flagOn = self.__gameInstance.flag()
        if flagOn and not self.__isRevealed:
            # Clicked cell is not revealed, so a flag can be added
            self.__flag = False if self.__flag else True
            # Because flag is on, we don't want to continue

        elif self.__mine and not flagOn:
            self.show()
            self.__gameInstance.gameOver()
            # GAME OVER!

        elif self.__isRevealed and not flagOn:
            # We are already shown, so let's show the neighbours
            self.__gameInstance.updateNeighbours(self.__x, self.__y)

        else:
            self.show()
        self.__gameInstance.update()

    def show(self):
        """ 
        Reveal Cell, used when Cell should show, 
        but not necessarily being pressed 
        """
        self.__isRevealed = True
