import copy
import math
import operator

from Reversi.reversi_utils import Cell, GRID_SIZE
from template import Agent

EARLY_GAME_THRESHOLD = 28
LATE_GAME_THRESHOLD = 57
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.depth = 3
        self.agent_id = _id
        self.stabilityMatrix = None

    def SelectAction(self, actions, game_state):
        actions = list(set(actions))
        return self.minimax(self.depth, self.agent_id, game_state, actions, -math.inf, math.inf, 0)[1]

    def minimax(self, depth, currentPlayer, game_state, actions, alpha, beta, mobilityHeuValue):
        """
        A function which maximises the heuristic hence the win rate of
        the agent and minimises the opponent agent. This function assumes
        the best play from the opponent measured by us. This function embeds
        the alpha-beta pruning strategy which gets rid of unnecessary
        calculation that doesn't improve the results to save time complexity.

        depth: The remaining depth of the search.
        currentPlayer: The agent id of the current player.
        """

        if depth == 0 or gameEnds(game_state):
            return self.evaluation(game_state, self.selectWeightSet(getTotalNumOfPieces(game_state)),
                                   mobilityHeuValue / self.depth), None

        if currentPlayer == self.agent_id:  # It's our turn, we want to maximise
            maxEval = (-math.inf, None)

            for action in actions:
                child_state = generateSuccessor(game_state, action, currentPlayer)
                nextPlayer = getNextAgentIndex(currentPlayer)
                nextPlayerActions = getLegalActions(child_state, nextPlayer)
                eval = self.minimax(depth - 1, nextPlayer, child_state,
                                    nextPlayerActions, alpha, beta,
                                    mobilityHeuValue + self.mobilityHeuristic(len(actions), len(nextPlayerActions)))[0]
                maxEval = max(maxEval, (eval, action), key=lambda x: x[0])
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return maxEval
        else:  # It's opponent turn, minimise to simulate them maximising
            minEval = (math.inf, None)

            for action in actions:
                child_state = generateSuccessor(game_state, action, currentPlayer)
                nextPlayer = getNextAgentIndex(currentPlayer)
                nextPlayerActions = getLegalActions(child_state, nextPlayer)
                eval = self.minimax(depth - 1, nextPlayer, child_state,
                                    nextPlayerActions, alpha, beta,
                                    mobilityHeuValue + self.mobilityHeuristic(len(nextPlayerActions), len(actions)))[0]
                minEval = min(minEval, (eval, action), key=lambda x: x[0])
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return minEval

    def evaluation(self, game_state, weights, mobilityHeuValue):
        return weights[0] * self.cornerHeuristic(game_state) \
               + weights[1] * self.pieceCountHeuristic(game_state) \
               + weights[2] * mobilityHeuValue + weights[3] * self.stabilityHeuristic(game_state)

    def mobilityHeuristic(self, mobility, mobility_op):
        if (mobility + mobility_op) != 0:
            return 100 * (mobility - mobility_op) / (mobility + mobility_op)
        else:
            return 0

    def cornerHeuristic(self, game_state):
        cornersCaptured = 0

        if game_state.board[0][0] == game_state.agent_colors[self.agent_id]:
            cornersCaptured += 1
        if game_state.board[0][GRID_SIZE - 1] == game_state.agent_colors[self.agent_id]:
            cornersCaptured += 1
        if game_state.board[GRID_SIZE - 1][0] == game_state.agent_colors[self.agent_id]:
            cornersCaptured += 1
        if game_state.board[GRID_SIZE - 1][GRID_SIZE - 1] == game_state.agent_colors[self.agent_id]:
            cornersCaptured += 1

        opCornersCaptured = 0
        op_agent_id = getNextAgentIndex(self.agent_id)

        if game_state.board[0][0] == game_state.agent_colors[op_agent_id]:
            opCornersCaptured += 1
        if game_state.board[0][GRID_SIZE - 1] == game_state.agent_colors[op_agent_id]:
            opCornersCaptured += 1
        if game_state.board[GRID_SIZE - 1][0] == game_state.agent_colors[op_agent_id]:
            opCornersCaptured += 1
        if game_state.board[GRID_SIZE - 1][GRID_SIZE - 1] == game_state.agent_colors[op_agent_id]:
            opCornersCaptured += 1

        if (cornersCaptured + opCornersCaptured) != 0:
            return 100 * (cornersCaptured - opCornersCaptured) / (cornersCaptured + opCornersCaptured)
        else:
            return 0

    def pieceCountHeuristic(self, game_state):
        score, opScore = countScoreForBoth(game_state.board, GRID_SIZE, game_state.agent_colors[self.agent_id])

        return 100 * (score - opScore) / (score + opScore)  # denominator always != 0 because of the game initialisation

    def selectWeightSet(self, curr_board_time):
        """
        Dynamically changing the weights based on the
        current board situation (time), measured in
        the number of pieces on the board.
        """
        weight_sets = [
            [100, -10, 5, 20],  # EARLY
            [100, 5, 5, 15],  # MIDDLE
            [100, 20, 5, 10],  # 57
            [100, 35, 5, 0],   # 58
            [100, 50, 3, 0],  # 59
            [100, 60, 3, 0],  # 60
            [100, 65, 3, 0],  # 61
            [100, 70, 3, 0],  # 62
            [100, 150, 0, 0],  # 63
            [0, 150, 0, 0]  # 64
        ]  # [corner heu, piece count, mobility]

        if curr_board_time < EARLY_GAME_THRESHOLD:
            return weight_sets[0]
        elif curr_board_time < LATE_GAME_THRESHOLD:
            return weight_sets[1]
        elif curr_board_time == LATE_GAME_THRESHOLD:
            return weight_sets[2]
        elif curr_board_time == LATE_GAME_THRESHOLD + 1:
            return weight_sets[3]
        elif curr_board_time == LATE_GAME_THRESHOLD + 2:
            return weight_sets[4]
        elif curr_board_time == LATE_GAME_THRESHOLD + 3:
            return weight_sets[5]
        elif curr_board_time == LATE_GAME_THRESHOLD + 4:
            return weight_sets[6]
        elif curr_board_time == LATE_GAME_THRESHOLD + 5:
            return weight_sets[7]
        elif curr_board_time == LATE_GAME_THRESHOLD + 6:
            return weight_sets[8]
        else:  # curr_board_time == 64
            return weight_sets[9]

    def calcStability(self, game_state, player):
        def isStableHorizontal(disc, stabilityMatrix1):
            if disc[1] in [0, GRID_SIZE - 1]:
                return True
            elif stabilityMatrix1[disc[0]][disc[1] - 1] == 1 \
                    or stabilityMatrix1[disc[0]][disc[1] + 1] == 1:
                return True
            else:
                return False

        def isStableVertical(disc, stabilityMatrix1):
            if disc[0] in [0, GRID_SIZE - 1]:
                return True
            elif stabilityMatrix1[disc[0] - 1][disc[1]] == 1 \
                    or stabilityMatrix1[disc[0] + 1][disc[1]] == 1:
                return True
            else:
                return False

        def isStableLeftDiagonal(disc, stabilityMatrix1):
            if disc[0] == 0 or disc[1] == 0 or disc[0] == GRID_SIZE - 1 or disc[1] == GRID_SIZE - 1:
                return True
            elif stabilityMatrix1[disc[0] - 1][disc[1] - 1] or stabilityMatrix1[disc[0] + 1][disc[1] + 1]:
                return True
            else:
                return False

        def isStableRightDiagonal(disc, stabilityMatrix1):
            if disc[0] == 0 or disc[1] == 0 or disc[0] == GRID_SIZE - 1 or disc[1] == GRID_SIZE - 1:
                return True
            elif stabilityMatrix1[disc[0] - 1][disc[1] + 1] or stabilityMatrix1[disc[0] + 1][disc[1] - 1]:
                return True
            else:
                return False

        stablePieces = 0
        stabilityMatrix = [[False for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        processingList = []

        for i in [0, GRID_SIZE - 1]:
            for j in [0, GRID_SIZE - 1]:
                if game_state.board[i][j] == game_state.agent_colors[player]:
                    stabilityMatrix[i][j] = True
                    processingList.append((i, j))
                    stablePieces += 1

        while len(processingList) != 0:
            pos = processingList.pop(0)

            for direction in DIRECTIONS:
                x, y = tuple(map(operator.add, pos, direction))

                if not validPos((x, y)):
                    continue
                if not game_state.board[x][y] == game_state.agent_colors[player]:
                    continue
                if stabilityMatrix[x][y]:
                    continue

                if isStableVertical((x, y), stabilityMatrix) \
                        and isStableHorizontal((x, y), stabilityMatrix) \
                        and isStableLeftDiagonal((x, y), stabilityMatrix) \
                        and isStableRightDiagonal((x, y), stabilityMatrix):
                    stablePieces += 1
                    stabilityMatrix[x][y] = True
                    processingList.append((x, y))

        return stablePieces

    def stabilityHeuristic(self, game_state):
        stability = self.calcStability(game_state, self.agent_id)
        stability_op = self.calcStability(game_state, getNextAgentIndex(self.agent_id))

        if stability + stability_op != 0:
            return 100 * (stability - stability_op) / (stability + stability_op)
        else:
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


def validPos(pos):
    x, y = pos
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