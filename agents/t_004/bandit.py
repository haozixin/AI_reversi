import math
import random


class MultiArmedBandit:
    """ Select an action for this state given from a list given a Q-function """

    def select(self, state, agent_id, actions, qfunction, node_visits, maximising):
        pass

    """ Reset a multi-armed bandit to its initial configuration """

    def reset(self):
        self.__init__()


class ModifiedUpperConfidenceBounds(MultiArmedBandit):
    """
    Note: This is a modified version of UCB1, in order to
    fit the dedicated MCTS algorithm.
    """

    def select(self, state, actions, qfunction, node_visits, maximising, C=1):
        """
        return an action based on the UCB1 algorithm.

        All actions are supposed to be selected at least once,
        as guaranteed by MCTS selection: i.e., no MultiArmedBandit
        selection will be called unless all actions are expanded
        for a particular node.
        """
        best_actions = []
        best_value = -math.inf if maximising else math.inf

        for action in actions:
            value = qfunction.get_q_value(state, action) + C * math.sqrt(
                2 * math.log(node_visits[state]) / node_visits[(state, action)])

            if maximising:
                if value > best_value:
                    best_actions = [action]
                    best_value = value
                elif value == best_value:
                    best_actions += [action]
            else:
                if value < best_value:
                    best_actions = [action]
                    best_value = value
                elif value == best_value:
                    best_actions += [action]

        # if there are multiple actions with the highest value
        # choose one randomly
        result = random.choice(best_actions)

        return result
