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

#define game variables
rows = 5
cols = 5

# define colors for health bar
red = (255, 0, 0)
blue = (0, 0, 255)
alien_cooldown = 1000 # bullet cooldown in ms
last_alien_shot = pygame.time.get_ticks()

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
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #set movement speed
        speed = 8
        # set cooldown variable in miliseconds
        cooldown = 400

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
        # record current time
        time_now = pygame.time.get_ticks()

        # shooting bullets
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # create a mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw helath bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width,  10))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, blue, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width *(self.health_remaining / self.health_start)),  10))


bullet_size = 10
bullet_img = pygame.image.load('green_bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (bullet_size, bullet_size))



# bullet class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
            # check for collision
            # first arg is sprite to check on, second arg is sprite to watch for, 3rd arg is aotu kill option
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            print(explosion)
            explosion_group.add(explosion)


alien_size = 20
alien1_img = pygame.image.load('alien.png')
alien1_img = pygame.transform.scale(alien1_img, (alien_size, alien_size))

alien2_img = pygame.image.load('alien2.png')
alien2_img = pygame.transform.scale(alien2_img, (alien_size, alien_size))

aliens = [alien1_img, alien2_img]

# Alien class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = aliens[random.randint(0,1)]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


alien_bullet_size = 20
alien_bullet_img = pygame.image.load('alien_bullet.png')
alien_bullet_img = pygame.transform.scale(alien_bullet_img, (alien_bullet_size + 50, alien_bullet_size))

# bullet class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            #reduce spaceship health.
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)



# change powerup size
powerup_size = 20
powerup_img = pygame.image.load('powerup.png')
powerup_img = pygame.transform.scale(powerup_img, (powerup_size, powerup_size))

# poweruo  class
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = powerup_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.bottom > screen_height - 100:
            self.kill()
            self.rect.y = -10
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            if spaceship.health_remaining < 3:
                spaceship.health_remaining += 1
            self.kill( )


# create explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 4):
			img = pygame.image.load(f"exp{num}.jpeg")
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			#add the image to the list
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0


	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, delete explosion
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()





# create sprite group
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

powerup_group = pygame.sprite.Group()

def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

# create aliens
create_aliens()

def rand():
    return random.randint(10, screen_width)




# create player
ship_health = 3
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, ship_health)
spaceship_group.add(spaceship)

powerup = Powerup(200,10)
powerup_group.add(powerup)


#game loop
run = True
while run:
    # set tick spped to frams per second
    clock.tick(fps)
    # draw background
    draw_bg()

    # pick an alien to fire a bullet
    # record current time
    time_now = pygame.time.get_ticks()
    # shooting
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 8 and len(alien_group) > 0:
        attacking_alien = random.choice(alien_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        alien_bullet_group.add(alien_bullet)
        last_alien_shot = time_now

    if time_now % 70 == 0:
        powerup = Powerup(rand(), -10)
        powerup_group.add(powerup)


    # end game with esc button
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
         run = False

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update spaceship
    spaceship.update()

    # update sprite groups
    bullet_group.update()
    powerup_group.update()
    alien_group.update()
    alien_bullet_group.update()
    explosion_group.update()


    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    powerup_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update()



# ensure pygame closes.
pygame.quit()
print("end game")

# displaying the memory
print(TM.get_traced_memory())


# stopping the library
TM.stop()
