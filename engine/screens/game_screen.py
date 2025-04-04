from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QTextEdit, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from engine.effects import fade, dissolve, hpunch, slide_out_to_right
from engine.screens.dialog_history_screen import DialogHistoryScreen
from engine.screens.notebook import Notebook
from engine.screens.pause_menu import PauseMenu
import json

music_player = None


class GameScreen(QWidget):
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.settings_screen = None

        # Фон сцены
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.background_label)

        # Текстовый контейнер (для текста и textbox)
        self.text_container = QWidget(self)
        self.text_container.setFixedSize(1920, 1080)

        # Фон текстового блока (textbox.png)
        self.textbox_label = QLabel(self.text_container)
        self.textbox_label.setPixmap(QPixmap("assets/png/textbox2.png"))
        self.textbox_label.setAlignment(Qt.AlignBottom)
        self.textbox_label.adjustSize()

        # Контейнер для текста (располагается поверх textbox.png)
        self.text_layout = QVBoxLayout(self.text_container)
        self.text_layout.setAlignment(Qt.AlignTop)
        self.text_layout.setContentsMargins(470, 800, 500, 200)  # Отступы для центрирования
        self.text_container.setLayout(self.text_layout)

        # Добавляем контейнер текста в макет
        self.layout.addWidget(self.text_container)
        self.text_container.raise_()  # Поднимаем текстовой контейнер над textbox.png

        self.choice_container = None  # Контейнер для вариантов выбора
        self.choice_result = None  # Хранит выбранный результат
        self.choice_loop = None  # EventLoop для синхронного ожидания выбора
        self.character_labels = {}

        # Очередь реплик
        self.dialogues = []
        self.current_dialogue_index = 0
        self.characters = {}

        # Слой для отображения персонажей
        self.character_layer = QLabel(self)
        self.character_layer.setAlignment(Qt.AlignCenter)
        self.character_layer.setFixedSize(1920, 1080)
        self.layout.addWidget(self.character_layer)
        self.character_layer.lower()

        # Основные элементы (например, текст диалога)
        self.dialogue_label = QLabel(self)
        self.dialogue_label.setGeometry(200, 800, 1520, 200)
        self.dialogue_label.setStyleSheet("font-size: 32px; color: white;")

        # История диалогов (хранение)
        self.dialogue_history = []

        # Экран истории
        self.history_screen = DialogHistoryScreen(parent=self)
        self.layout.addWidget(self.history_screen)
        self.history_screen.hide()

        self.choice_container = QWidget(self)
        self.choice_layout = QVBoxLayout()
        self.choice_container.setLayout(self.choice_layout)
        self.choice_container.setFixedSize(1920, 1080)
        self.choice_container.hide()
        self.layout.addWidget(self.choice_container)


        self.pause_menu = PauseMenu(game_engine)
        self.layout.addWidget(self.pause_menu)
        self.pause_menu.hide()

        self.text_container.show()
        self.character_layer.show()

        self.notebook = Notebook(parent=self)

        self.notebook.setParent(self)
        self.notebook.raise_()
        self.notebook.tabs_container.setParent(self)
        self.notebook.close_notebook_button.setParent(self)

        self.notebook.raise_()
        self.notebook.tabs_container.raise_()
        self.notebook.close_notebook_button.raise_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_J:
            if not self.pause_menu.isVisible():
                print("Нажата клавиша J.")
                self.notebook.toggle_notebook()
                return
        elif event.key() == Qt.Key_Escape:
            print("Нажата клавиша ESC.")
            if self.notebook.is_notebook_active:
                self.notebook.toggle_notebook()
                return
            if self.settings_screen:
                self.settings_screen.hide()
            if self.pause_menu.isHidden():
                self.pause_menu.show()
                self.pause_menu.raise_()
            else:
                self.resume_game()
            return
        if self.pause_menu.isVisible() or self.notebook.is_notebook_active:
            return
        if event.key() == Qt.Key_Space:
            print("Нажата клавиша пробел.")
            if not self.history_screen.isVisible():
                self.show_next_dialogue()

    def resume_game(self):
        self.pause_menu.hide()
        self.text_container.show()
        self.character_layer.show()

    def say(self, character, text):
        self.dialogues.append((character, text))
        if len(self.dialogues) == 1:
            self.show_next_dialogue()

    def show_next_dialogue(self):
        if self.current_dialogue_index < len(self.dialogues):
            command = self.dialogues[self.current_dialogue_index]

            # Очищаем предыдущий текст
            while self.text_layout.count():
                widget = self.text_layout.takeAt(0).widget()
                if widget:
                    widget.deleteLater()

            # Локальный импорт для избежания циклической зависимости
            from engine.game_logic import Character

            # Обработка команд
            if isinstance(command, tuple) and len(command) > 0:
                command_type = command[0]
                if command_type == "__CHOICE__":
                    options = command[1]
                    print("Обнаружена команда выбора.")
                    self.a_show_choices(options)
                    self.current_dialogue_index += 1
                    return
                elif command_type == "__SCENE__":
                    scene_name, effect = command[1], command[2]
                    print(f"Меняем сцену на: {scene_name}")
                    self.a_show_scene(scene_name, effect)
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return
                elif command_type == "__SHOW__":
                    character_name, position = command[1], command[2]
                    print(f"Показываем персонажа: {character_name}")
                    self.a_show_character(character_name, position)
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return
                elif command_type == "__HIDE__":
                    character_name = command[1]
                    print(f"Скрываем персонажа: {character_name}")
                    if character_name in self.character_labels:
                        self.character_labels[character_name].hide()
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return
                elif command_type == "__CHAPTER__":
                    chapter_title, effect, next_script = command[1], command[2], command[3]
                    print(f"Показываю заголовок главы: {chapter_title}")
                    self.a_show_chapter(chapter_title, effect, next_script)
                    self.current_dialogue_index += 1
                    return
                else:
                    character, text = command
                    if isinstance(character, Character):  # Проверяем, что character — это объект Character
                        if character.name:  # Проверяем, что имя персонажа не None
                            name_label = QLabel(f"<font color='{character.color}'><b>{character.name}:</b></font>")
                            name_label.setStyleSheet(
                                "font-size: 36px;"
                                "font-family: 'Arial';"
                                "font-weight: bold;"
                                "padding-bottom: 5px;"
                            )
                            self.text_layout.addWidget(name_label)
                    text_label = QLabel(f"<font color='white'>{text}</font>")
                    text_label.setWordWrap(True)
                    text_label.setStyleSheet(
                        "font-size: 32px;"
                        "font-family: 'Arial';"
                        "line-height: 1.4;"
                        "font-weight: bold;"
                        "padding-left: 10px;"
                    )
                    self.text_layout.addWidget(text_label)
                    self.current_dialogue_index += 1
        else:
            print("Все реплики показаны.")
            if hasattr(self, "on_intro_end") and callable(self.on_intro_end):
                self.on_intro_end()

    def show_scene(self, scene_name, effect="none"):
        #print(f"Добавляю команду смены сцены: {scene_name} ({effect})")
        self.dialogues.append(("__SCENE__", scene_name, effect))
        if len(self.dialogues) == 1 and self.current_dialogue_index == 0:
            self.show_next_dialogue()

    def a_show_scene(self, scene_name, effect="none"):
        pixmap_path = f"assets/backgrounds/{scene_name}.png"
        #print(f"Загружаю фон: {pixmap_path}")
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            print(f"Ошибка загрузки изображения: {pixmap_path}")
            self.background_label.setStyleSheet("background-color: gray; color: white; font-size: 48px;")
            self.background_label.setText(f"Фон не найден:\n{scene_name}")
            self.background_label.setAlignment(Qt.AlignCenter)
            self.background_label.show()
            return
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setStyleSheet("")
        if effect == "fade":
            fade(self.background_label)
        elif effect == "dissolve":
            dissolve(self.background_label)
        elif effect == "hpunch":
            hpunch(self.background_label)
        elif effect == "slide_out_to_right":
            slide_out_to_right(self.background_label)
        self.update()

    def log_dialogue(self, character, text):
        self.dialogue_history.append((character, text))

    def mousePressEvent(self, event):
        if self.pause_menu.isVisible() or self.notebook.is_notebook_active:
            return
        if event.button() == Qt.LeftButton:
            print("Нажата левая кнопка мыши.")
            if not self.history_screen.isVisible():
                self.show_next_dialogue()
        elif event.button() == Qt.RightButton:
            print("Нажата правая кнопка мыши.")
            if self.history_screen.isVisible():
                self.history_screen.hide()
            else:
                filtered_dialogues = [
                    dialogue for dialogue in self.dialogues[:self.current_dialogue_index]
                    if not (isinstance(dialogue[0], str) and dialogue[0].startswith("__"))
                ]
                self.history_screen.show_history(filtered_dialogues)
                self.history_screen.raise_()

    def play_music(self, file_name, loop=False):
        global music_player
        if music_player is None:
            music_player = QMediaPlayer()
        url = QUrl.fromLocalFile(f"assets/music/{file_name}")
        #print(f"Загружаю музыку: {file_name}")
        music_player.setMedia(QMediaContent(url))
        if loop:
            music_player.mediaStatusChanged.connect(self._loop_music)
        print("Начинаем воспроизведение музыки.")

        try:
            with open("engine/settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
        except FileNotFoundError:
            settings = {"music_volume": 50, "fullscreen": False}

        music_player.setVolume(settings.get("music_volume", 50))
        music_player.play()

    def _loop_music(self, status):
        if status == QMediaPlayer.EndOfMedia and music_player:
            music_player.setPosition(0)
            music_player.play()

    def show_character(self, character_name, position="center"):
        #print(f"Добавляю команду показа персонажа: {character_name} ({position})")
        self.dialogues.append(("__SHOW__", character_name, position))
        if len(self.dialogues) == 1:
            self.show_next_dialogue()

    def a_show_character(self, character_name, position="center"):
        pixmap_path = f"assets/characters/{character_name}.png"
        print(f"Загружаю персонажа: {pixmap_path}")
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            print(f"Ошибка загрузки изображения персонажа: {pixmap_path}")
            return
        if character_name in self.character_labels:
            character_label = self.character_labels[character_name]
        else:
            character_label = QLabel(self)
            self.character_labels[character_name] = character_label
        character_label.setPixmap(pixmap.scaledToHeight(800, Qt.SmoothTransformation))
        character_label.setFixedSize(800, 1080)
        character_label.setScaledContents(True)

        positions = {"left": 100, "right": 1200, "center": 600}
        character_label.move(positions.get(position, 600), 200)
        character_label.show()

        character_label.raise_()
        self.background_label.lower()
        self.text_container.raise_()

    def hide_character(self, character_name):

        print(f"Добавляю команду скрытия персонажа: {character_name}")
        self.dialogues.append(("__HIDE__", character_name))
        if len(self.dialogues) == 1:
            self.show_next_dialogue()

    def clear_characters(self):
        for character in self.characters.values():
            character.hide()

    def show_chapter(self, chapter_title, effect="fade", next_script=None):
        print(f"Добавляю команду отображения заголовка главы: {chapter_title}")
        self.dialogues.append(("__CHAPTER__", chapter_title, effect, next_script))
        if len(self.dialogues) == 1 and self.current_dialogue_index == 0:
            self.show_next_dialogue()

    def a_show_chapter(self, chapter_title, effect="fade", next_script=None):
        print(f"Показываю заголовок главы: {chapter_title}")

        # Создаем QLabel для заголовка
        chapter_label = QLabel(chapter_title, self)
        chapter_label.setAlignment(Qt.AlignCenter)
        chapter_label.setStyleSheet("""
            font-size: 64px;
            font-family: 'Arial';
            font-weight: bold;
            color: white;
            background-color: rgba(0, 0, 0, 150);
            padding: 20px;
            border-radius: 10px;
        """)
        chapter_label.setFixedSize(800, 200)
        chapter_label.move((self.width() - 800) // 2, (self.height() - 200) // 2)
        chapter_label.show()

        # Анимация (если выбран эффект fade)
        if effect == "fade":
            fade(chapter_label)

        # Удаляем заголовок после завершения анимации
        QTimer.singleShot(2000, lambda: chapter_label.deleteLater())

        # Переход к следующему скрипту
        if next_script:
            QTimer.singleShot(2000, lambda: self.game_engine.start_script(next_script))


    def show_choices(self, options):
        #print(f"Добавляю команду отображения выборов.")
        self.dialogues.append(("__CHOICE__", options))

        # Если это первая команда в очереди, запускаем обработку
        if len(self.dialogues) == 1 and self.current_dialogue_index == 0:
            self.show_next_dialogue()

    def a_show_choices(self, options):
        print("Отображаю варианты...")

        # Очищаем предыдущие выборы
        if hasattr(self, "choice_container") and self.choice_container:
            self.choice_container.deleteLater()

        # Создаём контейнер для выборов
        self.choice_container = QWidget(self)
        self.choice_container.setFixedSize(800, len(options) * 80 + 120)
        self.choice_container.move((self.width() - 800) // 2, (self.height() - (len(options) * 80 + 120)) // 2)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        for text, value in options:
            button = QPushButton(text)
            button.setFixedSize(600, 60)
            button.setFont(QFont("Arial", 24))
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
            button.clicked.connect(lambda _, v=value: self.handle_choice(v))
            layout.addWidget(button)

        self.choice_container.setLayout(layout)
        self.choice_container.show()

    def handle_choice(self, choice_id):
        print(f"Выбран вариант: {choice_id}")
        self.choice_result = choice_id
        self.clear_choices()

    def clear_choices(self):
        if hasattr(self, "choice_container") and self.choice_container:
            self.choice_container.deleteLater()
            self.choice_container = None

    def _on_choice_selected(self, value):
        print(f"Выбран вариант: {value}")
        self.choice_container.hide()
        self.current_dialogue_index += 1
        self.show_next_dialogue(choice_result=value)
