# engine/effects.py
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget

def fade(widget, duration=500):
    """
    Эффект затухания (появление элемента от прозрачного к непрозрачному).
    :param widget: Виджет, к которому применяется эффект.
    :param duration: Длительность анимации в миллисекундах.
    """
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setDuration(duration)
    animation.setStartValue(0.0)  # Начальная прозрачность
    animation.setEndValue(1.0)   # Конечная прозрачность
    animation.start()

def dissolve(widget, duration=500):
    """
    Эффект растворения (плавное появление элемента).
    :param widget: Виджет, к которому применяется эффект.
    :param duration: Длительность анимации в миллисекундах.
    """
    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    animation.setStartValue(widget.pos())  # Начальная позиция
    animation.setEndValue(widget.pos())    # Конечная позиция (можно изменить логику)
    animation.start()

def slide_in_from_left(widget, duration=500):
    """
    Эффект "выезда" элемента слева.
    :param widget: Виджет, к которому применяется эффект.
    :param duration: Длительность анимации в миллисекундах.
    """
    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    start_pos = widget.pos() - QPoint(widget.width(), 0)  # Начальная позиция (слева за экраном)
    end_pos = widget.pos()                               # Конечная позиция
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)
    animation.start()

def slide_out_to_right(widget, duration=500):
    """
    Эффект "выезда" элемента вправо.
    :param widget: Виджет, к которому применяется эффект.
    :param duration: Длительность анимации в миллисекундах.
    """
    animation = QPropertyAnimation(widget, b"pos")
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InCubic)
    start_pos = widget.pos()                             # Начальная позиция
    end_pos = widget.pos() + QPoint(widget.width(), 0)  # Конечная позиция (за экраном справа)
    animation.setStartValue(start_pos)
    animation.setEndValue(end_pos)
    animation.start()