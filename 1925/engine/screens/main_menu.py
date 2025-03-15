# engine/screens/main_menu.py

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from engine.screens.settings_menu import SettingsScreen  # Импорт окна настроек

class MainMenu(QWidget):
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine  # Ссылка на движок игры
        self.music_player = None  # Добавляем переменную для музыки
        self.settings_screen = None  # Переменная для окна настроек
        self.init_ui()
        self.play_music("menu_theme.mp3")  # Включаем музыку при загрузке меню

    def init_ui(self):
        # **Фоновое изображение (анимированный GIF)**
        self.background_label = QLabel(self)
        self.movie = QMovie("assets/backgrounds/windowgif.gif")  # Путь к GIF
        self.background_label.setMovie(self.movie)
        self.movie.start()  # Запускаем анимацию
        self.background_label.setAlignment(Qt.AlignCenter)

        # **Заглушка (градиентный PNG)**
        self.overlay_label = QLabel(self)
        pixmap = QPixmap("assets/png/main_menu.png")  # Загружаем изображение
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setScaledContents(True)  # Растягиваем картинку

        # **Обработка изменения размеров окна**
        self.resizeEvent = self.on_resize

        # **Создание кнопок**
        button_x = 20
        button_y = 350

        start_button = QPushButton("НАЧАТЬ", self)
        start_button.setFont(QFont("Arial", 24))
        start_button.setStyleSheet("background-color: transparent; color: white;")
        start_button.clicked.connect(self.start_new_game)
        start_button.move(button_x, button_y)
        button_y += 60

        load_button = QPushButton("ЗАГРУЗИТЬ", self)
        load_button.setFont(QFont("Arial", 24))
        load_button.setStyleSheet("background-color: transparent; color: white;")
        load_button.clicked.connect(self.load_game)
        load_button.move(button_x, button_y)
        button_y += 60

        settings_button = QPushButton("НАСТРОЙКИ", self)
        settings_button.setFont(QFont("Arial", 24))
        settings_button.setStyleSheet("background-color: transparent; color: white;")
        settings_button.clicked.connect(self.open_settings)
        settings_button.move(button_x, button_y)
        button_y += 60

        exit_button = QPushButton("ВЫХОД", self)
        exit_button.setFont(QFont("Arial", 24))
        exit_button.setStyleSheet("background-color: transparent; color: white;")
        exit_button.clicked.connect(self.game_engine.exit_game)
        exit_button.move(button_x, button_y)

    def play_music(self, file_name):
        """Воспроизводит музыку в главном меню."""
        if self.music_player is None:
            self.music_player = QMediaPlayer()

        url = QUrl.fromLocalFile(f"assets/music/{file_name}")
        print(f"Загружаю музыку: {file_name}")  # Отладочное сообщение
        self.music_player.setMedia(QMediaContent(url))
        self.music_player.play()
        print("Музыка главного меню воспроизводится.")  # Отладка

    def on_resize(self, event):
        """При изменении размеров окна подгоняем фон и заглушку."""
        self.background_label.resize(event.size())  # Растягиваем фон
        self.overlay_label.resize(event.size())  # Растягиваем заглушку
        super().resizeEvent(event)

    def start_new_game(self):
        """Запускает новую игру и останавливает музыку главного меню."""
        if self.music_player is not None:  # Проверяем, что плеер существует
            self.music_player.stop()  # Останавливаем воспроизведение музыки
            print("Музыка главного меню остановлена.")  # Отладочное сообщение
        self.game_engine.start_script("scripts.chapter1:start")  # Запускаем сценарий

    def load_game(self):
        print("We in the rolling armour")

    def open_settings(self):
        """Открывает окно настроек"""
        if not self.settings_screen:
            self.settings_screen = SettingsScreen(self, self.music_player)  # Передаем music_player
        self.settings_screen.show()

