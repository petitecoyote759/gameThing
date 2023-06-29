import pygame, math, time

from src.javalin import Javalin

class Camera:

    speed = 0.14

    def __init__(self, posx, posy, zoom):

        self.pos = [posx,posy]
        self.zoom = zoom
        self.calcRange()
        self.image = pygame.image.load("res/woodPlayer.png")
        self.tier = 1
        self.cooldown = 0
        self.inventory = ""

        self.projectileImages = {
            "javalin" : pygame.image.load("res/javalin.png"),
            "bolt" : pygame.image.load("res/bolt.png")
            }

        self.projectiles = []

    def calcRange(self):

        self.squarePerRow = 640/self.zoom+4
        self.squarePerColumn = 480/self.zoom+4

    def update(self, dt, world, selected):

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.pos[1] -= dt*Camera.speed/self.zoom
        if keys[pygame.K_a]:
            self.pos[0] -= dt*Camera.speed/self.zoom
        if keys[pygame.K_s]:
            self.pos[1] += dt*Camera.speed/self.zoom
        if keys[pygame.K_d]:
            self.pos[0] += dt*Camera.speed/self.zoom
        if keys[pygame.K_UP]:
            self.zoom += 1
        if keys[pygame.K_DOWN]:
            self.zoom -= 1

        if self.cooldown != 0 and self.cooldown >= dt/100:
            self.cooldown -= dt/100
        elif self.cooldown != 0:
            self.cooldown = 0

        if keys[pygame.K_SPACE] and self.cooldown == 0 and self.inventory == "":
            self.shoot()
            if self.tier == 1:                
                self.cooldown = 7
            elif self.tier == 2:
                self.cooldown = 10
            else:
                self.cooldown = 1


        if keys[pygame.K_e] and self.inventory != "":
            selectedBuilding = world.buildings[selected[0]][selected[1]]
            if selectedBuilding != "":
                if (self.pos[0]-60) ** 2 + (selected[0]-60)** 2 < 5 ** 2:
                    if (self.pos[1]-60) ** 2 + (selected[1]-60) ** 2 < 5 ** 2:
                        if selectedBuilding == "taken":
                            world.hub.inventory[self.inventory.name] += 1
                            self.inventory = ""
                        elif selectedBuilding.name == "hub":
                            world.hub.inventory[self.inventory.name] += 1
                            self.inventory = ""


        elif keys[pygame.K_e] and self.inventory == "":
            for item in world.items:

                mousePos = pygame.mouse.get_pos()
                mouseBlockPos = [(mousePos[0] - 320)/self.zoom + self.pos[0],
                                 (mousePos[1] - 240)/self.zoom + self.pos[1]]  
                if item.pos[0]+0.5 < mouseBlockPos[0] < item.pos[0]+1:
                    if item.pos[1]+0.5 < mouseBlockPos[1] < item.pos[1]+1:
                        if (self.pos[0]-60) ** 2 + (item.pos[0]-60)** 2 < 5 ** 2:
                            if (self.pos[1]-60) ** 2 + (item.pos[1]-60) ** 2 < 5 ** 2:
                                self.inventory = item
                                world.items.remove(item)
                        
                        

        if self.zoom < 10:
            self.zoom = 10
        if self.zoom > 99:
            self.zoom = 99

        self.calcRange()

        if self.pos[0] > 120-self.squarePerRow/2+2:
            self.pos[0] = 120-self.squarePerRow/2+2
            
        if self.pos[0] < self.squarePerRow/2-2:
            self.pos[0] = self.squarePerRow/2-2
            
        if self.pos[1] > 120-self.squarePerColumn/2+2:
            self.pos[1] = 120-self.squarePerColumn/2+2
            
        if self.pos[1] < self.squarePerColumn/2-2:
            self.pos[1] = self.squarePerColumn/2-2

    def render(self,screen):

        mousePos = pygame.mouse.get_pos()
        scaleImage = pygame.transform.scale(self.image, (2*self.zoom + 2, 2 * self.zoom + 2))
        scaleImage = pygame.transform.rotate(scaleImage, -math.atan2( (mousePos[1]-240), (mousePos[0]-320) )* 180/ math.pi-90)
        px, py = self.findPos(self.pos[0], self.pos[1])
        width = scaleImage.get_width()//2
        height = scaleImage.get_height()//2
        screen.blit(scaleImage, (px - width, py - height))
        
        if self.inventory != "":
            scaleImage = pygame.transform.scale(self.inventory.image, ((1+self.zoom),(self.zoom+1)))
            screen.blit(scaleImage, (px-16, py-16))

    def findPos(self, x, y):

        px = (x - self.pos[0]) * self.zoom + 320
        py = (y - self.pos[1]) * self.zoom + 240
        return px,py

    def shoot(self):

        mousePos = pygame.mouse.get_pos()
        
        if self.tier == 1:
            newJavalin = Javalin(self.projectileImages["javalin"], self.pos, time.perf_counter(), self, -math.atan2( (mousePos[1]-240), (mousePos[0]-320) )+math.pi/2, 5, 1.5)
            self.projectiles.append(newJavalin)
            
        elif self.tier == 2:
            newBolt = Javalin(self.projectileImages["bolt"], self.pos, time.perf_counter(), self, -math.atan2( (mousePos[1]-240), (mousePos[0]-320) )+math.pi/2, 15, 1.5)
            self.projectiles.append(newBolt)

    def changeTier(self):

        self.tier += 1
        if self.tier == 2:
            self.image = pygame.image.load("res/stonePlayer.png")

        

        


