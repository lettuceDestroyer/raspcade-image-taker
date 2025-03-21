import datetime
import os
import sys
import pygame
import pygame.camera
import pygame_gui as gui

pygame.init()
pygame.camera.init()
pygame.display.set_caption("image_taker")

# Constants
HEIGHT = 1000
WIDTH = 800
DISPLAY = pygame.display.set_mode([WIDTH, HEIGHT])
UI_MANAGER = gui.UIManager((WIDTH, HEIGHT))
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Variables
should_save_images = False
label: str

# todo: write cleaner code. Preferably using a class that sets these vales on init or start btn press
label = "label"
IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640

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

    camera_list = pygame.camera.list_cameras()
    if not camera_list:
        raise ValueError("Sorry, no cameras detected.")
    camera = pygame.camera.Camera(camera_list[0])
    camera.start()

    while True:
        time_delta = CLOCK.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.camera.quit()
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

        image = camera.get_image()
        image_height = image.get_height()
        image_width = image.get_width()

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
            pygame.image.save(image, filename)

        for i in range(1, number_of_horizontal_spaces):
            pygame.draw.line(image, pygame.Color("red"), (0, round(image_height / number_of_horizontal_spaces * i)),
                             (image_width, round(image_height / number_of_horizontal_spaces * i)))

        for i in range(1, number_of_vertical_spaces):
            pygame.draw.line(image, pygame.Color("red"), (round(image_width / number_of_vertical_spaces * i), 0),
                             (round(image_width / number_of_vertical_spaces * i), image_height))

        DISPLAY.blit(BACKGROUND, (0, 0))
        DISPLAY.blit(image, ((WIDTH - IMAGE_WIDTH) / 2, 10))
        UI_MANAGER.draw_ui(DISPLAY)

        pygame.display.update()


if __name__ == '__main__':
    main()
