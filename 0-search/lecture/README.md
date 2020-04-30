## Search Algorithms

- **Uninformed Search algorithms** - Search strategy that uses no problem-specific knowledge.
    * **Depth-First Search (DFS)** - Explores the deepest node in the frontier. In this case, the frontier is of Stack type (LIFO: last-in-first-out). Always finds a solution, but it might not be the optimal solution (if you are unlucky), but at a lesser cost.
    * **Breadth-First Search (BFS)** - Explores the shallowest node in the frontier. In this case, the frontier is of a Queue type (FIFO: first-in-first-out). Always finds the **optimal solution** but at a greater cost.
- **Informed Search algorithms** - Search strategy that uses problem-specific knowledge to find solutions more efficiently.
    * **Greedy Best-First Search** - Explores the node that is closest to the goal, as estimated by a heuristic function *h(n)*. Always finds a solution, but it might not be the optimal solution (if you are unlucky), but at a much lesser cost.
    * __A* Search__ - Explores the node with lowest value of *g(n) (cost to reach the node)* + *h(n) (estimated cost to goal)*. Always finds the **optimal solution IF the below conditions are met**, at a much lesser cost (though it depends).
        * Optimal if *h(n)* is admissible - never overestimates the true cost.
        * Optimal if *h(n)* is consistent - for every node *n* and successor *n'* with step cost *c, h(n) <= h(n') + c*.

In the lecture, example heuristic function *h(n)* was calculated using **Manhattan distance** which is the distance between two points measured along axes at right angles.

## Adversarial Search Algorithms

- **Minimax** - Tries to find the best move, by working backward from the end of the game.
    * *Max(x)* aims to maximize score *(because win value is 1)*
    * *Min(o)* aims to minimize score *(because win value is -1)*
    * **Alpha-Beta Pruning** - Minimax algorithm that tries to decrease the number of nodes that are evaluated by not exploring the nodes that do not give the optimal solution in the respective node.
    * **Depth-Limited Minimax** - Minimax algorithm that is limited to a certain number of moves.
        * Requires **Evaluation Function** - A function that estimates the expected utility of the game from a given state. Therefore the quality of the AI depends on the quality of the Evaluation Function.