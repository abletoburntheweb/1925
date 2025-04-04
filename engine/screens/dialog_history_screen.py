from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class DialogHistoryScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1920, 1080)

        # Фон истории
        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/history_screen.png")
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            self.background_label.setFixedSize(1920, 1080)
        else:
            print("Ошибка загрузки фонового изображения для экрана истории.")

        # Контейнер с историей
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(200, 100, 1520, 800)  # Размеры области прокрутки
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        # Внутренний виджет для истории
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setAlignment(Qt.AlignTop)  # Выравнивание по верху
        self.history_layout.setSpacing(10)  # Отступ между элементами
        self.scroll_area.setWidget(self.history_container)

        self.hide()

    def add_dialogue(self, character, text):
        if character and character.name:
            name_text = f"<font color='{character.color}'>{character.name}</font>: "
        else:
            name_text = ""

        dialogue_text = f"{name_text}{text}"
        label = QLabel(dialogue_text, self)
        label.setFont(QFont("Arial", 24))
        label.setStyleSheet("""
               color: white;
               padding: 10px;
           """)
        label.setWordWrap(True)
        self.history_layout.addWidget(label)

    def update_history(self, history):
        """
        Обновляет историю диалогов.
        :param history: Список кортежей (character, text).
        """
        # Очищаем старые сообщения
        while self.history_layout.count():
            widget = self.history_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        if not history:
            label = QLabel("История пуста.", self)
            label.setFont(QFont("Arial", 24))
            label.setStyleSheet("color: gray; padding: 10px;")
            self.history_layout.addWidget(label)
        else:
            for character, text in history:
                if character and character.name:
                    name_text = f"<font color='{character.color}'><b>{character.name}</b></font>: "
                else:
                    name_text = ""

                dialogue_text = f"{name_text}{text}"
                label = QLabel(dialogue_text, self)
                label.setFont(QFont("Arial", 24))
                label.setStyleSheet("color: white; padding: 10px;")
                label.setWordWrap(True)
                self.history_layout.addWidget(label)

    def show_history(self, history):
        """
        Показывает экран истории диалогов.
        :param history: Список кортежей (character, text).
        """
        self.update_history(history)
        self.show()
        self.raise_()

    def hide_history(self):
        self.hide()


