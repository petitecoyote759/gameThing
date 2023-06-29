import pygame
from src.item import Item

class Storage:

    def __init__(self, tier, name, image, pos):

        self.tier = tier # 1 for wood, 4 for diamond
        self.name = name
        self.image = image
        self.pos = pos
        self.inventory = {
            "log" : 0,
            "stone" : 0,
            "ore" : 0,
            "gem" : 0
            }
        self.selected = False

    def action(self, dt, world, cam):

        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.selected:

            world.buildings[self.pos[0]][self.pos[1]] = ""
            world.hub.inventory["log"] += 15
            if self.tier >= 2:
                world.hub.inventory["stone"] += 15
            if self.tier >= 3:
                world.hub.inventory["ore"] += 15
            if self.tier == 4:
                world.hub.inventory["gem"] += 15
            for item in range(self.inventory["log"]):
                NewItem = Item(self.pos, "log", world)
                world.items.append(NewItem)
            for item in range(self.inventory["stone"]):
                NewItem = Item(self.pos, "stone", world)
                world.items.append(NewItem)
            for item in range(self.inventory["ore"]):
                NewItem = Item(self.pos, "ore", world)
                world.items.append(NewItem)
            for item in range(self.inventory["gem"]):
                NewItem = Item(self.pos, "gem", world)
                world.items.append(NewItem)


        if self.inventory["log"] > self.tier * 50:
            self.inventory["log"] = self.tier * 50
            
        if self.inventory["stone"] > self.tier * 50:
            self.inventory["stone"] = self.tier * 50
            
        if self.inventory["ore"] > self.tier * 50:
            self.inventory["ore"] = self.tier * 50
            
        if self.inventory["gem"] > self.tier * 50:
            self.inventory["gem"] = self.tier * 50


    def upgrade(self, world, cam):

        pass

    def render(self, cam, screen, world):

        image = pygame.transform.scale(self.image, ((cam.zoom+1),(cam.zoom+1)))
        px, py = cam.findPos(self.pos[0], self.pos[1])
        screen.blit(image, (px,py))
