from typing import Callable


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
