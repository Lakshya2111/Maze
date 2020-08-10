# Maze
A maze generator and solver using BFS, DFS, A* (star) and Dijkstra algorithms with visual.
* For generating a maze run:
   * python generate.py unsolved_maze.txt(filename to save the maze)
* The generated visual of maze will be saved in unsolved_maze.png
* To solve a maze run:
   * python (specify the file).py unsolved_maze.txt
* To solve the maze using all the algorithms run:
    * python all.py unsolved_maze.txt
* Visual of maze will be saved to (algorithm_name).png
* You can check the visited states by changing the show_visited to "True" in the source code of the algorithms

### Unsolved Maze

![unsolved](/Images/unsolved_maze.png)

### A_star solution

![A-star](/Images/maze_a_star.png)

### A_star solution with explored states

![A-star explored states](/Images/maze_a_star_explored.png)

### Dijkstra solution

![Dijkstra](/Images/maze_dijkstra.png)

### BFS solution

![BFS](/Images/maze_BFS.png)

### DFS solution

![DFS](/Images/maze_DFS.png)
