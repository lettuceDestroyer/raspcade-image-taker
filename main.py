import datetime
import os
import sys
from typing import Any
import cv2
import numpy
import pygame
import pygame_gui as gui

pygame.init()
pygame.display.set_caption("image_taker")

# Constants
HEIGHT = 1000
WIDTH = 800
DISPLAY = pygame.display.set_mode([WIDTH, HEIGHT])
UI_MANAGER = gui.UIManager((WIDTH, HEIGHT))
CAMERA = cv2.VideoCapture(0)
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Variables
should_save_images = False
image: cv2.Mat | numpy.ndarray[Any, numpy.dtype]
label: str

# todo: write cleaner code. Preferably using a class that sets these vales on init or start btn press
label = "label"
image = CAMERA.read()[1]
IMAGE_HEIGHT, IMAGE_WIDTH, _ = image.shape

# GUI Elements
file_dialog: None | gui.windows.UIFileDialog

label_name_lbl = gui.elements.UILabel(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2, IMAGE_HEIGHT + 20, -1, -1), "Label")
label_name_input = gui.elements.UITextEntryLine(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2 + 50, IMAGE_HEIGHT + 20, 100, -1))
img_folder_lbl = gui.elements.UILabel(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2, IMAGE_HEIGHT + 50, -1, -1), "Folder")
img_folder_path_input = gui.elements.UITextEntryLine(
    pygame.Rect((WIDTH - IMAGE_WIDTH) / 2 + 50, IMAGE_HEIGHT + 50, 400, -1))
select_folder_btn = gui.elements.UIButton(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2 + 450, IMAGE_HEIGHT + 50, 100, 20),
                                          'Select folder')
start_btn = gui.elements.UIButton(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2, HEIGHT - 60, 100, 50), 'Start',
                                  UI_MANAGER)
stop_btn = gui.elements.UIButton(pygame.Rect((WIDTH - IMAGE_WIDTH) / 2 + 110, HEIGHT - 60, 100, 50), 'Stop',
                                 UI_MANAGER)

BACKGROUND.fill(pygame.Color("gray20"))


def main():
    global image
    global should_save_images

    image_folder_path = ""
    stop_btn.disable()

    while True:
        time_delta = CLOCK.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CAMERA.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

            if event.type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    should_save_images = True
                    start_btn.disable()
                    stop_btn.enable()
                elif event.ui_element == stop_btn:
                    should_save_images = False
                    stop_btn.disable()
                    start_btn.enable()
                if event.ui_element == select_folder_btn:
                    gui.windows.UIFileDialog(
                        pygame.Rect(50, 50, HEIGHT - 100, WIDTH - 100),
                        UI_MANAGER, allow_picking_directories=True)
            if event.type == gui.UI_FILE_DIALOG_PATH_PICKED:
                try:
                    image_folder_path = str(os.path.join(event.text, "image-taker", label_name_input.text))
                    img_folder_path_input.set_text(image_folder_path)
                except Exception as e:
                    print(e)

            UI_MANAGER.process_events(event)

        UI_MANAGER.update(time_delta)

        image = CAMERA.read()[1]
        thickness = 2
        image_height, image_width, _ = image.shape

        number_of_horizontal_spaces = 5
        number_of_vertical_spaces = 0

        if not image_folder_path == "" and not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        if should_save_images and not image_folder_path == "":
            now = str(datetime.datetime.now())
            now = now.replace(" ", "_")
            now = now.replace("-", "_")
            now = now.replace(":", "_")
            now = now.replace(".", "_")
            filename = str(os.path.join(image_folder_path, f"{now}.png"))
            cv2.imwrite(filename, image)

        for i in range(1, number_of_horizontal_spaces):
            image = cv2.line(image, (0, round(image_height / number_of_horizontal_spaces * i)),
                             (image_width, round(image_height / number_of_horizontal_spaces * i)),
                             pygame.Color("blue"),
                             thickness)

        for i in range(1, number_of_vertical_spaces):
            image = cv2.line(image, (round(image_width / number_of_vertical_spaces * i), 0),
                             (round(image_width / number_of_vertical_spaces * i), image_height),
                             pygame.Color("blue"),
                             thickness)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image_as_surface = pygame.surfarray.make_surface(image)
        DISPLAY.blit(BACKGROUND, (0, 0))
        DISPLAY.blit(image_as_surface, ((WIDTH - IMAGE_WIDTH) / 2, 10))
        UI_MANAGER.draw_ui(DISPLAY)

        pygame.display.update()


if __name__ == '__main__':
    main()
