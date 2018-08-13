
from sample_players import DataPlayer

LOWERBOUND, EXACT, UPPERBOUND = -1,0,1
HASH_SIZE = 1000000

class AIMove():
    def __init__(self, move, score):
        self.move = move
        self.score = score

class TT_HASH():
    def __init__(self, start_list = None):
        self.list = start_list if start_list else {}

    def store_node(self, state, score, alpha, beta, depth):
        state_ID = state.board
        zobrist_key = int(state_ID % HASH_SIZE)

        node = {"state":state,
                "score":score,
                "alpha":alpha,
                "beta":beta,
                "depth":depth
                }

        self.list[zobrist_key] = node


    def retrieve_node(self, state):
        state_ID = state.board
        zobrist_key = int(state_ID % HASH_SIZE)

        if zobrist_key <= len (self.list) and zobrist_key in self.list.keys():
            return self.list[zobrist_key]
        else:
            return None

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
            tt = self.context if self.context else TT_HASH()
            best_move = self.iterative_deepening(state, 3, tt)
            self.context = tt if tt else None
            self.queue.put(best_move.move)


    def iterative_deepening(self, state, depth_limit = 4, tt = None):

        ai_move = AIMove(state, self.utility(state))

        """ Iterative Deepening loop """
        for depth in range(1, depth_limit + 1):
            ai_move = self.mtdf(state, depth, ai_move, tt)
            #ai_move = self.alpha_beta(state, depth)

        """ Save transposition table """
        return ai_move

    #def mtdf(self, state, depth, guess, tt = None):
    def mtdf(self, state, depth, ai_move, tt):
        alpha, beta = float("-inf"), float("inf")

        while alpha < beta:
            if ai_move.score == alpha:
                gamma = ai_move.score + 1
            else:
                gamma = ai_move.score

            ai_move = self.negamax_alpha_beta_TT(state, gamma - 1, gamma, depth, tt)
            if ai_move.score < gamma:
                beta = ai_move.score
            else:
                alpha = ai_move.score
        return ai_move


    def negamax_alpha_beta_TT(self, state, alpha, beta, depth, tt):
        """ Return the legal move (column, row) for the current player
         along a branch of the game tree that has the best possible value.

        Negamax was implemented to simplify alpha-beta pruning as isolation
        is a zero-sum game. It was enhanced through a transposition table.

        Implementation based on: https://arxiv.org/pdf/1505.01603.pdf
        https://homepages.cwi.nl/~paulk/theses/Carolus.pdf

        Alpha - Maximum lower bound
        Beta - Minimum upper bound

        Depth - Number of iterations to perform

        """

        known_node = None if (tt is None) else tt.retrieve_node(state)

        # Check if node exists
        if known_node:
            if known_node['depth'] >= depth:
                # The current state has been visited at least at the current depth

                if known_node['beta'] <= alpha or known_node['beta'] == known_node['alpha']:
                    return AIMove(known_node["state"],known_node['beta'])

                if known_node['alpha'] >= beta:
                    return AIMove(known_node["state"],known_node['alpha'])

        # Maximum depth or terminal test
        if state.terminal_test() or depth <= 0:

            val = state.utility(self.player_id) if state.terminal_test() else  self.utility(state)

            # Save alpha and beta as the same
            tt.store_node(state, val, val, val, depth)

            return AIMove(state,val)

        val = float("-inf")
        a = alpha

        for action in state.actions():
            val = max(val, -self.negamax_alpha_beta_TT(state.result(action),
                                                              -beta,
                                                              -a,
                                                              depth - 1,
                                                              tt).score)
            a = max(a, val)
            best_move = action

            if val < beta:
                break

        if val <= alpha:
            tt.store_node(state, val, alpha, val, depth)
        elif val >= beta:
            tt.store_node(state, val, val, beta, depth)
        else: tt.store_node(state, val, val, val, depth)

        tt.store_node(state, val, val, beta, depth)

        return AIMove(best_move, val)


    def negamax_alpha_beta_TT_2(self, state, alpha, beta, depth, tt):
        """ Return the legal move (column, row) for the current player
         along a branch of the game tree that has the best possible value.

        Negamax was implemented to simplify alpha-beta pruning as isolation
        is a zero-sum game. It was enhanced through a transposition table.

        Implementation based on: https://homepages.cwi.nl/~paulk/theses/Carolus.pdf

        Alpha - Maximum lower bound
        Beta - Minimum upper bound

        Depth - Number of iterations to perform

        """

        known_node = None if (tt is None) else tt.retrieve_node(state)

        # Check if node exists
        if known_node:
            if known_node['depth'] >= depth:
                # The current state has been visited at least at the current depth
                if known_node['val_type'] == EXACT:
                    return AIMove(known_node['state'], known_node["score"])

                if known_node['val_type'] == LOWERBOUND and known_node['score'] > alpha:
                    alpha = known_node['score']

                elif known_node["val_type"] == UPPERBOUND and known_node["score"] < beta:
                    beta = known_node["score"]

                if alpha >= beta:
                    return AIMove(known_node["state"],known_node["score"])

        if state.terminal_test() or depth <= 0:

            val = self.utility(state) if depth<=0 else state.utility(self.player_id)

            if val <= alpha: val_type = LOWERBOUND
            elif val >= beta: val_type = UPPERBOUND
            else: val_type = EXACT

            tt.store_node(state, val, val_type, depth)

            return AIMove(state,val)

        best_score = float("-inf")

        for action in state.actions():
            val = max(best_score, -self.negamax_alpha_beta_TT_2(state.result(action),
                                                  -beta,
                                                  -alpha,
                                                  depth - 1,
                                                  tt).score)

            alpha = max(alpha, val)

            if val > best_score:
                best_score = val
                best_move = action
            if best_score > alpha:
                alpha = best_score

        if best_score <= alpha:
            val_type = LOWERBOUND
        elif best_score >= beta:
            val_type = UPPERBOUND
        else: val_type = EXACT

        tt.store_node(state, val, val_type, depth)

        print(val_type, best_score)
        return AIMove(best_move,best_score)



    def alpha_beta(self, state, depth = 2):
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
            val = self.min_value(state.result(action), alpha, beta, depth - 1)
            alpha = max(alpha, val)
            if val > best_score:
                  best_score = val
                  best_move = action
        return AIMove(best_move, best_score)

    def min_value(self, state, alpha, beta, depth):
        """
        Iterate until the max depth is reached. Then calculate the utility.

        Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """

        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.utility(state)

        val = float("inf")
        for action in state.actions():
            val = min(val, self.max_value(state.result(action), alpha, beta, depth - 1))
                #= -max(-val, -self.max_value(state.result(action), alpha, beta, depth - 1))
            if val <= alpha:
                return val
            beta = min(beta, val)
        return val


    def max_value(self, state, alpha, beta, depth):
        """
        Iterate until the max depth is reached. Then calculate the utility.

        Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """

        if state.terminal_test():
            return state.utility(self.player_id)

        if depth <= 0:
            return self.utility(state)


        val = float("-inf")
        for action in state.actions():
            val = max(val, self.min_value(state.result(action), alpha, beta, depth - 1))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        return val



    def utility(self, state):

        player_loc = state.locs[self.player_id]
        player_liberties = state.liberties(player_loc)
        opponent_loc = state.locs[1- self.player_id]
        opponent_liberties = state.liberties(opponent_loc)
        return len(player_liberties) - len(opponent_liberties)
