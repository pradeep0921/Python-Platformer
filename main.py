import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

mixer.init()
pygame.init()

CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 20)

#color
white = (255, 255, 255)
blue = (150, 20, 255)

# images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
bg_img_scaled = pygame.transform.scale(bg_img, (800, 800))
dirt_img = pygame.image.load('img/dirt.png')
grass_img = pygame.image.load('img/grass.png')
grass1_img = pygame.image.load('img/grass (1).png')
grass2_img = pygame.image.load('img/grass (2).png')
grass3_img = pygame.image.load('img/grass (4).png')
restart_button = pygame.image.load('img/restart_btn.png')
start_button = pygame.image.load('img/start_btn.png')
exit_button = pygame.image.load('img/exit_btn.png')
join1_img = pygame.image.load('img/join1.png')
join2_img = pygame.image.load('img/join2.png')

#Sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)

jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)

game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)

#Game Variables
tile_size = 40
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))

def reset_level(level):
    player.reset(100, SCREEN_HEIGHT - 130)
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    #Load new level
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #Get Mouse I/P
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #Draw Button
        SCREEN.blit(self.image, self.rect)
        return action

class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            #Get Input
            key = pygame.key.get_pressed()

            #Jumpping
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                mixer.Sound.play(jump_fx)
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False

            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.index = 0
                self.counter = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #Player Animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #Gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #Collision
            self.in_air = True
            for tile in world.tile_list:
                #x_collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                #y_collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #Collision with Enemy
            if pygame.sprite.spritecollide(self, blob_group, False):
                mixer.Sound.play(game_over_fx)
                game_over = -1

            #Collision with Lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                mixer.Sound.play(game_over_fx)
                game_over = -1

            #Collision with exit gate
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #Collision with Platform
            for platform in platform_group:
                #x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                #y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #Below
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #Above
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0

                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction
                         

            #Update player position
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_img
            draw_text('GAME OVER', font, (255, 0, 55), (SCREEN_WIDTH // 2) - 170, SCREEN_HEIGHT // 2)
            
            if self.rect.y > 200:
                self.rect.y -= 5

        #Draw player
        SCREEN.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        
        for num in range(1, 5):
                img_right = pygame.image.load(f'img/guy{num}.png')
                img_right = pygame.transform.scale(img_right, (40, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_left.append(img_left)
                self.images_right.append(img_right)

        self.dead_img = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World:
    def __init__(self, data):
        self.tile_list = []

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 7)    
                    blob_group.add(blob)

                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)

                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)

                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)

                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)

                if tile == 9:
                    img = pygame.transform.scale(grass1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 10:
                    img = pygame.transform.scale(grass2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 11:
                    img = pygame.transform.scale(grass3_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 12:
                    img = pygame.transform.scale(join1_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == 13:
                    img = pygame.transform.scale(join2_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)


                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(100, SCREEN_HEIGHT - 130)
platform_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Score Coin
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#Load level data
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    world = World(world_data)

restart_btn = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, restart_button)
start_btn = Button(SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 2, start_button)
exit_btn = Button(SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 2, exit_button)

run = True
while run:
    SCREEN.blit(bg_img_scaled, (0, 0))
    SCREEN.blit(sun_img, (100, 80))

    if main_menu == True:
        if exit_btn.draw():
            run = False
        if start_btn.draw():
            main_menu = False
    else:
        world.draw()
        
        if game_over == 0:
            platform_group.update()
            blob_group.update()
            if pygame.sprite.spritecollide(player, coin_group, True):
                mixer.Sound.play(coin_fx)
                score += 1
            
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

        if game_over == 1:
            level += 1

            #Reset and load next level
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, blue, (SCREEN_WIDTH // 2 - 140), (SCREEN_HEIGHT // 2))
                if restart_btn.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

        if game_over == -1:
            if restart_btn.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
        
        platform_group.draw(SCREEN)
        blob_group.draw(SCREEN)
        lava_group.draw(SCREEN)
        coin_group.draw(SCREEN)
        exit_group.draw(SCREEN)

        game_over = player.update(game_over)
  
    #Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    CLOCK.tick(60)
    pygame.display.update()
