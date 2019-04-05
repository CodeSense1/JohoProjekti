
from cell import Cell
# This class holds data about minesweeper field


class Minesweeper():

    def __init__(self, width, height, mines):
        self.__width = width
        self.__height = height

        self.__mines = mines

        self.__board = [Cell(0, 0, False)] * (width * height + width)
        self.initializeBoard()

    def initializeBoard(self):
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[j * self.__height + i] = Cell(i, j, False)

    def getMines(self):
        mineCount = 0
        for i in range(self.__width):
            for j in range(self.__height):
                if self.__board[j * self.__height + i].isMine():
                    mineCount += 1
        return mineCount

    def printBoard(self):
        for i in range(self.__width):
            for j in range(self.__height):
                print(self.__board[j * self.__height + i])
