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
    def __init__(self, color, wid, hei):
        pygame.sprite.Sprite.__init__(self) # наследование от Sprite
        self.image = pygame.Surface((50, 50)) # размер
        self.image.fill(color) # цвет
        self.rect = self.image.get_rect() # прямоугольник, который окружает объект
        self.rect.center = (wid, hei) # распологаем игрока по центру экрана

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
        # вправо
        if keystate[pygame.K_d]:
            self.speedx = speed
        # вверх
        if keystate[pygame.K_w]:
            self.speedy = -speed
        # вниз
        if keystate[pygame.K_s]:
            self.speedy = speed
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

# создаем игру и окно
pygame.init()
pygame.mixer.init() # звук
window = pygame.display.set_mode((width, height)) # окно
pygame.display.set_caption("Chess 0.0.1-alfa") # название окна
clock = pygame.time.Clock() # задержка между кадрами

player_blue = Player(blue, width / 2, height / 2) # создаём игрока
player_green = Player(green, width / 4, height / 2) # создаём игрока

# рисование игроков
sprites = pygame.sprite.Group()

# хранение игроков
entities = list()

# добавление игроков
def add_player(player):
    sprites.add(player)
    entities.append(player)

add_player(player_green)
add_player(player_blue)

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

    # обновление
    sprites.update()

    # рендеринг
    window.fill(black)
    sprites.draw(window)
    # переворот экрана
    pygame.display.flip()

pygame.quit()