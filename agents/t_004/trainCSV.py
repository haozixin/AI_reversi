
from agents.t_004.bandit import ModifiedUpperConfidenceBounds
from agents.t_004.mdp import Reversi_MDP
from agents.t_004.qtable import QTable
from agents.t_004.single_agent_mcts import SingleAgentMCTS, Node
from agents.t_004.myTeam_utils import *
from template import Agent
import pandas as pd


if USE_CSV:
    qTabel = QTable().initial_q_table(Q_FILE_PATH)
else:
    qTabel = QTable()
counter = 0


class myAgent(Agent):

    def __init__(self, _id):
        super().__init__(_id)
        self.agent_id = _id

    def SelectAction(self, actions, game_state):
        global qTabel
        global counter
        actions = list(set(actions))
        static_game_state = embedReversiState(game_state, self.agent_id)

        mdp = Reversi_MDP(self.agent_id, game_state, actions)
        ucb = ModifiedUpperConfidenceBounds()
        single_agent_mcts = SingleAgentMCTS(mdp, qTabel, ucb)
        single_agent_mcts.mcts()

        # if the game is over, save the qtable to a csv file
        print(qTabel.qtable)
        counter += 1
        # out put the qtable to a csv file when the game is around going to the 50th round/ 100th round/ 150th round...
        if counter in [50*30, 150*30, 200*30, 300*30]:
            update_q_to_csv()

        return max([(action, qTabel.get_q_value(static_game_state, action))
                    for action in actions], key=lambda x: x[1])[0]


def update_q_to_csv():
    """
    save the qtable to csv file using pandas
    """
    # using pandas
    # format:
    #         0
    # (1, 2)  3
    # (4, 5)  6

    global qTabel
    global counter

# self.qtable[(state, action)]

    df = pd.DataFrame.from_dict(qTabel.qtable, orient='index')
    # under the t_004 folder
    df.to_csv('./qtable_'+str(int(counter/30))+'.csv')

    # same Node.visits to csv file
    df = pd.DataFrame.from_dict(Node.visits, orient='index')
    df.to_csv('./Node_visits_'+str(int(counter/30))+'.csv')



