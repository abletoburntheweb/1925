# effects.py

from PyQt5.QtCore import QPropertyAnimation, QTimer, QPoint
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel
import random

class Effect:
    def __init__(self, game_window):
        self.game_window = game_window

    def fade(self, widget, start_opacity, end_opacity, duration=1000):
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)

        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.start()

    def dissolve(self, old_widget, new_widget, duration=1000):
        self.fade(old_widget, 1.0, 0.0, duration // 2)

        QTimer.singleShot(duration // 2, lambda: self.fade(new_widget, 0.0, 1.0, duration // 2))

        QTimer.singleShot(duration, old_widget.deleteLater)

    def flash(self, duration=200):
        flash_layer = QLabel(self.game_window)
        flash_layer.setStyleSheet("background-color: white;")
        flash_layer.setGeometry(0, 0, 1920, 1080)
        flash_layer.show()

        QTimer.singleShot(duration, flash_layer.deleteLater)

    def vpunch(self, widget, intensity=20, duration=300):
        if not widget:
            print("Ошибка: Виджет не найден!")
            return

        geometry = widget.geometry()
        original_y = geometry.y()
        print(f"Исходное положение по Y: {original_y}")

        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setKeyValueAt(0.0, geometry)
        animation.setKeyValueAt(0.25, geometry.translated(0, -intensity))
        animation.setKeyValueAt(0.75, geometry.translated(0, intensity))
        animation.setKeyValueAt(1.0, geometry)
        animation.start()

        QTimer.singleShot(duration, lambda: self.restore_position(widget, geometry))

    def shake(self, widget, intensity=10, duration=500, steps=10):
        original_pos = widget.pos()

        def random_offset():
            return QPoint(random.randint(-intensity, intensity), random.randint(-intensity, intensity))

        for i in range(steps):
            QTimer.singleShot(i * (duration // steps), lambda: widget.move(original_pos + random_offset()))

        QTimer.singleShot(duration, lambda: widget.move(original_pos))

    def restore_position(self, widget, geometry):
        widget.setGeometry(geometry)
        print(f"Положение восстановлено: {geometry}")