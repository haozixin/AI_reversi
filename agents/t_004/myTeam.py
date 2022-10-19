import math
from template import Agent
from agents.t_004.myTeam_utils import *


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
DEPTH = 3
MID_GAME = 32
EARLY_GAME_THRESHOLD = 28
LATE_GAME_THRESHOLD = 57
INIT_STATIC_WEIGHTS = [
    [4, -3, 2, 2, 2, 2, -3, 4],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [2, -1, 1, 0, 0, 1, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 1, 0, 0, 1, -1, 2],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [4, -3, 2, 2, 2, 2, -3, 4]]

WEIGHT_SETS = [
    [200, -2, 10, 150, 50, 10],  # EARLY
    [200, 1, 10, 150, 50, 15],  # MIDDLE
    [200, 20, 5, 150, 20, 15],  # 57
    [200, 30, 5, 150, 20, 15],  # 58
    [200, 50, 5, 150, 20, 0],  # 59
    [200, 60, 5, 150, 0, 0],  # 60
    [200, 80, 0, 150, 0, 0],  # 61
    [200, 100, 0, 0, 0, 0],  # 62
    [100, 150, 0, 0, 0, 0],  # 63
    [0, 150, 0, 0, 0, 0]  # 64
]  # [corner heu, piece count, mobility, stability, static weights, frontier]


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.depth = DEPTH
        self.agent_id = _id
        self.estimated_board_time = 4

    def SelectAction(self, actions, game_state):
        actions = list(set(actions))
        self.estimated_board_time = getTotalNumOfPieces(game_state) + self.depth
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
        pieceCountHeuValue, staticWeightHeuValue, frontierHeuValue = \
            self.calcPieceCountAndStaticWeightsAndFrontierHeuristics(game_state)

        corner = weights[0] * self.cornerHeuristic(game_state)
        counts = weights[1] * pieceCountHeuValue
        mobility = weights[2] * mobilityHeuValue
        stability = weights[3] * self.stabilityHeuristic(game_state)
        sw = weights[4] * staticWeightHeuValue
        frontier = weights[5] * frontierHeuValue
        total = corner + counts + mobility + stability + sw + frontier

        # msg = "Board time: {}, Corner: {}, Counts: {}, mobility: {}, stability: {}, static weights: {}, frontier: {}, total: {}".format(self.estimated_board_time, corner, counts, mobility, stability, sw, frontier, total)
        # print(msg)

        return total

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

        return 25 * (cornersCaptured - opCornersCaptured)

    def selectWeightSet(self, curr_board_time):
        """
        Dynamically change the weights based on the
        current board situation (time), measured in
        the number of pieces on the board.
        """
        if curr_board_time < EARLY_GAME_THRESHOLD:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 10]
        elif curr_board_time < LATE_GAME_THRESHOLD:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 9]
        elif curr_board_time == LATE_GAME_THRESHOLD:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 8]
        elif curr_board_time == LATE_GAME_THRESHOLD + 1:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 7]
        elif curr_board_time == LATE_GAME_THRESHOLD + 2:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 6]
        elif curr_board_time == LATE_GAME_THRESHOLD + 3:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 5]
        elif curr_board_time == LATE_GAME_THRESHOLD + 4:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 4]
        elif curr_board_time == LATE_GAME_THRESHOLD + 5:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 3]
        elif curr_board_time == LATE_GAME_THRESHOLD + 6:
            return WEIGHT_SETS[len(WEIGHT_SETS) - 2]
        else:  # curr_board_time == 64
            return WEIGHT_SETS[len(WEIGHT_SETS) - 1]

    def calcStability(self, game_state, player):
        """
        Starting from the corners, assess their neighbors, propagate around.
        A location is stable if all four directions have adjacent stable pieces.

        All stable pieces will be counted. As even if one location isn't
        marked as stable due to the sequence of its stable neighbors haven't
        been assessed, when its stable neighbors being assessed, that location
        will be assessed again as a different neighbor.
        """

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
        processingList = []  # store stable pieces, popped later to assess their neighbors

        for i in [0, GRID_SIZE - 1]:
            for j in [0, GRID_SIZE - 1]:
                """Starting from the corners, only corners are immediate stable."""
                if game_state.board[i][j] == game_state.agent_colors[player]:
                    stabilityMatrix[i][j] = True
                    processingList.append((i, j))
                    stablePieces += 1

        while len(processingList) != 0:
            pos = processingList.pop(0)

            for direction in DIRECTIONS:
                """
                For each neighbor.
                (Please NOTE*: x and y are inverse, i.e., x is actually row, y is column.)
                """
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

        return stability - stability_op  # ranges from -64 to 64

    def calcPieceCountAndStaticWeightsAndFrontierHeuristics(self, game_state):
        score = 0
        op_score = 0
        weight = 0
        op_weight = 0
        frontier = 0
        op_frontier = 0

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if game_state.board[row][col] == game_state.agent_colors[self.agent_id]:
                    score += 1
                    weight += INIT_STATIC_WEIGHTS[row][col]

                    if self.estimated_board_time <= MID_GAME:
                        for direction in DIRECTIONS:
                            neighbor = (row + direction[0], col + direction[1])
                            if validPos(neighbor) and game_state.board[neighbor[0]][neighbor[1]] == Cell.EMPTY:
                                frontier += 1
                elif game_state.board[row][col] == game_state.agent_colors[1 - self.agent_id]:
                    op_score += 1
                    op_weight += INIT_STATIC_WEIGHTS[row][col]

                    if self.estimated_board_time <= MID_GAME:
                        for direction in DIRECTIONS:
                            neighbor = (row + direction[0], col + direction[1])
                            if validPos(neighbor) and game_state.board[neighbor[0]][neighbor[1]] == Cell.EMPTY:
                                op_frontier += 1
                else:
                    if self.estimated_board_time > MID_GAME:
                        for direction in DIRECTIONS:
                            neighbor = (row + direction[0], col + direction[1])
                            if validPos(neighbor):
                                if game_state.board[neighbor[0]][neighbor[1]] == \
                                        game_state.agent_colors[self.agent_id]:
                                    frontier += 1
                                elif game_state.board[neighbor[0]][neighbor[1]] == \
                                        game_state.agent_colors[1 - self.agent_id]:
                                    op_frontier += 1

        """denominator always != 0 because of the game initialisation"""
        piece_count_heu = 100 * (score - op_score) / (score + op_score)

        static_weight_heu = weight - op_weight

        frontier_heu = 100 * (op_frontier - frontier) / (frontier + op_frontier) if frontier + op_frontier != 0 else 0

        return piece_count_heu, static_weight_heu, frontier_heu

    def staticWeightsHeuristic(self, game_state):
        weight = 0
        op_weight = 0

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if game_state.board[i][j] == game_state.agent_colors[self.agent_id]:
                    weight += INIT_STATIC_WEIGHTS[i][j]
                elif game_state.board[i][j] == game_state.agent_colors[1 - self.agent_id]:
                    op_weight += INIT_STATIC_WEIGHTS[i][j]

        return weight - op_weight

    def pieceCountHeuristic(self, game_state):
        score, opScore = countScoreForBoth(game_state.board, GRID_SIZE, game_state.agent_colors[self.agent_id])

        return 100 * (score - opScore) / (score + opScore)  # denominator always != 0 because of the game initialisation

    def frontierHeuristic(self, game_state):
        frontier = 0
        op_frontier = 0

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if game_state.board[row][col] == game_state.agent_colors[self.agent_id]:
                    for direction in DIRECTIONS:
                        neighbor = tuple(map(operator.add, (row, col), direction))
                        if validPos(neighbor) and game_state.board[neighbor[0]][neighbor[1]] == Cell.EMPTY:
                            frontier += 1
                elif game_state.board[row][col] == game_state.agent_colors[1 - self.agent_id]:
                    for direction in DIRECTIONS:
                        neighbor = tuple(map(operator.add, (row, col), direction))
                        if validPos(neighbor) and game_state.board[neighbor[0]][neighbor[1]] == Cell.EMPTY:
                            op_frontier += 1

        return 100 * (op_frontier - frontier) / (frontier + op_frontier) if frontier + op_frontier != 0 else 0
