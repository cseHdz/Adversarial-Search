
from sample_players import DataPlayer
from isolation.isolation import _WIDTH as board_width, _HEIGHT as board_height, _SIZE as board_size

LOWERBOUND, EXACT, UPPERBOUND = -1,0,1
HASH_SIZE = 2048

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
        self.tt = self.context if self.context else {}

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
        self.tt = self.context
        best_move = iterative_deepening(state, 4, self.tt)["best_move"]

        # Save the Transposition Table into the Context and put the next move
        self.context = self.tt if self.tt else None
        self.queue.put(best_move)
    
    def retrieve_node(state, tt):
        state_ID = state.bitboard_string
        zobrist_key = state_ID % HASH_SIZE

        return tt[zobrist_key] if tt[zobrist_key] else None


    def store_node(state, score, type, depth, tt):
        state_ID = state.bitboard_string
        zobrist_key = state_ID % HASH_SIZE

        node = {"state":state,
                "score":score,
                "type":type,
                "depth":depth
               }

        if not(tt): tt = {}
        tt[zobrist_key] = {zobrist_key:node}


    def iterative_deepening(self, state, depth_limit = 4, tt = None):
        ai_move = {"best_move": state, "best_score": -10}

        """ Iterative Deepening loop """
        for depth in range(1, depth_limit + 1):
            ai_move = mtdf(state, ai_move, depth, tt, player_ID)

      	# Minimax with Alpha-Beta Pruning and Iterative Deepening
        # best_move = alpha_beta_search(playerID, state, depth)

        """ Save transposition table """
        return best_move


    def mtdf(state, guess, depth, tt, player_ID):
        alpha, beta = -10, 10
        ai_move = guess

        while alpha < beta:
            if ai_move["best_score"] == alpha:
                gamma = ai_move["best_score"] + 1
            else:
                gamma = ai_move["best_score"]

            ai_move = negamax_alpha_beta_TT(state, gamma - 1, gamma, depth, tt, player_ID)

            if ai_move["best_score"] < gamma:
                beta = gamma
            else:
                alpha = gamma
        return ai_move


    def negamax_alpha_beta_TT(state, alpha, beta, depth, tt, player_ID):
        """ Return the legal move (column, row) for the current player
         along a branch of the game tree that has the best possible value.

        Negamax was implemented to simplify alpha-beta pruning as isolation
        is a zero-sum game. It was enhanced through a transposition table.

        Implementation based on: https://homepages.cwi.nl/~paulk/theses/Carolus.pdf

        Alpha - Maximum lower bound
        Beta - Minimum upper bound

        Depth - Number of iterations to perform

        """

        known_node = None if (tt is None) else retrieve_node(state, tt)

        # Check if node exists
        if known_node:
            if known_node['depth'] >= depth:
                # The current state has been visited at least at the current depth
                type, value = known_node['type'], known_node ["score"]
            if known_node['type'] == EXACT:
                return {"best_move": known_node['state'], "best_score": known_node["score"]}

            if known_node['type'] == LOWERBOUND and known_node['score'] > alpha:
                alpha = known_node['score']

            elif known_node["type"] == UPPERBOUND and known_node["score"] < beta:
                beta = known_node["score"]

            if alpha >= beta:
                return {"best_move": known_node["state"], "best_score": known_node["score"]}

        #	node = {"best_move":None, "score": float("-inf")}

        if state.terminal_test() or depth <= 0:
            val = utility(state, player_ID) if depth<=0 else state.utility(player_ID)

            if best_score <= alpha: type = LOWERBOUND
            elif best_score >= beta: type = UPPERBOUND
            else: type = EXACT

            store_node(state, val, type, depth, tt)

            return {"best_move": state, "best_score": val}

        best_score = float("-inf") - 1

        for action in state.actions():
            val = -negamax_alpha_beta_TT(state.result(action), -alpha, -beta, depth - 1, tt, playerID)

            alpha = max(alpha, val)

            if val > best_score:
                best_score = val
                best_move = action
            if best_score > alpha:
                alpha = best_score
            if best_score >= beta:
                break

        if best_score <= alpha: type = LOWERBOUND
        elif best_score >= beta: type = UPPERBOUND
        else: type = EXACT

        store_node(state, val, type, depth, tt)
       	return {"best_move": state, "best_score": best_score}

    def alpha_beta(state, depth = 2, player_ID):
        """ Return the legal move (column, row) for the current player
        along a branch of the game tree that has the best possible value.

        Alpha - Maximum lower bound
        Beta - Minimum upper bound

        Depth - Number of iterations to perform

        """
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None

        for action in state.actions():
            val = min_value(state.result(action), alpha, beta, depth - 1, player_ID)
            alpha = max(alpha, val)
            if val > best_score:
                  best_score = val
                  best_move = action
        return best_move

    def min_value(state, alpha, beta, depth, player_ID):
        """
        Iterate until the max depth is reached. Then calculate the utility.

        Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if state.terminal_test():
            return state.utility(playerID)

        if depth <= 0:
            return utility(state, playerID)

        val = float("inf")
        for action in state.actions():
            val = min(val, max_value(playerID, state.result(action), alpha, beta, depth - 1))
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val


    def max_value(state, alpha, beta, depth, player_ID):
        """
        Iterate until the max depth is reached. Then calculate the utility.

        Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """

        if state.terminal_test():
            return state.utility(playerID)

        if depth <= 0:
            return utility(state, playerID)


        val = float("-inf")
        for action in state.actions():
            val = max(val, min_value(playerID, state.result(action), alpha, beta, depth - 1))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val


    def utility(state, playerID):

        opponentID = int(not(playerID))

        player_loc = state.locs[playerID]
        player_liberties = state.liberties(player_loc)

        opponent_loc = state.locs[opponentID]
        opponent_liberties = state.liberties(opponent_loc)

        return len(player_liberties) - len(opponent_liberties)
