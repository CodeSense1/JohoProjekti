import tkinter as tk
from minesweeper import Minesweeper

# Minesweeper

# TODO: 1. Handle errorreus inputs
#       2. New game - button and implementation
#       3. Scoring system
#       4. Proper documentation


class GUI():
    def __init__(self):
        """ Initialize game dimensions and select difficulty """
        self.__root = tk.Tk()

        self.__width = tk.IntVar()
        self.__height = tk.IntVar()
        self.__minecount = tk.IntVar()

        tk.Label(self.__root, text="Enter the width:").grid(row=1, column=0)
        tk.Label(self.__root, text="Enter the height:").grid(row=2, column=0)
        tk.Label(self.__root, text="Enter the amount of mines:").grid(row=3, column=0)

        infoLabel = tk.Label(self.__root, text="")
        infoLabel.grid(row=0, column=1)

        widthEntry = tk.Entry(self.__root, textvariable=self.__width)
        widthEntry.grid(row=1, column=1)

        heightEntry = tk.Entry(self.__root, textvariable=self.__height)
        heightEntry.grid(row=2, column=1)

        mineEntry = tk.Entry(self.__root, textvariable=self.__minecount)
        mineEntry.grid(row=3, column=1)

        startBtn = tk.Button(self.__root, text="Start game",
                             command=self.setup)
        startBtn.grid(row=4, column=1)

        self.__root.mainloop()

    def setup(self):
        """ Setup the game """
        self.__root.destroy()
        self.__window = tk.Tk()
        self.__game = Minesweeper(
            self.__window, self.__width.get(), self.__height.get(), self.__minecount.get())
        self.__l1 = tk.Label(
            self.__window, text="Mines on the field: " + str(self.__game.getMineCount()))
        self.__l1.grid(row=0, column=0)

        # Create buttons
        self.createButtons()

        # Update game
        self.__game.update()

    def start(self):
        try:
            self.__window.mainloop()
        except AttributeError:
            # User exit the program, so nothing to loop over
            return

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
        self.__resetBtn.grid(row=3, column=0)

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


def main():

    game = GUI()
    game.start()


main()
