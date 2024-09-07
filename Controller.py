from queue import Queue
from threading import Thread
import pygame
import sys
from time import sleep

from Board import Board
from GameScreen import *
from MoveEvaluator.MinimaxMoveSelector import MinimaxMoveSelector
from MoveEvaluator.PositionEvaluator.GreedyEvaluator import GreedyEvaluator
from MoveEvaluator.PositionEvaluator.HeuristicEvaluator import HeuristicEvaluator
from MoveEvaluator.MinimaxWABMoveSelector import MinimaxWABMoveSelector
from MoveEvaluator.MinimaxWABWSMoveSelector import MinimaxWABWSMoveSelector
from MoveEvaluator.NegaScoutMoveSelector import NegaScoutMoveSelector
import time

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
field_color = (0, 128, 0)
valid_move_color = (0, 255, 0)
gray = (127, 127, 127)

white_player = 1
black_player = -1


def calculate_move_in_background(queue, move_selector, board, current_player):
    move = move_selector.getMove(board, current_player)
    queue.put(move)

class Controller:
    def __init__(self):
        self.gameScreen = GameScreen()
        self.gameScreen.set_controller(self)

        self.black_move_selector = None
        self.white_move_selector = None

        self.board = Board()
        self.state = START_SCREEN
        self.played_move = None
        self.current_player = -1

    def get_state(self):
        if self.current_player == -1:
            if self.black_move_selector is not None:
                return BOT_PLAYS
            else:
                return PLAYER_TURN
        else:
            if self.white_move_selector is not None:
                return BOT_PLAYS
            else:
                return PLAYER_TURN

    # Main loop
    # Reversi game logic
    def play_reversi(self):
        # Game setup
        self.current_player = -1

        self.state = START_SCREEN

        # Game loop
        while self.state != EXIT:

            while self.state == START_SCREEN:
                self.gameScreen.start_screen()
                if self.state != START_SCREEN:
                    self.state = self.get_state()

            self.played_move = None

            # Switch player if current player has no valid moves
            if not self.board.has_valid_move(self.current_player):
                self.current_player = -self.current_player
                # pygame.display.set_caption('Player plays again')
                # pygame.time.wait(1000)

            # Draw the board
            self.gameScreen.draw_board(self.board, self.current_player, self.state)

            if self.state == GAME_OVER or self.state == START_SCREEN or self.state == EXIT:
                continue

            # If both players have no valid moves, end the game
            if not self.board.has_valid_move(self.current_player):
                self.state = GAME_OVER
                continue
                
            if self.state == CALCULATING:
                if not queue.empty():
                    move = queue.get()
                    self.board.make_move(self.current_player, *move)
                    self.current_player = -self.current_player
                    self.state = self.get_state()
                continue

            if self.current_player == 1 and self.white_move_selector is not None:
                if self.state != CALCULATING:
                    self.state = CALCULATING
                    queue = Queue()
                    thread = Thread(target=calculate_move_in_background, args=(queue, self.white_move_selector, self.board, self.current_player))
                    thread.start()
            elif self.current_player == -1 and self.black_move_selector is not None:
                if self.state != CALCULATING:
                    self.state = CALCULATING
                    queue = Queue()
                    thread = Thread(target=calculate_move_in_background, args=(queue, self.black_move_selector, self.board, self.current_player))
                    thread.start()
            else:
                # Check for player input
                if self.played_move and self.board.is_valid_move(self.current_player, *self.played_move):
                    self.board.make_move(self.current_player, *self.played_move)
                    self.current_player = -self.current_player
                    self.state = self.get_state()
                    self.played_move = None
    
    def exit(self):
        self.state = EXIT
    
    def play_again(self):
        self.board = Board()
        self.state = START_SCREEN
        self.played_move = None
        self.current_player = -1
    
    def undo_move(self):
        if self.white_move_selector is not None and self.black_move_selector is not None:
            return
        if self.board.undo_move():
            self.current_player = -self.current_player
        if self.white_move_selector is not None or self.black_move_selector is not None:
            if self.board.undo_move():
                self.current_player = -self.current_player
        self.state = PLAYER_TURN
    
    def play_move(self, move):
        self.played_move = move

    def start_game(self, choosen_players, choosen_algorithms, choosen_evaluators, choosen_depths):
        self.state = PLAYER_TURN if choosen_players[0] == "player" else BOT_PLAYS
        if choosen_players[0] == "player":
            self.black_move_selector = None
        else:
            if choosen_evaluators[0] == "greedy":
                self.heuristic_evaluator_b = GreedyEvaluator()
            else:
                self.heuristic_evaluator_b = HeuristicEvaluator()
            choosen_depths[0] = int(choosen_depths[0])
            if choosen_algorithms[0] == "minmax":
                self.black_move_selector = MinimaxMoveSelector(choosen_depths[0], self.heuristic_evaluator_b)
            elif choosen_algorithms[0] == "αβ":
                self.black_move_selector = MinimaxWABMoveSelector(choosen_depths[0], self.heuristic_evaluator_b)
            elif choosen_algorithms[0] == "negascout":
                self.black_move_selector = NegaScoutMoveSelector(choosen_depths[0], self.heuristic_evaluator_b)
            else:
                self.black_move_selector = MinimaxWABWSMoveSelector(choosen_depths[0], self.heuristic_evaluator_b)

        if choosen_players[1] == "player":
            self.white_move_selector = None
        else:
            if choosen_evaluators[1] == "greedy":
                self.heuristic_evaluator_w = GreedyEvaluator()
            else:
                self.heuristic_evaluator_w = HeuristicEvaluator()
            choosen_depths[1] = int(choosen_depths[1])
            if choosen_algorithms[1] == "minmax":
                self.white_move_selector = MinimaxMoveSelector(choosen_depths[1], self.heuristic_evaluator_w)
            elif choosen_algorithms[1] == "αβ":
                self.white_move_selector = MinimaxWABMoveSelector(choosen_depths[1], self.heuristic_evaluator_w)
            elif choosen_algorithms[1] == "negascout":
                self.white_move_selector = NegaScoutMoveSelector(choosen_depths[1], self.heuristic_evaluator_w)
            else:
                self.white_move_selector = MinimaxWABWSMoveSelector(choosen_depths[1], self.heuristic_evaluator_w)