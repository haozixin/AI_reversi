import copy
import math
import operator

from Reversi.reversi_model import ReversiGameRule
from Reversi.reversi_utils import Cell, GRID_SIZE, countScore
from template import Agent


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.depth = 3
        self.agent_id = _id

    def SelectAction(self, actions, game_state):
        actions = list(set(actions))
        return self.minimax(self.depth, self.agent_id, game_state, actions, -math.inf, math.inf)[1]

    def minimax(self, depth, currentPlayer, game_state, actions, alpha, beta):
        """
        A function which maximises the heuristic hence the win rate of
        the agent and minimises the opponent agent. This function assumes
        the best play from the opponent measured by us. This function embeds
        the alpha-beta pruning strategy which gets rid of unnecessary
        calculation that doesn't improve the results to save time complexity.

        depth: The remaining depth of the search.
        reversi_game_rule: Essentially the current state of the game with
        the necessary functions (Refers to ReversiGameRule class).
        currentPlayer: The agent id of the current player.
        """

        if depth == 0 or gameEnds(game_state):
            return self.evaluation(game_state, [30, 25]), None

        if currentPlayer == self.agent_id:  # It's our turn, we want to maximise
            maxEval = (-math.inf, None)

            for action in actions:
                game_state = generateSuccessor(game_state, action, currentPlayer)
                nextPlayer = getNextAgentIndex(currentPlayer)
                eval = self.minimax(depth - 1, nextPlayer, game_state,
                                    getLegalActions(game_state, nextPlayer), alpha, beta)[0]
                maxEval = max(maxEval, (eval, action), key=lambda x: x[0])
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return maxEval
        else:  # It's opponent turn, minimise to simulate them maximising
            minEval = (math.inf, None)

            for action in actions:
                game_state = generateSuccessor(game_state, action, currentPlayer)
                nextPlayer = getNextAgentIndex(currentPlayer)
                eval = self.minimax(depth - 1, nextPlayer, game_state,
                                    getLegalActions(game_state, nextPlayer), alpha, beta)[0]
                minEval = min(minEval, (eval, action), key=lambda x: x[0])
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return minEval

    def evaluation(self, game_state, weights):
        print("Evaluation: ")
        print("Corners:", self.cornerHeuristic(game_state))
        print("pieces:", self.pieceCountHeuristic(game_state))
        return weights[0] * self.cornerHeuristic(game_state) + weights[1] * self.pieceCountHeuristic(game_state)

    def mobilityHeuristic(self):
        pass

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
        score = countScore(game_state.board, GRID_SIZE, game_state.agent_colors[self.agent_id])
        opScore = countScore(game_state.board, GRID_SIZE, game_state.agent_colors[getNextAgentIndex(self.agent_id)])

        return 100 * (score - opScore) / (score + opScore)  # denominator always != 0 because of the game initialisation


def generateSuccessor(game_state, action, agent_id):
    if action == "Pass":
        return game_state
    else:
        next_state = copy.deepcopy(game_state)
        update_color = game_state.agent_colors[agent_id]
        next_state.board[action[0]][action[1]] = update_color
        # iterate over all 8 directions and check pieces that require updates
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            cur_pos = (action[0] + direction[0], action[1] + direction[1])
            update_list = list()
            flag = False
            # Only searching for updates if the next piece in the direction is from the agent's opponent
            # if next_state.board[cur_pos[0]][cur_pos[1]] == self.agent_colors[(agent_id+1)%2]:
            while cur_pos in validPos() and next_state.board[cur_pos[0]][cur_pos[1]] != Cell.EMPTY:
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
    validPosList = validPos()
    actions = []
    # print(f"Current game state: \n{boardToString(game_state.board,GRID_SIZE)}")
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if game_state.board[x][y] == Cell.EMPTY:
                pos = (x, y)
                appended = False

                for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    if appended:
                        break

                    temp_pos = tuple(map(operator.add, pos, direction))
                    if temp_pos in validPosList and game_state.getCell(temp_pos) != Cell.EMPTY and game_state.getCell(
                            temp_pos) != game_state.agent_colors[agent_id]:
                        while temp_pos in validPosList:
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


def validPos():
    pos_list = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pos_list.append((x, y))
    return pos_list


def getNextAgentIndex(agent_id):
    return (agent_id + 1) % 2
