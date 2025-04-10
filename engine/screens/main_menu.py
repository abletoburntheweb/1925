from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QMovie, QPixmap
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import json
from engine.screens.settings_menu import SettingsScreen
from engine.screens.case_screen import CaseScreen

class MainMenu(QWidget):
    def __init__(self, game_engine):
        super().__init__()

        self.game_engine = game_engine
        self.music_player = QMediaPlayer()
        self.load_settings()
        self.settings_screen = None
        self.init_ui()
        self.play_music("main_menu.mp3")

    def init_ui(self):
        self.background_label = QLabel(self)
        self.movie = QMovie("assets/backgrounds/windowgif.gif")
        self.background_label.setMovie(self.movie)
        self.movie.start()
        self.background_label.setAlignment(Qt.AlignCenter)

        self.overlay_label = QLabel(self)
        pixmap = QPixmap("assets/png/main_menu.png")
        self.overlay_label.setPixmap(pixmap)
        self.overlay_label.setScaledContents(True)

        self.resizeEvent = self.on_resize

        button_x = 20
        button_y = 350
        buttons_data = [
            ("НАЧАТЬ", self.start_new_game),
            ("ЗАГРУЗИТЬ", self.load_game),
            ("НАСТРОЙКИ", self.open_settings),
            ("ДОСЬЕ", self.open_case_screen),
            ("ВЫХОД", self.game_engine.exit_game),
        ]

        for text, callback in buttons_data:
            button = self.create_button(text, button_x, button_y, callback)
            button_y += 60

        version_label = QLabel(f"Версия: 0.6", self)
        version_label.setFont(QFont("Arial", 18))
        version_label.setStyleSheet("""
                    color: rgba(200, 200, 200, 200);
                """)
        version_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.version_label = version_label

    def create_button(self, text, x, y, callback):
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 24))
        button.setStyleSheet("background-color: transparent; color: white;")
        button.clicked.connect(callback)
        button.move(x, y)
        return button

    def load_settings(self):
        try:
            with open("engine/settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {"music_volume": 50, "fullscreen": False}

        self.music_player.setVolume(settings.get("music_volume", 50))

        if settings.get("fullscreen", False):
            self.game_engine.showFullScreen()
        else:
            self.game_engine.showNormal()
            self.game_engine.move(0, 0)

    def play_music(self, file_name):
        url = QUrl.fromLocalFile(f"assets/music/{file_name}")
        print(f"Загружаю музыку: {file_name}")
        self.music_player.setMedia(QMediaContent(url))
        self.music_player.play()
        print("Музыка главного меню воспроизводится.")

    def on_resize(self, event):
        if hasattr(self, "background_label") and self.background_label:
            self.background_label.resize(event.size())
            self.overlay_label.resize(event.size())

            self.position_version_label()
        super().resizeEvent(event)

    def position_version_label(self):
        margin = 10
        x = self.width() - self.version_label.fontMetrics().boundingRect(
            self.version_label.text()).width() - margin
        y = self.height() - self.version_label.fontMetrics().height() - margin
        self.version_label.setGeometry(x, y,
                                       self.version_label.fontMetrics().boundingRect(
                                           self.version_label.text()).width(),
                                       self.version_label.fontMetrics().height())

    def start_new_game(self):
        self.music_player.stop()
        if self.settings_screen:
            self.settings_screen.hide()
        print("Музыка главного меню остановлена.")
        self.game_engine.start_script("scripts.intro:start")

    def load_game(self):
        print("Загрузка игры...")

    def open_settings(self):
        if not self.settings_screen:
            self.settings_screen = SettingsScreen(self, self.music_player)
            self.settings_screen.setParent(self)
            self.settings_screen.setGeometry(420, 0, 1500, 1080)

        self.settings_screen.raise_()
        self.settings_screen.show()

    def open_case_screen(self):
        case_screen = CaseScreen(self.game_engine)
        self.game_engine.addWidget(case_screen)
        self.game_engine.setCurrentWidget(case_screen)

    def showEvent(self, event):
        super().showEvent(event)
        if self.music_player.state() != QMediaPlayer.PlayingState:
            self.play_music("main_menu.mp3")

        QTimer.singleShot(100, self.position_version_label)