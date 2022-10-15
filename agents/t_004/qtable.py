from collections import defaultdict
from agents.t_004.qfunction import QFunction


class QTable(QFunction):
    def __init__(self, default=0.0):
        self.qtable = defaultdict(lambda: default)

    def update(self, state, agent_id, action, delta):
        self.qtable[(state, agent_id, action)] = self.qtable[(state, action)] + delta

    def get_q_value(self, state, agent_id, action):
        return self.qtable[(state, agent_id, action)]
