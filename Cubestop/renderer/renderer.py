import pygame

from typing import Protocol


class IRenderer(Protocol):

    @property
    def y_position(self) -> float:
        raise NotImplementedError()

    def on_render(self, surface: pygame.Surface) -> None:
        raise NotImplementedError()
