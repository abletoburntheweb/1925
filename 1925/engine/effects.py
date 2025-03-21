# engine/effects.py
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect


def fade(widget, duration=500):
    """
    Эффект плавного появления (затухания) элемента с мягким замедлением.
    """
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutQuad)  # Плавный переход
    animation.setStartValue(0.2)  # Начинаем не с полной прозрачности
    animation.setEndValue(1.0)  # Завершаем с полной видимостью

    widget.animation = animation
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
    animation.setEndValue(1.0)  # Завершаем с полной видимостью

    widget.animation = animation
    animation.start()


def hpunch(widget, duration=400):
    """
    Эффект горизонтального "удара" (встряхивания) элемента.
    """
    original_pos = widget.pos()

    # Анимация смещения влево
    animation_left = QPropertyAnimation(widget, b"pos")
    animation_left.setDuration(duration // 3)
    animation_left.setEasingCurve(QEasingCurve.OutQuad)
    animation_left.setStartValue(original_pos)
    animation_left.setEndValue(QPoint(original_pos.x() - 50, original_pos.y()))  # Сильное смещение влево

    # Анимация смещения вправо
    animation_right = QPropertyAnimation(widget, b"pos")
    animation_right.setDuration(duration // 3)
    animation_right.setEasingCurve(QEasingCurve.OutQuad)
    animation_right.setStartValue(QPoint(original_pos.x() - 50, original_pos.y()))
    animation_right.setEndValue(QPoint(original_pos.x() + 30, original_pos.y()))  # Сильное смещение вправо

    # Анимация возвращения в исходную позицию
    animation_return = QPropertyAnimation(widget, b"pos")
    animation_return.setDuration(duration // 3)
    animation_return.setEasingCurve(QEasingCurve.OutQuad)
    animation_return.setStartValue(QPoint(original_pos.x() + 30, original_pos.y()))
    animation_return.setEndValue(original_pos)

    # Запускаем анимации последовательно
    animation_left.finished.connect(animation_right.start)
    animation_right.finished.connect(animation_return.start)
    animation_left.start()

def slide_in_from_left(widget, position="center", duration=500):
    """
    Эффект "выезда" персонажа слева.
    :param widget: Виджет персонажа.
    :param position: Конечная позиция ("left", "right", "center").
    :param duration: Длительность анимации.
    """
    positions = {"left": 100, "right": 1200, "center": 600}
    end_x = positions.get(position, 600)  # Определяем конечную позицию
    start_pos = QPoint(-widget.width(), 200)  # Начальная позиция за экраном слева
    end_pos = QPoint(end_x, 200)  # Конечная позиция

    widget.move(start_pos)  # Устанавливаем начальную позицию за экраном

    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)

    widget.animation = animation
    animation.start()


def slide_out_to_right(widget, position="center", duration=500):
    """
    Эффект "ухода" персонажа вправо.
    :param widget: Виджет персонажа.
    :param position: Начальная позиция ("left", "right", "center").
    :param duration: Длительность анимации.
    """
    positions = {"left": 100, "right": 1200, "center": 600}
    start_x = positions.get(position, 600)  # Определяем начальную позицию
    start_pos = QPoint(start_x, 200)  # Начальная позиция
    end_pos = QPoint(1920 + widget.width(), 200)  # Конечная позиция за экраном справа

    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InCubic)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)

    widget.animation = animation
    animation.start()
