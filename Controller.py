import pygame
import sys
from time import sleep

from Board import Board
from GameScreen import GameScreen
from MoveEvaluator.GreddyMinimaxSolver import GreddyMinimaxSolver
from MoveEvaluator.PositionalMinimaxSolver import PositionalMinimaxSolver
from MoveEvaluator.MinimaxMoveSelector import MinimaxMoveSelector
from MoveEvaluator.PositionEvaluator.GreedyEvaluator import GreedyEvaluator

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
field_color = (0, 128, 0)
valid_move_color = (0, 255, 0)
gray = (127, 127, 127)

class Controller:
    def __init__(self):
        # self.solver = GreddyMinimaxSolver(3)
        # self.solver = PositionalMinimaxSolver(3)
        self.solver = MinimaxMoveSelector(3, GreedyEvaluator())
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
        always_evaluate = False 

        # Game loop
        while not game_over:
            mouse_pos = None
            evaluate = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        evaluate = True
                    elif event.key == pygame.K_RETURN:
                        always_evaluate = not always_evaluate

            if always_evaluate:
                evaluate = True

            # Fill screen with gray color
            screen.fill(gray)

            # Switch player if current player has no valid moves
            if not self.board.has_valid_move(current_player):
                current_player = -current_player
                pygame.display.set_caption('Player plays again')
                # pygame.time.wait(1000)

            # Draw the board
            self.gameScreen.draw_board(self.board, current_player)

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

            if evaluate and current_player == 1:
                pygame.display.flip()
                move = self.solver.getMove(self.board, current_player)
                self.board.make_move(current_player, *move)
                current_player = -current_player
                pygame.display.flip()
            elif evaluate and current_player == -1:
                pygame.display.flip()
                move = self.solver.getMove(self.board, current_player)
                self.board.make_move(current_player, *move)
                current_player = -current_player
                pygame.display.flip()
            else:
                # Check for player input
                if mouse_pos:
                    if undo_button.collidepoint(mouse_pos):
                        # Undo the last move
                        self.board.undo_move()
                        self.board.undo_move()
                    else:
                        if mouse_pos[1] > 800:
                            continue
                        row, col = GameScreen.get_clicked_position(mouse_pos)
                        if self.board.is_valid_move(current_player, row, col):
                            self.board.make_move(current_player, row, col)
                            current_player = -current_player

    
