import random
import math
from soundPlayer import *


class mazeObject:
    allObj = []

    def __init__(self, symbol='', name=''):
        self.symbol = symbol
        self.name = name
        mazeObject.allObj.append(self)


class playerClass(mazeObject):
    def __init__(self):
        super().__init__('@', 'player')


class wallClass(mazeObject):
    def __init__(self):
        super().__init__('.')


class goalClass(mazeObject):
    def __init__(self):
        super().__init__('O', 'down staircase')


class levelClass:
    spaceChar = ' '
    emptyChar = ' '

    def __init__(self, difficulty, p):
        self.difficulty = difficulty
        self.size = difficulty // 3 + int(not bool(difficulty // 3 % 2)) + 3
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.playerStart = 0
        b = self.board
        for y in range(self.size):
            for x in range(self.size):
                if not bool(random.randint(0, int(1 + math.pow(2, 4 - difficulty)))):
                    b[y][x] = wallClass()
        b[self.playerStart][self.playerStart] = p
        y, x = [random.randint(0, self.size - 1) for _ in range(2)]
        while y == self.playerStart and x == self.playerStart:
            y, x = [random.randint(0, self.size - 1) for _ in range(2)]
        b[y][x] = goalClass()

    def prettyPrint(self):
        for row in self.board:
            for obj in row:
                if obj is None:
                    print(levelClass.emptyChar, end=levelClass.spaceChar)
                else:
                    print(obj.symbol, end=levelClass.spaceChar)
            print()

    def moveObj(self, targety, targetx, desty, destx):
        temp = self.board[desty][destx]
        if type(self.board[desty][destx]) != wallClass:
            self.board[desty][destx] = self.board[targety][targetx]
            self.board[targety][targetx] = None
        else:
            self.board[desty][destx] = None
        return temp

    def movePlayer(self, direction, p):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        y, x = self.getCoords(p)
        return self.moveObj(y, x, y + change[0], x + change[1])

    def inspect(self, direction, p):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        y, x, = self.getCoords(p)
        target = self.board[y + change[0]][x + change[1]]
        if target is not None:
            print(self.board[y + change[0]][x + change[1]].name)
        else:
            print('There is nothing here.')

    def getCoords(self, obj):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == obj:
                    return y, x

    def getObjAtCoords(self, y, x):
        return self.board[y][x]


player = playerClass()
testLevel = levelClass(5, player)
testLevel.prettyPrint()
print('---------------------------')


while True:
    action = input().lower()
    if action in ['w', 'd', 's', 'a']:
        direction = ['w', 'd', 's', 'a'].index(action)
        t = testLevel.movePlayer(direction, player)
        if type(t) == goalClass:
            testLevel = levelClass(testLevel.difficulty + 1, player)
    elif action in ['i', 'l', 'k', 'j']:
        direction = ['i', 'l', 'k', 'j'].index(action)
        testLevel.inspect(direction, player)
    testLevel.prettyPrint()
