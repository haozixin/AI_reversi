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
        action=None
    ):
        super().__init__(mdp, parent, state, qfunction, bandit, reward, action)

        self.agent_id = agent_id
        # A dictionary from actions to a set of node-probability pairs
        self.children = {}

    """ Return true if and only if all child actions have been expanded """
    def is_fully_expanded(self):
        valid_actions = self.mdp.get_actions(self.state)
        if len(valid_actions) == len(self.children):
            return True
        else:
            return False

    """ Select a node that is not fully expanded """
    def select(self):
        if not self.is_fully_expanded() or self.mdp.is_terminal(self.state):
            return self
        else:
            """Otherwise fully expanded and not terminal state"""
            actions = list(self.children.keys())
            action = self.bandit.select(self.state, actions, self.qfunction, Node.visits)
            return self.get_outcome_child(action).select()

    """ Expand a node if it is not a terminal node """
    def expand(self):
        if not self.mdp.is_terminal(self.state):
            # Randomly select an unexpanded action to expand
            actions = self.mdp.get_actions(self.state) - self.children.keys()
            action = random.choice(list(actions))

            self.children[action] = []
            return self.get_outcome_child(action)
        return self

    """ Back propagate the reward back to the parent node """
    def back_propagate(self, reward, child):
        action = child.action

        Node.visits[self.state] = Node.visits[self.state] + 1
        Node.visits[(self.state, action)] = Node.visits[(self.state, action)] + 1

        delta = (1 / (Node.visits[(self.state, action)])) * (
            reward - self.qfunction.get_q_value(self.state, action)
        )
        self.qfunction.update(self.state, action, delta)

        if self.parent:  # if parent is not None
            self.parent.back_propagate(self.reward + reward, self)

    """ Simulate the outcome of an action, and return the child node """
    def get_outcome_child(self, action):
        (next_state, reward) = self.mdp.execute(self.state, action)

        # Find the corresponding state and return if this already exists
        if self.children[action]:
            return self.children[action]

        # This outcome has not occurred from this state-action pair previously
        new_child = SingleAgentNode(
            self.mdp, self, next_state, self.qfunction, self.bandit, reward, action
        )

        self.children[action] = new_child
        return new_child


class SingleAgentMCTS(MCTS):
    def create_root_node(self):
        return SingleAgentNode(self.mdp, None, self.mdp.get_initial_state(),
                               self.qfunction, self.bandit, self.mdp.init_agent_id)
