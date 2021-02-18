### Terminology:
- **Agent** - an entity that perceives its environment and acts upon that environment (ex. a car that is trying to get to a destination or the player who is trying to solve a puzzle).
- **State** - a configuration of the agent and its environment (ex. in chess it is the chessboard and how all the pieces are arranged). Each of the states can require different solutions to get to the goal.
    * **Initial State** - the state in which the agent begins. Starting point. This is where we try to figure out what actions to apply to get from the initial state to the goal.
- **Actions** - choices that can be made in any given state. Usually defined by function `actions(s)` which returns the set of actions that can be executed in state `s`. (ex. in Tic Tac Toe it's all possible moves you can make as player X in that turn).
- **Transition Model** - a description of what state results from performing any applicable action in any state. Usually defined by function `result(s, a)` which returns the state resulting from performing action `a` in state `s`.
- **State Space** - by using the transition model we can acquire the set of all states reachable from the initial state by any sequence of actions.
- **Goal Test** - way to determine whether a given state is a goal state (ex. in driving directions if the agent is in the destination you typed in the goal is achieved).
- **Path Cost** - the numerical cost associated with a given path (ex. in driving directions - time, distance, etc.). Interpretation - some number how expensive it is to take this path. The goal is to find the path that minimizes the path cost.
- **Solution** - a sequence of actions that leads from the initial state to a goal state.
    * **Optimal Solution** - a solution that has the lowest path cost among all solutions.
- **Node** - a data structure that keeps track of:
    * a state
    * a parent (node that generated this node). Will allow us to get the solution (sequence of actions that got us here).
    * an action (action applied to the parent to get to this node)
    * a path cost (from the initial state to node)
- **Frontier** - represents all of the states that we can explore next.

### The general approach:
1. Start with a frontier that contains the initial state.
2. Start with an empty explored set.
3. Repeat/Loop:
    * If the frontier is empty, then there is no solution.
    * Remove a node from the frontier.
    * If the node contains a goal state (by using goal test), return the solution.
    * Add the node to the explored set.
    * Expand node (consider all possible actions and what nodes can you get to from this one), add resulting nodes to the frontier if they aren't already in the frontier or the explored set.

## Search Algorithms

- **Uninformed Search algorithms** - Search strategy that uses no problem-specific knowledge.
    * **Depth-First Search (DFS)** - Explores the deepest node in the frontier. In this case, the frontier is of Stack type (LIFO: last-in-first-out). Always finds a solution, but it might not be the optimal solution (if you are unlucky), but at a lesser cost.
    * **Breadth-First Search (BFS)** - Explores the shallowest node in the frontier. In this case, the frontier is of a Queue type (FIFO: first-in-first-out). Always finds the **optimal solution** but at a greater cost.
- **Informed Search algorithms** - Search strategy that uses problem-specific knowledge to find solutions more efficiently.
    * **Greedy Best-First Search** - Explores the node that is closest to the goal, as estimated by a heuristic function *h(n)*. Always finds a solution, but it might not be the optimal solution (if you are unlucky), but at a much lesser cost.
    * __A* Search__ - Explores the node with lowest value of *g(n) (cost to reach the node)* + *h(n) (estimated cost to goal)*. Always finds the **optimal solution IF the below conditions are met**, at a much lesser cost (though it depends).
        * Optimal if *h(n)* is admissible - never overestimates the true cost.
        * Optimal if *h(n)* is consistent - for every node *n* and successor *n'* with step cost *c, h(n) <= h(n') + c*.

In the lecture, the example heuristic function *h(n)* was calculated using **Manhattan distance** which is the distance between two points measured along axes at right angles.

## Adversarial Search Algorithms

- **Minimax** - Tries to find the best move, by working backward from the end of the game.
    * *Max(x)* aims to maximize score *(because win value is 1)*
    * *Min(o)* aims to minimize score *(because win value is -1)*
    * **Alpha-Beta Pruning** - Minimax algorithm that tries to decrease the number of nodes that are evaluated by not exploring the nodes that do not give the optimal solution in the respective node.
    * **Depth-Limited Minimax** - Minimax algorithm that is limited to a certain number of moves.
        * Requires **Evaluation Function** - A function that estimates the expected utility of the game from a given state. Therefore the quality of the AI depends on the quality of the Evaluation Function.
