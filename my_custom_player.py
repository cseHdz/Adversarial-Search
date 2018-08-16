
from sample_players import DataPlayer
import random

HASH_SIZE = 10000000

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        baseline_flag = 1
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:

            if not baseline_flag: tt = self.context if self.context else {}
            depth_limit = 5
            guess = 2
            for depth in range(1, depth_limit + 1):
                best_move = self._mtdf(state, guess, depth, tt) if not baseline_flag else self._alpha_beta(state, depth)
                self.queue.put(best_move)
            self.context = tt if tt else None

    def _alpha_beta(self, state, depth):

        def min_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.utility(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                if value <= alpha: return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):

            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.utility(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                if value >= beta: return value
                alpha = max(alpha, value)
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), float("-inf"), float("inf"), depth - 1))

    def _mtdf(self, state, guess, depth = 3, tt = None):

        self.tt = tt

        def store_node(state, lower, upper, depth):
            zobrist_key = int(state.board % HASH_SIZE)
            node = {'lower':lower,
                    'upper':upper,
                    'depth':depth,}
            self.tt[zobrist_key] = node

        def retrieve_node(state):
            zobrist_key = int(state.board % HASH_SIZE)
            return None if not(zobrist_key in self.tt.keys()) else self.tt[zobrist_key]

        def _mt(state, gamma, depth):
            if not(self.tt is None):
                node = retrieve_node(state)
                if node != None:
                    lower, upper = node['lower'], node['upper']
                    if lower == upper: return upper
                    if lower > gamma: return lower
                    if upper < gamma: return upper

            value = float("-inf")

            if state.terminal_test() or depth <= 0:
                value = state.utility(self.player_id) if state.terminal_test() else  self.utility(state)
                lower = upper = value
            else:
                for action in state.actions():
                    if value >= gamma: break
                    value = -mt(state.result(action), -gamma, depth - 1)
                if value < gamma: upper = value
                else: lower = value

            if not(self.tt is None):
                store_node(state, lower, upper, depth)
            return value

        def AB_SSS(state, depth):
            value = float("inf")
            gamma = 0
            while value < gamma:
                gamma = value
                value = _mt(state, gamma - 1, depth)
            return value

        def mtdf(state, first, depth):
            value = first
            lower, upper = float("-inf"), float("inf")
            while lower < upper:
                if value == lower: gamma = value + 1
                else: gamma = value
                value = _mt(state, gamma - 1, depth)
                if value < gamma: upper = value
                else: lower = value
            return value

        return max(state.actions(), key=lambda x: mtdf(state.result(x), guess, depth - 1))

    def utility(self, state):

        player_loc = state.locs[self.player_id]
        player_liberties = state.liberties(player_loc)
        opponent_loc = state.locs[1- self.player_id]
        opponent_liberties = state.liberties(opponent_loc)
        return len(player_liberties) - len(opponent_liberties)
