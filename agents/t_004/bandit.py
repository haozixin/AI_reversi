import math
import random


class MultiArmedBandit:

    """ Select an action for this state given from a list given a Q-function """
    def select(self, state, actions, qfunction):
        pass

    """ Reset a multi-armed bandit to its initial configuration """
    def reset(self):
        self.__init__()


class EpsilonGreedy(MultiArmedBandit):
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def reset(self):
        pass

    def select(self, state, actions, qfunction):
        # Select a random action with epsilon probability
        if random.random() < self.epsilon:
            return random.choice(actions)
        (arg_max_q, _) = qfunction.get_max_q(state, actions)
        return arg_max_q


class EpsilonDecreasing(MultiArmedBandit):
    def __init__(self, epsilon=0.2, alpha=0.999):
        self.epsilon_greedy_bandit = EpsilonGreedy(epsilon)
        self.initial_epsilon = epsilon
        self.alpha = alpha

    def reset(self):
        self.epsilon_greedy_bandit = EpsilonGreedy(self.initial_epsilon)

    def select(self, state, actions, qfunction):
        result = self.epsilon_greedy_bandit.select(state, actions, qfunction)
        self.epsilon_greedy_bandit.epsilon *= self.alpha
        return result


class Softmax(MultiArmedBandit):
    def __init__(self, tau=1.0):
        self.tau = tau

    def reset(self):
        pass

    def select(self, state, actions, qfunction):

        # calculate the denominator for the softmax strategy
        total = 0.0
        for action in actions:
            total += math.exp(qfunction.get_q_value(state, action) / self.tau)

        rand = random.random()
        cumulative_probability = 0.0
        result = None
        for action in actions:
            probability = (
                math.exp(qfunction.get_q_value(state, action) / self.tau) / total
            )
            if cumulative_probability <= rand <= cumulative_probability + probability:
                result = action
            cumulative_probability += probability

        return result


class UpperConfidenceBounds(MultiArmedBandit):
    def __init__(self):
        self.total = 0
        # number of times each action has been chosen
        self.times_selected = {}

    def select(self, state, actions, qfunction):
        """
        return an action based on the UCB1 algorithm
        """

        # First execute each action one time
        for action in actions:
            if action not in self.times_selected.keys():
                self.times_selected[action] = 1
                self.total += 1
                return action

        max_actions = []
        max_value = float("-inf")
        for action in actions:
            value = qfunction.get_q_value(state, action) + math.sqrt(
                (2 * math.log(self.total)) / self.times_selected[action]
            )
            if value > max_value:
                max_actions = [action]
                max_value = value
            elif value == max_value:
                max_actions += [action]

        # if there are multiple actions with the highest value
        # choose one randomly
        result = random.choice(max_actions)
        self.times_selected[result] = self.times_selected[result] + 1
        self.total += 1

        return result

