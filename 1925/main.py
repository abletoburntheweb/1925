import sys
from PyQt5.QtWidgets import QApplication
from engine.main_menu import MainMenu
from script import start_scene

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scenes, characters = start_scene()
    menu = MainMenu(scenes=scenes, characters=characters)
    menu.show()

    sys.exit(app.exec_())