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

    def enterEvent(self, event):
        self.setStyleSheet("color: #0095FF;")  # Изменяем цвет текста при наведении

    def leaveEvent(self, event):
        self.setStyleSheet("color: white;")  # Возвращаем исходный цвет текста

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class MainMenu(QMainWindow):
    def __init__(self, background_path, game_background, scenes, characters):
        super().__init__()
        self.setWindowTitle("1925 - Главное меню")
        self.setFixedSize(1920, 1080)
        self.setStyleSheet(MENU_STYLES)

        self.game_background = game_background
        self.scenes = scenes
        self.characters = characters

        # Фон меню с GIF-анимацией
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)

        self.movie = QMovie(background_path)
        self.movie.setScaledSize(self.size())
        self.background.setMovie(self.movie)
        self.movie.start()  # Запуск анимации

        # Музыкальный плеер
        self.music_player = QMediaPlayer()
        self.current_music = None

        self.play_music("../assets/music/menu_theme.mp3")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignTop)

        self.label_start = ClickableLabel("НАЧАТЬ", self)
        self.label_load = ClickableLabel("ЗАГРУЗИТЬ", self)
        self.label_settings = ClickableLabel("НАСТРОЙКИ", self)

        # Шрифт
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        for label in [self.label_start, self.label_load, self.label_settings]:
            label.setFont(font)
            label.setStyleSheet("color: white;")
            label.setCursor(QCursor(Qt.PointingHandCursor))
            self.button_layout.addWidget(label)

        self.main_layout.addLayout(self.button_layout)

        self.label_start.clicked.connect(self.start_game)
        self.label_load.clicked.connect(self.load_game)
        self.label_settings.clicked.connect(self.show_settings)

        self.game_window = GameWindow(self.game_background, self.scenes, self.characters)

    def play_music(self, music_path):
        abs_music_path = os.path.join(os.path.dirname(__file__), music_path)
        if not os.path.exists(abs_music_path):
            print(f"Ошибка: Музыкальный файл не найден {abs_music_path}")
            return

        if self.current_music != abs_music_path:
            self.music_player.stop()
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(abs_music_path)))
            self.music_player.setVolume(50)
            self.music_player.play()
            self.current_music = abs_music_path

            # Перезапуск после окончания
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
        """Запуск игры"""
        print("Запуск игры...")
        self.stop_music()
        self.hide()
        self.game_window.start_game()
        self.game_window.show()

    def load_game(self):
        print("Загрузка игры...")

    def show_settings(self):
        print("Открываем настройки...")
