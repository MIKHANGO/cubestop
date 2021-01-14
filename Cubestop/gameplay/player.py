import pygame

from copy import copy

from core.event import Event
from core.event_dispather import EventDispather
from renderer.renderer import IRenderer


class Player:

    def __init__(self, position: pygame.Vector2) -> None:
        self.__shooted = Event()

        self.__speed = 400.0
        self.__position = position
        self.__previous_direction = pygame.Vector2(0, 1)

    @property
    def shooted(self) -> Event:
        return self.__shooted

    @property
    def position(self) -> pygame.Vector2:
        return self.__position

    @property
    def direction(self) -> pygame.Vector2:
        return self.__previous_direction

    def on_event(self, event: pygame.event.Event) -> None:
        dispather = EventDispather(event)
        dispather.dispatch_mouse_button_down(1, self.__shoot)

    def on_update(self, delta_time: float) -> None:
        direction = self.__get_direction()

        if direction.length() > 0:
            self.__previous_direction = direction
            direction = direction.normalize()

        self.__position += direction * self.__speed * delta_time

    def __shoot(self, event: pygame.event.Event) -> None:
        mouse_position = pygame.Vector2(event.pos)

        if mouse_position != self.__position:
            self.shooted.invoke(
                copy(self.__position), mouse_position,
            )

    def __get_direction(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()

        return pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w],
        )


class PlayerRenderer(IRenderer):

    def __init__(self, handle: Player) -> None:
        self.__handle = handle

        self.__frames = [
            pygame.image.load("assets/player/left.jpeg"),
            pygame.image.load("assets/player/right.jpeg"),
            pygame.image.load("assets/player/top.jpeg"),
            pygame.image.load("assets/player/bottom.jpeg"),
        ]

    @property
    def y_position(self) -> float:
        return self.__handle.position.y

    def on_render(self, surface: pygame.Surface) -> None:
        frame = self.__get_frame(self.__handle.direction)
        position = self.__handle.position

        surface.blit(frame, position - pygame.Vector2(frame.get_size()) / 2)

    def __normolize_axis(self, axis: int) -> int:
        return int(bool(axis + 1))

    def __get_frame_index(self, direction: pygame.Vector2) -> int:
        if abs(direction.x) > 0:
            return self.__normolize_axis(direction.x)

        if abs(direction.y) > 0:
            return self.__normolize_axis(direction.y) + 2

    def __get_frame(self, direction: pygame.Vector2) -> pygame.Surface:
        return self.__frames[
            self.__get_frame_index(direction)
        ]
