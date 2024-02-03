import pygame
import time

pygame.init()

win_width = 1920
win_height = 1080
FPS = 120
tank_shot = pygame.mixer.Sound('Sound/tank_shot.mp3')
boom_tank = pygame.mixer.Sound('Sound/Boom_tank.mp3')
boom_block = pygame.mixer.Sound('Sound/Boom_Block.mp3')
victory = pygame.mixer.Sound('Sound/victory.mp3')
sound_menu = pygame.mixer.Sound('Sound/Sound_Menu.mp3')
Music_menu = pygame.mixer.Sound('Sound/Sound-Fon.mp3')

menu_fon = pygame.transform.scale(pygame.image.load("Game_Texture/Fon_menu.jpg"),(win_width, win_height))

game = False
menu = True
Menu = True
bullets = []

back = pygame.transform.scale(pygame.image.load("Game_Texture/sand.jpg"), (win_width, win_height))
win = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

world = ['']
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.startimage = self.image
        # self.rect = pygame.Rect(x, y, width, height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    # Клас GameSprite
    # Добавляє хітбокс і тестуру гравця

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, sound_path=None):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft =(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound("Sound/Sound_Menu.mp3")

        self.is_hovered = False

    def draw(self, win):
        current_image = self.image
        win.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        global menu, game
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button =self))
            menu = False
            game = True




class Player1(GameSprite):
    def __init__(self, image, x, y, width, height, speed, direction):
        self.direction = direction
        super().__init__(image, x, y, width, height, speed)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank2.rect):
                self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.startimage, 90)
            self.direction = 90
        elif keys[pygame.K_d] and self.rect.x < 1920:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank2.rect):
                self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.startimage, 270)
            self.direction = 270
        elif keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank2.rect):
                self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.startimage, 0)
            self.direction = 0
        elif keys[pygame.K_s] and self.rect.y < 1080:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank2.rect):
                self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.startimage, 180)
            self.direction = 180
        if keys[pygame.K_e] and len(bullets) < 1:
            self.fire()
            tank_shot.play()

    def fire(self):
        bullet1 = Bullet("Game_Texture/Bullet.png", self.rect.x, self.rect.y, 30, 30, 100, self.direction, self)
        bullets.append(bullet1)



class Player2(GameSprite):
    def __init__(self, image, x, y, width, height, speed, direction):
        self.direction = direction
        super().__init__(image, x, y, width, height, speed)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank1.rect):
                self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.startimage, 90)
            self.direction = 90
        elif keys[pygame.K_RIGHT] and self.rect.x < 1920:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank1.rect):
                self.rect.x -= self.speed
            self.image = pygame.transform.rotate(self.startimage, 270)
            self.direction = 270
        elif keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank1.rect):
                self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.startimage, 0)
            self.direction = 0
        elif keys[pygame.K_DOWN] and self.rect.y < 1080:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, blocks, False) or self.rect.colliderect(tank1.rect):
                self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.startimage, 180)
            self.direction = 180
        if keys[pygame.K_RCTRL] and len(bullets) < 1:
            self.fire()
            tank_shot.play()

    def fire(self):
        bullet1 = Bullet("Game_Texture/Bullet.png", self.rect.x, self.rect.y, 30, 30, 5, self.direction, self)
        bullets.append(bullet1)
class Bullet(GameSprite):
    def __init__(self, image, x, y, width, height, speed, direction, tank):
        super().__init__(image, x, y, width, height, speed)
        self.direction = direction
        self.speed = 10
        self.tank = tank
        # self.image = pygame.image.load(image)

    def fly(self):
        if self.rect.x < win_width and self.rect.y < win_height:
            if self.direction == 0:
                self.rect.y -= self.speed
            elif self.direction == 90:
                self.rect.x -= self.speed
            elif self.direction == 180:
                self.rect.y += self.speed
            elif self.direction == 270:
                self.rect.x += self.speed
            if self.rect.x >= win_width or self.rect.y >= win_height or self.rect.y <= 1 or self.rect.x <= 1:
                bullets.remove(bullet)
                boom_block.play()
            if pygame.sprite.spritecollide(self, blocks, False) and len(bullets) > 0:
                bullets.remove(bullet)
                boom_block.play()


