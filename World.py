
from random import randint

WUMPUS = "W"
GOLD = "G"
PIT = "P"
EMPTY = "-"
BREEZE = "B"
STENCH = "S"
OUT = "O"
AGENT = "A"

UP = (1, 0)
DOWN = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
MOVES = (UP, LEFT, RIGHT, DOWN)

class WorldCell:
    
    def __init__(self, content: str):
        self.value = content

class World:

    def __init__(self, dir: str):
        file = open(dir, "r")
        self.n = int(file.readline().replace("\n", ""))
        self.__map = [[WorldCell("-") for _ in range(self.n)] for _ in range(self.n)]
        self.agent = None
        for i in reversed(range(self.n)):
            line = file.readline().replace("\n", "").split(".")
            for j in range(self.n):
                if line[j] == AGENT:
                    self.__map[i][j].value = EMPTY
                    self.agent = [i, j]
                else:
                    self.__map[i][j] = WorldCell(line[j])
        file.close()

    def randInit(self) -> list:
        for _ in range(1000):
            x = randint(0, self.n - 1)
            y = randint(0, self.n - 1)
            if self.__map[x][y].value == EMPTY:
                return [x, y]
        return []
    
    def _cellState(self, x: int, y: int) -> list: # 0: cell content, 1: stench (if has), 2: breeze {if has}
        s = False
        b = False
        states = [self.__map[x][y].value]
        if x in range(0, self.n) and y in range(0, self.n):
            if self.__map[x][y].value in (WUMPUS, PIT):
                return [self.__map[x][y].value]   
        if x > 0:
            if self.__map[x - 1][y].value == WUMPUS:
                s = True
            if self.__map[x - 1][y].value == PIT:
                b = True
        if x < self.n - 1:
            if self.__map[x + 1][y].value == WUMPUS:
                s = True
            if self.__map[x + 1][y].value == PIT:
                b = True
        if y > 0:
            if self.__map[x][y - 1].value == WUMPUS:
                s = True
            if self.__map[x][y - 1].value == PIT:
                b = True
        if y < self.n - 1:
            if self.__map[x][y + 1].value == WUMPUS:
                s = True
            if self.__map[x][y + 1].value == PIT:
                b = True

        states.extend([STENCH, BREEZE] if s and b else [STENCH] if s else [BREEZE] if b else [])
        return states

    def move(self, move: tuple) -> list | None:
        if self.agent is None:
            print("You are dead!")
            return None
        # condition checking
        if move in MOVES:
            if self.agent == [0, 0] and move == DOWN:
                self.agent = None
                return [OUT]
            self.agent[0] += move[0]
            self.agent[1] += move[1]
            if self.agent[0] not in range(0, self.n) or self.agent[1] not in range(0, self.n):
                print("Invalid move!")
                self.agent[0] -= move[0]
                self.agent[1] -= move[1]
                return None
            # update map
            states = self._cellState(self.agent[0], self.agent[1])
            # Dead
            if states[0] in (WUMPUS, PIT):
                self.agent = None
                return states
            # Gold and Empty
            else:
                self.__map[self.agent[0]][self.agent[1]].value = EMPTY
                return states
        print("Invalid move!")
        return None
    
    def shoot(self, move: tuple) -> bool | None:
        if move in MOVES:
            x = self.agent[0] + move[0]
            y = self.agent[1] + move[1]
            if x not in range(0, self.n) or y not in range(0, self.n):
                return None
            if self.__map[x][y].value != WUMPUS:
                return False
            self.__map[x][y].value = EMPTY
            return True
        return None
    
    def isBorder(self, x: int, y: int) -> bool: # x, y is position base on the position of agent
        pos_x = self.agent[0] + x
        pos_y = self.agent[1] + y
        return (pos_x not in range(0, self.n) or pos_y not in range(0, self.n)) and (pos_x, pos_y) != (-1, 0) # skip exist move
    
    def printWorld(self) -> None:
        for i in reversed(range(self.n)):
            for j in range(self.n):
                if self.agent == [i, j]:
                    print(AGENT, end = " ")
                else:
                    print(self.__map[i][j].value, end = " ")
            print()
        print()
