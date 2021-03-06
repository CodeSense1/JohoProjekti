# TIE-02102
# Joonas Kakkuri, joonas.kakkuri@tuni.fi, 274166
# Ilari Hauhia, ilari.hauhia@tuni.fi, 282273
# Skaalautuva projekti: Miinaharava



# Minesweeper tyylinen peli. Aluksi pelaaja valitsee vaikeustason easy/medium/hard
# tai vaihtoehtoisesti kenttään voi syöttää haluamansa luvut, kuitenkin pienin
# rajoittein: pelikentän tulee olla vähintään 5x5 kokoinen.
#
# Pelin kulku:
# Solua painamalla voit avata solun. Avatun solun numero kertoo, kuinka monta
# miinaa sitä ympäröi. Pelin voittaa, kun avaa kaikki solut, jotka eivät ole miinoja.
#
# Pelaamista helpottamiseksi voit asettaa kysymysmerkin solun päälle jotka
# voisivat olla miinoja. Merkin saat painamalla FLAG-nappia, jolloin sen väri muuttuu
# punaiseksi. Merkattuja soluja ei voi avata, eikä niitä oteta huomioon.


import tkinter as tk
from minesweeper import Minesweeper


class GUI():
    def __init__(self):
        """ Initialize game dimensions and select difficulty """
        self.__root = tk.Tk()

        # Set a static size
        self.__root.geometry("350x150")

        # Variables for board dimensions
        self.__width = tk.IntVar()
        self.__height = tk.IntVar()
        self.__minecount = tk.IntVar()

        # Create labels for menu
        tk.Label(self.__root, text="Enter the width:").grid(row=1, column=0)
        tk.Label(self.__root, text="Enter the height:").grid(row=2, column=0)
        tk.Label(self.__root, text="Enter the amount of mines:").grid(
            row=3, column=0)

        self.__errorLabel = tk.Label(self.__root, text="")
        self.__errorLabel.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        infoLabel = tk.Label(self.__root, text="")
        infoLabel.grid(row=0, column=1)

        # entries for game dimensions
        widthEntry = tk.Entry(self.__root, textvariable=self.__width)
        widthEntry.grid(row=1, column=1)

        heightEntry = tk.Entry(self.__root, textvariable=self.__height)
        heightEntry.grid(row=2, column=1)

        mineEntry = tk.Entry(self.__root, textvariable=self.__minecount)
        mineEntry.grid(row=3, column=1)

        # Buttons for difficulty
        easyBtn = tk.Button(self.__root, text="Easy",
                            command=self.easy)
        easyBtn.grid(row=1, column=2, sticky=tk.E)

        mediumBtn = tk.Button(self.__root, text="Medium", command=self.medium)
        mediumBtn.grid(row=2, column=2, sticky=tk.E)

        hardBtn = tk.Button(self.__root, text="Hard", command=self.hard)
        hardBtn.grid(row=3, column=2, sticky=tk.E)

        # Start button
        startBtn = tk.Button(self.__root, text="Start game",
                             command=self.setup, height=2, width=7)

        startBtn.grid(row=4, column=1, sticky=tk.W)

        self.__root.mainloop()

    def setup(self):
        """ Setup the game """
        try:
            # Check for valid input
            w = self.__width.get()
            h = self.__height.get()
            m = self.__minecount.get()

            if m < 0:
                self.__errorLabel.configure(text="Can't have negative mines!")
                return

            if w < 5 or h < 5:
                # Too small board
                self.__errorLabel.configure(
                    text="width/height must be over 5!")
                return

        except tk.TclError:
            # User entered invalid argument
            self.__errorLabel.configure(text="Invalid input!")

            return

        # desrtoy menu and start the game
        self.__root.destroy()
        self.__window = tk.Tk()
        self.__window.title("Minesweeper")

        # Initialize game
        self.__game = Minesweeper(
            self, self.__window, self.__width.get(), self.__height.get(), self.__minecount.get())

        l1 = tk.Label(self.__window, text="Options")
        l1.grid(row=0, column=0)

        self.__l2 = tk.Label(
            self.__window, text=":|")
        self.__l2.grid(row=1, column=self.__width.get() // 2, columnspan=5)

        # Create buttons
        self.createButtons()

        # Update game
        self.__game.update()
        self.updateText(self.__game.hasWon())

    def easy(self):
        """ Preset values for easy difficulty """
        self.__width.set(9)
        self.__height.set(9)
        self.__minecount.set(10)

    def medium(self):
        """ Preset values for medium difficulty """
        self.__width.set(16)
        self.__height.set(16)
        self.__minecount.set(40)

    def hard(self):
        """ Preset values for hard difficulty """
        self.__width.set(20)
        self.__height.set(20)
        self.__minecount.set(65)

    def start(self):
        """ Start the game """
        try:
            self.__window.mainloop()
        except AttributeError:
            # User exit the program, so nothing to loop over
            return

    def reset(self):
        """ Resets the game """
        # Set smiley face back to default
        self.__l2.configure(text=":|")
        # Hide all cells
        self.__game.hideAll()
        # Configure new board
        self.__game.initializeBoard()
        # Reset flag- button to default
        if self.__flagBtn.cget("bg") == "orange red":
            self.flag()

    def updateText(self, hasWon):
        """ Update smiley face """

        state = ":|"  # Default state
        if self.__game.lose():
            # Sad face, if game is over
            state = ":("
        elif hasWon:
            # Smiley face for victory
            state = ":)"

        # Show current state
        self.__l2.configure(text=state)

    def createButtons(self):
        """ Create buttons for the game window """

        # Flag - Button
        self.__flagBtn = tk.Button(
            self.__window, text="Flag OFF", command=self.flag, width=12)
        self.__flagBtn.grid(row=2, column=0)
        self.__flagBtn.configure(bg='grey63')

        # New game
        self.__newGameBtn = tk.Button(
            self.__window, text="New Game", command=self.newGame, width=12)
        self.__newGameBtn.grid(row=self.__height.get() - 1, column=0)
        # Reset - Button
        self.__resetBtn = tk.Button(
            self.__window, text="Reset game", command=self.reset, width=12)
        self.__resetBtn.grid(row=self.__height.get() - 2, column=0)

        # End - Button
        self.__endBtn = tk.Button(
            self.__window, text="QUIT", command=self.quitGame, width=12)
        self.__endBtn.grid(row=self.__height.get(), column=0)

    def quitGame(self):
        """ Quit the game """
        self.__window.destroy()

    def newGame(self):
        """ Setup new game """

        self.__window.destroy()  # Destroy current window
        self.__init__()  # Initialize new game

    def flag(self):
        """ Toggle flag state """
        # Toggle flag
        self.__game.toggleFlag()

        # Update flag color and text
        if self.__game.flag():
            self.__flagBtn.configure(bg='orange red', text="Flag ON")

        else:
            self.__flagBtn.configure(bg="grey", text="Flag OFF")


def main():

    game = GUI()
    game.start()


main()
