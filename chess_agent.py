import abc
import chess
from chess_utils import game_over
from chess_eval import order_moves
import math
import time

#Abstract Class for Agents
class Agent(metaclass=abc.ABCMeta):

    def register(self, hash):
        self.id = hash

    def get_next_move(self, board):
        pass


class HumanAgent(Agent):

    def get_next_move(self, board):
        move = input("Make your move, in UCI Notation: ")
        return move

class WhiteScholarAgent(Agent):

    def __init__(self):
        self.moves = ["e2e4", "d1f3", "f1c4", "f3f7"]
        self.counter = 0

    def get_next_move(self, board):
        move = self.moves[self.counter]
        self.counter += 1
        return move

class BlackScholarAgent(Agent):

    def __init__(self):
        self.moves = ["e7e5", "b8c6", "a7a6"]
        self.counter = 0

    def get_next_move(self, board):
        move = self.moves[self.counter]
        self.counter += 1
        return move

class MinimaxAgent(Agent):

    def __init__(self, color, evaluationFunction, depth=None):
        if depth is None:
            depth = 1

        self.color = color
        self.evaluationFunction = evaluationFunction
        self.depth = depth

    def get_next_move(self, chess_board):
        print("minimax move")
        start = time.time()
        _, move, num_eval = self.minimax(chess_board, self.depth, self.color, -1 * math.inf, math.inf)
        end = time.time()
        print(f"Minimax took {end-start}, and evaluated {num_eval} positions")
        return str(move)

    def nextAgent(self, color):
        return not color

    def generate_successor(self, chess_board, move):
        board = chess_board.copy()
        board.push(move)
        return board

    def minimax(self, chess_board, depth, color, alpha, beta):
        if depth == 0 or game_over(chess_board):
            return self.evaluationFunction(chess_board, self.color), None, 1

        legal_moves = list(chess_board.legal_moves)
        ordered_moves = order_moves(chess_board, legal_moves)

        # Maximize for yourself
        if color == self.color: 
            v = -1 * math.inf
            best_move = None
            eval_acc = 0
            for move in ordered_moves:
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _, child_eval_acc = self.minimax(childState, depth - 1, nextUp, alpha, beta)
                eval_acc += child_eval_acc
                alpha = max(alpha, new_v)
                if new_v > v:
                    v = new_v
                    best_move = move
                if beta < alpha:
                    break
            return v, best_move, eval_acc

        # Minimize for opponent
        else:
            v = math.inf
            best_move = None
            eval_acc = 0
            for move in ordered_moves:
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _, child_eval_acc = self.minimax(childState, depth - 1, nextUp, alpha, beta)
                eval_acc += child_eval_acc
                if new_v < v:
                    v = new_v
                    best_move = move
                beta = min(beta, new_v)
                if beta < alpha:
                    break
            return v, best_move, eval_acc