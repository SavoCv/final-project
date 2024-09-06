import sys
import pygame

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

# Screen states
PLAYER_TURN = 0
GAME_OVER = 1
BOT_PLAYS = 2
EXIT = 3
CALCULATING = 4
START_SCREEN = 5

class GameScreen:
    # Initialize the game screen
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 802))
        self.board_width = 802
        self.board_height = 802
        pygame.display.set_caption("Reversi")
    
    def set_controller(self, controller):
        self.controller = controller

    # Draw the game board
    def draw_board(self, board, current_player, state):
         # Fill screen with gray color
        self.screen.fill(gray)
        
        mouse_pos = None
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
        
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.screen, field_color, (col * field_size, row * field_size, field_size, field_size))
                if board[row][col] == -1:
                    pygame.draw.circle(self.screen, black, (col * field_size + field_size // 2, row * field_size + field_size // 2), tile_size_radius)
                elif board[row][col] == 1:
                    pygame.draw.circle(self.screen, white, (col * field_size + field_size // 2, row * field_size + field_size // 2), tile_size_radius)
                elif board.is_valid_move(current_player, row, col):
                    pygame.draw.circle(
                        self.screen, 
                        gray if state==BOT_PLAYS or state == CALCULATING else valid_move_color, 
                        (col * field_size + field_size // 2, row * field_size + field_size // 2), 
                        valid_move_radius
                    )
        font = pygame.font.Font(None, 36)
        for row in range(8):
            text = font.render(str(row + 1), True, black)
            text_rect = text.get_rect(left=padding, bottom=(row + 1) * field_size - padding)
            self.screen.blit(text, text_rect)
        for col in range(8):
            text = font.render(chr(ord('a') + col), True, black)
            text_rect = text.get_rect(right=(col + 1) * field_size - padding, top=padding)
            self.screen.blit(text, text_rect)
        for row in range(-1, 8):
            pygame.draw.line(self.screen, black, (0, row * field_size + field_size), (800, row * field_size + field_size), 2)
        for col in range(-1, 8):
            pygame.draw.line(self.screen, black, (col * field_size + field_size, 0), (col * field_size + field_size, 800), 2)
        
        black_count = sum(row.count(-1) for row in board)
        white_count = sum(row.count(1) for row in board)
        font = pygame.font.Font(None, 36)
        black_text = font.render(f"Black: {black_count}", True, white)
        white_text = font.render(f"White: {white_count}", True, white)
        self.screen.blit(black_text, (810, 10))
        self.screen.blit(white_text, (810, 50))
        undo_button = pygame.Rect(810, 90, 100, 40)
        pygame.draw.rect(self.screen, white, undo_button, border_radius=15)
        undo_text = font.render("Undo", True, black)
        undo_text_rect = undo_text.get_rect(center=undo_button.center)
        self.screen.blit(undo_text, undo_text_rect)

        if state == CALCULATING:
            text = font.render("Calculating...", True, black, white)
            text_rect = text.get_rect(center=(self.board_width // 2, self.board_height // 2))
            self.screen.blit(text, text_rect)

        if mouse_pos:
            if undo_button.collidepoint(mouse_pos):
                self.controller.undo_move()
            else:
                if mouse_pos[0] < 800 and mouse_pos[1] < 800:
                    self.controller.play_move(GameScreen.get_clicked_position(mouse_pos))

    
    # End game dialog
    def end_game_dialog(self, board):
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
        text_rect = text.get_rect(center=(self.board_width // 2, self.board_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        # Play again option
        play_again_button = pygame.Rect(300, 500, 200, 50)
        play_again_text = font.render("Play Again", True, black)
        play_again_text_rect = play_again_text.get_rect(center=(play_again_button.centerx, play_again_button.centery))
        pygame.draw.rect(self.screen, (0, 255, 0), play_again_button, border_radius=10)
        self.screen.blit(play_again_text, play_again_text_rect)

        # Exit option
        exit_button = pygame.Rect(300, 600, 200, 50)
        exit_text = font.render("Exit", True, black)
        exit_text_rect = exit_text.get_rect(center=(exit_button.centerx, exit_button.centery))
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button, border_radius=10)
        self.screen.blit(exit_text, exit_text_rect)

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

    # Get the position of the mouse click
    @staticmethod
    def get_clicked_position(mouse_pos):
        x, y = mouse_pos
        row = y // field_size
        col = x // field_size
        return row, col
