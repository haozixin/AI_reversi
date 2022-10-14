import copy
import operator

from Reversi.reversi_utils import GRID_SIZE, Cell


# from agents.t_004.myTeam import *

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
class MDP:
    """
    Abstract class
    """

    """ Return all states of this MDP """
    def get_states(self):
        pass

    """ Return all actions with non-zero probability from this state """
    def get_actions(self, state, player):
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
        pass

    """ Return the initial state of this MDP """
    def get_initial_state(self):
        # TODO: Implement this method
        pass

    """ Return all goal states of this MDP """
    def get_goal_states(self):
        pass

    def execute(self, state, action, player):
        pass
        # return (next_state, reward)

class Reversi_mdp(MDP):
    """
    MDP Model
    """
    def __init__(self, actions, game_state):
        self.actions = actions
        self.game_state = game_state

    def get_root_actions(self):
        dic = {}
        for action in self.actions:
            dic[action] = []
        return dic

    def get_actions(self, state, agent_id):
        # TODO: Implement this method
        return getLegalActions(state, agent_id)

    def is_terminal(self, state):
        # state is game_state
        if getLegalActions(state, 0) == ["Pass"] \
                and getLegalActions(state, 1) == ["Pass"]:
            return True
        else:
            return False

    def get_transitions(self, state, action):
        pass

    def get_initial_state(self):
        return self.game_state

    def execute(self, state, action, agent_id):
        """
        return (next_state, reward)
        """
        next_state = generateSuccessor(state, action, agent_id)

        # reward is 1 if we win, -1 if we lose, 0 otherwise
        reward = getReward(state)
        return (next_state, reward)

    def get_discount_factor(self):
        return 0.9

def getReward(state):
    game_is_end = gameEnds(state)
    if game_is_end:
        player_color = state.agent_colors[0]
        board = state.board
        score = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == player_color:
                    score += 1
                if score > 32:
                    return 1
        # we lose the game
        return -1
    else:
        # if the game is not end, return 0
        #TODO: maybe we could calculate stability as reward here
        return 0

def generateSuccessor(game_state, action, agent_id):
    if action == "Pass":
        return game_state
    else:
        next_state = copy.deepcopy(game_state)
        update_color = game_state.agent_colors[agent_id]
        next_state.board[action[0]][action[1]] = update_color
        # iterate over all 8 directions and check pieces that require updates
        for direction in DIRECTIONS:
            cur_pos = (action[0] + direction[0], action[1] + direction[1])
            update_list = list()
            flag = False
            # Only searching for updates if the next piece in the direction is from the agent's opponent
            # if next_state.board[cur_pos[0]][cur_pos[1]] == self.agent_colors[(agent_id+1)%2]:
            while validPos(cur_pos) and next_state.board[cur_pos[0]][cur_pos[1]] != Cell.EMPTY:
                if next_state.board[cur_pos[0]][cur_pos[1]] == update_color:
                    flag = True
                    break
                update_list.append(cur_pos)
                cur_pos = (cur_pos[0] + direction[0], cur_pos[1] + direction[1])
            if flag and len(update_list) != 0:
                for i, j in update_list:
                    next_state.board[i][j] = update_color
        return next_state


def gameEnds(game_state):
    if getLegalActions(game_state, 0) == ["Pass"] \
            and getLegalActions(game_state, 1) == ["Pass"]:
        return True
    else:
        return False

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