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
        position_eval = 0
        available_moves = 0

        # Cache range and matrix access
        for row in range(8):
            for col in range(8):
                current_value = board[row][col]
                position_eval += current_value * position_matrix[row][col]

                # Check valid moves for both players in a single loop
                if board.is_valid_move(-1, row, col):
                    available_moves -= 1
                if board.is_valid_move(1, row, col):
                    available_moves += 1

        # Evaluate corners and adjacent cells
        corner_positions = [(0, 0, [(1, 0), (0, 1), (1, 1)]),
                            (0, 7, [(1, 7), (0, 6), (1, 6)]),
                            (7, 0, [(6, 0), (7, 1), (6, 1)]),
                            (7, 7, [(6, 7), (7, 6), (6, 6)])]

        for corner_row, corner_col, adjacents in corner_positions:
            if board[corner_row][corner_col] != 0:
                for adj_row, adj_col in adjacents:
                    position_eval += board[adj_row][adj_col] * 12

        # Add available moves score
        position_eval += available_moves * 5

        return position_eval

    def get_evaluated_and_reset(self):
        self.evaluated, evaluated = 0, self.evaluated
        return evaluated
