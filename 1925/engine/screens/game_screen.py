from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QStackedLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from engine.effects import fade, dissolve

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
        self.textbox_label.setPixmap(QPixmap("assets/png/textbox.png"))
        self.textbox_label.setAlignment(Qt.AlignBottom)
        self.textbox_label.setFixedSize(1920, 1080)  # Фиксируем размер фона

        # Контейнер для текста (располагается поверх textbox.png)
        self.text_layout = QVBoxLayout(self.text_container)
        self.text_layout.setAlignment(Qt.AlignBottom)
        self.text_layout.setContentsMargins(500, 0, 500, 100)  # Отступы для центрирования
        self.text_container.setLayout(self.text_layout)

        # Добавляем контейнер текста в макет
        self.layout.addWidget(self.text_container)
        self.text_container.raise_()  # Поднимаем текстовой контейнер над textbox.png

        # Очередь реплик
        self.dialogues = []
        self.current_dialogue_index = 0

        # Слой для отображения персонажей
        self.character_layer = QLabel(self)
        self.character_layer.setAlignment(Qt.AlignCenter)
        self.character_layer.setFixedSize(1920, 1080)  # Фиксируем размер
        self.layout.addWidget(self.character_layer)
        self.character_layer.lower()  # Перемещаем слой персонажей под текст

        self.text_container.show()

    def say(self, character, text):
        """Добавляет реплику в очередь для последовательного вывода."""
        print(f"Добавлена реплика: {text}")
        self.dialogues.append((character, text))

        if len(self.dialogues) == 1:
            self.show_next_dialogue()

    def show_next_dialogue(self):
        """Показывает следующую реплику из очереди."""
        if self.current_dialogue_index < len(self.dialogues):
            # **Очищаем предыдущий текст**
            while self.text_layout.count():
                widget = self.text_layout.takeAt(0).widget()
                if widget:
                    widget.deleteLater()

            # Получаем текущую реплику
            character, text = self.dialogues[self.current_dialogue_index]

            print(f"Отображаю реплику: {character.name}: {text}")

            # QLabel для имени персонажа
            name_label = QLabel(f"<font color='{character.color}'><b>{character.name}</b></font>")
            name_label.setAlignment(Qt.AlignLeft)  # Имя выравниваем по левому краю
            name_label.setStyleSheet(
                "font-size: 36px;"  # Крупный шрифт для имени
                "font-family: 'Arial';"
                "font-weight: bold;"
                "padding-bottom: 5px;"  # Маленький отступ перед текстом
            )

            # QLabel для текста персонажа
            text_label = QLabel(f"<font color='white'>{text}</font>")
            text_label.setWordWrap(True)
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Текст тоже слева
            text_label.setStyleSheet(
                "font-size: 32px;"
                "font-family: 'Arial';"
                "line-height: 1.4;"
                "font-weight: bold;"
                "padding-left: 10px;"  # Чуть сдвигаем текст, чтобы было красиво
            )

            # Добавление имени и текста персонажа в контейнер
            self.text_layout.addWidget(name_label)
            self.text_layout.addWidget(text_label)
            self.text_container.show()
            self.text_container.raise_()
            self.update()

            print(f"Количество виджетов в text_layout: {self.text_layout.count()}")

            # Переход к следующей реплике
            self.current_dialogue_index += 1
        else:
            print("Все реплики показаны.")

    def keyPressEvent(self, event):
        """Обрабатывает нажатие клавиш."""
        if event.key() == Qt.Key_Space:
            print("Нажата клавиша пробел.")
            self.show_next_dialogue()

    def show_scene(self, scene_name, effect="none"):
        """Загружает фоновое изображение."""
        pixmap_path = f"assets/backgrounds/{scene_name}.png"
        print(f"Загружаю фон: {pixmap_path}")
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            print(f"Ошибка загрузки изображения: {pixmap_path}")
            return

        # Добавляем изображение в фон
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

        # Применяем эффект
        if effect == "fade":
            fade(self.background_label)
        elif effect == "dissolve":
            dissolve(self.background_label)

        self.update()

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
        Отображает персонажа на экране.
        :param character_name: Имя файла изображения персонажа (без расширения).
        :param position: Позиция персонажа ('left', 'center', 'right').
        """
        pixmap_path = f"assets/characters/{character_name}.png"
        print(f"Загружаю персонажа: {pixmap_path}")
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            print(f"Ошибка загрузки изображения персонажа: {pixmap_path}")
            return

        # Устанавливаем позицию персонажа
        scaled_pixmap = pixmap.scaledToHeight(800, Qt.SmoothTransformation)  # Масштабируем изображение
        self.character_layer.setPixmap(scaled_pixmap)

        if position == "left":
            self.character_layer.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        elif position == "right":
            self.character_layer.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        else:
            self.character_layer.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        self.character_layer.show()
        self.character_layer.raise_()