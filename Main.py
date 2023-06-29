# add comments 
# make main menu
# make save system
# make escape menu (escape opens if hotbar.active is False)
# add slide in animation for HUD
# add controls area:
# 1,2,3,4 to build when hotbar active, escape to remove hotbar
# control to set collect destination, shift to set deliver destination
# add green area to show which tiles the guys can move to
# space to shoot, wasd, arrows to zoom

# add person in collector (Astar)
# add upgrade system for collector (more range + more collection areas + more people)
# add upgrade system to hub - levels up guy
# add health system for guy
# add green health bars
# add better pathing for zombies so they try to kill you (Astar)
# make so max level is determined by hub level
# add bounding box for zombies so they cant enter buildings



import pygame, sys, random, time
from src.perlin import Perlin
from src.camera import Camera
from src.world import World
from src.hud import Hotbar
from src.zombie import Zombie



pygame.init()

clock = pygame.time.Clock()


width, height = 120,120
posx, posy = width//2, height//2 #starting of camera (in list position)
zoom = 32

screen = pygame.display.set_mode((640, 480))
                    


cam = Camera(posx,posy,zoom)
world = World(width,height,cam)
hotbar = Hotbar(320 - (150/2), 480 - int(150 * 0.2775) - 16, world)
cam.hotbar = hotbar
pygame.mouse.set_pos((320,240))


zombies = []
count = 0

while True:

    dt = clock.tick()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            for row in world.buildings:
                for building in row:
                    if building != "" and building != "taken":
                        building.upgrade(world, cam)
                    if building == "taken":
                        world.hub.upgrade(world, cam)

    count += dt
    if count > 15 * 1000 and time.perf_counter() > 30:
        count = 0
        zombies.append(Zombie([0,0], world))
        for zombie in zombies:
            if zombie.alive == False:
                zombie.alive = True
                zombie.health = 10
                zombie.pos = [0, random.randint(0,60)]

            
    if pygame.mouse.get_pressed()[0] == 1:
        
        hotbar.active = True
        mousePos = pygame.mouse.get_pos()
        hotbar.selected = [
            int(((mousePos[0] - 320)/cam.zoom + cam.pos[0])//1),
            int(((mousePos[1] - 240)/cam.zoom + cam.pos[1])//1)]
        selectedBuilding = world.buildings[hotbar.selected[0]][hotbar.selected[1]]
        for row in world.buildings:
            for building in row:
                if building != "" and building != "taken":
                    building.selected = False
            if selectedBuilding != "" and selectedBuilding != "taken":
                selectedBuilding.selected = True
            elif selectedBuilding == "taken":
                world.hub.selected = True
            
        
    if pygame.key.get_pressed()[pygame.K_ESCAPE] and hotbar.active:

        hotbar.active = False

    hotbar.update(world)



    cam.update(dt, world, hotbar.selected)



    screen.fill((0,0,0))
    world.draw(cam,screen)

    for row in world.buildings:
        for building in row:
            if building != "" and building != "taken":
                building.action(dt, world, cam)
                building.render(cam, screen, world) # only render if in range !!CHANGE!!
    
    for item in world.items:
        if int(cam.pos[0] - cam.squarePerRow/2) < item.pos[0] < int(cam.pos[0] + cam.squarePerRow/2):
            if int(cam.pos[1] - cam.squarePerColumn/2) < item.pos[1] < int(cam.pos[1] + cam.squarePerColumn/2):

                px = (item.pos[0] - cam.pos[0]) * cam.zoom + 320
                py = (item.pos[1] - cam.pos[1]) * cam.zoom + 240
                
                scaleImage = pygame.transform.scale(item.image, (cam.zoom+1,cam.zoom+1))
                screen.blit(scaleImage, (px,py))


    

    world.drawBox(screen, cam)
    
    for item in zombies:
            item.move(dt)
            item.render(screen,cam) # only render if in range !!CHANGE!!
            
    hotbar.display(screen, cam, world)
    for item in cam.projectiles:
        item.move(cam, screen, zombies)
    cam.render(screen)
    #world.renderFog(screen, cam)

    pygame.display.update()
