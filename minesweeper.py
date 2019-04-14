
from cell import Cell
from random import randint
# This class holds data about minesweeper field


class Minesweeper():
    """
        Minesweeper is an object, that hold information about minesweeper game´s
        state. This is not responsible for displaying, it just holds essential
        information related to the game.
    """

    def __init__(self, window, master, width, height, mines):
        self.__window = window  # Instance of window object
        self.__master = master  # Master window, where elements are drawn
        self.__width = width    # Width of the board
        self.__height = height  # Height of the board
        self.__mines = mines    # Amount of mines on the field

        # Indicates wether the flag is on or off
        self.__flag = False
        self.__gameover = False
        self.__win = False
        self.__amountOfRevealedCells = 0

        # Initialize 2-dimensional data structure
        self.__board = [[None for _ in range(
            self.__width)] for _ in range(self.__height)]

        self.initializeBoard()  # Initialize and place Cells on correct positions

    def toggleFlag(self):
        """ Toggle wether player wants to flag cell of turn a cell """
        self.__flag = False if self.__flag else True

    # _______ Getters and Setters ___________
    def flag(self):
        """ Get current state of the flag """
        return self.__flag

    def win(self):
        """ Check if player has won the game """
        return self.__win

    def lose(self):
        """ Check if player has lost the game """
        return self.__gameover

    def showAll(self):
        """ Show all cells on the board """
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[i][j].show()

    def hideAll(self):
        """ Hide all cells on the board """
        self.__gameover = False
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[i][j].setState(False)

    def gameOver(self):
        """ End the game """
        self.__gameover = True
        self.showAll()

    def initializeBoard(self):
        """ Initialize the board with random minepositions """
        self.__gameover = False
        self.__amountOfRevealedCells = 0
        # Initialize random positions for mines
        minepos = []
        if self.__mines >= (self.__width * self.__height):
            # There are more or equal amount of mines than cells
            for i in range(self.__width):
                for j in range(self.__height):
                    minepos.append([i, j])

        else:
            while len(minepos) < self.__mines:
                # select unique random positions, where mines
                # will be placed
                pos = [randint(0, self.__width - 1),
                       randint(0, self.__height - 1)]
                if pos in minepos:
                    # There is already a mine in this cell
                    continue
                else:
                    # Store all positions for mines
                    minepos.append(pos)

        # Populate new board with Cells
        for i in range(self.__width):
            for j in range(self.__height):
                if [i, j] in minepos:

                    # Cell at i,j is mine
                    state = True
                else:
                    state = False

                # Update board
                self.__board[i][j] = Cell(
                    self.__window, i, j, state, self.__master, self)

        # Count neighbours, so amount of mines can be shown on
        # revealed cell
        for i in range(self.__width):
            for j in range(self.__height):
                self.countNeighbours(i, j)

    def getMines(self):
        """ Returns all mines as a 1d list """
        return [j for foo in self.__board for j in foo]

    def getFlaggedMines(self):
        """ Get amount of mines, that are marked with flag """
        flagged = 0
        # Loop over all the cells in the board
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__board[i][j].isFlag():
                    # This cell is flagged
                    flagged += 1

        return flagged

    def hasWon(self):
        """ Wether player has won the game """
        if self.__mines + self.__amountOfRevealedCells >= self.__height * self.__width and not self.__gameover:
            # All cells are revealed, except those that are mines
            return True
        else:
            return False

    def countRevealedNeighbours(self):
        self.__amountOfRevealedCells = 0
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__board[i][j].isRevealed():
                    self.__amountOfRevealedCells += 1

    def update(self):
        """ Update board """
        # Loop over every cell in the board
        for i in range(self.__width):
            for j in range(self.__height):
                # Let's update this cell
                cell = self.__board[i][j]

                if cell.isRevealed():
                    if not cell.isMine():
                        # cell is revealed and it's not mine
                        # This variable is used to check if player has
                        # won the game
                        self.countRevealedNeighbours()

                    if cell.getCellNumber() == 0:
                        self.countRevealedNeighbours()
                        # No mines nearby, so lets update surrounding neighbours
                        self.updateNeighbours(i, j)
                    else:
                        # cell has mine in its neighbour
                        cell.update()
                else:
                    # Cell is not revealed, but it may have flag
                    # so it must be updated
                    cell.update()
        # Update texts on the main window
        self.__window.updateText(self.hasWon())

    def updateNeighbours(self, cellX, cellY):
        """ Update neighbour cells around cellX and cellY
            :param cellX, cellY: Cell coordinates, which neighbours should be
                                 updated
            :return None:
        """
        # Get offset around current cell
        for x in range(-1, 2):
            for y in range(-1, 2):

                if x == 0 and y == 0:
                    # Update current cell
                    self.__board[cellX][cellY].update()
                    continue

                # Apply offset
                i = x + cellX
                j = y + cellY

                if i < 0 or j < 0:
                    # Eliminate case list[-1], which is not
                    # neighbour to this cell
                    continue

                try:
                    # This is the cell we want to update
                    neighbour = self.__board[i][j]

                    if neighbour.isFlag():
                        # Neighbour is flagged, so we don't want to check it
                        continue

                    if neighbour.isMine():
                        # Neighbour was mine...
                        self.gameOver()
                        return

                    # Check if neighbours neighbourcount is 0
                    if neighbour.getCellNumber() == 0 and not neighbour.isRevealed():
                        self.countRevealedNeighbours()
                        # Neighbour has no mines nearby, so we can reveal all its
                        # neighbours too.

                        neighbour.show()  # Show current neighbour

                        # Update other cells around this neighbour cell
                        self.updateNeighbours(i, j)
                    else:

                        # Show and update neighbour
                        neighbour.show()
                    # Finally update neighbour
                    neighbour.update()

                except IndexError:
                    # In case offset becomes too big i.e. We are trying to
                    # check cells on the positive border line
                    # There is no cells, so let's move on to the next one
                    continue

    def countNeighbours(self, x, y):
        """ Counts how many mines cell at x,y has
            :param x,y: Position in the board, i.e which cell we want to process

        """

        # Let's count this cell's neighbours
        cell = self.__board[x][y]
        if cell.isRevealed():
            # we dont need to process revealed cells
            return

        minecount = 0
        # Apply offset to x, y positions
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    # We don't want to compare to ourself
                    continue
                if x + i < 0 or y + j < 0:
                    # We dont want to check for top and botton cells together
                    continue

                try:
                    # This is the neighbour that we are checking
                    neighbour = self.__board[x + i][y + j]
                    if neighbour.isMine():
                        # If neighbour is mine, update minecount
                        minecount += 1
                        continue

                except IndexError:
                    # We are on the edge of the board, no neighbours there...
                    continue
        # Set number of mines that cell has in its neighbours
        cell.setCellNumber(minecount)
