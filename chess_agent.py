import abc
import chess
from chess_utils import game_over
from chess_eval import order_moves
import math
import time
import bisect

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

class OutOfTimeException(Exception):
    "The Minimax Agent ran out of time to compute"
    pass

class MinimaxAgent(Agent):

    def __init__(self, color, evaluationFunction, depth=None, moveTime=None, iterate=True):
        if depth is None:
            depth = 1
        if moveTime is None:
            moveTime = math.inf

        self.color = color
        self.evaluationFunction = evaluationFunction
        self.depth = depth
        self.moveTime = moveTime
        self.iterate = iterate

    def times_up(self, startTime):
        return time.time() - startTime > self.moveTime

    def get_next_move(self, chess_board):
        print("minimax move")
        start = time.time()
        alpha = -1 * math.inf
        beta = math.inf
        if self.iterate: 
            v, move, num_eval = self.iterative_minimax(chess_board, self.depth, alpha, beta, start)
        else:
            v, move, num_eval, _ = self.minimax(chess_board, self.depth, self.color, alpha, beta, start)
        end = time.time()
        prefix = f"Iterative Minimax to depth {self.depth}" if self.iterate else f"Minimax to depth {self.depth}"
        print(f"{prefix} took {end-start}, and evaluated {num_eval} positions")
        print(f"Move: {str(move)} with score {v}")
        return str(move)

    def nextAgent(self, color):
        return not color

    def generate_successor(self, chess_board, move):
        board = chess_board.copy()
        board.push(move)
        return board

    def iterative_minimax(self, chess_board, depth, alpha, beta, startTime):
        best_moves = None
        best_move = None
        num_eval = 0
        for i in range(1, self.depth+1):
            v, best_move, new_num_eval, best_moves = self.minimax(chess_board, i, self.color, alpha, beta, startTime, ordered_moves=best_moves)
            num_eval += new_num_eval
            if self.times_up(startTime):
                return best_move, num_eval
        return v, best_move, num_eval
            
    def minimax(self, chess_board, depth, color, alpha, beta, startTime, ordered_moves=None):
        """
        Performs minimax with alpha beta pruning to the given depth, or until the given start time has been reached.
        Returns: Final Evaluation, Best Move, Number of States Evaluated, Ordered List-Of [(Final Evaluation, Best Move)] Tuples
        """
        if ordered_moves is None:
            legal_moves = list(chess_board.legal_moves)
            ordered_moves = order_moves(chess_board, legal_moves)

        if depth == 0 or game_over(chess_board):
            v = self.evaluationFunction(chess_board, self.color)
            move = None
            return v, move, 1, [v, move]

        if depth == self.depth and False:
            my_moves = [x[0] for x in ordered_moves]
            board_moves = list(chess_board.legal_moves)
            print(my_moves)
            print(board_moves)

        best_moves = []
        # Maximize for yourself
        if color == self.color: 
            v = -1 * math.inf
            best_move = None
            eval_acc = 0
            for move, _ in ordered_moves:
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _, child_eval_acc, _ = self.minimax(childState, depth - 1, nextUp, alpha, beta, startTime=startTime)
                bisect.insort(best_moves, (move, new_v), key=lambda x: x[1])
                eval_acc += child_eval_acc
                alpha = max(alpha, new_v)
                if new_v > v:
                    v = new_v
                    best_move = move
                if beta < alpha:
                    break
                if self.times_up(startTime):
                    break
            #print(f"Maximize: {v, best_move, eval_acc, best_moves}")
            return v-1, best_move, eval_acc, best_moves

        # Minimize for opponent
        else:
            v = math.inf
            best_move = None
            eval_acc = 0
            for move, _ in ordered_moves:
                childState = self.generate_successor(chess_board, move)
                nextUp = self.nextAgent(color)
                new_v, _, child_eval_acc, _ = self.minimax(childState, depth - 1, nextUp, alpha, beta, startTime=startTime)
                bisect.insort(best_moves, (move, new_v), key=lambda x: -1*x[1])
                eval_acc += child_eval_acc
                if new_v < v:
                    v = new_v
                    best_move = move
                beta = min(beta, new_v)
                if beta < alpha:
                    break
                if self.times_up(startTime):
                    break
            #print(f"Minimize: {v, best_move, eval_acc, best_moves}")
            return v-1, best_move, eval_acc, best_moves