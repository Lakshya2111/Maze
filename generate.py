from PIL import ImageDraw,Image
import random,sys
from random import randint
height=randint(10,20)
width=randint(20,40)
maze=[]
for i in range(height):
    row=[]
    for j in range(width):
        row.append('#')
    maze.append(row)
start=(randint(0,height-1),randint(0,width-1))
stack=[start]
visited=dict()
visited[start]=True
def print_maze(maze):
    print()
    for i in range(height):
        for j in range(width):
            if maze[i][j]=='A':
                print('A',end='')
            if maze[i][j]=='B':
                print('B',end='')
            if maze[i][j]=='#':
                print("█", end="")
            else:
                print(' ',end="")

        print()
    print()
def get_neighbour(node,visited):
    row,col=node
    neighbour=[]
    actions=[(row+2,col),(row-2,col),(row,col+2),(row,col-2)]
    for r,c in actions:
        if 0<=r<height and 0<=c<width and (r,c) not in visited.keys():
            neighbour.append((r,c))
    return neighbour
path=[]
while(stack):
    node=stack.pop()
    path.append(node)
    maze[node[0]][node[1]]=" "
    neighbour=get_neighbour(node,visited)
    random.shuffle(neighbour)
    for i in range(len(neighbour)):
        r,c=neighbour[i]
        stack.append(neighbour[i])
        visited[neighbour[i]]=True
for i in range(1,len(path)):
    if path[i][0]==path[i-1][0]:
        if path[i][1]+1<width and path[i][1]>path[i-1][1]:
            maze[path[i][0]][path[i][1]+1]=" "
        elif path[i][1]-1>=0:
            maze[path[i][0]][path[i][1]-1]=" "
    else:
        if path[i][0]+1<height and path[i][0]>path[i-1][0]:
            maze[path[i][0]+1][path[i][1]]=" "
        elif path[i][0]+1>=0:
            maze[path[i][0]-1][path[i][1]]=" "
free=[]
for i in range(height):
    for j in range(width):
        if maze[i][j]=='#':
            free.append((i,j))
start,end=free[randint(0,len(free)-1)],free[randint(0,len(free)-1)]
maze[start[0]][start[1]]='A'
maze[end[0]][end[1]]='B'
for i in range(height):
    for j in range(width):
        if maze[i][j]=='#':
            maze[i][j]=' '
        elif maze[i][j]==' ':
            maze[i][j]='#'
print_maze(maze)
if len(sys.argv) != 2:
    sys.exit("Usage: python generate.py maze.txt")
filename = sys.argv[1]
with open(filename,'w') as file:
    for i in maze:
        file.write(''.join(i))
        file.write('\n')
def output_image(filename):
    cell_size = 50
    cell_border = 2

    # Create a blank canvas
    img = Image.new(
        "RGBA",
        (width * cell_size, height * cell_size),
        "black"
    )
    draw = ImageDraw.Draw(img)

    for i in range(height):
        for j in range(width):

            # Walls
            if maze[i][j]=='#':
                fill = (40, 40, 40)

            # Start
            elif (i, j) == start:
                fill = (255, 0, 0)

            # End
            elif (i, j) == end:
                fill = (0, 171, 28)

            # Empty
            else:
                fill = (237, 240, 252)

            # Draw cell
            draw.rectangle(
                ([(j * cell_size + cell_border, i * cell_size + cell_border),
                  ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                fill=fill
            )

    img.save(filename)
output_image('unsolved_maze.png')
