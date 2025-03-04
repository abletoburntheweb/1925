import sys
import os
from PyQt5.QtWidgets import QApplication
from engine.main_menu import MainMenu
from script import start_scene

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
background_main_menu = os.path.join(ASSETS_DIR, "backgrounds", "main_menu_bg.gif")
background_game = os.path.join(ASSETS_DIR, "backgrounds", "hall.png")

if not os.path.exists(background_main_menu):
    print(f"Ошибка: Файл {background_main_menu} не найден.")
    sys.exit(1)

if not os.path.exists(background_game):
    print(f"Ошибка: Файл {background_game} не найден.")
    sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Инициализация сценария
    scenes, characters = start_scene()

    # Передаем пути в главное меню
    menu = MainMenu(background_path=background_main_menu, game_background=background_game, scenes=scenes, characters=characters)
    menu.show()

    sys.exit(app.exec_())