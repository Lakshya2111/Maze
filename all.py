import sys
 
if len(sys.argv) != 2:
    sys.exit("Usage: python all.py maze.txt")

import BFS
import DFS
import a_star
import dijkstra
