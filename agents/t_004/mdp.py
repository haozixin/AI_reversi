import operator

from Reversi.reversi_utils import GRID_SIZE, Cell

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


class MDP:
    """
    Abstract class
    """

    """ Return all states of this MDP """
    def get_states(self):
        pass

    """ Return all actions with non-zero probability from this state """
    def get_actions(self, state):
        # TODO: Implement this method
        pass

    """ Return all non-zero probability transitions for this action
        from this state, as a list of (state, probability) pairs
    """
    def get_transitions(self, state, action):
        # TODO: Implement this method
        pass

    """ Return the reward for transitioning from state to
        nextState via action
    """
    def get_reward(self, state, action, next_state):
        pass

    """ Return true if and only if state is a terminal state of this MDP """
    def is_terminal(self, state):
        # TODO: Implement this method
        pass

    """ Return the discount factor for this MDP """
    def get_discount_factor(self):
        # TODO: Implement this method
        pass

    """ Return the initial state of this MDP """
    def get_initial_state(self):
        # TODO: Implement this method
        pass

    """ Return all goal states of this MDP """
    def get_goal_states(self):
        pass

    def execute(self, state, action):
        pass
        # return (next_state, reward)


class Reversi_mdp(MDP):
    """
    MDP Model
    """
    def __init__(self, agent_id, game_state):
        self.agent_id = agent_id
        self.game_state = game_state

    def get_actions(self, game_state):
        # TODO: Implement this method
        return getLegalActions(game_state, self.agent_id)

    def is_terminal(self, game_state):
        return gameEnds(game_state)

    def get_transitions(self, state, action):
        pass

    def get_initial_state(self):
        return self.game_state

    def execute(self, state, action):
        # TODO: Implement this method
        pass


def validPos(pos):
    x, y = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE


def getLegalActions(game_state, agent_id):
    actions = []
    # print(f"Current game state: \n{boardToString(game_state.board,GRID_SIZE)}")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if game_state.board[x][y] == Cell.EMPTY:
                pos = (x, y)
                appended = False

                for direction in DIRECTIONS:
                    if appended:
                        break

                    temp_pos = tuple(map(operator.add, pos, direction))
                    if validPos(temp_pos) and game_state.getCell(temp_pos) != Cell.EMPTY and game_state.getCell(
                            temp_pos) != game_state.agent_colors[agent_id]:
                        while validPos(temp_pos):
                            if game_state.getCell(temp_pos) == Cell.EMPTY:
                                break
                            if game_state.getCell(temp_pos) == game_state.agent_colors[agent_id]:
                                actions.append(pos)
                                appended = True
                                break
                            temp_pos = tuple(map(operator.add, temp_pos, direction))

    if len(actions) == 0:
        actions.append("Pass")

    return actions


def getTotalNumOfPieces(game_state):
    """
    Returns the total number of
    pieces on the board in the current
    game state.
    """
    count = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if game_state.board[i][j] != Cell.EMPTY:
                count += 1

    return count


def getNextAgentIndex(agent_id):
    return (agent_id + 1) % 2


def gameEnds(game_state):
    if getLegalActions(game_state, 0) == ["Pass"] \
            and getLegalActions(game_state, 1) == ["Pass"]:
        return True
    else:
        return False


def countScoreForBoth(board, grid_size, player_color):
    score = 0
    opScore = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] == player_color:
                score += 1
            elif board[i][j] != Cell.EMPTY:
                """Opponent color"""
                opScore += 1

    return score, opScore
