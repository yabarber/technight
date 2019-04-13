import random
import math
from playsound import playsound


class mazeObject:
    allObj = []
    chance = 0

    def __init__(self, symbol='', name='', filename='', attacked=None):
        self.symbol = symbol
        self.name = name
        self.filename = filename
        self.attacked = attacked
        mazeObject.allObj.append(self)

    def sound(self):
        playsound(self.filename + '.mp3')


class playerClass(mazeObject):
    def __init__(self):
        super().__init__('@', 'player')


class wallClass(mazeObject):
    chance = 3

    def __init__(self):
        super().__init__('.', 'wall')

    def breakSound(self):
        playsound()


class trapClass(mazeObject):
    chance = 10

    def __init__(self):
        super().__init__('#', 'trap')


class monsterClass(mazeObject):
    chance = 20

    def __init__(self):
        super().__init__('M', 'monster')
        self.direction = random.randint(0, 3)

    def update(self, board, y, x):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][self.direction]
        board.moveObj(y, x, (y + change[0]) % board.size, x + (change[1]) % board.size)


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
                for obj in mazeObject.__subclasses__():
                    if obj.chance != 0 and not bool(random.randint(0, obj.chance)) and b[y][x] is None:
                        b[y][x] = obj()
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
        desty = desty % self.size
        destx = destx % self.size
        temp = self.board[desty][destx]
        if temp is not None:
            self.board[desty][destx] = temp.attacked
        else:
            self.board[desty][destx] = self.board[targety][targetx]
            self.board[targety][targetx] = None
        return temp

    def movePlayer(self, direction, p, look=True):
        look = False
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        y, x = self.getCoords(p)
        out = self.moveObj(y, x, y + change[0], x + change[1])
        if look:
            for i in range(4):
                self.inspect(i, p)
        return out

    def inspect(self, direction, p):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        y, x, = self.getCoords(p)
        target = self.board[(y + change[0]) % self.size][(x + change[1]) % self.size]
        if target is not None:
            print(target.name)
        else:
            print('There is nothing here.')

    def getCoords(self, obj):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == obj:
                    return y, x

    def getObjAtCoords(self, y, x):
        return self.board[y][x]

    def updateLevel(self):
        for y in range(self.size):
            for x in range(self.size):
                if type(self.board[y][x]) == monsterClass:
                    self.board = self.board[y][x].update(self, y, x)

player = playerClass()
testLevel = levelClass(5, player)
testLevel.prettyPrint()

while True:
    action = input().lower()
    if action in ['w', 'd', 's', 'a']:
        direction = ['w', 'd', 's', 'a'].index(action)
        t = testLevel.movePlayer(direction, player)
        if type(t) == goalClass:
            testLevel = levelClass(testLevel.difficulty + 1, player)
        else:
            print(testLevel.board)
            testLevel.updateLevel()
    elif action in ['i', 'l', 'k', 'j']:
        direction = ['i', 'l', 'k', 'j'].index(action)
        testLevel.inspect(direction, player)
    testLevel.prettyPrint()
