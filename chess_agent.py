import abc
import chess
from chess_utils import game_over
import math

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
        _, move = self.minimax(chess_board, self.depth * 2, self.color)
        return str(move)

    def nextAgent(self, color):
        return not color

    def generate_successor(self, chess_board, move):
        board = chess_board.copy()
        board.push(move)
        return board

    def minimax(self, chess_board, depth, color):
        if depth == 0 or game_over(chess_board):
            return self.evaluationFunction(chess_board), None

        if color == chess.WHITE: 
            v = -1 * math.inf
            best_move = None
            for move in list(chess_board.legal_moves):
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _ = self.minimax(childState, depth - 1, nextUp)
                if new_v > v:
                    v = new_v
                    best_move = move
            return v, best_move

        else:
            v = math.inf
            best_move = None
            for move in list(chess_board.legal_moves):
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _ = self.minimax(childState, depth - 1, nextUp)
                if new_v < v:
                    v = new_v
                    best_move = move
            return v, best_move