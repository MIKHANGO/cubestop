import pygame

from typing import Callable


class EventDispather:

    def __init__(self, handle: pygame.event.Event) -> None:
        self.__handle = handle

    def dispatch(self, type: int, callback: Callable) -> None:
        if self.__check_type(type):
            callback(self.__handle)

    def dispatch_mouse_button_up(self, button: int, callback: Callable) -> None:
        if self.__check_type(pygame.MOUSEBUTTONUP) and self.__handle.button == button:
            callback(self.__handle)

    def dispatch_mouse_button_down(self, button: int, callback: Callable) -> None:
        if self.__check_type(pygame.MOUSEBUTTONDOWN) and self.__handle.button == button:
            callback(self.__handle)

    def dispatch_key_up(self, key: int, callback: Callable) -> None:
        if self.__check_type(pygame.KEYUP) and self.__handle.key == key:
            callback(self.__handle)

    def dispatch_key_down(self, key: int, callback: Callable) -> None:
        if self.__check_type(pygame.KEYDOWN) and self.__handle.key == key:
            callback(self.__handle)

    def __check_type(self, type: int) -> bool:
        return self.__handle.type == type
