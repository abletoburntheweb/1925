from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QHBoxLayout, QGraphicsDropShadowEffect, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap

class SettingsScreen(QWidget):
    def __init__(self, parent=None, music_player=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setFixedSize(1920, 1080)

        # Сохраняем ссылку на music_player
        self.music_player = music_player

        # **Добавляем фоновое изображение**
        self.background_label = QLabel(self)
        pixmap = QPixmap("assets/png/settings_menu.png")  # Загружаем изображение
        if not pixmap.isNull():
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)  # Растягиваем изображение
        else:
            print("Ошибка загрузки фонового изображения settings_menu.png")

        layout = QVBoxLayout()

        # **Заголовок**
        title = QLabel("НАСТРОЙКИ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: white;")

        # **Добавляем тень к заголовку**
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
        self.text_speed_slider = self.add_slider(left_column, "Скорость текста")
        self.autoscroll_speed_slider = self.add_slider(left_column, "Скорость автоскролла")

        # **Правая колонка**
        self.music_volume_slider = self.add_slider(right_column, "Громкость музыки")
        self.sound_volume_slider = self.add_slider(right_column, "Громкость звуков")

        # **Подключаем слайдеры к функциям**
        self.music_volume_slider.valueChanged.connect(self.set_music_volume)
        self.sound_volume_slider.valueChanged.connect(self.set_sound_volume)

        # **Переключатель режима экрана**
        fullscreen_checkbox = QCheckBox("Полноэкранный режим")
        fullscreen_checkbox.setFont(QFont("Arial", 18))
        fullscreen_checkbox.setStyleSheet("color: white;")
        fullscreen_checkbox.setChecked(False)  # По умолчанию оконный режим
        fullscreen_checkbox.stateChanged.connect(self.toggle_fullscreen)
        right_column.addWidget(fullscreen_checkbox)

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
        back_button.clicked.connect(self.close)  # Закрытие окна при нажатии
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # **Добавляем общий макет**
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.background_label)  # Фоновое изображение
        main_layout.addLayout(layout)  # Основной контент
        self.setLayout(main_layout)

    def add_slider(self, layout, text):
        """Функция для добавления ползунка с подписью"""
        row = QHBoxLayout()
        label = QLabel(text)
        label.setFont(QFont("Arial", 18))
        label.setStyleSheet("color: white;")

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)  # По умолчанию среднее значение
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

    def toggle_fullscreen(self, state):
        """
        Переключает между оконным и полноэкранным режимами.
        """
        if state == Qt.Checked:
            self.parent().showFullScreen()  # Полноэкранный режим
        else:
            self.parent().showNormal()  # Оконный режим
            self.parent().setFixedSize(1920, 1080)  # Устанавливаем фиксированный размер

    def set_music_volume(self, value):
        """
        Устанавливает громкость музыки.
        """
        if self.music_player is not None:
            self.music_player.setVolume(value)

    def set_sound_volume(self, value):
        """
        Устанавливает громкость звуков.
        """
        # Здесь можно добавить код для установки громкости звуков, если это необходимо
        print(f"Громкость звуков изменена: {value}")