class Board:
    # Create the game board
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
    
    # Check if a move is valid
    def is_valid_move(self, player, row, col):
        if self.board[row][col] != 0:
            return False
        opponent = 1 if player == -1 else -1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            if x < 0 or x >= 8 or y < 0 or y >= 8 or self.board[x][y] != opponent:
                continue
            x, y = x + dx, y + dy
            while x >= 0 and x < 8 and y >= 0 and y < 8:
                if self.board[x][y] == 0:
                    break
                if self.board[x][y] == player:
                    return True
                x, y = x + dx, y + dy
        return False

    # Make a move
    def make_move(self, player, row, col):
        opponent = 1 if player == -1 else -1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.board[row][col] = player
        for dx, dy in directions:
            x, y = row + dx, col + dy
            if x < 0 or x >= 8 or y < 0 or y >= 8 or self.board[x][y] != opponent:
                continue
            positions_to_flip = []
            # x, y = x + dx, y + dy
            while x >= 0 and x < 8 and y >= 0 and y < 8:
                if self.board[x][y] == 0:
                    break
                if self.board[x][y] == player:
                    for i, j in positions_to_flip:
                        self.board[i][j] = player
                    break
                positions_to_flip.append((x, y))
                x, y = x + dx, y + dy

    # Check if the game is over
    def has_valid_move(self, current_player):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 0 and self.is_valid_move(current_player, row, col):
                    return True
        return False

    def __getitem__(self, key):
        return self.board[key]