from collections import namedtuple

_ERS = namedtuple("EmbeddedReversiState", "board agent_id")

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
DISCOUNT_FACTOR = 0.9
class EmbeddedReversiState(_ERS):
    def getBoard(self):
        return self.board

    def getAgentId(self):
        return self.agent_id


def embedReversiState(game_state, agent_id):
    return EmbeddedReversiState(board=tuple_lise(game_state.board),
                                agent_id=agent_id)


def tuple_lise(board):
    new_board = []

    for row in board:
        new_board.append(tuple(row))

    return tuple(new_board)
