# main_menu.py

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QMovie, QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from engine.styles import MENU_STYLES
from engine.game_window import GameWindow


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        self.setFont(QFont("", 24, QFont.Bold))
        self.setStyleSheet("color: white;")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.setStyleSheet("color: #0095FF;")

    def leaveEvent(self, event):
        self.setStyleSheet("color: white;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class MainMenu(QMainWindow):
    def __init__(self, scenes, characters):
        super().__init__()
        self.setWindowTitle("1925 - Главное меню")
        self.setFixedSize(1920, 1080)
        self.setStyleSheet(MENU_STYLES)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
        self.background_path = os.path.join(ASSETS_DIR, "backgrounds", "main_menu_bg.gif")
        self.game_background = os.path.join(ASSETS_DIR, "backgrounds", "hall.png")

        # Фон. анимация
        self.set_background_animation()

        # Музыкальный плеер (КАКИЕ ЕЩЁ ФОРМАТЫ)
        self.music_player = QMediaPlayer()
        self.current_music = None
        self.play_music(os.path.join(ASSETS_DIR, "music", "menu_theme.mp3"))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.add_labels()

        self.main_layout.addLayout(self.button_layout)

        self.game_window = GameWindow(self.game_background, scenes, characters)

    def set_background_animation(self):
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)
        self.movie = QMovie(self.background_path)
        self.movie.setScaledSize(self.size())
        self.background.setMovie(self.movie)
        self.movie.start()

    def add_labels(self):
        labels = [("НАЧАТЬ", self.start_game), ("ЗАГРУЗИТЬ", self.load_game), ("НАСТРОЙКИ", self.show_settings)]
        for text, callback in labels:
            label = ClickableLabel(text, self)
            label.clicked.connect(callback)
            self.button_layout.addWidget(label)

    def play_music(self, music_path):
        if not os.path.exists(music_path):
            print(f"Ошибка: Музыкальный файл не найден {music_path}")
            return
        if self.current_music != music_path:
            self.music_player.stop()
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
            self.music_player.setVolume(50)
            self.music_player.play()
            self.current_music = music_path
            self.music_player.stateChanged.connect(self.loop_music)

    def loop_music(self, state):
        if state == QMediaPlayer.StoppedState:
            self.music_player.play()

    def stop_music(self):
        if self.music_player.state() == QMediaPlayer.PlayingState:
            self.music_player.stop()
            self.music_player.setMedia(QMediaContent())
            print("Музыка главного меню остановлена.")

    def start_game(self):
        print("Запуск игры...")
        self.stop_music()
        self.hide()
        self.game_window.start_game()
        self.game_window.show()

    def load_game(self):
        print("Загрузка игры...")

    def show_settings(self):
        print("Открываем настройки...")
