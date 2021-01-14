import pygame

from renderer.renderer import IRenderer


class Bullet:

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        self.__speed = 600.0
        self.__position = position
        self.__direction = (target - position).normalize()

    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    @property
    def direction(self) -> pygame.Vector2:
        return self.__direction

    def on_update(self, delta_time: float) -> None:
        self.__position += self.__direction * self.__speed * delta_time


class BulletRenderer(IRenderer):

    __sprite = pygame.image.load("assets/player/weapon.png")

    def __init__(self, handle: Bullet) -> None:
        self.__handle = handle

    @property
    def y_position(self) -> float:
        return self.__handle.position.y

    def on_render(self, surface: pygame.Surface) -> None:
        angle = self.__calculate_angle(self.__handle.direction)
        rotated_sprite = pygame.transform.rotate(self.__sprite, angle)

        surface.blit(
            rotated_sprite,
            self.__handle.position - pygame.Vector2(rotated_sprite.get_size()) / 2
        )

    def __calculate_angle(self, direction: pygame.Vector2) -> float:
        return direction.angle_to(pygame.Vector2(0, -1))
