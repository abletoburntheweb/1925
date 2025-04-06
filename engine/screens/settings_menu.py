import json
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap


def load_settings():
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
    with open("engine/settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


class SettingsScreen(QWidget):
    def __init__(self, parent=None, music_player=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(1920, 1080)

        self.music_player = music_player
        self.settings = load_settings()

        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/settings_menu.png")
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            self.background_label.setGeometry(-420, 0, 1920, 1080)

        title = QLabel("НАСТРОЙКИ", self)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setGeometry(600, 350, 400, 50)

        self.text_speed_slider = self.add_slider(70, 500, "Скорость текста", self.settings["text_speed"])
        self.autoscroll_speed_slider = self.add_slider(70, 550, "Скорость автоскролла", self.settings["autoscroll_speed"])

        self.music_volume_slider = self.add_slider(800, 500, "Громкость музыки", self.settings["music_volume"])
        self.music_volume_slider.valueChanged.connect(self.set_music_volume)
        self.sound_volume_slider = self.add_slider(800, 550, "Громкость звуков", self.settings["sound_volume"])

        self.fullscreen_checkbox = QCheckBox("Полноэкранный режим", self)
        self.fullscreen_checkbox.setFont(QFont("Arial", 18))
        self.fullscreen_checkbox.setStyleSheet("color: white;")
        self.fullscreen_checkbox.setChecked(self.settings["fullscreen"])
        self.fullscreen_checkbox.stateChanged.connect(self.update_settings)
        self.fullscreen_checkbox.setGeometry(800, 600, 300, 50)

        back_button = QPushButton("Назад", self)
        back_button.setFont(QFont("Arial", 20))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
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
        back_button.setGeometry(640, 900, 200, 50)
        back_button.clicked.connect(self.close)

        self.text_speed_slider.valueChanged.connect(self.update_settings)
        self.autoscroll_speed_slider.valueChanged.connect(self.update_settings)
        self.music_volume_slider.valueChanged.connect(self.update_settings)
        self.sound_volume_slider.valueChanged.connect(self.update_settings)

    def add_slider(self, x, y, text, default_value=50):
        label = QLabel(text, self)
        label.setFont(QFont("Arial", 18))
        label.setStyleSheet("color: white;")
        label.setGeometry(x, y, 300, 30)

        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(default_value)
        slider.setGeometry(x + 310, y, 300, 30)
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
        return slider

    def update_settings(self):
        self.settings["text_speed"] = self.text_speed_slider.value()
        self.settings["autoscroll_speed"] = self.autoscroll_speed_slider.value()
        self.settings["music_volume"] = self.music_volume_slider.value()
        self.settings["sound_volume"] = self.sound_volume_slider.value()
        self.settings["fullscreen"] = self.fullscreen_checkbox.isChecked()

        save_settings(self.settings)

        game_engine = self.parent().game_engine
        if self.settings["fullscreen"]:
            #print("Переход в полноэкранный режим")
            game_engine.showFullScreen()
        else:
            #print("Выход из полноэкранного режима")
            game_engine.showNormal()
            game_engine.move(0, 0)

    def set_music_volume(self, value):
        if self.music_player is not None:
            self.music_player.setVolume(value)
