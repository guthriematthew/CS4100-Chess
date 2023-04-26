import chess
import random
import copy
import enum
from chess_utils import game_over

class ChessColors(enum.Enum):
    White = "white"
    Black = "black"

STARTING_AGENTS = {chess.WHITE: None, chess.BLACK: None}

class ChessGame(object):

    def __init__(self, starting_position=None, white_to_move=True):
        if not starting_position:
            starting_position = chess.STARTING_BOARD_FEN

        self.board = chess.Board(starting_position)
        self.board.turn = white_to_move
        self.white_to_move = white_to_move
        self._agents = copy.deepcopy(STARTING_AGENTS)
        self.moves = []

    def register_agent(self, agent, as_white):
        if self.num_agents == 2:
            raise ValueError("A game of Chess has only two players")

        if as_white and self._agents[chess.WHITE]:
            raise ValueError("There is already a white player playing the game")

        if not as_white and self._agents[chess.BLACK]:
            raise ValueError("There is already a black player playing the game")

        hash = random.getrandbits(128)
        agent.register(hash)
        if as_white:
            self._agents[chess.WHITE] = agent
        else: 
            self._agents[chess.BLACK] = agent

    def can_make_move(self, agent_id=None, move=None):
        if agent_id is None and move is None:
            return True, None

        if agent_id is None or move is None:
            return False, "Cannot validate without knowing both agent and move"

        if self.white_to_move and agent_id != self._agents[chess.WHITE].id:
            return False, "A non-white player attempted to move during white's turn"

        if not self.white_to_move and agent_id != self._agents[chess.BLACK].id:
            return False, "A non-black player attempted to move during black's turn"

        if self.board.is_checkmate():
            return False, "The board is in checkmate - the game is over"

        if chess.Move.from_uci(move) not in self.board.legal_moves:
            return False, "The given move is illegal"

        return True, None

    def make_move(self, agent_id, move):
        can_move, reason = self.can_make_move(agent_id, move)
        if not can_move:
            raise ValueError(reason)

        move_as_move = chess.Move.from_uci(move)
        self.board.push(move_as_move)
        self.white_to_move = not self.white_to_move

    def play_game(self):
        if self.num_agents != 2:
            raise Exception("The game is not ready to be played")

        display_buffer = "==============="
        print(display_buffer)
        print("Starting Position:")
        print(self.board)
        print(display_buffer)

        while(not self.game_over()):
            if self.white_to_move:
                moving_agent = self._agents[chess.WHITE]
            else:
                moving_agent = self._agents[chess.BLACK]
            
            move = moving_agent.get_next_move(self.board)
            self.moves.append(move)

            self.make_move(moving_agent.id, move)

            print(self.board)
        print(display_buffer)

        outcome = self.board.outcome(claim_draw=True)
        result = outcome.result()

        print(f"The game is over, result: {result}")
        print(f'Moves {self.moves}')
        return outcome

    def game_over(self):
        return game_over(self.board)

    def get_legal_actions():
        return self.board.legal_moves()

    @property
    def num_agents(self):
        num_agents = 0
        num_agents += 1 if self._agents[chess.WHITE] else 0
        num_agents += 1 if self._agents[chess.BLACK] else 0

        return num_agents

    @property
    def agent_ids(self):
        return copy.deepcopy(self._agents)
    

