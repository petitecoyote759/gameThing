# all in list
# loop through list to .move
# find path when spawn
# all respawn if dead every 30 seconds, with 1 extra zombie added to list
import math, pygame

class Zombie:

    def __init__(self, pos, world):

        self.health = 10
        self.pos = [0,0]
        self.image = world.enemies["zombie"]
        self.speed = 0.002
        self.alive = True

    def move(self, dt):

        if self.health <= 0:
            self.alive = False
            self.pos = [0,0]
        ratio = self.speed/(((self.pos[1]-60)**2 + (self.pos[0]-60)**2)**0.5)
        self.pos[0] += dt * ratio * (60 - self.pos[0])
        self.pos[1] += dt * ratio * (60 - self.pos[1])

    def render(self, screen, cam):

        if self.alive:

            image = pygame.transform.scale(self.image, (cam.zoom+1, cam.zoom+1))
            image = pygame.transform.rotate(image, (180 - (math.atan2(self.pos[0]-320, self.pos[1]-240))))
            px, py = cam.findPos(self.pos[0], self.pos[1])
            screen.blit(image, (px,py))
