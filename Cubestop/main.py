import pygame

from typing import Protocol, Callable, List

from core.layer import Layer
from core.application import Application
from core.window import WindowToolkit
from core.event_dispather import EventDispather

from renderer.renderer import IRenderer

from gameplay.player import Player, PlayerRenderer
from gameplay.bullet import Bullet, BulletRenderer


class IScene(Protocol):

    def on_enable(self) -> None:
        raise NotImplementedError()

    def on_disable(self) -> None:
        raise NotImplementedError()

    def on_transition(self, context: Layer) -> None:
        raise NotImplementedError()

    def on_event(self, event: pygame.event.Event) -> None:
        raise NotImplementedError()

    def on_update(self, delta_time: float) -> None:
        raise NotImplementedError()

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()


class GameScene(IScene):

    def __init__(self) -> None:
        self.__player = Player(pygame.Vector2(450, 300))
        self.__player_renderer = PlayerRenderer(self.__player)

        self.__bullets = list()
        self.__world_bounds = pygame.Rect(0, 0, 900, 600)

    def on_enable(self) -> None:
        self.__player.shooted.add_listener(self.__on_shoot)

    def on_disable(self) -> None:
        self.__player.shooted.remove_listener(self.__on_shoot)

    def on_transition(self, context: Layer) -> None:
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


class MainLayer(Layer):

    def on_attach(self) -> None:
        self.__active_scene = GameScene()
        self.__active_scene.on_enable()

    def on_detach(self) -> None:
        self.__active_scene.on_disable()

    def on_update(self, dt: float) -> None:
        self.__active_scene.on_transition(self)
        self.__active_scene.on_update(dt)

    def on_render(self, toolkit: WindowToolkit) -> None:
        self.__active_scene.on_render(toolkit.handle.render_context)

    def on_event(self, event: pygame.event.Event) -> None:
        self.__active_scene.on_event(event)


app = Application()
app.add_layer(MainLayer())
app.run()
