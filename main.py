# импортируем библиотеки
import pygame
import random

width = 1000  # ширина игрового окна
height = 500 # высота игрового окна
fps = 60 # частота кадров в секунду
speed = 8 # скорость игрока

# Цвета (R, G, B)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# игрок
class Player(pygame.sprite.Sprite):

    # init
    def __init__(self, wid, hei, img, angel):
        pygame.sprite.Sprite.__init__(self) # наследование от Sprite
        self.image = img # размер
        self.angel = angel # поворот пули
        self.rect = self.image.get_rect() # прямоугольник, который окружает объект
        self.rect.center = (wid, hei) # распологаем игрока по центру экрана
        self.weapon_coordx = 0
        self.weapon_coordy = 0

    # update
    def update_speed(self):
        # задаём скорость
        self.speedx = 0
        self.speedy = 0
        # нажатие клавиш
        keystate = pygame.key.get_pressed()
        # влево
        if keystate[pygame.K_a]:
            self.speedx = -speed
            self.image = pygame.image.load("img/left.jpeg").convert()
            self.angel = 270
            self.weapon_coordx = 0
            self.weapon_coordy = -10

        # вправо
        if keystate[pygame.K_d]:
            self.speedx = speed
            self.image = pygame.image.load("img/right.jpeg").convert()
            self.angel = 0
            self.weapon_coordx = 0
            self.weapon_coordy = 10

        # вверх
        if keystate[pygame.K_w]:
            self.speedy = -speed
            self.image = pygame.image.load("img/top.jpeg").convert()
            self.angel = 90
            self.weapon_coordx = -10
            self.weapon_coordy = 0

        # вниз
        if keystate[pygame.K_s]:
            self.speedy = speed
            self.image = pygame.image.load("img/bottom.jpeg").convert()
            self.angel = 180
            self.weapon_coordx = 10
            self.weapon_coordy = 0

        # операции с координатами
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # ограничения
        # лево / право
        if self.rect.right < 0:
            self.rect.right = width
        if self.rect.left > width:
            self.rect.left = 0
        # верх / низ
        if self.rect.bottom < 0:
            self.rect.bottom = height
        if self.rect.top > height:
            self.rect.top = 0

    # shoot
    def shoot(self):
        # нажатие клавиш
        keystate = pygame.key.get_pressed()

        # стрельба пулями
        if keystate[pygame.K_e]:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.angel, weapon, self.weapon_coordx, self.weapon_coordy)
            sprites.add(bullet)
            bullets.add(bullet)

# bullets
class Bullet(Player, pygame.sprite.Sprite):
    def __init__(self, x, y, angel, weapon, weapon_coordx, weapon_coordy):
        pygame.sprite.Sprite.__init__(self)
        self.image = weapon
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = weapon_coordy
        self.speedx = weapon_coordx
        self.angel = angel

    def update(self):
        # для полёта
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

# создаем игру и окно
pygame.init()
pygame.mixer.init() # звук
window = pygame.display.set_mode((width, height)) # окно
pygame.display.set_caption("Chess 0.0.1-alfa") # название окна
clock = pygame.time.Clock() # задержка между кадрами

# рисование игроков
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# хранение игроков
entities = []

# добавление игроков
def add_player(player):
    sprites.add(player)
    entities.append(player)

# player_green = Player(green, width / 4, height / 2) # создаём игрока

# add_player(player_green) # добавляем его

player = Player(width / 2, height / 2, pygame.image.load("img/bottom.jpeg").convert(), 180) # создаём главного игрока
weapon = pygame.image.load("img/weapon.png").convert()
add_player(player) # добавляем главного игрока

# цикл игры
running = True
while running:
    # держим цикл на правильной скорости
    clock.tick(fps)
    # ввод процесса (события)
    for event in pygame.event.get():
        # проверка не закрыто ли окно с игрой
        if event.type == pygame.QUIT:
            running = False

    for entity in entities:
        entity.update_speed()
        entity.shoot()
        bullets.update()

    # обновление
    sprites.update()

    # рендеринг
    window.fill(black)
    sprites.draw(window)
    # переворот экрана
    pygame.display.flip()

pygame.quit()