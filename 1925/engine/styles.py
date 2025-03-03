MENU_STYLES = """
QMainWindow {
    background-color: black;
}

QPushButton {
    background-color: #0095FF; /* Синий цвет */
    color: white;
    font-size: 24px;
    font-weight: bold;
    font-family: Arial; /* Изменяем шрифт на Arial */
    border-radius: 15px; /* Уменьшили радиус скругления */
    padding: 10px 20px; /* Уменьшили внутренние отступы */
    min-width: 200px; /* Уменьшили минимальную ширину */
    min-height: 50px; /* Уменьшили минимальную высоту */
    margin-bottom: 20px; /* Добавили отступ снизу для каждой кнопки */
}

QPushButton:hover {
    background-color: #007ACC;
}
"""
GAME_WINDOW_STYLES = """
QMainWindow {
    background-color: black;
}

QFrame#text_frame {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(0, 0, 0, 128));
    border-radius: 10px;
    border: none;
}

QLabel#text_label {
    color: white;
    padding: 50px;
}
"""
