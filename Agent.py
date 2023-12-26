import queue
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
        print("Wumpus:", self.hasWumpus, "Pit:", self.hasPit, "Visited:", self.visited)
        
class Agent:

    def __init__(self, world: World) -> None:
        self.pos = [10, 10] # pos in knowledge, not in world
        self.world = world
        self.knowledge = [[KnowledgeCell() for _ in range(0, 21)] for _ in range(0, 21)]
        states = world._cellState(world.agent[0], world.agent[1])
        self.__logic(self.pos[0], self.pos[1], states)
        self.score = 0
        self.gold = 0.75
        self.knowledge[self.pos[0]][self.pos[1]].hasWumpus = False
        self.knowledge[self.pos[0]][self.pos[1]].hasPit = False
        self.knowledge[self.pos[0]][self.pos[1]].visited = True

    def __nextCell(self, x: int, y: int) -> list:
        return [(x + move[0], y + move[1]) for move in MOVES if x + move[0] in range(0, 21) and y + move[1] in range(0, 21) and self.world.isBorder(move[0], move[1]) is False]

    def __logic(self, x: int, y: int, states) -> None:
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
            states = self.world.move(move)
            # Invalid move
            if states is None:
                return None
            # Valid move
            self.pos[0] += move[0]
            self.pos[1] += move[1]
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
            self.knowledge[self.pos[0] + move[0]][self.pos[1] + move[1]].hasWumpus = False
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
                self.knowledge[i][j].print()

    def printXYKnowledge(self, x, y) -> None:
        print("(", x, ",", y, ")", sep="")
        self.knowledge[x][y].print()

    def findUnvisitedCell(self, killWUmpus: bool) -> tuple:
        queue = [self.pos]
        visited = set()
        visited.add(tuple(self.pos))
        path = [[None for _ in range(0, 21)] for _ in range(0, 21)]
        path[self.pos[0]][self.pos[1]] = self.pos

        while len(queue) > 0:
            current = queue.pop(0)
            # print("Current:", current)
            if self.knowledge[current[0]][current[1]].visited is False and self.knowledge[current[0]][current[1]].hasWumpus == killWUmpus:
                return current, path
            nextCells = self.__nextCell(current[0], current[1])
            for cell in nextCells:
                if cell not in visited and self.knowledge[cell[0]][cell[1]].hasPit is False:
                    if killWUmpus == False:
                        if self.knowledge[cell[0]][cell[1]].hasWumpus is not False:
                            continue
                    elif killWUmpus == True:
                        if self.knowledge[cell[0]][cell[1]].hasWumpus is True:
                            self.printXYKnowledge(cell[0], cell[1])
                    # print(" Next cell:", cell)
                    path[cell[0]][cell[1]] = current
                    queue.append(cell)
                    visited.add(tuple(cell))
        
        return None, None
    
    def moveToward(self) -> tuple:
        newPos, path = self.findUnvisitedCell(killWUmpus = False)
        if newPos is None:
            return False
        
        q = queue.LifoQueue()
        while newPos != self.pos:
            q.put(newPos)
            newPos = path[newPos[0]][newPos[1]]
            
        while q.qsize() > 0:
            next = q.get()
            nextMove = (next[0] - self.pos[0], next[1] - self.pos[1])
            self.move(nextMove)
            print("Now at:", self.pos, " Score:", self.score)
            self.world.printWorld()
        
        return True

    def moveTowardShoot(self) -> tuple:
        print("Shoot")
        newPos, path = self.findUnvisitedCell(killWUmpus = True)
        if newPos is None:
            return False
        
        q = queue.LifoQueue()
        while newPos != self.pos:
            q.put(newPos)
            newPos = path[newPos[0]][newPos[1]]
            
        while q.qsize() > 0:
            next = q.get()
            nextMove = (next[0] - self.pos[0], next[1] - self.pos[1])
            if q.qsize() == 1:
                self.shoot(nextMove)
            self.move(nextMove)
            print("Now at:", self.pos, " Score:", self.score)
            self.world.printWorld()

        return True
    
    def exit(self) -> None:
        print("Exit")
        self.score += 10
        self.world.agent = None

    def printVisitedKnowledge(self) -> None:
        for i in range(0, 21):
            for j in range(0, 21):
                if self.knowledge[i][j].visited:
                    self.printXYKnowledge(i, j)

    def printScore(self) -> None:
        print("Score:", self.score)