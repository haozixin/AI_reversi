from agents.t_004.bandit import ModifiedUpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import *
from template import Agent


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.agent_id = _id
        self.qfunction = QTable()

    def SelectAction(self, actions, game_state):
        # get index of set
        actions = list(set(actions))

        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = ModifiedUpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, self.qfunction, ucb)
        single_agent_mcts.mcts()

        return max([(action, self.qfunction.get_q_value(game_state, action))
                    for action in actions], key=lambda x: x[1])[0]

