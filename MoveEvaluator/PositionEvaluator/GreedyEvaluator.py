from .PositionEvaluator import PositionEvaluator

class GreedyEvaluator(PositionEvaluator):
    def evaluate(self, board):
        score = 0
        for row in range(8):
            for col in range(8):
                score += board[row][col]
        return score
