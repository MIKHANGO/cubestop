import pygame

from typing import List, Callable

from core.window import WindowToolkit


class Layer:

    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        pass

    def on_update(self, dt: float) -> None:
        pass

    def on_render(self, toolkit: WindowToolkit) -> None:
        pass

    def on_event(self, event: pygame.event.Event) -> None:
        pass


class LayerStack:

    def __init__(self) -> None:
        self.__layers = list()
        self.__core_layers = list()

    @property
    def layers(self) -> List[Layer]:
        return [*self.__core_layers, *self.__layers]

    def add_layer(self, layer: Layer) -> None:
        layer.on_attach()
        self.__layers.append(layer)

    def add_core_layer(self, layer: Layer) -> None:
        layer.on_attach()
        self.__core_layers.append(layer)

    def on_update(self, dt: float) -> None:
        self.__for_all_layers(lambda layer: layer.on_update(dt))

    def on_render(self, toolkit: WindowToolkit) -> None:
        self.__for_all_layers(lambda layer: layer.on_render(toolkit))

    def on_event(self, event: pygame.event.Event) -> None:
        self.__for_all_layers(lambda layer: layer.on_event(event))

    def detach_all_layers(self) -> None:
        self.__for_all_layers(lambda layer: layer.on_detach())

    def __for_all_layers(self, key: Callable) -> None:
        for layer in self.layers:
            key(layer)
