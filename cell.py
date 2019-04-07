import tkinter as tk


# Could this inherit from tkinter.Button?

class Cell():

    def __init__(self, x, y, mineState, master, gameInstance):

        # Reference to minesweeper game object
        self.__gameInstance = gameInstance

        # Reference to window object, where Cells are drawn
        self.__master = master

        # Cell object is basicly Button with extra methods
        self.__btn = tk.Button(self.__master, text=" ", command=self.press)
        self.__btn.grid(row=1+x, column=1+y)
        self.__btn.configure(width=3, height=2)

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

    def setState(state):
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

        self.__btn.configure(text=self.__txt)

    def press(self):
        """ Behavior that happens when Cell is pressed """

        if self.__gameInstance.flag():
            self.__flag = False if self.__flag else True

        elif self.__mine:
            self.show()
            self.__gameInstance.showAll()
            # GAME OVER!

        elif self.__isRevealed:
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
