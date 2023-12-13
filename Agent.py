
from World import World
from World import MOVES, WUMPUS, PIT, STENCH, BREEZE, GOLD

class KnowledgeCell:

    def __init__(self, w: bool = None, p: bool = None) -> None:
        self.hasWumpus = w
        self.hasPit = p

class Agent:

    def __init__(self, world: World) -> None:
        self.pos = world.agent
        self.knowledge = [[KnowledgeCell for _ in range(world.n)] for _ in range(world.n)]
        with world._cellState(self.pos[0], self.pos[1]) as states:
            self.__logic(self.pos[0], self.pos[1], states)
        self.world = world
        self.score = 0

    def __logic(self, x: int, y: int, states) -> None:
        if x in range(0, self.world.n) and y in range(0, self.world.n):
            nextCells = [(x + move[0], y + move[1]) for move in MOVES if x + move[0] in range(0, self.world.n) and y + move[1] in range(0, self.world.n)]
            if STENCH not in states:
                for cell in nextCells:
                    self.knowledge[cell[0]][cell[1]].hasWumpus = False
            if BREEZE not in states:
                for cell in nextCells:
                    self.knowledge[cell[0]][cell[1]].hasPit = False
    
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
                    self.score += 100
                # Update knowledge
                self.__logic(self.pos[0], self.pos[1], states)

    def shoot(self, move: tuple) -> bool | None:
        result = self.world.shoot(move)
        if result is None:
            return None
        else:
            self.score -= 100
            return result