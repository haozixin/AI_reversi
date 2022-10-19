import utils
import math
import time
import random
from collections import defaultdict
from Reversi.reversi_utils import GRID_SIZE
import pandas as pd
from agents.t_004.myTeam_utils import USE_CSV, V_FILE_PATH

TIMEOUT = 0.9


class Node:
    # Records the number of times states have been visited
    if USE_CSV:
        # read the csv file
        df = pd.read_csv(V_FILE_PATH, index_col=0)
        # convert the dataframe to dictionary (defaultdict)
        # default value is 0
        df.reset_index(inplace=True)
        key = df["index"]
        values = df["0"].apply(lambda x: float(x))
        data = dict(zip(key, values))

        visits = defaultdict(lambda: 0.0, data)
        # visits = defaultdict(lambda: 0)
    else:
        visits = defaultdict(lambda: 0)

    def __init__(self, mdp, parent, state, qfunction, bandit, reward=0.0, action=None):
        self.mdp = mdp
        self.parent = parent
        self.state = state

        # The Q function used to store state-action values
        self.qfunction = qfunction

        # A multi-armed bandit for this node
        self.bandit = bandit

        # The immediate reward received for reaching this state, used for backpropagation
        self.reward = reward

        # The action that generated this node
        self.action = action

    """ Select a node that is not fully expanded """

    def select(self):
        utils.raiseNotDefined()
        pass

    """ Expand a node if it is not a terminal node """

    def expand(self):
        utils.raiseNotDefined()
        pass

    """ Backpropogate the reward back to the parent node """

    def back_propagate(self, reward, child):
        utils.raiseNotDefined()
        pass

    """ Return the value of this node """

    def get_value(self):
        utils.raiseNotDefined()
        pass

    """ Get the number of visits to this state """

    def get_visits(self):
        return Node.visits[self.state]


class MCTS:
    def __init__(self, mdp, qfunction, bandit):
        self.mdp = mdp
        self.qfunction = qfunction
        self.bandit = bandit

    """
    Execute the MCTS algorithm from the initial state given, with timeout in seconds
    """

    # MCTS rollout
    def mcts(self, timeout=TIMEOUT, root_node=None):
        if root_node is None:
            root_node = self.create_root_node()

        start_time = time.time()
        current_time = time.time()
        while current_time < start_time + timeout:
            # Find a state node to expand
            selected_node = root_node.select()
            if not self.mdp.is_terminal(selected_node.state):
                child = selected_node.expand()
                reward = self.simulate(child)
                selected_node.back_propagate(reward, child)

            current_time = time.time()
        return root_node

    """ Create a root node representing an initial state """

    def create_root_node(self):
        utils.raiseNotDefined()
        pass

    """ Choose a random action. Heuristics can be used here to improve simulations."""

    # TODO: Implement a better action selection heuristic
    def choose(self, state, agent_id):
        actions = self.mdp.get_actions(state, agent_id)

        for action in actions:
            if action in [(0, 0), (0, GRID_SIZE - 1), (GRID_SIZE - 1, 0), (GRID_SIZE - 1, GRID_SIZE - 1)]:
                return action

        return random.choice(actions)

    """ Simulate until a terminal state """

    def simulate(self, node):
        state = node.state
        cumulative_reward = 0.0
        depth = 0
        current_agent = node.agent_id

        while not self.mdp.is_terminal(state):
            # Choose an action to execute
            action = self.choose(state, current_agent)

            # Execute the action
            (next_state, reward) = self.mdp.execute(state, action, current_agent)

            # Discount the reward
            cumulative_reward += pow(self.mdp.get_discount_factor(), depth) * reward
            depth += 1
            state = next_state
            current_agent = 1 - current_agent

        return cumulative_reward
