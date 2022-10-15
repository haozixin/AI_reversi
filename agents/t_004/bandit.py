import math
import random


class MultiArmedBandit:

    """ Select an action for this state given from a list given a Q-function """
    def select(self, state, actions, qfunction, node_visits):
        pass

    """ Reset a multi-armed bandit to its initial configuration """
    def reset(self):
        self.__init__()


class ModifiedUpperConfidenceBounds(MultiArmedBandit):
    """
    Note: This is a modified version of UCB1, in order to
    fit the dedicated MCTS algorithm.
    """

    def select(self, state, actions, qfunction, node_visits, C=0.5):
        """
        return an action based on the UCB1 algorithm.

        All actions are supposed to be selected at least once,
        as guaranteed by MCTS selection: i.e., no MultiArmedBandit
        selection will be called unless all actions are expanded
        for a particular node.
        """
        max_actions = []
        max_value = float("-inf")

        for action in actions:
            value = qfunction.get_q_value(state, action) + C * math.sqrt(
                2 * math.log(node_visits[state]) / node_visits[(state, action)])

            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        # if there are multiple actions with the highest value
        # choose one randomly
        result = random.choice(max_actions)

        return result

