from .PositionEvaluator import PositionEvaluator

position_matrix = [[ 40, -10, 10, 5, 5, 10, -10,  40,],
                   [-10, -10,  1, 1, 1,  1, -10, -10,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [-10, -10,  1, 1, 1,  1, -10, -10,],
                   [ 40, -10, 10, 5, 5, 10, -10,  40,]]

class HeuristicEvaluator(PositionEvaluator):
    def __init__(self, position_scaler = 1):
        self.position_scaler = position_scaler
        self.evaluated = 0

    def evaluate(self, board):
        self.evaluated += 1
        disks_diff = 0
        num_disks = 0
        for row in range(8):
            for col in range(8):
                disks_diff += board[row][col]
                if board[row][col] != 0:
                    num_disks += 1
        
        position_eval = 0
        for row in range(8):
            for col in range(8):
                position_eval += board[row][col] * position_matrix[row][col]

        if board[0][0] != 0:
            position_eval += board[1][0] * 12
            position_eval += board[0][1] * 12
        if board[0][7] != 0:
            position_eval += board[1][7] * 12
            position_eval += board[0][6] * 12
        if board[7][0] != 0:
            position_eval += board[6][0] * 12
            position_eval += board[7][1] * 12
        if board[7][7] != 0:
            position_eval += board[6][7] * 12
            position_eval += board[7][6] * 12
        
        available_moves = 0
        for row in range(8):
            for col in range(8):
                if board.is_valid_move(-1, row, col):
                    available_moves -= 1

        for row in range(8):
            for col in range(8):
                if board.is_valid_move(1, row, col):
                    available_moves += 1
        
        position_eval += available_moves * 5

        return position_eval

    def get_evaluated_and_reset(self):
        self.evaluated, evaluated = 0, self.evaluated
        return evaluated
