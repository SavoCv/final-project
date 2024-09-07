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

players = ["player", "bot"]
algorithms = ["minimax", "αβ", "negascout", "ordering αβ"]
evaluators = ["heuristic", "greedy"]
depths = [3, 4, 5, 6]

class GameScreen:
    # Initialize the game screen
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 802))
        self.board_width = 802
        self.board_height = 802
        pygame.display.set_caption("Reversi")
        self.choosen_players = ["player", "player"]
        self.choosen_algorithms = ["minimax", "minimax"]
        self.choosen_evaluators = ["heuristic", "heuristic"]
        self.choosen_depths = [3, 3]
    
    def set_controller(self, controller):
        self.controller = controller

    # Draw the game board
    def draw_board(self, board, current_player, state):    
         # Fill screen with gray color
        self.screen.fill(gray)

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
            pygame.draw.line(self.screen, black, (col * field_size + field_size, 0), (col * field_size + field_size, 802), 2)
        
        black_count = sum(row.count(-1) for row in board)
        white_count = sum(row.count(1) for row in board)
        font = pygame.font.Font(None, 36)
        black_text = font.render(f"Black: {black_count}", True, black)
        white_text = font.render(f"White: {white_count}", True, white)
        self.screen.blit(black_text, (810, 10))
        self.screen.blit(white_text, (810, 50))

        padding_buttons = 100
        undo_button = pygame.Rect(825, 360 - padding_buttons, 150, 40)
        pygame.draw.rect(self.screen, white, undo_button, border_radius=10)
        undo_text = font.render("Undo", True, black)
        undo_text_rect = undo_text.get_rect(center=undo_button.center)
        self.screen.blit(undo_text, undo_text_rect)

        play_again_button_right = pygame.Rect(825, 400 + padding_buttons, 150, 40)
        pygame.draw.rect(self.screen, white, play_again_button_right, border_radius=10)
        play_again_text = font.render("Play Again", True, black)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_right.center)
        self.screen.blit(play_again_text, play_again_text_rect)

        if state == CALCULATING:
            text = font.render("Calculating...", True, black, white)
            text_rect = text.get_rect(center=(self.board_width // 2, self.board_height // 2))
            self.screen.blit(text, text_rect)
        
        if state == GAME_OVER:
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
        
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos:
                    if undo_button.collidepoint(mouse_pos):
                        self.controller.undo_move()
                    elif play_again_button_right.collidepoint(mouse_pos):
                        self.controller.play_again()
                    elif state == GAME_OVER:
                        if play_again_button.collidepoint(mouse_pos):
                            self.controller.play_again()
                        elif exit_button.collidepoint(mouse_pos):
                            self.controller.exit()
                    elif mouse_pos[0] < 800 and mouse_pos[1] < 800:
                        self.controller.play_move(GameScreen.get_clicked_position(mouse_pos))

    
    # # End game dialog
    # def end_game_dialog(self, board):
        

    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 mouse_pos = pygame.mouse.get_pos()
    #                 if play_again_button.collidepoint(mouse_pos):
    #                     return False
    #                 elif exit_button.collidepoint(mouse_pos):
    #                     return True

    # Get the position of the mouse click
    @staticmethod
    def get_clicked_position(mouse_pos):
        x, y = mouse_pos
        row = y // field_size
        col = x // field_size
        return row, col
    
    def start_screen(self):
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

        self.screen.fill(gray)
        font = pygame.font.Font(None, 36)
        header_font = pygame.font.Font(None, 72)
        text = header_font.render("Welcome to Reversi!", True, black)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(text, text_rect)


        y = 200
        dyTextButton = 20
        dyButtonText = 80

        leftMargin = 50
        

        text = font.render("Choose black player:", True, black)
        text_rect = text.get_rect(center=((leftMargin * 2 + 205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, player in enumerate(players):
            button = pygame.Rect(leftMargin + i * 205, y, 200, 50)
            text = font.render(player, True, black)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (0, 123, 255) if player == self.choosen_players[0] else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_players[0] = player
        
        y += dyButtonText

        text = font.render("Choose algorithm:", True, black)
        text_rect = text.get_rect(center=((leftMargin * 2 + 205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, algorithm in enumerate(algorithms):
            button = pygame.Rect(leftMargin + (i % 2) * 205, y + i // 2 * 55, 200, 50)
            text = font.render(algorithm, True, black)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[0] == "player" 
                    else (0, 123, 255) if algorithm == self.choosen_algorithms[0] 
                    else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_algorithms[0] = algorithm
        
        y += dyButtonText + 55

        text = font.render("Choose evaluator:", True, black)
        text_rect = text.get_rect(center=((leftMargin * 2 + 205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, evaluator in enumerate(evaluators):
            button = pygame.Rect(leftMargin + i * 205, y, 200, 50)
            text = font.render(evaluator, True, black)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[0] == "player" 
                    else (0, 123, 255) if evaluator == self.choosen_evaluators[0] 
                    else (170, 170, 170), 
                    button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_evaluators[0] = evaluator
        
        y += dyButtonText

        text = font.render("Choose depth:", True, black)
        text_rect = text.get_rect(center=((leftMargin * 2 + 205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, depth in enumerate(depths):
            button = pygame.Rect(leftMargin + i * 102, y, 97, 50)
            text = font.render(str(depth), True, black)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[0] == "player" 
                    else (0, 123, 255) if depth == self.choosen_depths[0] 
                    else (170, 170, 170), 
                    button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_depths[0] = depth
        
        y = 200
        xPosition = 545

        text = font.render("Choose white player:", True, white)
        text_rect = text.get_rect(center=(xPosition + (205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, player in enumerate(players):
            button = pygame.Rect(xPosition + i * 205, y, 200, 50)
            text = font.render(player, True, white)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (0, 123, 255) if player == self.choosen_players[1] else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_players[1] = player
        
        y += dyButtonText

        text = font.render("Choose algorithm:", True, white)
        text_rect = text.get_rect(center=(xPosition + (205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, algorithm in enumerate(algorithms):
            button = pygame.Rect(xPosition + (i % 2) * 205, y + i // 2 * 55, 200, 50)
            text = font.render(algorithm, True, white)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[1] == "player" 
                    else (0, 123, 255) if algorithm == self.choosen_algorithms[1] 
                    else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_algorithms[1] = algorithm
        
        y += dyButtonText + 55

        text = font.render("Choose evaluator:", True, white)
        text_rect = text.get_rect(center=(xPosition + (205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, evaluator in enumerate(evaluators):
            button = pygame.Rect(xPosition + i * 205, y, 200, 50)
            text = font.render(evaluator, True, white)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[1] == "player" 
                    else (0, 123, 255) if evaluator == self.choosen_evaluators[1] 
                    else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_evaluators[1] = evaluator
        
        y += dyButtonText

        text = font.render("Choose depth:", True, white)
        text_rect = text.get_rect(center=(xPosition + (205 + 200) // 2, y))
        self.screen.blit(text, text_rect)

        y += dyTextButton

        for i, depth in enumerate(depths):
            button = pygame.Rect(xPosition + i * 102, y, 97, 50)
            text = font.render(str(depth), True, white)
            text_rect = text.get_rect(center=(button.centerx, button.centery))
            pygame.draw.rect(self.screen, 
                (80, 80, 80) if self.choosen_players[1] == "player" 
                    else (0, 123, 255) if depth == self.choosen_depths[1] 
                    else (170, 170, 170), 
                button, border_radius=10)
            self.screen.blit(text, text_rect)
            if mouse_pos and button.collidepoint(mouse_pos):
                self.choosen_depths[1] = depth
        
        y += dyButtonText

        start_button = pygame.Rect(1000 // 2 - 300 // 2, 680, 300, 70)
        start_button_font = pygame.font.Font(None, 48)
        start_text = start_button_font.render("Start", True, black)
        start_text_rect = start_text.get_rect(center=(start_button.centerx, start_button.centery))
        pygame.draw.rect(self.screen, (0, 200, 0), start_button, border_radius=10)
        self.screen.blit(start_text, start_text_rect)

        if mouse_pos and start_button.collidepoint(mouse_pos):
            self.controller.start_game(self.choosen_players, self.choosen_algorithms, self.choosen_evaluators, self.choosen_depths)

        pygame.display.flip()