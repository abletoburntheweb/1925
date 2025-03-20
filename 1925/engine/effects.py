# engine/effects.py
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect


def fade(widget, duration=500):
    """
    Эффект плавного появления (затухания) элемента.
    """
    effect = QGraphicsOpacityEffect(widget)  # Создаем эффект прозрачности
    widget.setGraphicsEffect(effect)  # Применяем его к виджету

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(0.0)  # Начинаем с полной прозрачности
    animation.setEndValue(1.0)  # Завершаем с полной видимостью

    widget.animation = animation  # Сохраняем анимацию в атрибуте объекта
    animation.start()

def dissolve(widget, duration=500):
    """
    Эффект растворения (плавное появление элемента).
    """
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    animation.setStartValue(0.0)  # Начинаем с полной прозрачности
    animation.setEndValue(1.0)    # Завершаем с полной видимостью

    widget.animation = animation
    animation.start()

def slide_in_from_left(widget, duration=500):
    """
    Эффект "выезда" элемента слева.
    """
    start_pos = QPoint(-widget.width(), widget.y())  # Начальная позиция за экраном слева
    end_pos = widget.pos()  # Обычная позиция виджета

    widget.move(start_pos)  # Устанавливаем начальную позицию за экраном

    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)

    widget.animation = animation
    animation.start()

def slide_out_to_right(widget, duration=500):
    """
    Эффект "ухода" элемента вправо.
    """
    start_pos = widget.pos()  # Начальная позиция
    end_pos = QPoint(widget.width() + start_pos.x(), widget.y())  # Позиция за экраном справа

    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InCubic)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)

    widget.animation = animation
    animation.start()