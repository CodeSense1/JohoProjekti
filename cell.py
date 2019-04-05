

class Cell():

    def __init__(self, x, y, flag):
        self.__x = x
        self.__y = y
        self.__flag = flag
        self.__isRevealed = False

    def __str__(self):
        return "x: {}, y: {}, is mine: {}".format(self.__x, self.__y, self._Cell__flag)

    def isMine(self):
        return self.__flag

    def show(self):
        self.__isRevealed = True
