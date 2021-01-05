import pygame

from copy import copy
from typing import Callable, Protocol, List

WIDTH, HEIGHT = 900, 600


class Event:

    def __init__(self) -> None:
        self.__listeners = list()

    def add_listener(self, listener: Callable) -> None:
        if listener not in self.__listeners:
            self.__listeners.append(listener)

    def remove_listener(self, listener: Callable) -> None:
        if listener in self.__listeners:
            self.__listeners.pop(self.__listeners.index(listener))

    def invoke(self, *args) -> None:
        for listener in self.__listeners:
            listener(*args)


class EventDispather:

    def __init__(self, handle: pygame.event.Event) -> None:
        self.__handle = handle

    def dispatch(self, type: int, callback: Callable) -> None:
        if self.__check_type(type):
            callback(self.__handle)

    def dispatch_key(self, key: int, callback: Callable) -> None:
        if self.__check_type(pygame.KEYDOWN) and self.__handle.key == key:
            callback(self.__handle)

    def dispatch_mouse_button(self, button: int, callback: Callable) -> None:
        if self.__check_type(pygame.MOUSEBUTTONDOWN) and self.__handle.button == button:
            callback(self.__handle)

    def __check_type(self, type: int) -> bool:
        return self.__handle.type == type


class IRenderer(Protocol):

    @property
    def y_position(self) -> float:
        raise NotImplementedError()

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()


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
        dispather.dispatch_mouse_button(1, self.__shoot)

    def on_update(self, delta_time: float) -> None:
        direction = self.__get_direction()

        if direction.length() > 0:
            self.__previous_direction = direction
            direction = direction.normalize()

        self.__position += direction * self.__speed * delta_time

    def __shoot(self, event: pygame.event.Event) -> None:
        self.shooted.invoke(
            copy(self.__position), pygame.Vector2(event.pos),
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
            pygame.image.load("img/left.jpeg"),
            pygame.image.load("img/right.jpeg"),
            pygame.image.load("img/top.jpeg"),
            pygame.image.load("img/bottom.jpeg"),
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

    __sprite = pygame.image.load("img/weapon.png")

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


class Application:
    pass


class IScene(Protocol):

    def on_enable(self) -> None:
        raise NotImplementedError()

    def on_disable(self) -> None:
        raise NotImplementedError()

    def on_transition(self, context: Application) -> None:
        raise NotImplementedError()

    def on_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError()

    def on_update(self, delta_time: float) -> None:
        raise NotImplementedError()

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()


class GameScene(IScene):

    def __init__(self) -> None:
        self.__player = Player(pygame.Vector2(WIDTH / 2, HEIGHT / 2))
        self.__player_renderer = PlayerRenderer(self.__player)

        self.__bullets = list()
        self.__world_bounds = pygame.Rect(0, 0, WIDTH, HEIGHT)

    def on_enable(self) -> None:
        self.__player.shooted.add_listener(self.__on_shoot)

    def on_disable(self) -> None:
        self.__player.shooted.remove_listener(self.__on_shoot)

    def on_transition(self, context: Application) -> None:
        pass

    def on_event(self, event: pygame.event.Event) -> None:
        self.__player.on_event(event)

    def on_update(self, delta_time: float) -> None:
        self.__player.on_update(delta_time)

        for bullet in self.__bullets:
            bullet.on_update(delta_time)

            if self.__should_remove_bullet(bullet):
                self.__remove_bullet(bullet)

    def on_render(self, surface: pygame.Surface) -> None:
        render_buffer = self.__generate_render_buffer()

        for renderer in render_buffer:
            renderer.on_render(surface)

    def __remove_bullet(self, bullet) -> None:
        self.__bullets.pop(self.__bullets.index(bullet))

    def __should_remove_bullet(self, bullet: Bullet) -> bool:
        return not self.__world_bounds.collidepoint(bullet.position)

    def __generate_render_buffer(self) -> List[IRenderer]:
        render_buffer = list()
        render_buffer.append(self.__player_renderer)

        for bullet in self.__bullets:
            render_buffer.append(BulletRenderer(bullet))

        return sorted(render_buffer, key=lambda x: x.y_position)

    def __on_shoot(self, position: pygame.Vector2, direction: pygame.Vector2) -> None:
        self.__bullets.append(Bullet(position, direction))


class Application:

    def __init__(self) -> None:
        self.__running = True
        self.__title = "Cubestop"

        self.__max_frame_rate = 60
        self.__clock = pygame.time.Clock()

        self.__active_scene = GameScene()

        pygame.display.set_caption(self.__title)
        self.__window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__background = pygame.image.load("img/background.png")
        self.__background = pygame.transform.scale(self.__background, (WIDTH, HEIGHT))

    @property
    def active_scene(self) -> IScene:
        return self.__active_scene

    @active_scene.setter
    def active_scene(self, scene: IScene) -> None:
        self.__active_scene.on_disable()

        self.__active_scene = scene
        self.__active_scene.on_enable()

    def run(self) -> None:
        self.__begin_session()

        while self.__running:
            self.__clock.tick(self.__max_frame_rate)

            pygame.display.update()
            self.__window.blit(self.__background, (0, 0))

            for event in pygame.event.get():
                self.__on_event(event)

            self.__active_scene.on_transition(self)
            self.__active_scene.on_update(self.__clock.get_time() / 1000)
            self.__active_scene.on_render(self.__window)

        self.__end_session()

    def __begin_session(self) -> None:
        self.__active_scene.on_enable()

    def __end_session(self) -> None:
        self.__active_scene.on_disable()

    def __on_event(self, event: pygame.event.Event) -> None:
        dispather = EventDispather(event)
        dispather.dispatch(pygame.QUIT, self.__on_shutdown)
        dispather.dispatch_key(pygame.K_ESCAPE, self.__on_shutdown)

        self.__active_scene.on_event(event)

    def __on_shutdown(self, event: pygame.event.Event) -> None:
        self.__running = False


app = Application()
app.run()
