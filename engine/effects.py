# engine/effects.py
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QPainter, QColor


def fade(widget, duration=500):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuad)
    animation.setStartValue(0.2)
    animation.setEndValue(1.0)

    widget.animation = animation
    animation.start()

def dissolve(widget, duration=450):
    class DissolveOverlay(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setParent(parent)
            self.setFixedSize(parent.size())
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.noise_level = 1.0

        def paintEvent(self, event):
            painter = QPainter(self)
            rect = self.rect()
            painter.fillRect(rect, QColor(0, 0, 0, int(255 * self.noise_level)))

    steps = 25
    interval = duration // steps
    noise_level = 1.0

    overlay = DissolveOverlay(widget)
    overlay.show()

    def update_noise():
        nonlocal noise_level
        noise_level -= 1 / steps
        overlay.noise_level = max(0, noise_level)
        overlay.update()

    timer = QTimer()
    timer.start(interval)
    timer.timeout.connect(update_noise)
    QTimer.singleShot(duration, lambda: timer.stop())
    QTimer.singleShot(duration, lambda: overlay.deleteLater())

def hider(widget, duration=500, param=False):
    class HiderOverlay(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setParent(parent)
            self.setFixedSize(parent.size())
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.opacity = 0.0

        def paintEvent(self, event):
            painter = QPainter(self)
            rect = self.rect()
            color = QColor(0, 0, 0, int(255 * self.opacity))
            painter.fillRect(rect, color)

    steps = 25
    interval = duration // steps
    opacity_step = 1 / steps

    overlay = HiderOverlay(widget)
    overlay.show()

    def update_opacity():
        nonlocal opacity
        opacity += opacity_step
        overlay.opacity = min(1.0, opacity)
        overlay.update()

    opacity = 0.0
    timer = QTimer()
    timer.timeout.connect(update_opacity)
    timer.start(interval)
    QTimer.singleShot(duration, lambda: timer.stop())
    QTimer.singleShot(duration, lambda: overlay.deleteLater())



def hpunch(widget, duration=400):
    original_pos = widget.pos()
    offsets = [-50, 30, -20, 10, 0]
    step_duration = duration // len(offsets)

    def apply_offset(index=0):
        if index < len(offsets):
            widget.move(original_pos.x() + offsets[index], original_pos.y())
            QTimer.singleShot(step_duration, lambda: apply_offset(index + 1))
        else:
            widget.move(original_pos)

    apply_offset()

def slide_in_from_left(widget, position="center", duration=500):
    positions = {"left": 100, "right": 1200, "center": 600}
    end_x = positions.get(position, 600)
    start_x = -widget.width()
    steps = 50  # Количество шагов
    step_duration = duration // steps
    step_size = (end_x - start_x) / steps

    widget.move(start_x, 200)

    def update_position():
        nonlocal start_x
        start_x += step_size
        widget.move(int(start_x), 200)
        if start_x < end_x:
            QTimer.singleShot(step_duration, update_position)

    update_position()


def slide_out_to_right(widget, position="center", duration=500):
    positions = {"left": 100, "right": 1200, "center": 600}
    start_x = positions.get(position, 600)
    end_x = 1920 + widget.width()
    steps = 50  # Количество шагов
    step_duration = duration // steps
    step_size = (end_x - start_x) / steps

    widget.move(start_x, 200)

    def update_position():
        nonlocal start_x
        start_x += step_size
        widget.move(int(start_x), 200)
        if start_x < end_x:
            QTimer.singleShot(step_duration, update_position)

    update_position()
