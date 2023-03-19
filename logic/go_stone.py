class Stone:
    def __init__(self, position, color, board):
        self.position =  position
        self.color = color
        self.board = board
        self.adjacent = []
    
    def opposite_color(self):
        if self.color == "black":
            return "white"
        if self.color == "white":
            return "black"
    
    def adjacent_stones(self):
        x, y = self.position
        north = -2
        south = -2
        west = -2
        east = -2

        if x not in [0, 18] and y not in [0,18]:
            north = self.board.board[x][y - 1]
            south = self.board.board[x][y + 1]
            west = self.board.board[x - 1][y]
            east = self.board.board[x + 1][y]
        elif x == 0 and y not in [0,18]:
            north = self.board.board[x][y - 1]
            south = self.board.board[x][y + 1]
            east = self.board.board[x + 1][y]
        elif x == 18 and y not in[0,18]:
            north = self.board.board[x][y - 1]
            south = self.board.board[x][y + 1]
            west = self.board.board[x - 1][y]
        elif x not in [0,18] and y == 0:
            south = self.board.board[x][y + 1]
            west = self.board.board[x - 1][y]
            east = self.board.board[x + 1][y]
        elif x not in [0,18] and y == 18:
            north = self.board.board[x][y - 1]
            west = self.board.board[x - 1][y]
            east = self.board.board[x + 1][y]
        elif x == 0 and y == 0:
            south = self.board.board[x][y + 1]
            east = self.board.board[x + 1][y]
        elif x == 0 and y == 18:
            north = self.board.board[x][y - 1]
            east = self.board.board[x + 1][y]
        elif x == 18 and y == 0:
            south = self.board.board[x][y + 1]
            west = self.board.board[x - 1][y]
        elif x == 18 and y == 18:
            north = self.board.board[x][y - 1]
            west = self.board.board[x - 1][y]
        
        self.adjacent =  [north, south, west, east]
    
    def surround_by_oppo(self):
        self.adjacent_stones()
        for surround in self.adjacent:
            if surround != -2:
                if surround == 0 or surround.color == self.color:
                    return False
        
        return True

    def has_empty_adjacency(self):
        self.adjacent_stones()
        for surround in self.adjacent:
            if surround == 0:
                return True
        
        return False

    def __str__(self):
        return "{}, {}".format(self.position, self.color)

class BlockStone:
    def __init__(self, board, stone):
        self.color = stone.color
        self.board = board
        self.stone = stone
    
    def find_block_stone(self):
        unique = []
        block = set()
        
        visited = set()
        stack = []
        visited.add(self.stone)
        stack.append(self.stone)
        while stack != []:
            ver = stack.pop()
            ver.adjacent_stones()
            for stones in ver.adjacent:
                if stones not in visited and stones != -2 and stones != 0 and stones.color == self.stone.color:
                    visited.add(stones)
                    stack.append(stones)
        
        for stone in visited:
            if stone.position not in unique:
                unique.append(stone.position)
                block.add(stone)
        
        return block
     

    def has_empty_adjacency(self):
        block = self.find_block_stone()
        for stone in block:
            if stone.has_empty_adjacency():
                return True
        return False


