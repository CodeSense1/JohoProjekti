
from cell import Cell
from random import randint
# This class holds data about minesweeper field


class Minesweeper():
    """
        Minesweeper is an object, that hold information about minesweeper game´s
        state. This is not responsible for displaying, it just holds essential
        information related to the game.
    """

    def __init__(self, master, width, height, mines):
        self.__master = master
        self.__width = width
        self.__height = height

        # Indicates wether the flag is on or off
        self.__flag = False
        self.__mines = mines

        # Initialize 2-dimensional data structure
        self.__board = [[None for i in range(
            self.__height)] for j in range(self.__width)]

        self.initializeBoard()  # Initialize and place Cells on correct positions

    def toggleFlag(self):
        """ Toggle wether player wants to flag cell of turn a cell """
        self.__flag = False if self.__flag else True

    def flag(self):
        return self.__flag

    def showAll(self):
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[i][j].show()

    def hideAll(self):
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[i][j].setState(False)

    def gameOver(self):

        self.showAll()

    def initializeBoard(self):
        """ Initialize the board with random minepositions """

        # Initialize random positions for mines
        minepos = []
        if self.__mines >= (self.__width * self.__height):
            # There are more or equal amount of mines than cells
            for i in range(self.__width):
                for j in range(self.__height):
                    minepos.append([i, j])

        else:
            while len(minepos) < self.__mines:

                pos = [randint(0, self.__width - 1),
                       randint(0, self.__height - 1)]
                if pos in minepos:
                    continue
                else:
                    minepos.append(pos)

        # Populate new board with Cells
        # TODO: Find a way that player doesn't lose on first turn
        for i in range(self.__width):
            for j in range(self.__height):
                if [i, j] in minepos:
                    state = True
                else:
                    state = False

                self.__board[i][j] = Cell(i, j, state, self.__master, self)

        # Get random Cells and convert them to mines.

        for i in range(self.__width):
            for j in range(self.__height):
                self.countNeighbours(i, j)

    def getMines(self):
        return [j for sub in self.__board for j in sub]

    def getFlaggedMines(self):
        flagged = 0
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__board[i][j].isFlag():
                    flagged += 1

        return flagged

    def getMineCount(self):
        """
        Returns how many mines are not revealed.
        """
        mineCount = 0
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__board[i][j].isMine():
                    mineCount += 1
        return mineCount

    def update(self):
        """ Update board """
        for i in range(self.__width):
            for j in range(self.__height):
                # Let's update this cell
                cell = self.__board[i][j]

                if cell.isRevealed():
                    if cell.getCellNumber() == 0:
                        # No mines nearby, so lets update surrounding neighbours
                        self.updateNeighbours(i, j)
                    else:
                        # cell has mine in its neighbour
                        cell.update()
                else:
                    cell.update()

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

                i = x + cellX
                j = y + cellY

                if i < 0 or j < 0:
                    # Eliminate case list[-1], which is not
                    # neighbour to this cell
                    continue

                try:

                    neighbour = self.__board[i][j]

                    if neighbour.isFlag():
                        # Neighbour is flagged, so we don't want to check it
                        continue

                    if neighbour.isMine():
                        self.gameOver()
                        return

                    # Check if neighbours neighbourcount is 0
                    if neighbour.getCellNumber() == 0 and not neighbour.isRevealed():
                        # Neighbour has no mines nearby, so we can reveal all its
                        # neighbours too.

                        neighbour.show()
                        self.updateNeighbours(i, j)
                    else:

                        # Show and update neighbour
                        neighbour.show()

                    neighbour.update()

                except IndexError:
                    continue

    def countNeighbours(self, x, y):
        """ Counts how many neighbours cell has and """

        cell = self.__board[x][y]
        if cell.isRevealed():
            return
        minecount = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    # We don't want to compare to ourself
                    continue
                if x + i < 0 or y + j < 0:
                    # We dont want to check for top and botton cells together
                    continue

                try:
                    neighbour = self.__board[x + i][y + j]
                    if neighbour.isMine():
                        minecount += 1
                        continue

                except IndexError:
                    # We are on the edge of the board, no neighbours there...
                    continue

        cell.setCellNumber(minecount)
