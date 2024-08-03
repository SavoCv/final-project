import pygame
import sys

screen = None

# Constants
field_size = 100
field_count = 8
tile_size_radius = field_size // 2 * 0.8
valid_move_radius = field_size // 10
padding = 5

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
field_color = (0, 128, 0)
valid_move_color = (0, 255, 0)
gray = (127, 127, 127)

# Create the game board
def create_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1
    return board

# Draw the game board
def draw_board(board, current_player):
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(screen, field_color, (col * field_size, row * field_size, field_size, field_size))
            # pygame.draw.line(screen, black, (col * field_size, row * field_size), (col * field_size + field_size, row * field_size), 2)
            # pygame.draw.line(screen, black, (col * field_size, row * field_size), (col * field_size, row * field_size + field_size), 2)
            if board[row][col] == -1:
                pygame.draw.circle(screen, black, (col * field_size + field_size // 2, row * field_size + field_size // 2), tile_size_radius)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, white, (col * field_size + field_size // 2, row * field_size + field_size // 2), tile_size_radius)
            elif is_valid_move(board, current_player, row, col):
                pygame.draw.circle(screen, valid_move_color, (col * field_size + field_size // 2, row * field_size + field_size // 2), valid_move_radius)
    font = pygame.font.Font(None, 36)
    for row in range(8):
        text = font.render(str(row + 1), True, black)
        text_rect = text.get_rect(left=padding, bottom=(row + 1) * field_size - padding)
        screen.blit(text, text_rect)
    for col in range(8):
        text = font.render(chr(ord('a') + col), True, black)
        text_rect = text.get_rect(right=(col + 1) * field_size - padding, top=padding)
        screen.blit(text, text_rect)
    for row in range(-1, 8):
        pygame.draw.line(screen, black, (0, row * field_size + field_size), (800, row * field_size + field_size), 2)
    for col in range(-1, 8):
        pygame.draw.line(screen, black, (col * field_size + field_size, 0), (col * field_size + field_size, 800), 2)

# Get the position of the mouse click
def get_clicked_position(mouse_pos):
    x, y = mouse_pos
    row = y // field_size
    col = x // field_size
    return row, col

# Check if a move is valid
def is_valid_move(board, player, row, col):
    if board[row][col] != 0:
        return False
    opponent = 1 if player == -1 else -1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != opponent:
            continue
        x, y = x + dx, y + dy
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if board[x][y] == 0:
                break
            if board[x][y] == player:
                return True
            x, y = x + dx, y + dy
    return False

# Make a move
def make_move(board, player, row, col):
    opponent = 1 if player == -1 else -1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    board[row][col] = player
    for dx, dy in directions:
        x, y = row + dx, col + dy
        if x < 0 or x >= 8 or y < 0 or y >= 8 or board[x][y] != opponent:
            continue
        positions_to_flip = []
        # x, y = x + dx, y + dy
        while x >= 0 and x < 8 and y >= 0 and y < 8:
            if board[x][y] == 0:
                break
            if board[x][y] == player:
                for i, j in positions_to_flip:
                    board[i][j] = player
                break
            positions_to_flip.append((x, y))
            x, y = x + dx, y + dy

# Check if the game is over
def has_valid_move(board, current_player):
    for row in range(8):
        for col in range(8):
            if board[row][col] == 0 and is_valid_move(board, current_player, row, col):
                return True
    return False

# End game dialog
def end_game_dialog(board):
    x_count = sum(row.count(-1) for row in board)
    o_count = sum(row.count(1) for row in board)
    if x_count > o_count:
        winner = "Black"
    elif o_count > x_count:
        winner = "White"
    else:
        winner = 'No one'
    pygame.display.set_caption('Game Over')
    font = pygame.font.Font(None, 36)
    
    text = font.render(f"The game is over. {winner} won with a score of {x_count}-{o_count}.", True, black, white)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Play again option
    play_again_button = pygame.Rect(300, 500, 200, 50)
    play_again_text = font.render("Play Again", True, black)
    play_again_text_rect = play_again_text.get_rect(center=(play_again_button.centerx, play_again_button.centery))
    pygame.draw.rect(screen, (0, 255, 0), play_again_button)
    screen.blit(play_again_text, play_again_text_rect)

    # Exit option
    exit_button = pygame.Rect(300, 600, 200, 50)
    exit_text = font.render("Exit", True, black)
    exit_text_rect = exit_text.get_rect(center=(exit_button.centerx, exit_button.centery))
    pygame.draw.rect(screen, (255, 0, 0), exit_button)
    screen.blit(exit_text, exit_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    return False
                elif exit_button.collidepoint(mouse_pos):
                    return True

# Main loop
# Reversi game logic
def play_reversi():
    # Game setup
    board = create_board()
    current_player = -1
    game_over = False

    # Game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill screen with gray color
        screen.fill(gray)

        # Draw the board
        draw_board(board, current_player)

        black_count = sum(row.count(-1) for row in board)
        white_count = sum(row.count(1) for row in board)
        font = pygame.font.Font(None, 36)
        black_text = font.render(f"Black: {black_count}", True, white)
        white_text = font.render(f"White: {white_count}", True, white)
        screen.blit(black_text, (810, 10))
        screen.blit(white_text, (810, 50))

        # Update display
        pygame.display.flip()

        # Check for player input
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > 800:
                continue
            row, col = get_clicked_position(mouse_pos)
            if is_valid_move(board, current_player, row, col):
                make_move(board, current_player, row, col)
                current_player = -current_player

        # Switch player if current player has no valid moves
        if not has_valid_move(board, current_player):
            current_player = -current_player
            pygame.display.set_caption('Player plays again')
            # pygame.time.wait(1000)

        # If both players have no valid moves, end the game
        if not has_valid_move(board, current_player):
            game_over = True
            draw_board(board, current_player)
            end_game = end_game_dialog(board)
            if end_game:
                return
            board = create_board()
            current_player = -1
            game_over = False

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((1000, 802))
pygame.display.set_caption('Reversi')

# Call the Reversi game function
play_reversi()
