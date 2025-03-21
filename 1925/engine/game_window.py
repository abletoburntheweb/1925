# game_window.py

from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QPainter, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from engine.styles import GAME_WINDOW_STYLES
from engine.functions import Scene, Dialogue,Menu
from engine.effects import Effect

class GameWindow(QMainWindow):
    def __init__(self, background_path, scenes, characters):
        super().__init__()
        self.setWindowTitle("1925 - Игровой процесс")
        self.setFixedSize(1920, 1080)
        self.setStyleSheet(GAME_WINDOW_STYLES)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Фон
        self.background = QLabel(self)
        pixmap = QPixmap(background_path)
        if not pixmap.isNull():
            self.background.setPixmap(pixmap.scaled(1920, 1080, Qt.KeepAspectRatioByExpanding))
            self.background.setGeometry(0, 0, 1920, 1080)
        else:
            print(f"Ошибка: Изображение {background_path} не найдено или повреждено.")

        self.text_frame = CustomTextFrame(self, height=480)
        self.text_frame.update_geometry()

        self.character_label = QLabel("", self.text_frame)
        self.character_label.setFont(QFont("Arial", 26, QFont.Bold))
        self.character_label.setAlignment(Qt.AlignLeft)
        self.character_label.setStyleSheet("color: white; padding-left: 10px;")
        self.character_label.hide()

        self.text_label = QLabel("", self.text_frame)
        self.text_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("color: white; padding: 10px;")

        text_layout = QVBoxLayout(self.text_frame)
        text_layout.addWidget(self.character_label)
        text_layout.addWidget(self.text_label)
        text_layout.addStretch(1)

        self.scenes = scenes
        self.characters = characters
        self.current_scene_index = -1
        self.waiting_for_input = False

        self.music_player = QMediaPlayer()
        self.current_music = None


        #ВОТ ТУТ
        self.effect_manager = Effect(self)

        self.choice_buttons = []  # Список кнопок выбора

        self.text_frame.mousePressEvent = self.next_scene_on_click
        self.keyPressEvent = self.next_scene_on_key_press

    def start_game(self):
        """Запускает игру и включает музыку для первой сцены"""
        self.stop_music()
        if self.scenes:
            first_scene = self.scenes[0]
            if isinstance(first_scene, Scene) and first_scene.music:
                music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "music",
                                          first_scene.music)
                self.play_music(music_path)
        self.show_next_scene()

    def show_next_scene(self):
        if self.waiting_for_input:
            return

        self.current_scene_index += 1
        if self.current_scene_index < len(self.scenes):
            scene = self.scenes[self.current_scene_index]

            if isinstance(scene, Dialogue):
                character = scene.character
                text = scene.text

                if character.name:
                    self.character_label.setText(character.name)
                    self.character_label.setStyleSheet(f"color: {character.color}; padding-left: 10px;")
                    self.character_label.show()
                else:
                    self.character_label.hide()

                self.display_text(text)

            elif isinstance(scene, Scene):
                new_background_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                                                   "backgrounds", f"{scene.name}.png")
                self.change_background(new_background_path)
                self.text_label.setText("")
                self.character_label.hide()

                if scene.music:
                    music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "music",
                                              scene.music)
                    self.play_music(music_path)

            elif isinstance(scene, Menu):
                self.show_menu(scene)  # Показываем меню

        else:
            print("Конец сценария")

    def show_menu(self, menu):
        """Показывает меню с вариантами выбора."""
        self.text_label.setText(menu.prompt)

        for button in self.choice_buttons:
            button.deleteLater()
        self.choice_buttons.clear()

        choice_widget = QWidget(self)
        choice_layout = QVBoxLayout(choice_widget)
        choice_layout.setSpacing(10)
        choice_layout.setAlignment(Qt.AlignCenter)
        choice_widget.setGeometry(0, 400, 1920, 300)
        choice_widget.setStyleSheet("background-color: transparent;")

        for choice in menu.choices:
            button = QPushButton(choice.text, self)
            button.setFont(QFont("Arial", 16))
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 200);  
                    color: white;                          
                    border: none;                         
                    margin: 5px;
                    width: 800px;                          
                    height: 30px;                          
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 150);
                }
            """)
            button.setCheckable(False)
            button.clicked.connect(lambda _, r=choice.result: self.handle_choice(r))
            choice_layout.addWidget(button)
            self.choice_buttons.append(button)

        choice_widget.show()

    def handle_choice(self, result):
        """Обрабатывает выбор игрока."""
        if callable(result):  # Если результат — функция
            result()
        elif isinstance(result, list):  # Если результат — список сцен
            self.scenes = result  # Заменяем текущий сценарий на выбранный
            self.current_scene_index = -1  # Начинаем с начала нового сценария
            self.show_next_scene()
        else:
            print("Ошибка: Неизвестный тип результата выбора.")

    def display_text(self, full_text):
        self.full_text = full_text
        self.current_text = ""
        self.text_label.setText("")
        self.text_timer = QTimer(self)
        self.text_timer.timeout.connect(self.update_text)
        self.text_timer.start(40)
        self.waiting_for_input = True

    def update_text(self):
        """Обновление текста по буквам"""
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.text_label.setText(self.current_text)
        else:
            self.text_timer.stop()
            self.waiting_for_input = False

    def change_background(self, new_background_path):
        """Смена фона"""
        pixmap = QPixmap(new_background_path)
        if not pixmap.isNull():
            self.background.setPixmap(pixmap.scaled(1920, 1080, Qt.KeepAspectRatioByExpanding))
        else:
            print(f"Ошибка: Изображение {new_background_path} не найдено.")

    def next_scene_on_click(self, event):
        if hasattr(self, 'text_timer') and self.text_timer.isActive():
            self.text_timer.stop()
            self.text_label.setText(self.full_text)
            self.waiting_for_input = False
        else:
            self.show_next_scene()

    def next_scene_on_key_press(self, event):
        if event.key() == Qt.Key_Space:
            if hasattr(self, 'text_timer') and self.text_timer.isActive():
                self.text_timer.stop()
                self.text_label.setText(self.full_text)
                self.waiting_for_input = False
            else:
                self.show_next_scene()

    def play_music(self, music_path):
        if not os.path.exists(music_path):
            print(f"Ошибка: Файл музыки не найден: {music_path}")
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
        self.music_player.stop()


class CustomTextFrame(QFrame):
    """Текстовая панель с градиентом"""
    def __init__(self, parent=None, height=480):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.height = height

    def set_height(self, height):
        self.height = height
        self.update_geometry()

    def update_geometry(self):
        """Фиксированное положение текста"""
        self.setGeometry(0, 700, 1920, self.height)

    def paintEvent(self, event):
        """Градиент"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height)
        gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
        gradient.setColorAt(0.2, QColor(0, 0, 0, 180))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 220))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())