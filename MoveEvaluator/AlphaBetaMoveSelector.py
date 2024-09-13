from .MoveSelector import MoveSelector
from copy import deepcopy

# Minimax with Alpha-Beta pruning
class AlphaBetaMoveSelector(MoveSelector):
    def __init__(self, max_depth, position_evaluator):
        self.max_depth = max_depth
        self.position_evaluator = position_evaluator
    
    def min_max(self, board, player, depth, alpha, beta):
        if depth == 0 or not board.has_valid_move(player):
            if depth != 0 and not board.has_valid_move(-player):
                return self.min_max(board, -player, depth - 1, -beta, -alpha)
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
                    _, score = self.min_max(
                        temp_board, -player, depth - 1, alpha, beta)
                    
                    # Update the best score and move
                    if player == -1:
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)
                        beta = min(beta, best_score)
                    else:
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
                        alpha = max(alpha, best_score)
                    
                    # Pruning
                    if beta <= alpha:
                        break
            # Pruning
            if beta <= alpha:
                break
        
        return (best_move, best_score)

    def getMove(self, board, player):
        move, _ = self.min_max(board, player, self.max_depth, float('-inf'), float('inf'))
        return move
