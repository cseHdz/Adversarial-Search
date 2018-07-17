
from sample_players import DataPlayer
from isolation.isolation import _WIDTH as board_width, _HEIGHT as board_height, _SIZE as board_size


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


def mtdf_search(state, first_guess, depth):
    
    bound = 8 # Maximum Heusistic at any point
    best_move = first_guess
    
    upperbound = bound
    lowerbound = -bound
    
    while lowerbound < upperbound:
        
        if best_move["beta"] = lowerbound: 
            window = best_move["beta"] + 1
        
        best_move = negamax_alpha_beta_TT(state, window - 1, window, depth)
        
        if best_move < beta  :
            
            
            if g[1]!=None:
        best = g
      if g[0] < beta:
        upperBound = g[0]
      else:
        lowerBound = g[0]
    return best
    
    return best_move
    
def retrieve(state, depth)

    
def alpha_beta_TT(state, alpha, beta, depth, tt)
 
	known_node = None if (tt is None) else tt.retrieve(state)
    alpha, beta = float("-inf"), float("inf")
    best_move = None
    
    if known_node and known_node['depth'] >= depth:
      # The current state has been visited at least at the current depth
      
      if known_node['alpha'] >= beta: 
        return known_node['alpha]
      elif known_node.beta <= alpha:
      	return known_node['beta']
                          sim
      alpha = max(alpha, known_node.alpha)
      beta = max(beta, known_node.beta)
            
  	if state.terminal_test():
        return state.utility(playerID)
    
    if depth <= 0: 
      	return utility(state, playerID)
    
   	val = float("-inf")
    for action in state.actions():
        val = -alpha_beta_TT(state.result(action), -alpha, -beta, depth - 1)

        alpha = max(alpha, val)     
        
        if val > best_score:
        	best_score = val
        	best_move = action
        
        if val <= alpha then 

    
    	
    
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


