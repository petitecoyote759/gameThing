import pygame, math, time

class Javalin:

    def __init__(self, image, startPos, startTime, cam, angle, damage, duration):

        self.image = image
        self.angle = angle
        self.startTime = startTime
        self.image = pygame.transform.rotate(self.image, angle*180/math.pi)
        self.speed = 0.2
        self.pos = [startPos[0]-1, startPos[1]-1]
        self.damage = damage
        self.duration = duration

    def move(self, cam, screen, zombies):

        for zombie in zombies:
            if zombie.pos[0] - 0.5 < self.pos[0] < zombie.pos[0] + 0.5:
                if zombie.pos[1] - 1 < self.pos[1] < zombie.pos[1]:
                    zombie.health -= self.damage
                    try:
                        cam.projectiles.remove(self)
                    except:
                        pass    
            

        if time.perf_counter() - self.startTime > self.duration:

            try:
                cam.projectiles.remove(self)
            except:
                pass


        else:

            self.pos[0] += self.speed * math.sin(self.angle)
            self.pos[1] += self.speed * math.cos(self.angle)
            self.render(cam, screen)


    def render(self, cam, screen):

        px, py = cam.findPos(self.pos[0], self.pos[1])
        image = pygame.transform.scale(self.image, (2*(cam.zoom+1),2*(cam.zoom+1)))
        image = pygame.transform.rotate(image, 180)
        screen.blit(image, (px,py))

        
