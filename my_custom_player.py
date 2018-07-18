
from sample_players import DataPlayer
from isolation.isolation import _WIDTH as board_width, _HEIGHT as board_height, _SIZE as board_size

LOWERBOUND, EXACT, UPPERBOUND = -1,0,1

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
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        # import random



        """ Retrieve transposition table """
        # if self.context:
        #    tt = self.context



        self.queue.put(best_move)

        """ Save transposition table """
        #self.context = tt



""" Adversarial search Algorithm:


    Ensure there is always an answer within the time period

"""

def iterative_deepening(self, state):

     depth_limit = 2
     best_move = {
                 "alpha" : 1
                 "beta"  : -1
                 "depth" : 0
                 "state" : None
                 }

     """ Iterative Deepening loop """

    for depth in range(1, depth_limit + 1):
        best_move = mtdf_search(state, best_move, depth)

        # Minimax with Alpha-Beta Pruning and Iterative Deepening
        # best_move = alpha_beta_search(playerID, state, depth)

    return best_move



def retrieve_node(state, depth):


def store_node():


def alpha_beta_TT(state, alpha, beta, depth, tt):

    """ Return the legal move (column, row) for the current player
    along a branch of the game tree that has the best possible value.

    Alpha - Maximum lower bound
    Beta - Minimum upper bound

    Depth - Number of iterations to perform

    """

	known_node = None if (tt is None) else retrieve_node(state)

    # Check if node exists
    if known_node:
        if known_node['depth'] >= depth:
            # The current state has been visited at least at the current depth
            type, value = known_node['type'], known_node ['value']
            if known_node['type'] = EXACT:
                return {"best_move": known_node['state'], "best_score": known_node["score"]}

            if known_node['type'] = LOWERBOUND and known_node['value'] > alpha:
                alpha = known_node['value']

            elif known_node['type'] = UPPERBOUND and known_node['value'] < beta:
                beta = known_node['value']

            if alpha >= beta:
                return {"best_move": known_node['state'], "best_score": known_node["score"]}

    node = {"best_move":None, "score": float("-inf")}

  	if state.terminal_test() or if depth <= 0:
        val = utility(state, playerID) if depth<=0 else state.utility(playerID)

        if best_score <= alpha:
            store_node(state, val, LOWERBOUND, depth)
        elif best_score >= beta:
            store_node(state val, UPPERBOUND, depth)
        else:
            store_node(state, val, EXACT, depth)
        return {"best_move": state, "best_score": val}

    best_score = float("-inf") - 1

    for action in state.actions():
        val = -alpha_beta_TT(state.result(action), -alpha, -beta, depth - 1, tt)

        alpha = max(alpha, val)

        if val > best_score:
        	best_score = val
        	best_move = action
        if best_score > alpha:
            alpha = best_score
        if best_score >= beta:
            break

    if best_score <= alpha:
        store_node(state, best_score, LOWERBOUND, depth)
    elif best_score >= beta:
        store_node(state best_score, UPPERBOUND, depth)
    else:
        store_node(state, best_score, EXACT, depth)
    return {"best_move": state, "best_score": best_score}



def alpha_beta_search(playerID, state, depth = 2):
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
        val = min_value(playerID, state.result(action), alpha, beta, depth - 1)

        alpha = max(alpha, val)
        if val > best_score:
            best_score = val
            best_move = action

    return best_move


def min_value(playerID, state, alpha, beta, depth):
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


def max_value(playerID, state, alpha, beta, depth):
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
