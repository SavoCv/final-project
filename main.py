import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Reversi')

# Create the game board
def create_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'
    return board

# Draw the game board
def draw_board(board, current_player):
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, (0, 128, 0), (col * 100, row * 100, 100, 100))
            pygame.draw.line(screen, (0, 0, 0), (col * 100, row * 100), (col * 100 + 100, row * 100), 2)
            pygame.draw.line(screen, (0, 0, 0), (col * 100, row * 100), (col * 100, row * 100 + 100), 2)
            if board[row][col] == 'X':
                pygame.draw.circle(screen, (0, 0, 0), (col * 100 + 50, row * 100 + 50), 40)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, (255, 255, 255), (col * 100 + 50, row * 100 + 50), 40)
            elif is_valid_move(board, current_player, row, col):
                pygame.draw.circle(screen, (0, 255, 0), (col * 100 + 50, row * 100 + 50), 10)

# Get the position of the mouse click
def get_clicked_position(mouse_pos):
    x, y = mouse_pos
    row = y // 100
    col = x // 100
    return row, col

# Check if a move is valid
def is_valid_move(board, player, row, col):
    if board[row][col] != ' ':
        return False
    opponent = 'O' if player == 'X' else 'X'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != opponent:
            continue
        x, y = x + dx, y + dy
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if board[x][y] == ' ':
                break
            if board[x][y] == player:
                return True
            x, y = x + dx, y + dy
    return False

# Make a move
def make_move(board, player, row, col):
    opponent = 'O' if player == 'X' else 'X'
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    board[row][col] = player
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != opponent:
            continue
        positions_to_flip = []
        # x, y = x + dx, y + dy
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if board[x][y] == ' ':
                break
            if board[x][y] == player:
                for i, j in positions_to_flip:
                    board[i][j] = player
                break
            positions_to_flip.append((x, y))
            x, y = x + dx, y + dy

# Check if the game is over
def is_game_over(board, current_player):
    for row in range(8):
        for col in range(8):
            if board[row][col] == ' ' and is_valid_move(board, current_player, row, col):
                return False
    return True

# Main loop
# Reversi game logic
def play_reversi():
    # Game setup
    board = create_board()
    current_player = 'X'
    game_over = False

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen with white color
        screen.fill((255, 255, 255))

        # Draw the board
        draw_board(board, current_player)

        # Update display
        pygame.display.flip()

        # Check for player input
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            row, col = get_clicked_position(mouse_pos)
            if is_valid_move(board, current_player, row, col):
                make_move(board, current_player, row, col)
                current_player = 'O' if current_player == 'X' else 'X'

        # Check for game over condition
        if is_game_over(board, current_player):
            game_over = True

# Call the Reversi game function
play_reversi()
