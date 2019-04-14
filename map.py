import random
from playsound import playsound
from gtts import gTTS


class mazeObject:
    allObj = []
    chance = 0

    def __init__(self, symbol='', name='', monstersCanKill=True):
        self.symbol = symbol
        self.name = name
        self.monstersCanKill = monstersCanKill
        mazeObject.allObj.append(self)

    def attacked(self, b, y, x):
        b.board[y][x] = None

    def sound(self, direction):
        try:
            direction = ['Forward', 'Right', 'Forward', 'Left'][direction]
            # print(self.name + direction + '.mp3')
            playsound(self.name + direction + '.mp3')
        except:
            pass


class playerClass(mazeObject):
    def __init__(self):
        super().__init__('@', 'Player')

    def sound(self, direction):
        playsound('Walk' + str(random.randint(1, 2)) + '.mp3')


class wallClass(mazeObject):
    chance = 3

    def __init__(self):
        super().__init__('.', 'Wall')

    # def breakSound(self):
    #     playsound()


class rockClass(mazeObject):
    chance = 10

    def __init__(self):
        super().__init__('#', 'Rock')

    def sound(self, direction):
        playsound('Walk2.mp3')
        playsound('Walk2.mp3')
        playsound('Walk2.mp3')

    def attacked(self, b, y, x):
        pass


class monsterClass(mazeObject):
    chance = 20

    def __init__(self, symbol='M', name='Monster'):
        super().__init__(symbol, name)
        self.direction = random.randint(0, 3)

    def update(self, board, y, x, p, rot=1):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][self.direction]
        obj = board.moveObj(y, x, (y + change[0]) % board.size, (x + change[1]) % board.size)
        if obj is not None and not obj.monstersCanKill:
            self.direction = (self.direction + rot) % 4
        if board.getCoords(p) is None:
            return None


class goalClass(mazeObject):
    def __init__(self):
        super().__init__('O', 'Goal', monstersCanKill=False)
        self.locked = True


class keyClass(mazeObject):
    keyAdj = ['Fuzzy', 'Jagged', 'Scented', 'Smooth', 'Slippery']

    for adj in keyAdj:
        tts = gTTS(text=adj + ' key', lang='en')
        tts.save(adj + 'Key' + '.mp3')
    playsound('FuzzyKey.mp3')

    def __init__(self):
        super().__init__(';', 'Key', monstersCanKill=False)
        self.adj = random.choice(keyClass.keyAdj)

    def attacked(self, b, y, x):
        b.board[y][x] = monsterClass()
        b.board[b.goalCoords[0]][b.goalCoords[1]].locked = False

    def sound(self, direction):
        playsound(self.adj + 'Key.mp3')


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
        y1, x1, y2, x2 = [random.randint(0, self.size - 1) for _ in range(4)]
        while (y1 == self.playerStart and x1 == self.playerStart) or (y2 == self.playerStart and x2 == self.playerStart) or [y1, x1] == [y2, x2]:
            y1, x1, y2, x2 = [random.randint(0, self.size - 1) for _ in range(4)]
        self.goalCoords = (y1, x1)
        b[y1][x1] = goalClass()
        b[y2][x2] = keyClass()

    def prettyPrint(self):
        for row in self.board:
            for obj in row:
                if obj is None:
                    print(levelClass.emptyChar, end=levelClass.spaceChar)
                else:
                    print(obj.symbol, end=levelClass.spaceChar)
            print()

    def moveObj(self, targety, targetx, desty, destx):
        desty %= self.size
        destx %= self.size
        temp = self.board[desty][destx]
        if type(temp) != goalClass:
            if temp is not None:
                temp.attacked(self, desty, destx)
            else:
                self.board[desty][destx] = self.board[targety][targetx]
                self.board[targety][targetx] = None
        return temp

    def movePlayer(self, direction, p):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        y, x = self.getCoords(p)
        out = self.moveObj(y, x, y + change[0], x + change[1])
        return out

    def inspectAdjacents(self, p):
        for i in range(4):
            self.inspect(i, p)

    def inspect(self, direction, p):
        change = [[-1, 0], [0, 1], [1, 0], [0, -1]][direction]
        try:
            y, x, = self.getCoords(p)
        except TypeError:
            return
        target = self.board[(y + change[0]) % self.size][(x + change[1]) % self.size]
        if target is not None:
            target.sound(direction)
        else:
            playsound('Walk1.mp3')

    def getCoords(self, obj):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == obj:
                    return y, x
        return None

    def getObjAtCoords(self, y, x):
        return self.board[y][x]

    def updateLevel(self, p):
        for y in range(self.size):
            for x in range(self.size):
                if type(self.board[y][x]) == monsterClass:
                    if self.board[y][x].update(self, y, x, p) is None:
                        return None


player = playerClass()
testLevel = levelClass(5, player)
testLevel.prettyPrint()


while True:
    action = input().lower()
    if action in ['w', 'd', 's', 'a']:
        direction = ['w', 'd', 's', 'a'].index(action)
        t = testLevel.movePlayer(direction, player)
        if type(t) == goalClass and not t.locked:
            testLevel = levelClass(testLevel.difficulty + 1, player)
            testLevel.inspectAdjacents(player)
        else:
            testLevel.updateLevel(player)
            testLevel.inspectAdjacents(player)
        testLevel.prettyPrint()
    elif action in ['i', 'l', 'k', 'j']:
        direction = ['i', 'l', 'k', 'j'].index(action)
        testLevel.inspect(direction, player)
    if testLevel.getCoords(player) is None:
        break
print('You died')
