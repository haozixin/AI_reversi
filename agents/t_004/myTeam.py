from agents.t_004.bandit import ModifiedUpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import *
from template import Agent
from collections import namedtuple


_ERS = namedtuple("EmbeddedReversiState", "board agent_colors agent_id")


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.agent_id = _id
        self.states = set()
        self.qfunction = QTable()

    def SelectAction(self, actions, game_state):
        # get index of set
        actions = list(set(actions))
        game_state = embedReversiState(game_state, self.agent_id)
        self.states.add(game_state)

        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = ModifiedUpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, self.qfunction, ucb)
        single_agent_mcts.mcts()

        return max([(action, self.qfunction.get_q_value(game_state, self.agent_id, action))
                    for action in actions], key=lambda x: x[1])[0]


class EmbeddedReversiState(_ERS):
    def getBoard(self):
        return self.board

    def getAgentColor(self):
        return self.agent_colors

    def getAgentId(self):
        return self.agent_id

    def getCell(self, cell):
        x, y = cell
        return self.board[x][y]


def embedReversiState(game_state, agent_id):
    return EmbeddedReversiState(board=game_state.board, agent_colors=game_state.agent_colors, agent_id=agent_id)


def tuple_lise(board):
    new_board = []

    for row in board:
        new_board.append(tuple(row))

    return tuple(new_board)
