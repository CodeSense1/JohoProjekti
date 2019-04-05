import tkinter as tk
from minesweeper import Minesweeper

# Minesweeper


class GUI():
    def __init__(self, boardSizeX, boardSizeY, mineCount):
        self.__game = Minesweeper(boardSizeX, boardSizeY, mineCount)
        self.__window = tk.Tk()
        self.__cCountX = boardSizeX
        self.__cCountY = boardSizeY
        self.__cellButtons = {}
        self.__pressed = [0, 3]
        self.__l1 = tk.Label(self.__window, text="Mines left: " + str(self.__game.getMines()))
        self.__l1.grid(row=0, column=0, columnspan=4)
        # Make a board
        self.initializeBoard()

    def initializeBoard(self):
        # Really weird shit...
        for i in range(self.__cCountX):
            for j in range(self.__cCountY):
                btnToAdd = tk.Button(self.__window, text="   ").grid(row=1 + i, column=j)
                # Set the grid for every button
                self.__cellButtons[j * self.__cCountX + i] = btnToAdd

    def start(self):
        self.__window.mainloop()


def main():
    gui = GUI(9, 9, 10)
    gui.start()


main()
