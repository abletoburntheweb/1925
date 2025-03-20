from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class CaseScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.beck_label = QLabel(self)
        pixmap = QPixmap("assets/backgrounds/frst_blend.png")
        self.beck_label.setPixmap(pixmap)
        self.beck_label.setScaledContents(True)
        self.beck_label.lower()


        # Контейнер для изображений
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(1200, 800)
        self.image_label.move(360, 140)
        self.image_label.raise_()

        # Словарик
        self.images = [
            "assets/cases/case1.png",
            "assets/cases/case2.png"
            # "assets/cases/case3.png"   #потом...
        ]
        self.curr = 0  # системка для смены экрана
        self.show_currrrr()

        # Кнопка "Назад"
        start_button = QPushButton("НАЗАД", self)
        start_button.setFont(QFont("Arial", 24))
        start_button.setStyleSheet("background-color: transparent; color: white;")
        start_button.clicked.connect(self.go_beck)
        start_button.move(100, 100)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "beck_label"):
            self.beck_label.setGeometry(0, 0, self.width(), self.height())

    def show_currrrr(self):
        pixmap_path = self.images[self.curr]
        pixmap = QPixmap(pixmap_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            print(f"Ошибка загрузки йоу: {pixmap_path}")

    def mousePressEvent(self, event):
        width = self.width()
        click_x = event.pos().x()

        if click_x < width / 2:
            self.curr = (self.curr - 1) % len(self.images)
        else:
            self.curr = (self.curr + 1) % len(self.images)

        self.show_currrrr()

    def go_beck(self):
        self.parent().setCurrentWidget(self.parent().main_menu)