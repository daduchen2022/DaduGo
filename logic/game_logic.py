from go_stone import Stone, BlockStone
from go_board import GoBoard

class GameLogic:
    def __init__(self, board):
        self.step = 0
        self.record = []
        self.board = board

    def check_valid_move(self, stone):
        return not (self.already_has_stone(stone) or \
                    self.suicide_move(stone) or \
                    self.repeate_move(stone))
                    
    def does_remove_stone(self, board, stone):
        """
        如果棋盘上存在没气的棋，则输出是
        """
        remove = False
        x, y = stone.position

        board.board[x][y] = stone
        stone.adjacent_stones()

        for oppo in stone.adjacent:
            if oppo != -2 and oppo != 0 and oppo.color != stone.color:
                #oppo.adjacent_stones()
                #print(oppo.adjacent)
                if self.does_remove_block(board, oppo):
                    remove = True
        
        board.board[x][y] = 0

        return remove
        
    def does_remove_block(self, board, stone):
        """
        辅助函数;
        如果棋盘上存在没气的棋，则输出是
        """
        
        block = BlockStone(board, stone)


        if not block.has_empty_adjacency() :
            return True
        return False
    
    def remove_block(self, board, stone):
        lst = []
        x, y = stone.position
        board.board[x][y] = stone
        stone.adjacent_stones()

        for oppo in stone.adjacent:
            if oppo != -2 and oppo != 0 and oppo.color != stone.color:
                if self.does_remove_block(board, oppo):
                    block = BlockStone(board, oppo)
                    visited = block.find_block_stone()
                    for stones in visited:
                        a, b = stones.position
                        board.board[a][b] = 0
                        lst.append((a,b))
        board.board[x][y] = 0

        return lst
    
    def copy_board(self, board):
        copy = GoBoard()
        for i in range(19):
            for j in range(19):
                temp = board.board[i][j] 
                if temp != 0:
                    temp = Stone(temp.position, temp.color, copy)
                copy.board[i][j] = temp
        copy.turn = board.turn
        return copy

    def move(self, stone):
        if not self.check_valid_move(stone):
            return False
        
        self.remove_block(self.board, stone)
        x, y = stone.position
        self.board.board[x][y] = stone
        self.step += 1
        if self.step < 4:
            self.record.append(self.copy_board(self.board))
        else:
            prior = self.copy_board(self.record[2])
            prioror = self.copy_board(self.record[1])
            current = self.copy_board(self.board)
            self.record = [prioror, prior, current]
        
        self.board.opposite_color()

        return True
            

    def already_has_stone(self, stone):
        """
        不能下在已经有子的地方
        """
        x, y = stone.position
        if self.board.board[x][y] != 0:
            print("already has stone")
        return self.board.board[x][y] != 0

    def suicide_move(self, stone):
        """
        不能下禁入点，除非能够提子
        """
        if self.does_remove_stone(self.board, stone):
            return False
        
        x, y = stone.position
        self.board.board[x][y] = stone
        if not self.illegal_move(stone):
            self.board.board[x][y] = 0
            return False
        self.board.board[x][y] = 0
        print("suicide move")
        return True
    
    def repeate_move(self, stone):
        """
        打劫不能直接提劫
        """
        return self.compare_board_status(stone)
        
    def illegal_move(self, stone):
        block = BlockStone(self.board, stone)
        return not block.has_empty_adjacency()
    
    def board_status(self, curr_board):
        new_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        for i in range(19):
            for j in range(19):
                temp = curr_board.board[i][j]

                if temp != 0 and temp.color == "black":
                    new_board[i][j] = -1
                elif temp != 0 and temp.color == "white":
                    new_board[i][j] = 1
        
        return new_board
    
    def compare_board(self, board1, board2):
        for i in range(19):
            for j in range(19):
                if board1[i][j] != board2[i][j]:
                    return False
        return True
    
    def compare_board_status(self, stone):
        all_board = []
        if self.step < 3:
            return False
        
        prior = self.copy_board(self.record[2])
        prioror = self.copy_board(self.record[1])
        current = self.copy_board(self.board)
        new_stone = Stone(stone.position, stone.color, current)

        self.remove_block(current, new_stone)
        x, y = new_stone.position
        current.board[x][y] = new_stone
        
        temp = [prioror, prior, current]
    
        for i in temp:
            all_board.append(self.board_status(i))
        print(all_board[2])
        return self.compare_board(all_board[0], all_board[2])


    

        
      
                

           

    