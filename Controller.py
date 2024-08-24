import pygame
import sys
from time import sleep

from Board import Board
from GameScreen import GameScreen
from Solver.GreddyMinimaxSolver import GreddyMinimaxSolver
from Solver.PositionalMinimaxSolver import PositionalMinimaxSolver

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
field_color = (0, 128, 0)
valid_move_color = (0, 255, 0)
gray = (127, 127, 127)

class Controller:
    def __init__(self):
        # self.solver = GreddyMinimaxSolver(3)
        self.solver = PositionalMinimaxSolver(4)
        self.board = Board()
        self.gameScreen = GameScreen()

    # Main loop
    # Reversi game logic
    def play_reversi(self):
        # Game setup
        # board = Board()
        # gameScreen = GameScreen()
        screen = self.gameScreen.screen
        # board = create_board()
        current_player = -1
        game_over = False

        # Game loop
        while not game_over:
            mouse_pos = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

            # Fill screen with gray color
            screen.fill(gray)

            # Draw the board
            self.gameScreen.draw_board(self.board, current_player, bot_plays = current_player == 1)

            if current_player == 1:
                pygame.display.flip()
                sleep(0.2)
                move = self.solver.getMove(self.board, current_player)
                self.board.make_move(current_player, *move)
                current_player = -current_player
                pygame.display.flip()
                continue

            black_count = sum(row.count(-1) for row in self.board)
            white_count = sum(row.count(1) for row in self.board)
            font = pygame.font.Font(None, 36)
            black_text = font.render(f"Black: {black_count}", True, white)
            white_text = font.render(f"White: {white_count}", True, white)
            screen.blit(black_text, (810, 10))
            screen.blit(white_text, (810, 50))
            undo_button = pygame.Rect(810, 90, 100, 40)
            pygame.draw.rect(screen, white, undo_button, border_radius=15)
            undo_text = font.render("Undo", True, black)
            undo_text_rect = undo_text.get_rect(center=undo_button.center)
            screen.blit(undo_text, undo_text_rect)

            # Update display
            pygame.display.flip()

            # Check for player input
            if mouse_pos:
                if undo_button.collidepoint(mouse_pos):
                    # Undo the last move
                    print("undo clicked")
                    self.board.undo_move()
                    self.board.undo_move()
                else:
                    if mouse_pos[1] > 800:
                        continue
                    row, col = GameScreen.get_clicked_position(mouse_pos)
                    if self.board.is_valid_move(current_player, row, col):
                        self.board.make_move(current_player, row, col)
                        current_player = -current_player

            # Switch player if current player has no valid moves
            if not self.board.has_valid_move(current_player):
                current_player = -current_player
                pygame.display.set_caption('Player plays again')
                # pygame.time.wait(1000)

            # If both players have no valid moves, end the game
            if not self.board.has_valid_move(current_player):
                game_over = True
                self.gameScreen.draw_board(self.board, current_player)
                end_game = self.gameScreen.end_game_dialog(self.board)
                if end_game:
                    return
                self.board = Board()
                current_player = -1
                game_over = False

    
