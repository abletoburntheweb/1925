from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap


class PauseMenu(QWidget):
    def __init__(self, parent=None, music_player=None):
        super().__init__(parent)
        self.setWindowTitle("Пауза")
        self.setFixedSize(1920, 1080)

        # Сохраняем ссылку на music_player
        self.music_player = music_player

        # **Фоновое изображение (анимированный GIF)**
        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/settings_menu.png")  # Загружаем изображение
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            self.background_label.setGeometry(0, 0, 1920, 1080)  # Смещаем вправо
        else:
            print("Ошибка загрузки фонового изображения settings_menu.png")

        # **Заглушка (градиентный PNG)**
        self.overlay_label = QLabel(self)
        pixmap = QPixmap("assets/png/main_menu.png")  # Загружаем изображение
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setScaledContents(True)  # Растягиваем картинку
        self.overlay_label.setGeometry(0, 0, 1920, 1080)

        # **Кнопки**
        button_x = 20
        button_y = 350

        resume_button = QPushButton("ПРОДОЛЖИТЬ", self)
        resume_button.setFont(QFont("Arial", 24))
        resume_button.setStyleSheet("background-color: transparent; color: white;")
        resume_button.clicked.connect(self.resume_game)
        resume_button.move(button_x, button_y)
        button_y += 60

        load_button = QPushButton("ЗАГРУЗИТЬ", self)
        load_button.setFont(QFont("Arial", 24))
        load_button.setStyleSheet("background-color: transparent; color: white;")
        load_button.clicked.connect(self.load_game)
        load_button.move(button_x, button_y)
        button_y += 60

        save_button = QPushButton("СОХРАНИТЬ", self)
        save_button.setFont(QFont("Arial", 24))
        save_button.setStyleSheet("background-color: transparent; color: white;")
        save_button.clicked.connect(self.save_game)
        save_button.move(button_x, button_y)
        button_y += 60

        exit_button = QPushButton("ВЫХОД", self)
        exit_button.setFont(QFont("Arial", 24))
        exit_button.setStyleSheet("background-color: transparent; color: white;")
        exit_button.clicked.connect(self.exit_game)  # Выход из игры
        exit_button.move(button_x, button_y)

    def create_button(self, text, callback):
        """Создает кнопку с заданным текстом и обработчиком."""
        button = QPushButton(text)
        button.setFixedSize(300, 60)
        button.setFont(QFont("Arial", 20))
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 200);
            }
            QPushButton:pressed {
                background-color: rgba(120, 120, 120, 200);
            }
        """)
        button.clicked.connect(callback)
        return button

    def resume_game(self):
        """Продолжает игру (закрывает меню паузы)."""
        self.hide()

    def load_game(self):
        """Загружает сохраненную игру."""
        print("Загрузка игры...")  # Здесь можно добавить логику загрузки

    def save_game(self):
        """Сохраняет текущую игру."""
        print("Сохранение игры...")  # Здесь можно добавить логику сохранения

    def exit_game(self):
        """Завершает игру."""
        print("Завершение игры...")
        self.parent().exit_game()  # Вызываем метод родителя для выхода из игры