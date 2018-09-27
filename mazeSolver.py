from PIL import Image

class Maze:
    def __init__(self, mazeName):
        self.im = Image.open(mazeName)
        self.pix = self.im.load()

    def convert (self):
        pixels = []
        for y in range(self.im.width):
            pixels.append([])
            for x in range(self.im.height):
                r, g, b, d = self.pix[x, y]
                pixels[y].append(d == 255)
        return pixels

    def display (self, pixels):
        print()
        for x in range(self.im.width):
            for y in range(self.im.height):
                if pixels[x][y] == True:
                    print('O  ', end = '')
                else:
                    print('   ', end = '')
            print('\n')

    def solve (self):
        self.pix[3, 4] = (255, 0, 0, 255)
        self.im.save('solution.png')

m = Maze('maze2.png')
pixels = m.convert()
m.display(pixels)
m.solve()
