from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer


class DialogHistoryScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1920, 1080)

        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/history_screen.png")
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            self.background_label.setFixedSize(1920, 1080)
        else:
            print("Ошибка загрузки фонового изображения для экрана истории.")

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(200, 100, 1520, 800)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setAlignment(Qt.AlignTop)
        self.history_layout.setSpacing(10)
        self.scroll_area.setWidget(self.history_container)

        self.hide()

    def _scroll_to_bottom(self):
        if self.scroll_area.verticalScrollBar():
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
    def add_dialogue(self, character, text):
        if character and character.name:
            name_text = f"<font color='{character.color}'><b>{character.name}</b></font>: "
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
                if isinstance(text, str) and text.strip().startswith(("if ", "elif ", "else")):
                    continue

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

        QTimer.singleShot(100, self._scroll_to_bottom)

    def show_history(self, history):
        self.update_history(history)
        self.show()
        self.raise_()

    def hide_history(self):
        self.hide()