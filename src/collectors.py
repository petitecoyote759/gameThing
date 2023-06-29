import pygame
from src.man import Man


class Collector:

    def __init__(self, tier, name, image, pos):

        self.tier = tier # 1 for wood, 4 for diamond
        self.name = name
        self.image = image
        self.pos = pos
        self.selected = False
        self.collectPos = [[]] # tier number of destinations possible
        self.deliverPos = []
        self.mode = "gather"
        self.man = Man(self.pos, self.mode)

    def action(self, dt, world, cam):

        if self.selected:

            cam.hotbar.active = False

            keys = pygame.key.get_pressed()



            if keys[pygame.K_1]:

                self.mode = "gather"
                self.man.mode = self.mode
                self.collectPos = [[]]

            elif keys[pygame.K_2]:

                self.mode = "move"
                self.man.mode = self.mode



            if keys[pygame.K_LSHIFT]:
                
                mousePos = pygame.mouse.get_pos()
                mouseBlockPos = [int(((mousePos[0] - 320)/cam.zoom + cam.pos[0])//1),
                                 int(((mousePos[1] - 240)/cam.zoom + cam.pos[1])//1)]
                selectedBuilding = world.buildings[mouseBlockPos[0]][mouseBlockPos[1]]
                if (self.pos[0]-60)**2 + (self.pos[1]-60)**2 <= (8 + self.tier)**2:
                    if selectedBuilding != "" and selectedBuilding != "taken":
                        if selectedBuilding.name == "hub" or selectedBuilding.name == "barrel":
                            self.deliverPos = mouseBlockPos
                            self.man.changeDeliver(mouseBlockPos)
                    elif selectedBuilding == "taken":
                        self.deliverPos = mouseBlockPos
                        self.man.changeDeliver(mouseBlockPos)



            if self.mode == "move":

                if keys[pygame.K_LCTRL]:
                    
                    mousePos = pygame.mouse.get_pos()
                    mouseBlockPos = [int(((mousePos[0] - 320)/cam.zoom + cam.pos[0])//1),
                                     int(((mousePos[1] - 240)/cam.zoom + cam.pos[1])//1)]
                    selectedBuilding = world.buildings[mouseBlockPos[0]][mouseBlockPos[1]]
                    if (mouseBlockPos[0]-self.pos[0])**2 + (mouseBlockPos[1]-self.pos[1])**2 <= (4 + self.tier)**2:
                        if selectedBuilding != "" or selectedBuilding != "taken":
                            if selectedBuilding.name == "hub" or selectedBuilding.name == "barrel":
                                self.collectPos[0] = mouseBlockPos # make it so it has tier number



        if self.deliverPos != []:

            self.man.update(world, dt)
            


        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.selected:

            world.buildings[self.pos[0]][self.pos[1]] = ""
            world.hub.inventory["log"] += 10
            if self.tier >= 2:
                world.hub.inventory["stone"] += 10
            if self.tier >= 3:
                world.hub.inventory["ore"] += 10
            if self.tier == 4:
                world.hub.inventory["gem"] += 10

              
    def upgrade(self, world, cam):

        pass

    def render(self, cam, screen, world):

        image = pygame.transform.scale(self.image, (cam.zoom+1,cam.zoom+1))
        px, py = cam.findPos(self.pos[0], self.pos[1])
        screen.blit(image, (px,py))

        self.man.render(cam,screen, world)

        if self.selected:

            if self.collectPos != [[]]:

                for item in self.collectPos:
                    image = world.tiles["collectBox"]
                    image = pygame.transform.scale(image, (cam.zoom+1, cam.zoom+1))
                    px, py = cam.findPos(item[0], item[1])
                    screen.blit(image, (px, py))

            if len(self.deliverPos) != 0:

                image = world.tiles["deliverBox"]
                image = pygame.transform.scale(image, (cam.zoom+1,cam.zoom+1))
                px, py = cam.findPos(self.deliverPos[0], self.deliverPos[1])
                screen.blit(image, (px,py))

        
        
