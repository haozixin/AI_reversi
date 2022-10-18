from collections import defaultdict
from agents.t_004.bandit import ModifiedUpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import *
from agents.t_004.myTeam_utils import *
from template import Agent


qTabel = QTable()
n_visits = defaultdict(lambda: 0)



class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.agent_id = _id

    def SelectAction(self, actions, game_state):
        global qTabel
        global n_visits
        actions = list(set(actions))
        static_game_state = embedReversiState(game_state, self.agent_id)

        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = ModifiedUpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, qTabel, ucb, node_visits=n_visits)
        single_agent_mcts.mcts()

        n_visits = Node.visits

        return max([(action, qTabel.get_q_value(static_game_state, action))
                    for action in actions], key=lambda x: x[1])[0]





