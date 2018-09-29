from PIL import Image

class Node:
    def __init__(self, x, y, connections):
        self.x, self.y, self.connections= x, y, connections

class Maze:
    def __init__(self, mazeName):
        self.im = Image.open(mazeName)
        self.pix = self.im.load()
        self.pixels = self.nodes = []
        self.start_node = self.end_node = None

    def convert(self): # returns 2d boolean list representation of maze
        self.pixels = []
        for x in range(self.im.width):
            self.pixels.append([])
            for y in range(self.im.height):
                r, g, b, d = self.pix[x, y]
                # pixels are only black when rgb is 0, 0, 0 and d is 255
                self.pixels[x].append(r == g == b == 0 and d == 255)

    def create_nodes(self):
        self.convert()
        for y in range(self.im.height):
            for x in range(self.im.width):
                if not self.pixels[x][y]:                                       # is path
                    if y - 1 < 0:                                               # start
                        self.nodes.append(Node(x, y, []))
                        self.start_node = self.nodes[len(self.nodes)-1]
                    elif y + 1 >= self.im.height:                               # end
                        self.nodes.append(Node(x, y, []))
                        self.end_node = self.nodes[len(self.nodes)-1]
                    elif (self.pixels[x-1][y] != self.pixels[x+1][y] or         # left != right
                          self.pixels[x][y-1] != self.pixels[x][y+1]):          # down != up
                        self.nodes.append(Node(x, y, []))

    def connect_nodes(self):
        self.create_nodes()
        directions = [[1, 0], [0, 1]]

        for node in self.nodes:
            if node != self.end_node:
                for xdir, ydir in directions:                                   # checks right and down
                    currx = node.x + xdir
                    curry = node.y + ydir
                    size = len(node.connections)
                    while not self.pixels[currx][curry]:                        # while on a path
                        for other_node in self.nodes:
                            if currx == other_node.x and curry == other_node.y: # connects to node if met
                                node.connections.append(other_node)
                                other_node.connections.append(node)
                        if len(node.connections) > size:                        # if a connection was added
                            break
                        currx += xdir
                        curry += ydir

    def solve(self):
        self.connect_nodes()
        unvisited = []

        for node in self.nodes:
            unvisited.append([node.x, node.y])

        self.pix[self.start_node.x, self.start_node.y] = (255, 0, 0, 255)
        self.visit(self.start_node, unvisited)

        self.im.save('solution.png')

    def visit(self, node, unvisited):
        unvisited.remove([node.x, node.y])
        # base case
        if node == self.end_node:
            return True
        else:
            for adj in node.connections:
                if [adj.x, adj.y] in unvisited:
                    # if path to unvisited node exists
                    if self.visit(adj, unvisited):
                        xdir = 1 if adj.x > node.x else -1
                        ydir = 1 if adj.y > node.y else -1
                        xcurr, ycurr = node.x, node.y
                        # colors in path between nodes
                        for i in range(abs(adj.x - node.x)):
                            xcurr += xdir
                            self.pix[xcurr, ycurr] = (255, 0, 0, 255)
                        for i in range(abs(adj.y - node.y)):
                            ycurr += ydir
                            self.pix[xcurr, ycurr] = (255, 0, 0, 255)
                        return True

    def resize(self, ratio):
        large_im = Image.new('RGBA', (self.im.width * ratio, self.im.height * ratio), color = 'black')
        large_pix = large_im.load()
        for x in range(large_im.width):
            for y in range(large_im.height):
                large_pix[x, y] = self.pix[int(x / ratio), int(y / ratio)]
        large_im.save('solutionlarge.png')

m = Maze('maze.png')
m.solve()
m.resize(5)
