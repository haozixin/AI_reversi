import operator

from Reversi.reversi_model import ReversiGameRule
from Reversi.reversi_utils import Cell, GRID_SIZE, boardToString
from template import Agent, GameRule
import random


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.rule = ReversiGameRule(2)
        # make sure the current agent id is correct
        self.rule.current_agent_index = self.id
        self.rule.agent_colors = None
        self.weights_table = self.generate_static_weights(2)
        # self.stability_board = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

    def SelectAction(self, actions, game_state):
        # we use BLACK as the first player and WHITE as the second player
        # we use the following heuristic to evaluate the board
        # 1. the number of pieces on the board
        # 2. the number of pieces on the corner
        # 3. the number of pieces on the edge
        if self.rule.agent_colors is None:
            self.rule.agent_colors = game_state.agent_colors

        self.rule.current_game_state = game_state

        # remove redundant actions
        actions = list(set(actions))

        if len(actions) == 1:
            return actions[0]
        else:
            if len(actions)>7:
                depth = 2
            else:
                depth = 3
            h_value, best_action = self.minimax(game_state, depth, -float("inf"), float("inf"), True, actions)
        return best_action

        # return random.choice(actions)

    #  alpha beta pruning
    def minimax(self, gameState, depth, alpha, beta, maximizingPlayer, actions):
        """
        This is a minimax algorithm with alpha beta pruning.
        """
        # if the game is over or the depth is 0, return the score
        if depth == 0 or self.rule.gameEnds():
            # return self.rule.calScore(gameState, self.id), None
            return self.heuristic_function(gameState), None

        # if it is the maximizing player
        if maximizingPlayer:
            max_value = -float("inf")
            best_action = None
            # for each child of position/gameState
            state_with_actions = self.next_layer(gameState, actions, self.rule.getCurrentAgentIndex())
            for a_tuple in state_with_actions:
                child_state = a_tuple[0]
                next_actions = self.rule.getLegalActions(child_state, self.rule.getNextAgentIndex())

                max_mobility = len(actions)
                min_mobility = len(next_actions)
                mobility = (max_mobility - min_mobility)*100/(max_mobility+min_mobility)

                # get the value of the action
                value, _ = self.minimax(child_state, depth - 1, alpha, beta, False, next_actions)
                value += 4*mobility
                if value > max_value:
                    max_value = value
                    best_action = a_tuple[1]
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return max_value, best_action

        # if it is the minimizing player
        else:
            min_value = float("inf")
            worst_action = None
            # for each child of position/gameState
            state_with_actions = self.next_layer(gameState, actions, self.rule.getNextAgentIndex())
            for a_tuple in state_with_actions:
                child_state = a_tuple[0]
                next_actions = self.rule.getLegalActions(child_state, self.rule.getCurrentAgentIndex())

                min_mobility = len(actions)
                max_mobility = len(next_actions)
                mobility = (max_mobility - min_mobility) * 100 / (max_mobility + min_mobility)

                value, _ = self.minimax(child_state, depth - 1, alpha, beta, True, next_actions)
                value += 4*mobility
                if value < min_value:
                    min_value = value
                    worst_action = a_tuple[1]
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return min_value, worst_action

    def next_layer(self, game_state, actions, agent_id):
        """
        Helper function for minmax algorithm.
        Return new states(children of current position) that is generated by performing the actions on the Current game state
        """
        next_states = []
        for action in actions:
            # child of position
            new_state = self.rule.generateSuccessor(game_state, action, agent_id)
            next_states.append((new_state, action))

        # return the child of position
        return next_states

    def heuristic_function(self, game_state):
        """
        Component of the heuristic function. -- coin_parity
        This is a heuristic function that returns the difference between the number of pieces of the current player and the
        number of pieces of the opponent.

        Be suitable for the end game.(more weight when the game is close to the end)
        """
        corners = self.corner_captured(game_state)
        # stability = 0
        # utility_value_heuristic = 0  # it is the static Weights Heuristic (could be used at the beginning of the game)
        # mobility = self.mobility_heuristic(game_state)

        # get the current player's color
        current_player_color = self.rule.agent_colors[self.rule.getCurrentAgentIndex()]
        # get the opponent's color
        opponent_color = self.rule.agent_colors[self.rule.getNextAgentIndex()]
        # get the number of pieces of the current player
        board = game_state.board

        temp_max_player_score = 0
        temp_min_player_score = 0
        temp_max_utility_value = 0
        temp_min_utility_value = 0
        # For saving time,
        # we use the same following loop for every heuristic components that need to go through the whole board
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == current_player_color:
                    temp_max_player_score += 1
                    temp_max_utility_value += self.weights_table[i][j]

                elif board[i][j] == opponent_color:
                    temp_min_player_score += 1
                    temp_min_utility_value += self.weights_table[i][j]

        total_number = temp_max_player_score + temp_min_player_score
        difference = temp_max_player_score - temp_min_player_score
        coins = (difference * 100 / total_number)
        utility_value = (temp_max_utility_value - temp_min_utility_value) * 100 / total_number

        h = 30 * corners + 12 * coins + 12 * utility_value
        if total_number > 57:
            h = 30 * corners + 50 * coins

        return h

    def utility_value(self, game_state):
        """
        Component of the heuristic function.
        """
        # get the current player's color
        current_player_color = self.rule.agent_colors[self.rule.getCurrentAgentIndex()]
        # get the opponent's color
        opponent_color = self.rule.agent_colors[self.rule.getNextAgentIndex()]
        # get the number of pieces of the current player
        board = game_state.board
        max_player_score = 0
        min_player_score = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == current_player_color:
                    max_player_score += self.weights_table[i][j]
                elif board[i][j] == opponent_color:
                    min_player_score -= self.weights_table[i][j]
        return (max_player_score - min_player_score) * 100 / (max_player_score + min_player_score)

    def corner_captured(self, game_state):
        game_state = game_state.board
        # get the current player's color
        current_player_color = self.rule.agent_colors[self.rule.getCurrentAgentIndex()]
        # get the opponent's color
        opponent_color = self.rule.agent_colors[self.rule.getNextAgentIndex()]
        Max_player_corner = 0
        Min_player_corner = 0
        for x in [0, GRID_SIZE - 1]:
            for y in [0, GRID_SIZE - 1]:
                if game_state[x][y] == current_player_color:
                    Max_player_corner += 1
                    if x == 0 and y == 0:
                        self.weights_table[1][1] *= -1
                        self.weights_table[1][0] *= -1
                        self.weights_table[0][1] *= -1
                    elif x == 0 and y == GRID_SIZE - 1:
                        self.weights_table[1][GRID_SIZE - 2] *= -1
                        self.weights_table[1][GRID_SIZE - 1] *= -1
                        self.weights_table[0][GRID_SIZE - 2] *= -1
                    elif x == GRID_SIZE - 1 and y == 0:
                        self.weights_table[GRID_SIZE - 2][1] *= -1
                        self.weights_table[GRID_SIZE - 2][0] *= -1
                        self.weights_table[GRID_SIZE - 1][1] *= -1
                    elif x == GRID_SIZE - 1 and y == GRID_SIZE - 1:
                        self.weights_table[GRID_SIZE - 2][GRID_SIZE - 2] *= -1
                        self.weights_table[GRID_SIZE - 2][GRID_SIZE - 1] *= -1
                        self.weights_table[GRID_SIZE - 1][GRID_SIZE - 2] *= -1
                elif game_state[x][y] == opponent_color:
                    Min_player_corner += 1
        if (Max_player_corner + Min_player_corner) != 0:
            h_value = (Max_player_corner - Min_player_corner) * 100 / (Max_player_corner + Min_player_corner)
        else:
            h_value = 0
        return h_value

    def generate_static_weights(self, times):
        """
        The static weights are used to evaluate the board. Because some place is more important than others, we give them
        We can adjust the times of the weights to make the agent more clear that some places are important.

        Basic value is like the following:
        4  -3  2  2  2  2  -3  4
       -3  -4 -1 -1 -1 -1  -4 -3
        2  -1  1  0  0  1  -1  2
        2  -1  0  1  1  0  -1  2
        2  -1  0  1  1  0  -1  2
        2  -1  1  0  0  1  -1  2
       -3  -4 -1 -1 -1 -1  -4 -3
        4  -3  2  2  2  2  -3  4
        """
        # create a 8*8 matrix
        weights = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

        # the places in the corner are more important than the places in the edge
        # so, we give the corner places a higher weight - 4
        for x in [0, GRID_SIZE - 1]:
            for y in [0, GRID_SIZE - 1]:
                weights[x][y] = 4 * times

        # the places in the edge are less important(except cells beside corner) than the places in the corner
        # so, we give the edge places a lower weight - 2
        for x in range(2, GRID_SIZE - 2):
            weights[x][0] = 2 * times
            weights[x][GRID_SIZE - 1] = 2 * times
        for y in range(2, GRID_SIZE - 2):
            weights[0][y] = 2 * times
            weights[GRID_SIZE - 1][y] = 2 * times

        # the places in the middle are less important than the places in the edge
        # so, we give the middle places a lower weight - 1
        for x in [3, 4]:
            for y in [3, 4]:
                weights[x][y] = 1 * times
        for x in [2, 5]:
            for y in [2, 5]:
                weights[x][y] = 1 * times

        # places value = 0
        for x in [3, 4]:
            for y in [2, 5]:
                weights[x][y] = 0
        for x in [2, 5]:
            for y in [3, 4]:
                weights[x][y] = 0

        # places value = -1
        for x in range(2, GRID_SIZE - 2):
            weights[x][1] = -1 * times
            weights[x][GRID_SIZE - 2] = -1 * times
        for y in range(2, GRID_SIZE - 2):
            weights[1][y] = -1 * times
            weights[GRID_SIZE - 2][y] = -1 * times

        # places value = -3
        weights[1][0] = -3 * times
        weights[0][1] = -3 * times
        weights[GRID_SIZE - 2][0] = -3 * times
        weights[GRID_SIZE - 1][1] = -3 * times
        weights[1][GRID_SIZE - 1] = -3 * times
        weights[0][GRID_SIZE - 2] = -3 * times
        weights[GRID_SIZE - 2][GRID_SIZE - 1] = -3 * times
        weights[GRID_SIZE - 1][GRID_SIZE - 2] = -3 * times

        # places value = -4
        weights[1][1] = -4 * times
        weights[GRID_SIZE - 2][1] = -4 * times
        weights[1][GRID_SIZE - 2] = -4 * times
        weights[GRID_SIZE - 2][GRID_SIZE - 2] = -4 * times

        return weights

    # def mobility_heuristic(self, game_state):
    #     """
    #     Component of heuristic function
    #     Only use actual mobility - Actual mobility is the number of next moves a player has, given the current state of the game.
    #     """
    #     max_player_mobility = len(self.rule.getLegalActions(game_state, self.rule.getCurrentAgentIndex()))
    #     min_player_mobility = len(self.rule.getLegalActions(game_state, self.rule.getNextAgentIndex()))
    #     if (max_player_mobility + min_player_mobility) != 0:
    #         h_value = (max_player_mobility - min_player_mobility) * 100 / (max_player_mobility + min_player_mobility)
    #     else:
    #         h_value = 0
    #     return h_value


    # def stability_heuristic(self, game_state):
    #     """
    #     Weights are associated to each of the three categories( (i) stable, (ii) semi-stable and (iii) unstable.),
    #     and we sum the weights up to give
    #     rise to a final stability value for the player. Typical weights could be 1 for stable coins, -1 for
    #     unstable coins and 0 for semi-stable coins.
    #
    #     In the heuristic_function(), we could get the total score of the game_state (because go through board need
    #     a lot of time when we do it too many times separately)
    #     """
    #     max_stability = 0
    #     min_stability = 0
    #     # get the current player's color
    #     current_player_color = self.rule.agent_colors[self.rule.getCurrentAgentIndex()]
    #     # get the opponent's color
    #     opponent_color = self.rule.agent_colors[self.rule.getNextAgentIndex()]
    #     stability_board = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    #
    #     for x in range(GRID_SIZE):
    #         for y in range(GRID_SIZE):
    #             cell = (x, y)
    #             if game_state.board[x][y] == current_player_color:
    #                 # stable cases:
    #                 # 1. if the coin is in the corner, it's stable
    #                 if cell in [(0, 0), (0, GRID_SIZE - 1), (GRID_SIZE - 1, 0), (GRID_SIZE - 1, GRID_SIZE - 1)]:
    #                     max_stability += 1
    #                     stability_board[cell[0]][cell[1]] = 1
    #                 # 2. if the coin is in the edge, and the coin beside it is stable, it's stable
    #                 elif cell[0] == 0 and ((game_state.getCell(0, cell[1] + 1) == current_player_color and
    #                                         stability_board[0][cell[1] + 1] == 1)
    #                                        or (game_state.getCell(0, cell[1] - 1) == current_player_color and
    #                                            stability_board[0][
    #                                                cell[1] - 1] == 1)):
    #                     max_stability += 1
    #                     stability_board[cell[0]][cell[1]] = 1
    #                 elif cell[0] == GRID_SIZE - 1 and ((game_state.getCell(GRID_SIZE - 1,
    #                                                                        cell[1] + 1) == current_player_color and
    #                                                     stability_board[GRID_SIZE - 1][cell[1] + 1] == 1)
    #                                                    or (game_state.getCell(GRID_SIZE - 1,
    #                                                                           cell[1] - 1) == current_player_color and
    #                                                        stability_board[GRID_SIZE - 1][cell[1] - 1] == 1)):
    #                     max_stability += 1
    #                     stability_board[cell[0]][cell[1]] = 1
    #                 elif cell[1] == 0 and ((game_state.getCell(cell[0] + 1, 0) == current_player_color and
    #                                         stability_board[cell[0] + 1][0] == 1)
    #                                        or (game_state.getCell(cell[0] - 1, 0) == current_player_color and
    #                                            stability_board[cell[0] - 1][0] == 1)):
    #                     max_stability += 1
    #                     stability_board[cell[0]][cell[1]] = 1
    #                 elif cell[1] == GRID_SIZE - 1 and ((game_state.getCell(cell[0] + 1,
    #                                                                        GRID_SIZE - 1) == current_player_color and
    #                                                     stability_board[cell[0] + 1][GRID_SIZE - 1] == 1)
    #                                                    or (game_state.getCell(cell[0] - 1,
    #                                                                           GRID_SIZE - 1) == current_player_color and
    #                                                        stability_board[cell[0] - 1][GRID_SIZE - 1] == 1)):
    #                     max_stability += 1
    #                     stability_board[cell[0]][cell[1]] = 1
    #
    #                 #
    #                 # for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
    #
    #
    #             else:
    #
    #
    #     return None
