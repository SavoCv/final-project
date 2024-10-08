from copy import deepcopy
from .MoveSelector import MoveSelector

class MinimaxMoveSelector(MoveSelector):
    def __init__(self, max_depth, position_evaluator):
        self.max_depth = max_depth
        self.position_evaluator = position_evaluator

    # Min-max algorithm to calculate the best move
    def min_max(self, board, player, depth):
        if depth == 0 or not board.has_valid_move(player):
            if depth != 0 and not board.has_valid_move(-player):
                return self.min_max(board, -player, depth - 1)
            return (None, self.position_evaluator.evaluate(board))
        
        best_score = float('inf') if player == -1 else float('-inf')
        best_move = None
        
        for row in range(8):
            for col in range(8):
                if board.is_valid_move(player, row, col):
                    # Make a temporary move
                    temp_board = deepcopy(board)
                    temp_board.make_move(player, row, col)
                    
                    # Recursively call min_max for the opponent
                    _, score = self.min_max(temp_board, -player, depth - 1)

                    # Update the best score and move
                    if player == -1:
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)
                    else:
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)

        return (best_move, best_score)
    
    # Get the best move
    def getMove(self, board, player):
        move, _ = self.min_max(board, player, self.max_depth)
        return move
