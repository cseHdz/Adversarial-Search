
from sample_players import DataPlayer
import random

HASH_SIZE = 8192

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

        """ Retrieve transposition table """
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            tt = self.context if self.context else {}
            depth_limit = 5
            guess = -1
            for depth in range(1, depth_limit + 1):
                best_move = self._mtdf(state, guess, depth, tt)
            self.context = tt if tt else None
            self.queue.put(best_move)

    def _mtdf(self, state, guess, depth = 4, tt = None):

        self.tt = tt

        def store_node(state, alpha, beta, depth):
            zobrist_key = int(state.board % HASH_SIZE)
            node = {'alpha':alpha,
                    'beta':beta,
                    'depth':depth}
            self.tt[zobrist_key] = node

        def retrieve_node(state):
            zobrist_key = int(state.board % HASH_SIZE)
            return None if not(zobrist_key in self.tt.keys()) else self.tt[zobrist_key]

        def check_TT(state, alpha, beta, depth):
            node = retrieve_node(state)
            if not(node is None):
                if node['depth'] >= depth:
                    return (node['alpha'], node['beta'])
            return (None, None)

        def min_value(state, alpha, beta, depth):
            if not(self.tt is None):
                a, b = check_TT(state, alpha, beta, depth)
                if a and b:
                    if a >= beta: return a
                    if b <= alpha: return b
                    beta = max(beta, b)
                    alpha = max(alpha, a)
            if state.terminal_test() or depth <= 0:
                value = state.utility(self.player_id) if state.terminal_test() else  self.utility(state)
                alpha = beta = value
            else:
                value = float("inf")
                for action in state.actions():
                    value = min(value, max_value(state.result(action), alpha, beta, depth - 1))
                    if value <= alpha: return value
                    beta = min(beta, value)
            if not(self.tt is None): store_node(state, alpha, beta, depth)
            return value

        def max_value(state, alpha, beta, depth):
            if not(self.tt is None):
                value = check_TT(state, alpha, beta, depth)
                if not(value is None): return value
            if state.terminal_test() or depth <= 0:
                value = state.utility(self.player_id) if state.terminal_test() else  self.utility(state)
                alpha = beta = value
            else:
                value = float("-inf")
                for action in state.actions():
                    value = max(value, min_value(state.result(action), alpha, beta, depth - 1))
                    if value >= beta: return value
                    alpha = max(alpha, value)
            if not(self.tt is None): store_node(state, alpha, beta, depth)
            return value

        def alpha_beta(state, alpha, beta, depth):
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth))
            return value

        def alpha_beta_TT(state, alpha, beta, depth):

        def mtdf(state, guess, depth):
            value = guess
            alpha, beta = -1000, 1000
            while alpha < beta:
                if value == alpha: gamma = value + 1
                else: gamma = value
                value = alpha_beta(state, gamma - 1, gamma, depth)
                if value < gamma: beta = value
                else: alpha = value
            return value

        return max(state.actions(), key=lambda x: mtdf(state.result(x), guess, depth - 1))

    def utility(self, state):

        player_loc = state.locs[self.player_id]
        player_liberties = state.liberties(player_loc)
        opponent_loc = state.locs[1- self.player_id]
        opponent_liberties = state.liberties(opponent_loc)
        return len(player_liberties) - len(opponent_liberties)
