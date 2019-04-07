import tkinter as tk
from minesweeper import Minesweeper

# Minesweeper


class GUI():
    def __init__(self, boardSizeX, boardSizeY, mineCount):
        self.__window = tk.Tk()
        self.__game = Minesweeper(
            self.__window, boardSizeX, boardSizeY, mineCount)

        self.__width = boardSizeX
        self.__height = boardSizeY
        self.__l1 = tk.Label(
            self.__window, text="Mines left: " + str(self.__game.getMineCount()))
        self.__l1.grid(row=0, column=0)

        # Create buttons
        self.createButtons()

        # Update game
        self.__game.update()

    def start(self):
        self.__window.mainloop()

    def reset(self):
        self.__game.hideAll()
        self.__game.initializeBoard()
        if self.__flagBtn.cget("bg") == "red":
            self.flag()

    def createButtons(self):
        # Flag - Button
        self.__flagBtn = tk.Button(
            self.__window, text="Flag OFF", command=self.flag)
        self.__flagBtn.grid(row=1, column=0)
        self.__flagBtn.configure(bg='grey')

        # Reset - Button
        self.__resetBtn = tk.Button(
            self.__window, text="Reset game", command=self.reset)
        self.__resetBtn.grid(row=2, column=0)

        # End - Button
        self.__endBtn = tk.Button(
            self.__window, text="QUIT", command=self.quitGame)
        self.__endBtn.grid(row=4, column=0)

    def quitGame(self):
        self.__window.destroy()

    def flag(self):
        self.__game.toggleFlag()

        if self.__game.flag():
            self.__flagBtn.configure(bg='red', text="Flag ON")

        else:
            self.__flagBtn.configure(bg="grey", text="Flag OFF")


def menu():
    root = tk.Tk()

    tk.Label(root, text="Enter the width:").grid(row=0, column=0)
    tk.Label(root, text="Enter the height:").grid(row=1, column=0)
    tk.Label(root, text="Enter the amount of mines:").grid(row=2, column=0)

    width = tk.IntVar(value=None)
    widthEntry = tk.Entry(root,  textvariable=width)
    widthEntry.grid(row=0, column=1)

    height = tk.IntVar()
    heightEntry = tk.Entry(root, textvariable=height)
    heightEntry.grid(row=1, column=1)

    minecount = tk.IntVar()
    mineEntry = tk.Entry(root, textvariable=minecount)
    mineEntry.grid(row=2, column=1)

    startBtn = tk.Button(root, text="Start game",
                         command=lambda: root.destroy())
    startBtn.grid(row=3, column=2)
    root.mainloop()

    return width.get(), height.get(), minecount.get()


def main():

    w, h, m = menu()

    if m >= w*h / 10:
        # Too many mines...
        pass

    GRIDWIDTH = h
    GRIDHEIGHT = w
    MINES = m
    gui = GUI(GRIDWIDTH, GRIDHEIGHT, MINES)
    gui.start()


main()
