import pygame
from classes.Padding import Padding


class Container:
    height: int
    width: int
    child: None | list[object]

    def __init__(self, relative_rect: pygame.Rect, padding: None | Padding = None,
                 child: None | list[object] = None):
        """
        :param relative_rect: Normally a rectangle describing the position (relative to its container) and dimensions.
        Also accepts a position Coordinate where the dimensions will be in proportion to its container. Dynamic
        dimensions can be requested by setting the required dimension between 0.1 and 1, where 1 will be 100% and
        0.1 will be 10% of the available space.
        :param padding: Padding: the padding of the container
        :param child: the child of the container
        """
        super().__init__()
        self.relative_rect = relative_rect
        self.padding = Padding(0, 0, 0, 0) if padding is None else padding
        self.child = child