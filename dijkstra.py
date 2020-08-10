import sys
from PIL import ImageDraw,Image
from heapq import heapify, heappush, heappop
class Node():

    def __init__(self,pos):
        self.pos=pos

class Dijkstra_algo():

    def __init__(self):
        self.distance=dict()
        self.heap=[]
        heapify(self.heap)
        self.shortest_distance=dict()
        self.parent=dict()
    def add_distance(self,node,distance):
        heappush(self.heap,[distance,node])
        self.distance[node]=distance
    def add_shortest_distance(self,node,distance):
        self.shortest_distance[node]=distance
    def get_distance(self,node):
        return self.distance[node]
    def get_shortest_distance(self,node):
        return self.shortest_distance[node]
    def contains(self,node):
        if node in self.shortest_distance.keys():
            return True
        return False
    def empty(self):
        return len(self.heap)==0
    def remove(self):
        if not self.empty():
            return heappop(self.heap)
        else:
             raise Exception('Empty')
    def update(self,node,value):
        heappush(self.heap,[value,node])
        self.distance[node]=value
    def update_parent(self,node,parent):
        self.parent[node]=parent
    def get_parent(self,node):
        return self.parent[node]

class Maze():

    def __init__(self, filename):
        with open(filename) as f:
            contents=f.read()

        #validate start and end
        if contents.count('A')!=1:
            raise Exception('need exactly one starting point')
        if contents.count('B')!=1:
            raise Exception('need exactly one ending point')


        contents=contents.splitlines()
        self.height=len(contents)
        self.width=max(len(i) for i in contents)

        self.walls=[]
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j]=='A':
                        self.start=(i,j)
                    if contents[i][j]=='B':
                        self.end=(i,j)
                    if contents[i][j]=='#':
                        row.append(True)
                    else:
                        row.append(False)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution=None

    def neighbors(self,pos):

        row,col=pos
        neighbour=[]
        actions=[(row+1,col),(row-1,col),(row,col+1),(row,col-1)]
        for r,c in actions:
            if 0<=r<self.height and 0<=c<self.width and not self.walls[r][c]:
                neighbour.append((r,c))
        return neighbour

    def solve(self):
        self.visited=set()
        start=Node(self.start)
        end=Node(self.end)
        Dijkstra=Dijkstra_algo()
        for i in range(self.height):
            for j in range(self.width):
                Dijkstra.add_distance((i,j),float('inf'))
        Dijkstra.add_distance(start.pos,0)
        Dijkstra.update_parent(start.pos,None)
        self.explored=0
        while True:
            if Dijkstra.empty():
                break
            short_distance,now=Dijkstra.remove()
            if now==end.pos:
                break
            Dijkstra.add_shortest_distance(now,short_distance)
            self.explored+=1
            self.visited.add(now)
            for i in self.neighbors(now):
                if Dijkstra.contains(i):
                    continue
                if Dijkstra.get_distance(i)>short_distance+1:
                    Dijkstra.update(i,short_distance+1)
                    Dijkstra.update_parent(i,now)
        path=[]
        node=end.pos
        while(Dijkstra.get_parent(node)!=None):
            path.append(node)
            node=Dijkstra.get_parent(node)
        self.solution=path[::-1]

    def cost(self):
        return len(self.solution)
    def print(self):
        print()
        for i in range(self.height):
            for j in range(self.width):
                try:
                    if self.walls[i][j]==True:
                        print("█", end="")
                    elif (i,j)==self.end:
                        print('B',end="")
                    elif (i,j)==self.start:
                        print('A',end="")
                    elif self.solution!=None and (i,j) in self.solution:
                        print('*',end="")
                    else:
                        print(' ',end="")
                except IndexError:
                    print(" ",end="")
            print()
        print()

    def output_image(self, filename, show_solution, show_visited):
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):

                # Walls
                if self.walls[i][j]:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # End
                elif (i, j) == self.end:
                    fill = (0, 171, 28)

                # Solution
                elif self.solution is not None and show_solution and (i, j) in self.solution:
                    fill = (220, 235, 113)

                # Visited
                elif self.solution is not None and show_visited and (i, j) in self.visited:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)




if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

maze = Maze(sys.argv[1])
# print("Maze:")
# maze.print()
maze.solve()
print("Solution:")
maze.print()
print("States Explored:", maze.explored)
print("Cost of Dijkstra:",maze.cost())
maze.output_image("maze_dijkstra.png", show_solution=True,show_visited=True)

def all(file):
    maze = Maze(file)
    maze.solve()
    maze.output_image("maze_dijkstra.png", True,False)
