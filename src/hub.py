import pygame, time

class Hub:

    def __init__(self, tier, name, image, pos):

        self.tier = tier # 1 for wood, 4 for diamond
        self.name = name
        self.image = image
        self.pos = pos
        self.inventory = {
            "log" : 500,
            "stone" : 100,
            "ore" : 100,
            "gem" : 100
            }
        self.selected = False

    def action(self, dt, world, cam):

        pass

    def upgrade(self, world, cam):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_u] and self.tier != 4 and self.selected:
            if self.tier == 1 and self.inventory["stone"] >= 50:
                self.tier = 2
                world.hub.inventory["stone"] -= 50
                cam.changeTier()
                self.time = time.perf_counter()
                self.image = pygame.image.load("res/stoneHub.png")
            elif self.tier == 2 and self.inventory["ore"] >= 50 and time.perf_counter()-self.time > 0.5:
                self.tier = 3
                world.hub.inventory["ore"] -= 50
                cam.changeTier()
                self.time = time.perf_counter()
            elif self.tier == 3 and self.inventory["gem"] >= 50 and time.perf_counter()-self.time > 0.5:
                self.tier = 4
                world.hub.inventory["gem"] -= 50
                cam.changeTier()

    def render(self, cam, screen, world):

        image = pygame.transform.scale(self.image, (2*(cam.zoom+1),2*(cam.zoom+1)))
        px, py = cam.findPos(self.pos[0], self.pos[1])
        screen.blit(image, (px,py))

        if self.selected and self.tier != 4:
            image = world.hubUpgrades[self.tier]
            image = pygame.transform.scale(image, (2*(cam.zoom+1),2*(cam.zoom+1)))
            px, py = cam.findPos(self.pos[0], self.pos[1] - 2)
            screen.blit(image, (px,py))




            
