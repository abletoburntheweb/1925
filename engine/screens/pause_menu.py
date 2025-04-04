from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from engine.screens.settings_menu import SettingsScreen
from PyQt5.QtGui import QFont, QPixmap


class PauseMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Пауза")
        self.setFixedSize(1920, 1080)

        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/settings_menu.png")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1920, 1080)

        self.overlay_label = QLabel(self)
        pixmap = QPixmap("assets/png/main_menu.png")
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setScaledContents(True)
        self.overlay_label.setGeometry(0, 0, 1920, 1080)

        button_x = 20
        button_y = 350

        buttons_data = [
            ("ПРОДОЛЖИТЬ", self.resume_game),
            ("ЗАГРУЗИТЬ", self.load_game),
            ("СОХРАНИТЬ", self.save_game),
            ("НАСТРОЙКИ", self.settings),
            ("ГЛАВНОЕ МЕНЮ", self.exit_game),
        ]

        for text, callback in buttons_data:
            button = self.create_button(text, callback)
            button.move(button_x, button_y)
            button_y += 60

    def create_button(self, text, callback):

        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 24))
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
            }
        """)
        button.clicked.connect(callback)
        return button

    def resume_game(self):
        self.hide()

    def load_game(self):
        print("Загрузка игры...")

    def save_game(self):
        print("Сохранение игры...")

    def exit_game(self):
        self.parent().exit_game()

    def settings(self):
        self.parent().settings()