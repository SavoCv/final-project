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
        # self.solver = GreddyMinimaxSolver(3)
        # self.solver = PositionalMinimaxSolver(3)
        # self.solver = MinimaxMoveSelector(3, GreedyEvaluator())
        # self.solver = MinimaxMoveSelector(2, HeuristicEvaluator())
        # self.solver = MinimaxWABMoveSelector(3, HeuristicEvaluator())
        self.heuristic_evaluator_w = HeuristicEvaluator()
        self.tmp_eval = HeuristicEvaluator()
        self.heuristic_evaluator_b = HeuristicEvaluator()
        self.white_move_selector = MinimaxWABMoveSelector(4, self.heuristic_evaluator_w)
        self.tmp_move_selector =      NegaScoutMoveSelector(4, self.tmp_eval)
        self.black_move_selector = MinimaxWABMoveSelector(4, self.heuristic_evaluator_b)
        self.board = Board()
        self.gameScreen = GameScreen()
        self.gameScreen.set_controller(self)
        self.state = PLAYER_TURN
        self.played_move = None

    # Main loop
    # Reversi game logic
    def play_reversi(self):
        # Game setup
        current_player = -1
        white_time = 0
        white_evaluations = 0
        black_time = 0  
        black_evalutations = 0
        tmp_time = 0
        tmp_evalutations = 0

        self.state = BOT_PLAYS

        # Game loop
        while self.state != EXIT:
            self.played_move = None

            # Switch player if current player has no valid moves
            if not self.board.has_valid_move(current_player):
                current_player = -current_player
                # pygame.display.set_caption('Player plays again')
                # pygame.time.wait(1000)

            # Draw the board
            self.gameScreen.draw_board(self.board, current_player, self.state)

            # Update display
            pygame.display.flip()

            # If both players have no valid moves, end the game
            if not self.board.has_valid_move(current_player):
                self.state = GAME_OVER
                self.gameScreen.draw_board(self.board, current_player, self.state)
                print("Game over")
                print("White time", white_time)
                print("White evaluations", white_evaluations)
                print("Tmp time", tmp_time)
                print("Tmp evaluations", tmp_evalutations)
                print("Black time", black_time)
                print("Black evaluations", black_evalutations)
                white_time = white_evaluations = black_time = black_evalutations = tmp_time = tmp_evalutations = 0
                end_game = self.gameScreen.end_game_dialog(self.board)
                if end_game:
                    return
                self.board = Board()
                current_player = -1
                self.state = BOT_PLAYS
            
            evaluate = True

            if evaluate and current_player == 1:
                if self.state != CALCULATING:
                    self.state = CALCULATING
                    queue = Queue()
                    thread = Thread(target=calculate_move_in_background, args=(queue, self.white_move_selector, self.board, current_player))
                    thread.start()
                else:
                    if not queue.empty():
                        move = queue.get()
                        self.board.make_move(current_player, *move)
                        current_player = -current_player
                        self.state = PLAYER_TURN
            elif evaluate and current_player == -1:
                if self.state != CALCULATING:
                    self.state = CALCULATING
                    queue = Queue()
                    thread = Thread(target=calculate_move_in_background, args=(queue, self.black_move_selector, self.board, current_player))
                    thread.start()
                else:
                    if not queue.empty():
                        move = queue.get()
                        self.board.make_move(current_player, *move)
                        current_player = -current_player
                        self.state = PLAYER_TURN
            else:
                # Check for player input
                if self.played_move:
                    self.board.make_move(current_player, *self.played_move)
                    current_player = -current_player
                    self.played_move = None
    
    def exit(self):
        self.state = EXIT
    
    def undo(self):
        self.board.undo_move()
        self.board.undo_move()
        self.state = PLAYER_TURN
    
    def play_move(self, move):
        # self.state = BOT_PLAYS
        self.played_move = move
