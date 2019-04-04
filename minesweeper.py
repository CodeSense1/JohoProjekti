
from cell import Cell
# This class holds data about minesweeper field


class Minesweeper():

    def __init__(self, iWidth, iHeight):
        self.__width = iWidth
        self.__height = iHeight

        self.__board = [[0 for i in range(iWidth)] for j in range(iHeight)]
        self.initializeBoard()

    def initializeBoard(self):
        for i in range(self.__width):
            for j in range(self.__height):
                self.__board[i][j] = Cell(i, j, False)

    def printBoard(self):
        for i in range(self.__width):
            for j in range(self.__height):
                print(self.__board[i][j])
