import pygame

from typing import Callable


class WindowViewport:

    def __init__(self, resolution: pygame.Vector2) -> None:
        self.__scale_factor = 1.0
        self.__resolution = resolution
        # NOTE: На этой поверхности будет рисоваться
        # вообще всё. А потом она увеличивается и рисуется на окне.
        self.__surface = pygame.Surface(resolution)

    @property
    def scale_factor(self) -> float:
        return self.__scale_factor

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def view_surface(self) -> pygame.Surface:
        # NOTE: Тут как раз и изменяется размер
        # поверхности, причем поверхность увеличивается в scale_factor раз.
        scaled_resolution = self.__resolution * self.__scale_factor

        return pygame.transform.scale(
            self.__surface, (int(scaled_resolution.x), int(scaled_resolution.y))
        )

    def on_resize(self, event: pygame.event.Event) -> None:
        factor_x = event.w / self.__resolution.x
        factor_y = event.h / self.__resolution.y
        # NOTE: Перещитывается scale_factor, чтобы
        # поверхность, которая будет показываться увеличивалась в
        # корректное количество раз. И это как раз минимум от отношения нового
        # размера окна и фиксированного, по горизонтали и вертикали.
        self.__scale_factor = min(factor_x, factor_y)


class Window:

    def __init__(self, title: str, resolution: pygame.Vector2) -> None:
        pygame.display.set_caption(title)

        self.__title = title
        self.__resolution = resolution
        self.__viewport = WindowViewport(resolution)

        self.__native_window = pygame.display.set_mode(
            (int(self.__resolution.x), int(self.__resolution.y)), pygame.RESIZABLE)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        pygame.display.set_caption(value)
        self.__title = value

    @property
    def scale_factor(self) -> float:
        return self.__viewport.scale_factor

    @property
    def view_surface_blend(self) -> pygame.Vector2:
        return pygame.Vector2(self.__native_window.get_rect().center) \
             - pygame.Vector2(self.__viewport.view_surface.get_rect().center)

    @property
    def render_context(self) -> pygame.Surface:
        return self.__viewport.surface

    def on_resize(self, event: pygame.event.Event) -> None:
        self.__viewport.on_resize(event)

        self.__resolution = pygame.Vector2(event.w, event.h)
        self.__native_window = pygame.display.set_mode(
            (int(self.__resolution.x), int(self.__resolution.y)), pygame.RESIZABLE)

    def update(self, event_callback: Callable) -> None:
        pygame.display.update()

        # NOTE: Тут вот обрабатывается очередь событий
        # и эти события отправляются в event_callback, где после они будет обрабатываться.
        for event in pygame.event.get():
            event_callback(event)

    def prepare(self, color: pygame.Color) -> None:
        # NOTE: Тут подготавливаются поверхности к слудующему кадру,
        # потому что если этого не делать, то все, что было на предыдущем кадре
        # попадет и на этот, а это плохо.
        self.__viewport.surface.fill(color)
        self.__native_window.fill(pygame.Color(0, 0, 0))

    def render(self) -> None:
        # NOTE: Здесь увеличенная поверхность рисуется на поверхности окна.
        self.__native_window.blit(self.__viewport.view_surface, self.view_surface_blend)


class WindowToolkit:

    def __init__(self, handle: Window) -> None:
        self.__handle = handle

    @property
    def handle(self) -> Window:
        return self.__handle

    @property
    def normolized_mouse_position(self) -> pygame.Vector2:
        scaled_mouse_position = pygame.Vector2(pygame.mouse.get_pos()) \
            * self.__handle.scale_factor

        return scaled_mouse_position - self.__handle.view_surface_blend
