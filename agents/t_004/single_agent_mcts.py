import random

from agents.t_004.mcts import Node, MCTS


class SingleAgentNode(Node):
    def __init__(
            self,
            mdp,
            parent,
            state,
            qfunction,
            bandit,
            agent_id,
            reward=0.0,
            action=None,
            root_node=False,

    ):
        super().__init__(mdp, parent, state, qfunction, bandit, reward, action)

        # A dictionary from actions to a set of node-probability pairs {action: [(node, probability)]}
        # contains all the children of this node that have been expanded so far
        self.children = {}

        # record the player id, who is going to play at this state
        self.agent_id = agent_id

        # used when generating children
        self.next_agent_id = 1 - agent_id
        self.is_terminal = mdp.is_terminal(state)
        self.is_root = root_node

    """ Return true if and only if all child actions have been expanded """

    def is_fully_expanded(self):
        valid_actions = self.mdp.get_actions(self.state, self.agent_id)
        if len(valid_actions) == len(self.children):
            return True
        else:
            return False

    """ Select a node that is not fully expanded """

    def select(self):
        if not self.is_fully_expanded() or self.is_terminal:
            return self
        else:
            actions = list(self.children.keys())
            action = self.bandit.select(self.state, actions, self.qfunction)
            return self.get_outcome_child(action).select()

    """ Expand a node if it is not a terminal node """

    def expand(self):
        if not self.is_terminal:
            # Randomly select an unexpanded action to expand
            if self.is_root:
                actions = self.mdp.actions
            else:
                actions = self.mdp.get_actions(self.state, self.agent_id) - self.children.keys()
            action = random.choice(list(actions))
            # put new action into children
            self.children[action] = []
            return self.get_outcome_child(action)
        return self

    """ Backpropogate the reward back to the parent node """

    def back_propagate(self, reward, child):
        action = child.action

        Node.visits[self.state] = Node.visits[self.state] + 1
        Node.visits[(self.state, action)] = Node.visits[(self.state, action)] + 1

        q_value = self.qfunction.get_q_value(self.state, action)
        delta = (1 / (Node.visits[(self.state, action)])) * (
                reward - self.qfunction.get_q_value(self.state, action)
        )
        self.qfunction.update(self.state, action, delta)

        if self.parent:  # if parent not None
            self.parent.back_propagate(self.reward + reward, self)

    """ Simulate the outcome of an action, and return the child node """

    def get_outcome_child(self, action):
        """
        Simulate the outcome of an action, and return the child node
        Choose one outcome s' according to the transition probabilities
        """
        # Choose one outcome based on transition probabilities
        (next_state, reward) = self.mdp.execute(self.state, action, self.agent_id)

        # Find the corresponding state and return if this already exists
        for (child, _) in self.children[action]:
            if next_state == child.state:
                return child

        # This outcome has not occured from this state-action pair previously
        new_child = SingleAgentNode(
            self.mdp, self, next_state, self.qfunction, self.bandit, self.next_agent_id, reward, action,
        )

        self.children[action].append((new_child, 1.0))
        return new_child

        # # Find the probability of this outcome (only possible for model-based) for printing the search tree
        # probability = 0.0
        # for (outcome, probability) in self.mdp.get_transitions(self.state, action):
        #     if outcome == next_state:
        #         self.children[action] += [(new_child, probability)]
        #         return new_child

    def get_value(self):
        (_, max_q_value) = self.qfunction.get_max_q(
            self.state, self.mdp.get_actions(self.state, self.agent_id)
        )
        return max_q_value


class SingleAgentMCTS(MCTS):
    def create_root_node(self, agent_id):
        return SingleAgentNode(
            self.mdp, None, self.mdp.get_initial_state(), self.qfunction, self.bandit, agent_id=agent_id,
            root_node=True)
