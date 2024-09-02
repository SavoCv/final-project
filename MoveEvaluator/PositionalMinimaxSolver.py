from .MinimaxMoveSelector import MinimaxMoveSelector

position_matrix = [[ 30, -25, 10, 5, 5, 10, -25,  30,],
                   [-25, -25,  1, 1, 1,  1, -25, -25,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [-25, -25,  1, 1, 1,  1, -25, -25,],
                   [ 30, -25, 10, 5, 5, 10, -25,  30,]]

class PositionalMinimaxSolver(MinimaxMoveSelector):
    def __init__(self, max_depth, position_scaler = 1):
        super().__init__(max_depth)
        self.position_scaler = position_scaler
    
    # Evaluate the board state
    def evaluate(self, board, player):
        disks_diff = 0
        num_disks = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == player:
                    disks_diff += 1
                    num_disks += 1
                elif board[row][col] == -player:
                    disks_diff -= 1
                    num_disks += 1
        
        position_eval = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == player:
                    position_eval += position_matrix[row][col]
                elif board[row][col] == -player:
                    position_eval -= position_matrix[row][col]
        
        # This is called evaporation strategy
        if num_disks > 40:
            evaluation = disks_diff + self.position_scaler * position_eval
        else:
            evaluation = - disks_diff + self.position_scaler * position_eval
        # print(evaluation, disks_diff, position_eval)
        # print(board)
        # print()
        return evaluation