from agents.t_004.bandit import ModifiedUpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import *
from agents.t_004.myTeam_utils import *
from template import Agent

if USE_CSV:
    qTabel = QTable().initial_q_table(Q_FILE_PATH)
    # Node.visits will be set in mcts.py (Node class)
else:
    qTabel = QTable()
    # Node.visits will be initialized in mcts.py (Node class)


class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.agent_id = _id

    def SelectAction(self, actions, game_state):
        actions = list(set(actions))
        static_game_state = embedReversiState(game_state, self.agent_id)

        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = ModifiedUpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, qTabel, ucb)
        single_agent_mcts.mcts()

        return max([(action, qTabel.get_q_value(static_game_state, action))
                    for action in actions], key=lambda x: x[1])[0]
