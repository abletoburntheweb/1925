from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import json
from engine.screens.settings_menu import SettingsScreen  # Окно настроек
from engine.screens.case_screen import CaseScreen  # Экран досье

class MainMenu(QWidget):
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine  # Ссылка на движок игры
        self.music_player = QMediaPlayer()  # Музыкальный плеер
        self.settings_screen = None  # Окно настроек
        self.init_ui()
        self.load_settings()  # Загружаем настройки перед воспроизведением музыки
        self.play_music("menu_theme.mp3")

    def init_ui(self):
        # **Фон (GIF)**
        self.background_label = QLabel(self)
        self.movie = QMovie("assets/backgrounds/windowgif.gif")
        self.background_label.setMovie(self.movie)
        self.movie.start()
        self.background_label.setAlignment(Qt.AlignCenter)

        # **Заглушка (PNG)**
        self.overlay_label = QLabel(self)
        pixmap = QPixmap("assets/png/main_menu.png")
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setScaledContents(True)

        # **Обрабатываем изменение размеров окна**
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

        dossier_button = QPushButton("ДОСЬЕ", self)
        dossier_button.setFont(QFont("Arial", 24))
        dossier_button.setStyleSheet("background-color: transparent; color: white;")
        dossier_button.clicked.connect(self.open_case_screen)
        dossier_button.move(button_x, button_y)
        button_y += 60

        exit_button = QPushButton("ВЫХОД", self)
        exit_button.setFont(QFont("Arial", 24))
        exit_button.setStyleSheet("background-color: transparent; color: white;")
        exit_button.clicked.connect(self.game_engine.exit_game)
        exit_button.move(button_x, button_y)

    def load_settings(self):
        """Загружает настройки из settings.json и применяет их."""
        try:
            with open("engine/settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {"music_volume": 50, "fullscreen": False}

        # Устанавливаем громкость музыки
        self.music_player.setVolume(settings.get("music_volume", 50))

        # Применяем полноэкранный режим
        if settings.get("fullscreen", False):
            self.game_engine.showFullScreen()
        else:
            self.game_engine.showNormal()

    def play_music(self, file_name):
        """Воспроизводит музыку в главном меню."""
        url = QUrl.fromLocalFile(f"assets/music/{file_name}")
        print(f"Загружаю музыку: {file_name}")
        self.music_player.setMedia(QMediaContent(url))
        self.music_player.play()
        print("Музыка главного меню воспроизводится.")

    def on_resize(self, event):
        """Обрабатываем изменение размеров окна."""
        if hasattr(self, "background_label") and self.background_label:
            self.background_label.resize(event.size())
            self.overlay_label.resize(event.size())
        super().resizeEvent(event)

    def start_new_game(self):
        """Запускает новую игру и останавливает музыку главного меню."""
        self.music_player.stop()
        print("Музыка главного меню остановлена.")
        self.game_engine.start_script("scripts.intro:start")

    def load_game(self):
        print("Загрузка игры...")

    def open_settings(self):
        """Открывает окно настроек поверх основного меню."""
        if not self.settings_screen:
            self.settings_screen = SettingsScreen(self, self.music_player)
            self.settings_screen.setParent(self)
            self.settings_screen.setGeometry(420, 0, 1500, 1080)

        self.settings_screen.raise_()
        self.settings_screen.show()

    def open_case_screen(self):
        """Открывает экран досье."""
        case_screen = CaseScreen(self.game_engine)
        self.game_engine.addWidget(case_screen)
        self.game_engine.setCurrentWidget(case_screen)
