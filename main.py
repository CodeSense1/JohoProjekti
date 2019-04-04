import tkinter as tk
from minesweeper import Minesweeper

# Minesweeper


class GUI():
    def __init__(self, boardSizeX, boardSizeY):
        self.__window = tk.Tk()
        self.__cCountX = boardSizeX
        self.__cCountY = boardSizeY
        self.__cellButtons = []
        # Make a board
        self.initializeBoard()

    def initializeBoard(self):

        for i in range(self.__cCountX):
            for j in range(self.__cCountY):
                # Set the grid for every button
                self.__cellButtons.append(tk.Button(self.__window, text="0").grid(row=i, column=j))
                # self.__cellButtons[i * self.__cCountY + j].grid(row=i, column=j)

    def start(self):
        self.__window.mainloop()


def main():
    game = Minesweeper(9, 9)
    gui = GUI(9, 9)
    gui.start()


main()
