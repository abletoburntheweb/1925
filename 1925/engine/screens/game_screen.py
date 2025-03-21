from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QApplication
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from engine.effects import fade, dissolve, hpunch, slide_out_to_right
from engine.screens.dialog_history_screen import DialogHistoryScreen
from engine.screens.pause_menu import PauseMenu

music_player = None


class GameScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем главный стековый макет
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        # Фон сцены
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.background_label)

        # Текстовый контейнер (для текста и textbox)
        self.text_container = QWidget(self)
        self.text_container.setFixedSize(1920, 1080)  # Фиксируем размер контейнера

        # Фон текстового блока (textbox.png)
        self.textbox_label = QLabel(self.text_container)
        self.textbox_label.setPixmap(QPixmap("assets/png/textbox2.png"))
        self.textbox_label.setAlignment(Qt.AlignBottom)
        self.textbox_label.adjustSize()  # Фиксируем размер фона

        # Контейнер для текста (располагается поверх textbox.png)
        self.text_layout = QVBoxLayout(self.text_container)
        self.text_layout.setAlignment(Qt.AlignBottom)
        self.text_layout.setContentsMargins(500, 0, 500, 200)  # Отступы для центрирования
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
        self.character_layer.setFixedSize(1920, 1080)  # Фиксируем размер
        self.layout.addWidget(self.character_layer)
        self.character_layer.lower()  # Перемещаем слой персонажей под текст

        # Основные элементы (например, текст диалога)
        self.dialogue_label = QLabel(self)
        self.dialogue_label.setGeometry(200, 800, 1520, 200)
        self.dialogue_label.setStyleSheet("font-size: 32px; color: white;")

        # История диалогов (хранение)
        self.dialogue_history = []

        # Экран истории
        self.history_screen = DialogHistoryScreen(parent=self)
        self.layout.addWidget(self.history_screen)
        self.history_screen.hide()  # Изначально скрываем экран истории

        self.choice_container = QWidget(self)
        self.choice_layout = QVBoxLayout()
        self.choice_container.setLayout(self.choice_layout)
        self.choice_container.setFixedSize(1920, 1080)  # Фиксируем размер контейнера
        self.choice_container.hide()  # Изначально скрываем контейнер

        self.layout.addWidget(self.choice_container)

        # Меню паузы (используем готовый класс PauseMenu)
        self.pause_menu = PauseMenu(parent=self)  # Создаем экземпляр PauseMenu
        self.layout.addWidget(self.pause_menu)
        self.pause_menu.hide()  # Скрываем меню паузы при старте
        self.text_container.show()
        self.character_layer.show()

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

    def keyPressEvent(self, event):
        """Обрабатывает нажатие клавиш."""
        if event.key() == Qt.Key_Escape:
            print("Нажата клавиша ESC.")
            if self.pause_menu.isHidden():
                self.pause_menu.show()
                self.pause_menu.raise_()
            else:
                self.resume_game()
            return  # Чтобы не блокировались другие нажатия ESC

        if self.pause_menu.isVisible():
            return  # Если меню паузы активно, блокируем остальные нажатия

        if event.key() == Qt.Key_Space:
            print("Нажата клавиша пробел.")
            if not self.history_screen.isVisible():
                self.show_next_dialogue()
    def resume_game(self):
        """Продолжает игру (закрывает меню паузы)."""
        self.pause_menu.hide()
        self.text_container.show()
        self.character_layer.show()

    def exit_game(self):
        """
        Закрывает игру.
        """
        print("Завершение игры...")
        self.close()

    def say(self, character, text):
        print(f"Добавлена реплика: {text}")
        self.dialogues.append((character, text))
        if len(self.dialogues) == 1:
            self.show_next_dialogue()

    def show_next_dialogue(self):
        """
        Показывает следующую реплику или выполняет команды.
        """
        if self.current_dialogue_index < len(self.dialogues):
            command = self.dialogues[self.current_dialogue_index]

            # Очищаем предыдущий текст
            while self.text_layout.count():
                widget = self.text_layout.takeAt(0).widget()
                if widget:
                    widget.deleteLater()

            # Обработка команд
            if isinstance(command, tuple) and len(command) > 0:
                command_type = command[0]

                if command_type == "__SCENE__":
                    # Команда смены сцены
                    scene_name, effect = command[1], command[2]
                    print(f"Меняем сцену на: {scene_name}")
                    self._actually_show_scene(scene_name, effect)
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return

                elif command_type == "__SHOW__":
                    # Команда показа персонажа
                    character_name, position = command[1], command[2]
                    print(f"Показываем персонажа: {character_name}")
                    self._actually_show_character(character_name, position)
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return

                elif command_type == "__HIDE__":
                    # Команда скрытия персонажа
                    character_name = command[1]
                    print(f"Скрываем персонажа: {character_name}")
                    if character_name in self.character_labels:
                        self.character_labels[character_name].hide()
                    self.current_dialogue_index += 1
                    self.show_next_dialogue()
                    return

                else:
                    # Реплика персонажа
                    character, text = command
                    if character and character.name:
                        name_label = QLabel(f"<font color='{character.color}'><b>{character.name}:</b></font>")
                        name_label.setAlignment(Qt.AlignLeft)
                        name_label.setStyleSheet(
                            "font-size: 36px;"
                            "font-family: 'Arial';"
                            "font-weight: bold;"
                            "padding-bottom: 5px;"
                        )
                        self.text_layout.addWidget(name_label)

                    text_label = QLabel(f"<font color='white'>{text}</font>")
                    text_label.setWordWrap(True)
                    text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
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
                self.on_intro_end()  # Вызываем функцию завершения предисловия

    def show_scene(self, scene_name, effect="none"):
        """Добавляет команду смены сцены в очередь диалогов."""
        print(f"Добавляю команду смены сцены: {scene_name} ({effect})")
        self.dialogues.append(("__SCENE__", scene_name, effect))

        if len(self.dialogues) == 1 and self.current_dialogue_index == 0:
            self.show_next_dialogue()

    def _actually_show_scene(self, scene_name, effect="none"):
        """Реально загружает фоновое изображение или отображает его название на сером фоне, если изображение не найдено."""
        pixmap_path = f"assets/backgrounds/{scene_name}.png"
        print(f"Загружаю фон: {pixmap_path}")
        pixmap = QPixmap(pixmap_path)

        if pixmap.isNull():
            print(f"Ошибка загрузки изображения: {pixmap_path}")

            # Если изображение не найдено, создаем серый фон
            self.background_label.setStyleSheet("background-color: gray; color: white; font-size: 48px;")
            self.background_label.setText(f"Фон не найден:\n{scene_name}")
            self.background_label.setAlignment(Qt.AlignCenter)
            self.background_label.show()
            return

        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setStyleSheet("")  # Сбрасываем стиль, если фон был серым

        # Применяем эффект
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
        """Сохраняем реплику в историю диалогов."""
        self.dialogue_history.append((character, text))

    def mousePressEvent(self, event):
        """Обрабатывает нажатие мыши для перехода к следующему диалогу."""
        if self.pause_menu.isVisible():
            return  # Если меню паузы активно, блокируем переход к следующему диалогу

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
        """Воспроизводит музыку в игре."""
        global music_player

        if music_player is None:
            music_player = QMediaPlayer()

        url = QUrl.fromLocalFile(f"assets/music/{file_name}")
        print(f"Загружаю музыку: {file_name}")
        music_player.setMedia(QMediaContent(url))

        if loop:
            music_player.mediaStatusChanged.connect(self._loop_music)

        print("Начинаем воспроизведение музыки.")
        music_player.play()

    def _loop_music(self, status):
        """Обработчик для зацикливания музыки."""
        if status == QMediaPlayer.EndOfMedia and music_player:
            music_player.setPosition(0)
            music_player.play()

    def show_character(self, character_name, position="center"):
        """
        Добавляет команду показа персонажа в очередь событий.
        Теперь персонажи появляются после диалога, а не сразу.
        """
        print(f"Добавляю команду показа персонажа: {character_name} ({position})")
        self.dialogues.append(("__SHOW__", character_name, position))

        if len(self.dialogues) == 1:  # Если очередь была пуста, запускаем обработку
            self.show_next_dialogue()

    def _actually_show_character(self, character_name, position="center"):
        """Реально добавляет персонажа на экран, позади текстового контейнера."""
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

        # Устанавливаем изображение персонажа
        character_label.setPixmap(pixmap.scaledToHeight(800, Qt.SmoothTransformation))
        character_label.setFixedSize(800, 1080)
        character_label.setScaledContents(True)

        # Устанавливаем позицию персонажа
        positions = {"left": 100, "right": 1200, "center": 600}
        character_label.move(positions.get(position, 600), 200)
        character_label.show()

        # Размещаем персонажей выше фона, но ниже текстового контейнера
        character_label.raise_()
        self.background_label.lower()  # Фон всегда остается на заднем плане
        self.text_container.raise_()  # Поднимаем текстовый контейнер над персонажами

    def hide_character(self, character_name):
        """Добавляет скрытие персонажа в очередь, чтобы оно выполнялось после диалога."""
        print(f"Добавляю команду скрытия персонажа: {character_name}")
        self.dialogues.append(("__HIDE__", character_name))

        if len(self.dialogues) == 1:  # Если очередь была пуста, запустить обработку
            self.show_next_dialogue()

    def clear_characters(self):
        """Прячет всех персонажей."""
        for character in self.characters.values():
            character.hide()

    def show_choices(self, options):
        """
        Отображает варианты выбора на экране с использованием namebox.png в качестве фона.
        :param options: Список кортежей вида [("Текст выбора", "значение"), ...].
        """
        print("Отображаю варианты...")

        # Очищаем предыдущие выборы
        while self.choice_layout.count():
            widget = self.choice_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Фон для выбора
        self.choice_bg = QLabel(self.choice_container)
        self.choice_bg.setPixmap(QPixmap("assets/png/namebox.png"))  # Используем namebox.png
        self.choice_bg.setScaledContents(True)
        self.choice_bg.setFixedSize(800, len(options) * 80 + 120)  # Делаем размер адаптивным
        self.choice_bg.move(0, 0)  # Устанавливаем фон в начало контейнера

        # Добавляем фон в контейнер
        self.choice_layout.addWidget(self.choice_bg)

        # Создаем кнопки для каждого варианта
        for text, value in options:
            button = QPushButton(text)
            button.setFixedSize(600, 60)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 50, 50, 200);
                    color: white;
                    font-size: 24px;
                    border: 2px solid white;
                    border-radius: 10px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 100, 200);
                }
                QPushButton:pressed {
                    background-color: rgba(150, 150, 150, 200);
                }
            """)
            button.clicked.connect(lambda _, v=value: self._on_choice_selected(v))
            self.choice_layout.addWidget(button)

        # Показываем контейнер выборов
        self.choice_container.show()
        self.choice_container.raise_()

    def _on_choice_selected(self, value):
        """
        Обработчик выбора варианта.
        :param value: Значение выбранного варианта.
        """
        print(f"Выбран вариант: {value}")
        self.choice_container.hide()  # Скрываем контейнер выборов
        self.current_dialogue_index += 1
        self.show_next_dialogue(choice_result=value)  # Продолжаем диалог с выбранным значением
