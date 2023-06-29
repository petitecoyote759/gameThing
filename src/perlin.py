import pygame, sys, random


class Perlin:

    def __init__(self, scale, width, height):

        self.scale = scale
        self.width = width
        self.height = height
        self.grid = [[random.choice([(1,1), (1,-1), (-1,1), (-1,-1)]) for i in range((height//scale) + 2)] for j in range((width//scale) + 2)]
        
    
    def interpolate(self,  a0,  a1,  w):
        return (a1 - a0) * (3.0 - w * 2.0) * w * w + a0


    def dotGridGradient(self,  ix,  iy,  x,  y):

        gradient = self.grid[ix][iy]
         
        dx = x - ix
        dy = y - iy
         
        return (dx*gradient[0] + dy*gradient[1])




    def perlin(self, x, y):

        x /= float(self.scale)
        y /= float(self.scale)

        x0 = int(x//1)
        x1 = x0 + 1
        y0 = int(y//1)
        y1 = y0 + 1

        sx = x - x0
        sy = y - y0

        n0 = self.dotGridGradient(x0, y0, x, y)
        n1 = self.dotGridGradient(x1, y0, x, y)
        ix0 = self.interpolate(n0, n1, sx)

        n0 = self.dotGridGradient(x0, y1, x, y)
        n1 = self.dotGridGradient(x1, y1, x, y)
        ix1 = self.interpolate(n0, n1, sx)

        value = self.interpolate(ix0, ix1, sy);
        return value

def main():

    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    p = Perlin(4, 120, 120)


    for x in range(p.width):
        for y in range(p.height):
            value = p.perlin(x, y)
            #value = int((value + 1) * 255/2)
            value = 255 if value > 0.5 else 0
            screen.fill((value,value,value), (x*5,y*5,5,5))

                # change 0.5 to change size/ how common lumps are
                # change scale to change smaller clumps but more
            # rember to change size down when scale increases, they multiply


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main()


