from .PositionEvaluator import PositionEvaluator

position_matrix = [[ 30, -25, 10, 5, 5, 10, -25,  30,],
                   [-25, -25,  1, 1, 1,  1, -25, -25,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [  5,   1,  2, 1, 1,  2,   1,   5,],
                   [ 10,   1,  5, 2, 2,  5,   1,  10,],
                   [-25, -25,  1, 1, 1,  1, -25, -25,],
                   [ 30, -25, 10, 5, 5, 10, -25,  30,]]

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
        
        # This is called evaporation strategy
        if num_disks > 40:
            evaluation = disks_diff + self.position_scaler * position_eval
        else:
            evaluation = - disks_diff + self.position_scaler * position_eval
        # print(evaluation, disks_diff, position_eval)
        # print(board)
        # print()
        return evaluation

    def get_evaluated_and_reset(self):
        self.evaluated, evaluated = 0, self.evaluated
        return evaluated
