from agents.t_004.bandit import UpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import *
from template import Agent
import random


class myAgent(Agent):
    def __init__(self, _id):
        self.agent_id = _id
        super().__init__(_id)

    def SelectAction(self, actions, game_state):
        # get index of set

        qfunction = QTable()
        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = UpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, qfunction, ucb)

        root_node = single_agent_mcts.mcts()
        print(root_node)

        return random.choice(actions)

