import random,pygame
from src.item import Item

class Extractor:

    def __init__(self, tier, name, image, pos, material):

        self.tier = tier # 1 for wood, 4 for diamond
        self.name = name
        self.image = image
        self.pos = pos
        self.material = material
        
        if material == "log":
            self.rarity = 1
        if material == "stone":
            self.rarity = 2
        if material == "ore":
            self.rarity = 3
        if material == "gem":
            self.rarity = 4

        
            
        self.calcExtractTime()
        self.selected = False

    def action(self, dt, world, cam):

        if self.timeRemaining <= dt/1000:
            itemPresent = False
            for item in world.items:
                if item.pos == tuple(self.pos):
                    itemPresent = True
            if itemPresent == False:
                world.items.append(Item((self.pos[0],self.pos[1]), self.material, world))
            else:
                pass
            self.timeRemaining = self.timePerExtract

        else:
            self.timeRemaining -= dt/1000


        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.selected:

            world.buildings[self.pos[0]][self.pos[1]] = ""
            world.hub.inventory["log"] += 5
            if self.tier >= 2:
                world.hub.inventory["stone"] += 5
            if self.tier >= 3:
                world.hub.inventory["ore"] += 5
            if self.tier == 4:
                world.hub.inventory["gem"] += 5
            


    def upgrade(self,world, cam):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_u] and self.tier != 4 and self.selected:
            if self.tier == 1 and world.hub.inventory["stone"] >= 5:
                self.tier = 2
                world.hub.inventory["stone"] -= 5
                self.calcExtractTime()
            elif self.tier == 2 and world.hub.inventory["ore"] >= 5:
                self.tier = 3
                world.hub.inventory["ore"] -= 5
                self.calcExtractTime()
            elif self.tier == 3 and world.hub.inventory["gem"] >= 5:
                self.tier = 4
                world.hub.inventory["gem"] -= 5
                self.calcExtractTime()

        

    def render(self, cam, screen, world):

        if self.tier == 1:
            image = world.extractors["woodExtractor"]
        elif self.tier == 2:
            image = world.extractors["stoneExtractor"]
        elif self.tier == 3:
            image = world.extractors["metalExtractor"]
        else:
            image = world.extractors["diamondExtractor"]
        image = pygame.transform.scale(image, (cam.zoom+1,cam.zoom+1))
        px, py = cam.findPos(self.pos[0], self.pos[1])
        screen.blit(image, (px,py))

        if self.selected and self.tier != 4:
            image = world.extractorUpgrades[self.tier]
            scaleImage = pygame.transform.scale(image, (cam.zoom+1,cam.zoom+1))
            py -= cam.zoom
            screen.blit(scaleImage, (px,py))

    def calcExtractTime(self):

        self.timePerExtract = (1 - (self.tier / 5)) * 10 * self.rarity
        self.timeRemaining = self.timePerExtract

        
    
