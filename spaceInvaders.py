import pygame
#import tracemalloc as TM
from pygame import mixer
from pygame.locals import*
import random

pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

print('file running')

# define fps
clock = pygame.time.Clock()
fps = 60

# set up window
screen_width = 600
screen_height = 800


#starting bullet count
bullet_count = 1

#define game variables
rows = int(screen_width / 101)
cols = int(screen_height / 200 + 1)

# define colors for health bar
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

alien_cooldown = 1000 # bullet cooldown in ms


screen = pygame.display.set_mode((screen_width, screen_height))

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# window title
pygame.display.set_caption('Space invaders')

# load sounds
explosion_fx = pygame.mixer.Sound("invaderkilled.wav")
explosion_fx.set_volume(0.25)

shoot_fx = pygame.mixer.Sound("shoot.wav")
shoot_fx.set_volume(0.25)

alien_exp_fx = pygame.mixer.Sound('invaderkilled.wav')
alien_exp_fx.set_volume(0.25)

last_alien_shot = pygame.time.get_ticks()

# start window
countdown = 3
last_count = pygame.time.get_ticks()

game_over = 0 # 0 no game over, 1 means playwe win, -1 player looses

#background image load
bg = pygame.image.load('star.png')
bg = pygame.transform.scale(bg, (screen_width, screen_height))

def draw_bg():
    screen.blit(bg, (0,0))

# adding text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

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
        self.bullet_count = bullet_count

    def update(self):
        #set movement speed
        speed = 8
        # set cooldown variable in miliseconds
        cooldown = 400
        game_over = 0

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
            shoot_fx.play()
            # shot miltiple bullets
            for x in range(self.bullet_count):
                bullet = Bullets(self.rect.centerx + x * 20, self.rect.top)
                bullet_group.add(bullet)
            self.last_shot = time_now

        # create a mask
        self.mask = pygame.mask.from_surface(self.image)

        # draw helath bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width,  10))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, blue, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width *(self.health_remaining / self.health_start)),  10))
        elif self.health_remaining <= 0:
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over



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
            alien_exp_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
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
        self.move_counter += 1 * lvl
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


alien_bullet_size = 30
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
        self.rect.y += lvl + 1
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            #reduce spaceship health.
            spaceship.health_remaining -= 1
            explosion_fx.play()
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
            if spaceship.bullet_count < 5:
                spaceship.bullet_count += 1
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
ship_health = 5
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, ship_health)
spaceship_group.add(spaceship)

powerup = Powerup(200,10)
powerup_group.add(powerup)


def clear_sprites():
    for w in alien_bullet_group:
        w.kill()
    for x in alien_group:
        x.kill()
    for y in bullet_group:
        y.kill()
    for z in powerup_group:
        z.kill()


def update_score(num):
    score = str(num)
    first = 8 - len(score)
    return '0' * first + score

def update_lvl(num):
    if num == 99:
        return str(99)
    if num <= 9:
        return f'0{num}'
    return str(num)


# **********************************************************************game loop
score = 0
lvl = 1
run = True
while run:
    # set tick spped to frams per second
    clock.tick(fps)
    # draw background
    draw_bg()

    draw_text(f'{update_score(score)}', font40, white, screen_width - 170, 15)
    draw_text(f'{update_lvl(lvl)}', font40, white, 20, 15)

    if countdown == 0:
        # pick an alien to fire a bullet
        # record current time
        time_now = pygame.time.get_ticks()
        # shooting
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 8 and len(alien_group) > 0 and game_over == 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            shoot_fx.play()
            last_alien_shot = time_now

        # check if all aliens are dead
        if len(alien_group) <= 0:
            game_over = 1

        if time_now % 70 == 0:
            powerup = Powerup(rand(), -10)
            powerup_group.add(powerup)

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()
            len_alien_group = len(alien_group)

            # update sprite groups
            bullet_group.update()
            powerup_group.update()
            alien_group.update()
            if len_alien_group > len(alien_group):
                score += 3
            alien_bullet_group.update()
        else:
            if game_over == -1:
                    draw_text('Game Over! :(', font40, white, int(screen_width)/ 2 - 110, int(screen_height) / 2 + 50)
                    draw_text('Press any key', font40, white, int(screen_width)/ 2 - 110, int(screen_height) - 100)
                    draw_text('to play again', font40, white, int(screen_width)/ 2 - 110, int(screen_height) - 50)
                    # press s to start game again

            if game_over == 1:
                    draw_text('You Win! :)', font40, white, int(screen_width)/ 2 - 110, int(screen_height) / + 50)
                    draw_text('Press any key', font40, white, int(screen_width)/ 2 - 110, int(screen_height) - 100)
                    draw_text('to play again', font40, white, int(screen_width)/ 2 - 110, int(screen_height) - 50)
                    # press s to start game again

    if countdown > 0:
        draw_text('Get Ready', font40, white, int(screen_width)/ 2 - 110, int(screen_height) / 2 + 50)
        draw_text(str(countdown), font40, white, int(screen_width)/ 2 - 10, int(screen_height) / 2 + 100)
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    powerup_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    # keep animaiton independent
    explosion_group.update()

    key = pygame.key.get_pressed()
    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False
        elif event.type == pygame.KEYDOWN and game_over != 0:
            lvl +=1
            clear_sprites()
            create_aliens()
            spaceship.health_remaining = 3
            game_over = 0
            countdown = 3
            spaceship.kill()
            spaceship_group.add(spaceship)

    pygame.display.update()


# ensure pygame closes.
pygame.quit()
print("end game")
