import sys
from PIL import ImageDraw,Image
from collections import deque
class Node():

    def __init__(self,pos,parent):
        self.pos=pos
        self.parent=parent

class QUEUE():

    def __init__(self):
        self.queue=deque()
    def add(self,node):
        self.queue.append(node)
    def contains(self,node):
        if node in self.queue:
            return True
        return False
    def empty(self):
        return len(self.queue)==0
    def remove(self):
        if not self.empty():
            return self.queue.popleft()
        else:
             raise Exception('Empty')
    def print(self):
        for i in self.queue:
            print((i.pos,i.parent),end=" ")
        print()

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

        start=Node(self.start,None)
        end=Node(self.end,None)
        queue=QUEUE()
        queue.add(start)
        self.visited=set()
        self.explored=0
        while True:
            if queue.empty():
                break
            now=queue.remove()
            self.explored+=1
            if now.pos==end.pos:
                path=[]
                while now.parent:
                    path.append(now.pos)
                    now=now.parent
                path.reverse()
                self.solution=path[:]
                return
            self.visited.add(now.pos)
            for i in self.neighbors(now.pos):
                if not queue.contains(i) and i not in self.visited:
                    next=Node(i,parent=now)
                    queue.add(next)
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
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    maze = Maze(sys.argv[1])
    maze.solve()
    print("Solution:")
    maze.print()
    print("States Explored:", maze.explored)
    print("Cost of BFS:",maze.cost())
    maze.output_image("maze_BFS.png", show_solution=True,show_visited=False)

if __name__=='__main__':
    main()
else:
    file=sys.argv[1]
    maze = Maze(file)
    maze.solve()
    print("Cost of BFS:",maze.cost())
    maze.output_image("maze_BFS.png", show_solution=True,show_visited=False)
