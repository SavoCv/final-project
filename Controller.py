import pygame
import sys
from time import sleep

from Board import Board
from GameScreen import GameScreen
from Solver.GreddyMinimaxSolver import GreddyMinimaxSolver

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

class Controller:
    def __init__(self):
        self.sovler = GreddyMinimaxSolver(4)
        pass

    # Main loop
    # Reversi game logic
    def play_reversi(self):
        # Game setup
        global screen
        board = Board()
        gameScreen = GameScreen()
        screen = gameScreen.screen
        # board = create_board()
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
            gameScreen.draw_board(board, current_player, bot_plays = current_player == 1)

            if current_player == 1:
                pygame.display.flip()
                sleep(0.2)
                move = self.sovler.getMove(board, current_player)
                board.make_move(current_player, *move)
                current_player = -current_player
                pygame.display.flip()
                continue

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
                row, col = GameScreen.get_clicked_position(mouse_pos)
                if board.is_valid_move(current_player, row, col):
                    board.make_move(current_player, row, col)
                    current_player = -current_player

            # Switch player if current player has no valid moves
            if not board.has_valid_move(current_player):
                current_player = -current_player
                pygame.display.set_caption('Player plays again')
                # pygame.time.wait(1000)

            # If both players have no valid moves, end the game
            if not board.has_valid_move(current_player):
                game_over = True
                gameScreen.draw_board(board, current_player)
                end_game = gameScreen.end_game_dialog(board)
                if end_game:
                    return
                board = Board()
                current_player = -1
                game_over = False

    
