from .MinimaxSolver import MinimaxSolver

class GreddyMinimaxSolver(MinimaxSolver):
    def __init__(self, max_depth):
        super().__init__(max_depth)
    
    # Evaluate the board state
    def evaluate(self, board, player):
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == player:
                    score += 1
                elif board[row][col] == -player:
                    score -= 1
        return score
    