import copy
import operator
from collections import namedtuple
from Reversi.reversi_utils import GRID_SIZE, Cell

USE_CSV = True  # use csv file to initialize the q_table and visits
Q_FILE_PATH = "agents/t_004/qtable_50.csv"  # which file you want to use to initialize the q_table
V_FILE_PATH = "agents/t_004/Node_visits_50.csv"  # which file you want to use to initialize the visits

# _ERS = namedtuple("EmbeddedReversiState", "board agent_id")

DISCOUNT_FACTOR = 0.96
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# class EmbeddedReversiState(_ERS):
#
#
#     def getBoard(self):
#         return self.board
#
#     def getAgentId(self):
#         return self.agent_id


def embedReversiState(game_state, agent_id):
    return str(game_state.board) + str(agent_id)


def tuple_lise(board):
    new_board = []

    for row in board:
        new_board.append(tuple(row))

    return tuple(new_board)


def gameEnds(game_state):
    if getLegalActions(game_state, 0) == ["Pass"] \
            and getLegalActions(game_state, 1) == ["Pass"]:
        return True
    else:
        return False


def getLegalActions(game_state, agent_id):
    actions = []
    # print(f"Current game state: \n{boardToString(game_state.board,GRID_SIZE)}")
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if game_state.board[i][j] == Cell.EMPTY:
                pos = (i, j)
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


def validPos(pos):
    y, x = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE


def getNextAgentIndex(agent_id):
    return (agent_id + 1) % 2


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
