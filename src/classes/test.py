import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from classes.Container import Container
from classes.Padding import Padding

pygame.init()

WIDTH = 800
HEIGHT = 620

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('gray20'))

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

clock = pygame.time.Clock()
is_running = True


def iterate_through_gui_elements(container: Container):
    for child in container.child:
        if isinstance(child, Container):
            width = child.relative_rect.width
            height = child.relative_rect.height

            if 0.1 >= width >= 1:
                width = container.relative_rect.width / 10 * width

            if 0.1 >= height >= 1:
                height = container.relative_rect.height / 10 * height

            top = container.relative_rect.top + container.padding.top + child.relative_rect.top
            left = container.relative_rect.left + container.padding.left + child.relative_rect.left
            child.relative_rect = pygame.Rect(left, top, width, height)

            iterate_through_gui_elements(child)
        elif isinstance(child, pygame_gui.core.UIElement):
            top = container.relative_rect.top + container.padding.top + child.relative_rect.top
            left = container.relative_rect.left + container.padding.left + child.relative_rect.left
            child.set_position((top, left))


def create_gui():
    gui = Container(
        pygame.Rect(0, 0, WIDTH, HEIGHT),
        Padding(0, 0, 0, 0),
        [
            Container(
                pygame.Rect(0, 0, 1, 1),
                None,
                [
                    UIButton(pygame.Rect(0, 0, 50, 50), "press!", manager)
                ]
            ),
            Container(
                pygame.Rect(0, 0, 1, 1),
                Padding(10, 10, 10, 10),
                [
                    UIButton(pygame.Rect(0, 0, 50, 50), "press!", manager)
                ]
            )
        ]
    )

    iterate_through_gui_elements(gui)

create_gui()
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
