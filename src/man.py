import pygame

class Man:

    def __init__(self, collectorPos, mode):

        self.collectorPos = collectorPos[:]
        self.inventory = ""
        self.destination = ""
        self.pos = collectorPos[:]
        self.speed = 0.003
        self.deliverPos = []
        self.mode = mode

    def update(self, world, dt):

        if self.deliverPos != []:

            if self.mode == "gather":


                if self.inventory != "" and self.destination == "":

                    self.destination = self.deliverPos


                if round(self.pos[0]) == self.deliverPos[0] and round(self.pos[1]) == self.deliverPos[1] and self.inventory != "": # could make it a bounding box

                    if world.buildings[self.deliverPos[0]][self.deliverPos[1]] != "taken":
                        world.buildings[self.deliverPos[0]][self.deliverPos[1]].inventory[self.inventory.name] += 1
                    else:
                        world.hub.inventory[self.inventory.name] += 1
                    self.inventory = ""
                    self.destination = ""
                    

                if self.destination != "":
                    if round(self.pos[0]) == self.destination[0] and round(self.pos[1]) == self.destination[1] and self.inventory == "":
                        for item in world.items:
                            if item.pos[0] == round(self.pos[0]) and item.pos[1] == round(self.pos[1]):
                                self.inventory = item
                                world.items.remove(item)
                                break
                        # pick up

                if self.destination != "":
                    if round(self.pos[0]) == self.destination[0] and round(self.pos[1]) == self.destination[1]:

                        self.destination = ""
            
                if self.destination == "":
                    for item in world.items:
                        itemFound = False
                        if not(item.targeted):
                            if (item.pos[0]-self.collectorPos[1]) ** 2 + (item.pos[1]-self.collectorPos[1]) ** 2 <= 15 ** 2:
                                item.target = True
                                self.destination = item.pos 
                        if not(itemFound) and self.destination == "" and self.inventory == "":
                            print(f"set destination to {self.collectorPos}")
                            self.destination = self.collectorPos

                elif self.destination != "" and self.inventory == "":

                    ratio = self.speed/(((self.pos[1]-self.destination[1])**2 + (self.pos[0]-self.destination[0])**2)**0.5)
                    self.pos[0] += dt * ratio * (self.destination[0] - self.pos[0])
                    self.pos[1] += dt * ratio * (self.destination[1] - self.pos[1])


                else:

                    ratio = self.speed/(((self.pos[1]-self.destination[1])**2 + (self.pos[0]-self.destination[0])**2)**0.5)
                    self.pos[0] += dt * ratio * (self.deliverPos[0] - self.pos[0])
                    self.pos[1] += dt * ratio * (self.deliverPos[1] - self.pos[1])
                    
            

    def render(self, cam, screen, world):

        image = pygame.transform.scale(world.tiles["man"], (cam.zoom+1, cam.zoom+1))
        px, py = cam.findPos(self.pos[0], self.pos[1])
        screen.blit(image, (px,py))


    def changeDeliver(self, newPos):

        self.deliverPos = newPos[:]
