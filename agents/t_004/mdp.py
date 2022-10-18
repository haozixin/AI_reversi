import copy
import operator
from abc import abstractmethod
from Reversi.reversi_utils import GRID_SIZE, Cell
from agents.t_004.myTeam_utils import *


class MDP:
    """
    Abstract class
    """

    """ Return all actions with non-zero probability from this state """
    @abstractmethod
    def get_actions(self, state, agent_id):
        pass

    # """ Return all non-zero probability transitions for this action
    #     from this state, as a list of (state, probability) pairs
    # """
    # @abstractmethod
    # def get_transitions(self, state, action):
    #     pass

    """ Return the reward for transitioning from state to
        nextState via action
    """
    @abstractmethod
    def get_reward(self, state, action, next_state):
        pass

    """ Return true if and only if state is a terminal state of this MDP """
    @abstractmethod
    def is_terminal(self, state):
        # TODO: Implement this method
        pass

    """ Return the discount factor for this MDP """
    @abstractmethod
    def get_discount_factor(self):
        pass

    """ Return the initial state of this MDP """
    @abstractmethod
    def get_initial_state(self):
        # TODO: Implement this method
        pass


class Reversi_MDP(MDP):
    def __init__(self, agent_id, game_state, actions):
        self.init_agent_id = agent_id
        self.actions = actions
        self.game_state = game_state
        self.legalActionsDict = {}

    def get_actions(self, game_state, agent_id):
        embeddedGameState = embedReversiState(game_state, agent_id)
        if embeddedGameState in self.legalActionsDict:
            return self.legalActionsDict[embeddedGameState]
        else:
            legalActions = getLegalActions(game_state, agent_id)
            self.legalActionsDict[embeddedGameState] = legalActions
            return legalActions

    def is_terminal(self, game_state):
        return gameEnds(game_state)

    def get_reward(self, game_state, action, next_state):
        if gameEnds(next_state):
            score, opScore = countScoreForBoth(next_state.board, GRID_SIZE, next_state.agent_colors[self.init_agent_id])

            if score > opScore:
                return 1
            elif score == opScore:
                return 0
            else:
                return -1
        else:
            return 0.0

    def get_initial_state(self):
        return self.game_state

    def execute(self, game_state, action, agent_id):
        next_state = generateSuccessor(game_state, action, agent_id)
        return next_state, self.get_reward(game_state, action, next_state)

    def get_discount_factor(self):
        return DISCOUNT_FACTOR


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
