import pygame

from core.layer import Layer
from core.layer import LayerStack

from core.event_dispather import EventDispather

from core.window import Window
from core.window import WindowToolkit


class Application:

    def __init__(self) -> None:
        self.__max_frame_rate = 60
        self.__background_color = pygame.Color(18, 18, 18)
        self.__running = True
        self.__title = "Cubestop"
        self.__resolution = pygame.Vector2(900, 600)

        self.__clock = pygame.time.Clock()

        self.__layer_stack = LayerStack()
        self.__window = Window(self.__title, self.__resolution)
        self.__window_toolkit = WindowToolkit(self.__window)

    def add_layer(self, layer: Layer) -> None:
        self.__layer_stack.add_layer(layer)

    def add_core_layer(self, layer: Layer) -> None:
        self.__layer_stack.add_core_layer(layer)

    def run(self) -> None:
        while self.__running:
            self.__clock.tick(self.__max_frame_rate)

            dt = self.__clock.get_time() / 1000

            self.__window.title = f"{self.__title}: {self.__clock.get_fps()}"
            self.__window.update(self.__on_event)
            self.__window.prepare(self.__background_color)

            self.__layer_stack.on_update(dt)
            self.__layer_stack.on_render(self.__window_toolkit)

            self.__window.render()

    def __on_event(self, event: pygame.event.Event) -> None:
        dispather = EventDispather(event)

        dispather.dispatch(pygame.QUIT, self.__on_shutdown)
        dispather.dispatch(pygame.VIDEORESIZE, self.__on_resize)
        dispather.dispatch_key_down(pygame.K_ESCAPE, self.__on_shutdown)

        self.__layer_stack.on_event(event)

    def __on_shutdown(self, event: pygame.event.Event) -> None:
        self.__running = False
        self.__layer_stack.detach_all_layers()

    def __on_resize(self, event: pygame.event.Event) -> None:
        self.__window.on_resize(event)
