import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QHBoxLayout, QGraphicsDropShadowEffect, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap

def load_settings():
    """Загружает настройки из JSON-файла."""
    try:
        with open("engine/settings.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "text_speed": 50,
            "autoscroll_speed": 50,
            "music_volume": 50,
            "sound_volume": 50,
            "fullscreen": False
        }

def save_settings(settings):
    """Сохраняет настройки в JSON-файл."""
    with open("engine/settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)

class SettingsScreen(QWidget):
    def __init__(self, parent=None, music_player=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(1920, 1080)

        self.music_player = music_player
        self.settings = load_settings()

        # **Фон**
        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/settings_menu.png")
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            self.background_label.setGeometry(-420, 0, 1920, 1080)

        self.content_widget = QWidget(self)
        self.content_widget.setGeometry(-420, 0, 1920, 1080)
        layout = QVBoxLayout(self.content_widget)
        layout.setAlignment(Qt.AlignRight)

        # **Заголовок**
        title = QLabel("НАСТРОЙКИ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: white;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(3, 3)
        title.setGraphicsEffect(shadow)

        layout.addWidget(title)

        # **Разделы настроек**
        settings_layout = QHBoxLayout()
        left_column = QVBoxLayout()
        right_column = QVBoxLayout()

        # **Левая колонка**
        self.text_speed_slider = self.add_slider(left_column, "Скорость текста", self.settings["text_speed"])
        self.autoscroll_speed_slider = self.add_slider(left_column, "Скорость автоскролла", self.settings["autoscroll_speed"])

        # **Правая колонка**
        self.music_volume_slider = self.add_slider(right_column, "Громкость музыки", self.settings["music_volume"])
        self.music_volume_slider.valueChanged.connect(self.set_music_volume)
        self.sound_volume_slider = self.add_slider(right_column, "Громкость звуков", self.settings["sound_volume"])

        # **Переключатель режима экрана**
        self.fullscreen_checkbox = QCheckBox("Полноэкранный режим")
        self.fullscreen_checkbox.setFont(QFont("Arial", 18))
        self.fullscreen_checkbox.setStyleSheet("color: white;")
        self.fullscreen_checkbox.setChecked(self.settings["fullscreen"])
        self.fullscreen_checkbox.stateChanged.connect(self.update_settings)
        right_column.addWidget(self.fullscreen_checkbox)

        settings_layout.addLayout(left_column)
        settings_layout.addLayout(right_column)
        layout.addLayout(settings_layout)

        # **Кнопка возврата**
        back_button = QPushButton("Назад")
        back_button.setFixedSize(200, 50)
        back_button.setFont(QFont("Arial", 20))
        back_button.setStyleSheet("""
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
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # Связываем ползунки с обновлением настроек
        self.text_speed_slider.valueChanged.connect(self.update_settings)
        self.autoscroll_speed_slider.valueChanged.connect(self.update_settings)
        self.music_volume_slider.valueChanged.connect(self.update_settings)
        self.sound_volume_slider.valueChanged.connect(self.update_settings)

    def add_slider(self, layout, text, default_value=50):
        """Добавляет ползунок с подписью."""
        row = QHBoxLayout()
        label = QLabel(text)
        label.setFont(QFont("Arial", 18))
        label.setStyleSheet("color: white;")

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(default_value)
        slider.setFixedSize(300, 30)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(255, 255, 255, 50);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: 2px solid #aaa;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #ddd;
            }
        """)

        row.addWidget(label)
        row.addWidget(slider)
        layout.addLayout(row)
        return slider

    def update_settings(self):
        """Сохраняет настройки и применяет их."""
        self.settings["text_speed"] = self.text_speed_slider.value()
        self.settings["autoscroll_speed"] = self.autoscroll_speed_slider.value()
        self.settings["music_volume"] = self.music_volume_slider.value()
        self.settings["sound_volume"] = self.sound_volume_slider.value()
        self.settings["fullscreen"] = self.fullscreen_checkbox.isChecked()

        save_settings(self.settings)

        # Применяем полноэкранный режим сразу
        if self.parent() and hasattr(self.parent(), "game_engine"):
            game_engine = self.parent().game_engine
            if self.settings["fullscreen"]:
                print("Переход в полноэкранный режим")
                game_engine.showFullScreen()
            else:
                print("Выход из полноэкранного режима")
                game_engine.showNormal()

    def set_music_volume(self, value):
        """Изменяет громкость музыки."""
        if self.music_player is not None:
            self.music_player.setVolume(value)