# bullet1 = Bullet("Game_Texture/FireBall.png", 0, 0, 30, 30, 5, 0)
tank1 = Player1("Game_Texture/Tank2.png", 800, 840, 55, 55, 3, 0)
tank2 = Player2("Game_Texture/Tank.png", 800, 160, 55, 55, 3, 0)
Greenw = GameSprite("Game_Texture/Greenw.png", 0, 0, win_width, win_height, 0)
Greyw = GameSprite("Game_Texture/Greyw.png", 0, 0, win_width, win_height, 0)
Menu_fon = GameSprite("Game_Texture/Fon_menu.jpg", 0, 0, win_width, win_height, 0)
Button = Button(win_width/2 - (512/2), win_height/2 - (512/2), 512, 512, "Game_Texture/play.png", "Sound/Sound_Menu.mp3")
blocks = pygame.sprite.Group()
for i in range(30):
    block = GameSprite("Game_Texture/block.png" , 60 * i, 100, 60, 60, 0)
    blocks.add(block)
for i in range(3):
    block = GameSprite("Game_Texture/block.png" , 600 * i, 160, 60, 60, 0)
    blocks.add(block)
for i in range(3):
    block = GameSprite("Game_Texture/block.png" , 600 * i, 860, 60, 60, 0)
    blocks.add(block)
for i in range(30):
    block = GameSprite("Game_Texture/block.png" , 60 * i, 920, 60, 60, 0)
    blocks.add(block)
for i in range(16):
    block = GameSprite("Game_Texture/block.png" , 190, i * 60, 60, 60, 0)
    blocks.add(block)
for i in range(16):
    block = GameSprite("Game_Texture/block.png" , 60*28, i * 60, 60, 60, 0)
    blocks.add(block)
for i in range(3):
    block = GameSprite("Game_Texture/block.png", 250, i * 340, 60, 60, 0)
    blocks.add(block)
for i in range(3):
    block = GameSprite("Game_Texture/block.png", 1620, i * 340, 60, 60, 0)
    blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 340, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 400, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 460, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 520, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 580, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 640, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 430, 680, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 340, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 400, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 460, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 520, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 580, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 640, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1440, 680, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 600, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 660, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 720, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 780, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 840, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 900, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 960, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1020, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1080, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1140, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1200, 280, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 600, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 660, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 720, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 780, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 840, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 900, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 960, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1020, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1080, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1140, 735, 60, 60, 0)
blocks.add(block)
block = GameSprite("Game_Texture/block.png", 1200, 735, 60, 60, 0)
blocks.add(block)

menu = True
game = False
finish = False
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        Button.handle_event(event)
    if not finish:
        Music_menu.play()
        win.blit(menu_fon, (0, 0))
        Button.check_hover(pygame.mouse.get_pos())
        if Button.check_hover(pygame.mouse.get_pos()):
            game = True
            menu = False
        Button.draw(win)
        pygame.display.update()
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        menu = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    Music_menu.stop()
    if not finish:
        win.blit(back, (0, 0))
        tank1.update()
        tank1.draw()
        tank2.update()
        tank2.draw()
        print("Tank1", (tank1.rect.width,tank1.rect.height), (tank1.rect.x, tank1.rect.y))
        print("Tank2", (tank2.rect.width, tank2.rect.height), (tank2.rect.x, tank2.rect.y))
        blocks.draw(win)
        for bullet in bullets:
            if tank2.rect.colliderect(bullet.rect) and bullet.tank == tank1:
                bullets.remove(bullet)
                boom_tank.play()
                time.sleep(2)
                victory.play()
                Greenw.draw()
                finish = True
                break
            if tank1.rect.colliderect(bullet.rect) and bullet.tank == tank2:
                bullets.remove(bullet)
                boom_tank.play()
                time.sleep(2)
                victory.play()
                Greyw.draw()
                finish = True
                break
            bullet.fly()
            bullet.draw()


        pygame.display.update()
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        game = False