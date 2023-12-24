
from World import World
from World import MOVES, WUMPUS, PIT, STENCH, BREEZE, GOLD
import random

class KnowledgeCell:

    def __init__(self, w: bool = None, p: bool = None, v: bool = False) -> None:
        self.hasWumpus = w
        self.hasPit = p
        self.visited = v
        self.content = []

    def print(self):
        print("Wumpus:", self.hasWumpus)
        print("Pit:", self.hasPit)
        print("Visited:", self.visited)

class Agent:

    def __init__(self, world: World) -> None:
        self.pos = [10, 10] # pos in knowledge, not in world
        self.world = world
        self.knowledge = [[KnowledgeCell() for _ in range(0, 21)] for _ in range(0, 21)]
        states = world._cellState(world.agent[0], world.agent[1])
        self.__logic(self.pos[0], self.pos[1], states)
        self.score = 0
        self.gold = 0.75

    def __nextCell(self, x: int, y: int) -> list:
        return [(x + move[0], y + move[1]) for move in MOVES if x + move[0] in range(0, 21) and y + move[1] in range(0, 21)]

    def __logic(self, x: int, y: int, states: list) -> None:
        if x in range(0, 21) and y in range(0, 21):
            updated = False
            self.knowledge[x][y].content = states[1:]
            nextCells = self.__nextCell(x, y)
            if STENCH not in states:
                for cell in nextCells:
                    self.knowledge[cell[0]][cell[1]].hasWumpus = False
            if BREEZE not in states:
                for cell in nextCells:
                    self.knowledge[cell[0]][cell[1]].hasPit = False
            if updated:
                self.__fullLogic()

    def __fullLogic(self) -> None:
        for i in range(0, 21):
            for j in range(0, 21):
                if BREEZE in self.knowledge[i][j].content:
                    nextCells = self.__nextCell(i, j)
                    for cell in nextCells:
                        if self.knowledge[cell[0]][cell[1]].hasPit is True:
                            break
                        if self.knowledge[cell[0]][cell[1]].hasPit is False:
                            nextCells.remove(cell)
                    if len(nextCells) == 1:
                        self.knowledge[nextCells[0][0]][nextCells[0][1]].hasPit = True
                if STENCH in self.knowledge[i][j].content: 
                    nextCells = self.__nextCell(i, j)
                    for cell in nextCells:
                        if self.knowledge[cell[0]][cell[1]].hasWumpus is True:
                            break
                        if self.knowledge[cell[0]][cell[1]].hasWumpus is False:
                            nextCells.remove(cell)
                    if len(nextCells) == 1:
                        self.knowledge[nextCells[0][0]][nextCells[0][1]].hasWumpus = True

    
    def move(self, move: tuple) -> bool | None: # True if not end else False, None if invalid
        if move in MOVES:
            with self.world.move(move) as states:
                # Invalid move
                if states is None:
                    return None
                self.score -= 10
                # check cell content
                if states[0] in (WUMPUS, PIT):
                    self.score -= 10000
                    return False
                if states[0] == GOLD:
                    self.score += 1000
                    self.gold += 1
                # Update knowledge
                self.__logic(self.pos[0], self.pos[1], states)
                self.knowledge[self.pos[0]][self.pos[1]].visited = True

    def shoot(self, move: tuple) -> bool | None:
        result = self.world.shoot(move)
        if result is None:
            return None
        else:
            self.score -= 100
            return result
        
    def isQuit(self) -> bool:
        # count moveable unvisited cells
        count = 0
        for i in range(21):
            for j in range(21):
                k = self.knowledge[i][j]
                if k.visited or k.hasPit is None or k.hasWumpus is None:
                    continue
                if k.hasWumpus:
                    count += 0.1
                elif not k.hasPit:
                    count += 1
        random.seed()
        randFactor = random.uniform(0.5, 1.5)
        return count*randFactor/self.gold < 1
    
    def printKnowledge(self) -> None:
        for i in range(0, 21):
            for j in range(0, 21):
                print("(", i, ",", j, ")", sep="")
                self.knowledge[i][j].print()
                print()
                print()

