import pygame, sys
from src.collectors import Collector
from src.extractors import Extractor
from src.storage import Storage

# extractor
# mover
# guns
# ammo factory
# when click on one, 4 layers pop up to show levels (wood, rock, metal, diamond)



class Hotbar:

    def __init__(self, posx, posy, world):

        self.pos = [posx, posy]
        self.image = pygame.image.load("res/hotbar.png")
        self.pickImage = world.tiles["woodExtractor"]
        self.moverImage = world.tiles["woodCollector"]
        self.barrelImage = world.tiles["woodBarrel"]
        self.selectBox = pygame.image.load("res/selected.png")
        self.active = False
        self.selected = [60, 60]

        self.resources = {
            "logs" : 100}

    def display(self, screen, cam, world):

        if self.active:

            image = pygame.transform.scale(self.selectBox, (cam.zoom+1, cam.zoom+1))
            px, py = cam.findPos(self.selected[0], self.selected[1])
            screen.blit(image, (px,py))
            
            image = pygame.transform.scale(self.image, (150, int(150 * 0.2775)))
            screen.blit(image, (self.pos[0], self.pos[1]))

            pickImage = pygame.transform.scale(self.pickImage, (40, 40))
            screen.blit(pickImage, (self.pos[0], self.pos[1]))

            moverImage = pygame.transform.scale(self.moverImage, (30, 30))
            screen.blit(moverImage, (self.pos[0]+40, self.pos[1]+5))

            barrelImage = pygame.transform.scale(self.barrelImage, (30, 30))
            screen.blit(barrelImage, (self.pos[0]+77, self.pos[1]+2))


        image = world.itemPics["log"]
        image = pygame.transform.scale(image, (30,30))
        screen.blit(image,(180, 0))
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(world.hub.inventory["log"]), True, (0,0,0))
        screen.blit(img, (180+5, 30))

        image = world.itemPics["stone"]
        image = pygame.transform.scale(image, (40,40))
        screen.blit(image,(255, -10))
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(world.hub.inventory["stone"]), True, (0,0,0))
        screen.blit(img, (265, 30))

        image = world.itemPics["ore"]
        image = pygame.transform.scale(image, (40,40))
        screen.blit(image,(330, -10))
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(world.hub.inventory["ore"]), True, (0,0,0))
        screen.blit(img, (340+7, 30))

        image = world.itemPics["gem"]
        image = pygame.transform.scale(image, (40,40))
        screen.blit(image,(405, -10))
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(world.hub.inventory["gem"]), True, (0,0,0))
        screen.blit(img, (415+7, 30))
            

    def update(self, world):

        keys = pygame.key.get_pressed()


        
        if keys[pygame.K_1] and self.active and world.map[int(self.selected[0])][self.selected[1]] in world.ores and world.buildings[self.selected[0]][self.selected[1]] == "":
            if world.hub.inventory["log"] >= 5:
                world.buildings[self.selected[0]][self.selected[1]] = Extractor(1, "extractor", world.tiles["woodExtractor"], self.selected, world.drops[world.map[self.selected[0]][self.selected[1]]])
                world.hub.inventory["log"] -= 5

        if keys[pygame.K_2] and self.active and world.map[int(self.selected[0])][self.selected[1]] not in world.ores and world.buildings[self.selected[0]][self.selected[1]] == "":

            if world.hub.inventory["log"] >= 10:
                world.buildings[self.selected[0]][self.selected[1]] = Collector(1, "collector", world.tiles["woodCollector"], self.selected)
                world.hub.inventory["log"] -= 10

        if keys[pygame.K_3] and self.active and world.map[int(self.selected[0])][self.selected[1]] not in world.ores and world.buildings[self.selected[0]][self.selected[1]] == "":

            if world.hub.inventory["log"] >= 15:
                world.buildings[self.selected[0]][self.selected[1]] = Storage(1, "barrel", world.tiles["woodBarrel"], self.selected)
                world.hub.inventory["log"] -= 15


                

        if world.buildings[self.selected[0]][self.selected[1]] != "":
            if world.buildings[self.selected[0]][self.selected[1]] == "taken":
                world.hub.selected = True
            else:
                world.buildings[self.selected[0]][self.selected[1]].selected = True
            


def main():

    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    hotbar = Hotbar(320-113, 480 - 100)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        hotbar.display(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
