
# Build an Adversarial Game Playing Agent

![Example game of isolation on a square board](viz.gif)

## Project Overview

This project contains the solution for Udacity's Adversarial Search under the [Artificial Intelligence Nanodegree](https://www.udacity.com/course/ai-artificial-intelligence-nanodegree--nd898).


The objective is to build an adversarial game playing agent to play knights Isolation.


This implementation covers across multiple versions of game playing agent: 
    1. Minimax with Alpha-Beta prunning
    2. Iterative Deepening
    3. Alpha-Beta with Transpoition Tables
    4. Negamax Alpha Beta
    5. AB-SSS
    6. MTD-(f)

The detailed instructions from the Assignment are below.

*****

### Isolation

In the game Isolation, two players each control their own single token and alternate taking turns moving the token from one cell to another on a rectangular grid.  Whenever a token occupies a cell, that cell becomes blocked for the remainder of the game.  An open cell available for a token to move into is called a "liberty".  The first player with no remaining liberties for their token loses the game, and their opponent is declared the winner.

In knights Isolation, tokens can move to any open cell that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board.  On a blank board, this means that tokens have at most eight liberties surrounding their current location.  Token movement is blocked at the edges of the board (the board does not wrap around the edges), however, tokens can "jump" blocked or occupied spaces (just like a knight in chess).

Finally, agents have a fixed time limit (150 milliseconds by default) to search for the best move and respond.  The search will be automatically cut off after the time limit expires, and the active agent will forfeit the game if it has not chosen a move.

**You can find more information (including implementation details) about the in the Isolation library readme [here](/isolation/README.md).**


## Instructions

You must implement an agent in the `CustomPlayer` class defined in the `game_agent.py` file. The interface definition for game agents only requires you to implement the `.get_action()` method, but you can add any other methods to the class that you deem necessary.  You can build a basic agent by combining minimax search with alpha-beta pruning and iterative deepening from lecture.

**NOTE:** Your agent will **not** be evaluated in an environment suitable for running machine learning or deep learning agents (like AlphaGo); visit an office hours sessions **after** completing the project if you would like guidance on incorporating machine learning in your agent.

#### The get_action() Method
This function is called once per turn for each player. The calling function handles the time limit and 
```
def get_action(self, state):
    import random
    self.queue.put(random.choice(state.actions()))
```

- **DO NOT** use multithreading/multiprocessing (the isolation library already uses them, which may cause conflicts)
- **ALL** of the functions you add should be created as methods on the CustomPlayer class. Avoid nested classes & functions, especially for long-running procedures, as these may cause your agent to block the automatic timeout when your turn ends.

#### Initialization Data
Your agent will automatically read the contents of a file named `data.pickle` if it exists in the same folder as `my_custom_player.py`. The serialized object from the pickle file will be assigned to `self.data`. Your agent should not write to or modify the contents of the pickle file during search.

The log file will record a warning message if there is no data file, however a data file is NOT required unless you need it for your opening book. (You are allowed to use the data file to provide _any_ initialization information to your agent; it is not limited to an opening book.)


#### Saving Information Between Turns
The `CustomPlayer` class can pass internal state by assigning the data to the attribute `self.context`. An instance of your agent class will carry the context between each turn of a single game, but the contents will be reset at the start of any new game.
```
def get_action(...):
    action = self.mcts()
    self.queue.put(action)
    self.context = object_you_want_to_save  # self.context will contain this object on the next turn
```

## Experiment: Build an agent using advanced search techniques

- Create a performance baseline using `run_search.py` to evaluate the effectiveness of a baseline agent (e.g., an agent using your minimax or alpha-beta search code from the classroom)
- Use `run_search.py` to evaluate the effectiveness of your agent using your own custom search techniques
- You must decide whether to test with or without "fair" matches enabled--justify your choice in your report

## Report Requirements

The report must include a table or chart with data from an experiment to evaluate the performance of your agent as described above.  Use the data from your experiment to answer the relevant questions below. (You may choose one set of questions if your agent incorporates multiple techniques.)

**Advanced Search Techniques**
- Choose a baseline search algorithm for comparison (for example, alpha-beta search with iterative deepening, etc.). How much performance difference does your agent show compared to the baseline?
- Why do you think the technique you chose was more (or less) effective than the baseline?

## Evaluation

The rubric for the project can be found [here](https://review.udacity.com/#!/rubrics/1801/view).
