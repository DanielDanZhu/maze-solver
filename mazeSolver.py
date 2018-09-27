from PIL import Image

class Maze:
    def __init__(self, mazeName):
        self.im = Image.open(mazeName)
        self.pix = self.im.load()
        self.pixels = []
        self.nodes = []

    def in_range(self, x, y):
        return x >= 0 and x < self.im.width and y>= 0 and y < self.im.height

    def convert(self): # returns 2d boolean list representation of maze
        self.pixels = []
        for x in range(self.im.width):
            self.pixels.append([])
            for y in range(self.im.height):
                r, g, b, d = self.pix[x, y]
                # pixels are only black when rgb is 0, 0, 0 and d is 255
                self.pixels[x].append(r == g == b == 0 and d == 255)

    def create_nodes(self):
        for y in range(self.im.height):
            for x in range(self.im.width):
                if not self.pixels[x][y]:                                       # is path
                    if not self.in_range(x, y-1):                               # start
                        self.nodes.append(Node(x, y, [], True, False))
                    elif not self.in_range(x, y+1):                             # end
                        self.nodes.append(Node(x, y, [], False, True))
                    elif (self.pixels[x-1][y] != self.pixels[x+1][y] or         # left != right
                          self.pixels[x][y-1] != self.pixels[x][y+1]):          # down != up
                        self.nodes.append(Node(x, y, [], False, False))

    def connect_nodes(self):
        directions = [[1, 0], [0, 1]]

        for node in self.nodes:
            if not node.e:
                for xdir, ydir in directions:                                   # checks right and down
                    currx = node.x + xdir
                    curry = node.y + ydir
                    added = False
                    while not self.pixels[currx][curry]:                        # while on a path
                        for other_node in self.nodes:
                            if currx == other_node.x and curry == other_node.y: #connects to node if met
                                node.add_connection(other_node)
                                other_node.add_connection(node)
                                added = True
                        if added:
                            break
                        currx += xdir
                        curry += ydir

    def display_maze(self):
        for y in range(self.im.height):
            for x in range(self.im.width):
                if self.pixels[x][y]:
                    print('█', end = '')
                else:
                    print(' ', end = '')
            print('')

    def display_nodes(self):
        for i in self.nodes:
            print(str(i.x) + ", " + str(i.y) + ": " + str(len(i.connections)) + " " + str(i.s) + " " + str(i.e))

    def display_nodes_distance(self):
        for i in self.nodes:
            print("(" + str(i.x) + ", " + str(i.y) + "): ", end = '')
            for other in i.connections:
                print("[(" + str(other.x) + ", " + str(other.y) + "), " + str(i.get_distance(other)) + "] ", end = '')
            print()

class Node:
    def __init__(self, x, y, connections, s, e):
        self.x, self.y, self.connections, self.s, self.e = x, y, connections, s, e

    def add_connection(self, other_node):
        self.connections.append(other_node)

    def get_distance(self, other_node):
        if not other_node in self.connections:
            return 0
        return abs(self.x - other_node.x) + abs(self.y - other_node.y)

m = Maze('maze.png')
m.convert()
m.display_maze()
m.create_nodes()
m.connect_nodes()
m.display_nodes()
m.display_nodes_distance()
