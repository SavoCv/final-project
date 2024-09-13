from .MoveSelector import MoveSelector
from copy import deepcopy

class NegaScoutMoveSelector(MoveSelector):
    def __init__(self, max_depth, position_evaluator):
        self.max_depth = max_depth
        self.position_evaluator = position_evaluator
        self.cnt = 0
        self.cnt2 = 0
    
    def nega_scout(self, board, player, depth, alpha, beta):
        # Base case: if depth is 0 or no valid moves, return the evaluation of 
        # the current position
        if depth == 0 or not board.has_valid_move(player):
            if depth != 0 and not board.has_valid_move(-player):
                return self.nega_scout(board, -player, depth - 1, -beta, -alpha)
            return (None, self.position_evaluator.evaluate(board) * player)
        
        best_score = float('-inf')
        best_move = None
        b = beta

        move_board_score = []
        # Generate a list of valid moves and their corresponding boards and 
        # scores
        for row in range(8):
            for col in range(8):
                if board.is_valid_move(player, row, col):
                    # Make a temporary move
                    temp_board = deepcopy(board)
                    temp_board.make_move(player, row, col)
                    
                    move_board_score.append((
                        (row, col), 
                        temp_board, 
                        self.position_evaluator.evaluate(temp_board)))

        # Sort the moves in descending order based on their scores
        move_board_score.sort(key=lambda x: - x[2] * player)

        i = 0
        for move, temp_board, scr in move_board_score:
            i += 1
            row, col = move
            
            # Recursively call nega_scout for the opponent
            if depth != 1:
                _, score = self.nega_scout(
                    temp_board, -player, depth - 1, -b, -alpha)
            else:
                score = scr * (-player)
            score = -score
            
            # Perform a re-search if the score is within the bounds and it's not
            # the first move
            if alpha < score < beta and i != 1:
                if depth != 1:
                    _, score = self.nega_scout(
                        temp_board, -player, depth - 1, -beta, -alpha)
                else:
                    score = scr * (-player)
                score = -score
            
            # Update the best score and best move if the current score is better
            if score > best_score:
                best_score = score
                best_move = (row, col)
            
            # Update alpha with the maximum score encountered so far
            alpha = max(alpha, score)
            # Prune the search if alpha is greater than or equal to beta
            if alpha >= beta:
                break
            b = alpha + 1
        
        return (best_move, best_score)
    
    def getMove(self, board, player):
        self.cnt = 0
        self.cnt2 = 0
        best_move, _ = self.nega_scout(board, player, self.max_depth, float('-inf'), float('inf'))
        # print(self.cnt)
        # print(self.cnt2)
        return best_move
