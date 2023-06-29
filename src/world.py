import random, pygame
from src.perlin import Perlin
from src.hub import Hub

class World:

    def __init__(self, width, height,cam):

        self.width = width
        self.height = height

        woodNoise = Perlin(8, width, height)
        stoneNoise = Perlin(4, width, height)
        metalNoise = Perlin(4, width, height)
        diamondNoise = Perlin(4, width, height)

        self.items = []        
        
        self.map = [["grass" for i in range(height)] for j in range(width)]
        for x in range(width):
            for y in range(height):
                if woodNoise.perlin(x, y) > 0.4 and 40**2 > (x-self.width/2)**2 + (y-self.height/2)**2 > 4**2:
                    self.map[x][y] = "wood"
                if stoneNoise.perlin(x,y) > 0.4 and 60**2 > (x-self.width/2)**2 + (y-self.height/2)**2 > 20**2:
                    self.map[x][y] = "rock"
                if metalNoise.perlin(x,y) > 0.4 and (x-self.width/2)**2 + (y-self.height/2)**2 > 50**2:
                    self.map[x][y] = "metal"
                if metalNoise.perlin(x,y) > 0.5 and (x-self.width/2)**2 + (y-self.height/2)**2 > 70**2:
                    self.map[x][y] = "diamond"

        self.buildings = [["" for i in range(height)] for j in range(width)]
        self.buildings[width//2][height//2-1] = "taken"
        self.buildings[width//2-1][height//2] = "taken"
        self.buildings[width//2][height//2] = "taken"
                    
        self.tiles = {
            "wood" : pygame.image.load("res/wood.png"),
            "grass" : pygame.image.load("res/grass.png"),
            "rock" : pygame.image.load("res/rock.png"),
            "metal" : pygame.image.load("res/metal.png"),
            "diamond" : pygame.image.load("res/diamond.png"),
            "border" : pygame.image.load("res/border.png"),
            "hub" : pygame.image.load("res/woodHub.png"),
            "woodExtractor" : pygame.image.load("res/woodPick.png"),
            "fog" : pygame.image.load("res/fog.png"),
            "woodCollector" : pygame.image.load("res/woodMover.png"),
            "collectBox" : pygame.image.load("res/collectBox.png"),
            "deliverBox" : pygame.image.load("res/deliverBox.png"),
            "man" : pygame.image.load("res/man.png"),
            "woodBarrel" : pygame.image.load("res/woodBarrel.png")
               }

        self.extractorUpgrades = {
            1 : pygame.image.load("res/upgradeExtractStone.png"),
            2 : pygame.image.load("res/upgradeExtractMetal.png"),
            3 : pygame.image.load("res/upgradeExtractDiamond.png")
            }

        self.hubUpgrades = {
            1 : pygame.image.load("res/upgradeHubStone.png"),
            2 : pygame.image.load("res/upgradeHubMetal.png"),
            3 : pygame.image.load("res/upgradeHubDiamond.png")
            }

        self.extractors = {
            "woodExtractor" : pygame.image.load("res/woodPick.png"),
            "stoneExtractor" : pygame.image.load("res/stonePick.png"),
            "metalExtractor" : pygame.image.load("res/metalPick.png"),
            "diamondExtractor" : pygame.image.load("res/diamondPick.png")
            }

        self.ores = {
            "wood" : self.tiles["wood"],
            "rock" : self.tiles["rock"],
            "metal" : self.tiles["metal"],
            "diamond" : self.tiles["diamond"]
            }

        self.drops = {
            "wood" : "log",
            "rock" : "stone",
            "metal" : "ore",
            "diamond" : "gem"
            }

        self.itemPics = {
            "log" : pygame.image.load("res/log.png"),
            "stone" : pygame.image.load("res/stone.png"),
            "ore" : pygame.image.load("res/ore.png"),
            "gem" : pygame.image.load("res/gem.png")
            }

        self.enemies = {
            "zombie" : pygame.image.load("res/zombie.png")
            }

        self.fogMap = [["fog" for i in range(height)]for j in range(width)]
        for x in range (width//2 - 9, width//2 + 9):
            for y in range(height//2 - 9, height//2 + 9):
                self.fogMap[x][y] = ""

        self.hub = Hub(1, "hub", self.tiles["hub"], [width//2-1,height//2-1])
        self.buildings[width//2-1][height//2-1] = self.hub            
        


        

    def draw(self,cam,screen):

        for x in range(int(cam.pos[0] - cam.squarePerRow/2), int(cam.pos[0] + cam.squarePerRow/2)):
            for y in range(int(cam.pos[1] - cam.squarePerColumn/2), int(cam.pos[1] + cam.squarePerColumn/2)):
                
                px = (x - cam.pos[0]) * cam.zoom + 320
                py = (y - cam.pos[1]) * cam.zoom + 240
                
                if not(0 <= x < self.width and 0 <= y < self.height):
                    continue

                image = self.tiles[self.map[x][y]]
                image = pygame.transform.scale(image, (cam.zoom + 1,cam.zoom + 1))
                screen.blit(image, (px,py))

        for x in range(int(cam.pos[0] - cam.squarePerRow/2), int(cam.pos[0] + cam.squarePerRow/2)):
            for y in range(int(cam.pos[1] - cam.squarePerColumn/2), int(cam.pos[1] + cam.squarePerColumn/2)):

                px = (x - cam.pos[0]) * cam.zoom + 320
                py = (y - cam.pos[1]) * cam.zoom + 240
                
                if not(0 <= x < self.width and 0 <= y < self.height):
                    continue

                elif self.buildings[x][y] == "hub":

                    image = self.tiles["hub"]
                    image = pygame.transform.scale(image, (2*(cam.zoom + 1),2*(cam.zoom + 1)))
                    screen.blit(image, (px,py))




    def drawBox(self, screen, cam):

        mousePos = pygame.mouse.get_pos()
        
        ScaleMouseBox = pygame.transform.scale(self.tiles["border"], (cam.zoom + 1,cam.zoom + 1))

        grid_x, grid_y = int(((mousePos[0] - 320)/cam.zoom + cam.pos[0])//1),int(((mousePos[1] - 240)/cam.zoom + cam.pos[1])//1)
        px = (grid_x - cam.pos[0]) * cam.zoom + 320
        py = (grid_y - cam.pos[1]) * cam.zoom + 240
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            screen.blit(ScaleMouseBox, (px, py))



    def renderFog(self,screen,cam):

        for x in range(int(cam.pos[0] - cam.squarePerRow/2), int(cam.pos[0] + cam.squarePerRow/2)):
            for y in range(int(cam.pos[1] - cam.squarePerColumn/2), int(cam.pos[1] + cam.squarePerColumn/2)):
                try:
                    if self.fogMap[x][y] == "fog":
                        px, py = cam.findPos(x, y)
                        
                        image = pygame.transform.scale(self.tiles["fog"], (cam.zoom+2, cam.zoom+2))
                        screen.blit(image, (px,py))
                except:
                    pass



                

        





