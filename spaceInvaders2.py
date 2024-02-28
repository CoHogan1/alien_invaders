import pygame
import tracemalloc as TM
from pygame import mixer
from pygame.locals import*
import random

# start tracing memory usage
TM.start()

print('file running')

# define fps
clock = pygame.time.Clock()
fps = 60

# set up window
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# window title
pygame.display.set_caption('Test Space invaders')

# define colors for health bar
red = (255, 0, 0)
blue = (0, 0, 255)

#background image load
bg = pygame.image.load('star.png')
bg = pygame.transform.scale(bg, (screen_width, screen_height))

def draw_bg():
    screen.blit(bg, (0,0))

ship_size = 45
ship_img = pygame.image.load('ship2.png')
ship_img = pygame.transform.scale(ship_img, (ship_size, ship_size))


# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health

    def update(self):
        #set movement speed
        speed = 8

        #get any key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += speed

        # draw helath bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width,  10))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, blue, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width *(self.health_remaining / self.health_start)),  10))




# create sprite group
spaceship_group = pygame.sprite.Group()

# create player
ship_health = 3
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, ship_health)
spaceship_group.add(spaceship)



#game loop
run = True
while run:
    # set tick spped to frams per second
    clock.tick(fps)
    # draw background
    draw_bg()
    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update spaceship
    spaceship.update()


    #draw sprite groups
    spaceship_group.draw(screen)


    pygame.display.update()


# ensure pygame closes.
pygame.quit()
print("end game")

# displaying the memory
print(TM.get_traced_memory())


# stopping the library
TM.stop()
