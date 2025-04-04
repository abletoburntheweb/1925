from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Notebook(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_notebook_active = False

        # Блокнот
        self.notebook = QTextEdit(parent=self.parent)
        self.notebook.setFixedSize(800, 600)
        self.notebook.move(560, 240)
        self.notebook.setStyleSheet("""
            QTextEdit {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                font-size: 20px;
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.notebook.hide()

        self.tabs_container = QWidget(parent=self.parent)
        self.tabs_container.setFixedSize(200, 600)
        self.tabs_container.move(370, 240)
        self.tabs_layout = QVBoxLayout()
        self.tabs_layout.setAlignment(Qt.AlignTop)
        self.tabs_container.setLayout(self.tabs_layout)
        self.tabs_container.hide()

        # Кнопка "Главная"
        self.main_page_button = QPushButton("Главная", parent=self.tabs_container)
        self.main_page_button.setFixedSize(180, 40)
        self.main_page_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 200);
            }
        """)
        self.main_page_button.clicked.connect(self.switch_to_main_page)
        self.tabs_layout.addWidget(self.main_page_button)

        self.add_tab_button = QPushButton("+", parent=self.tabs_container)
        self.add_tab_button.setFixedSize(180, 40)
        self.add_tab_button.setFont(QFont("Arial", 20))
        self.add_tab_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 200);
            }
        """)
        self.add_tab_button.clicked.connect(self.create_new_tab)
        self.tabs_layout.addWidget(self.add_tab_button)

        # Список вкладок
        self.tabs = []  # Хранит виджеты вкладок (кнопки с названиями)

        # Кнопка закрытия блокнота
        self.close_notebook_button = QPushButton("×", parent=self.parent)
        self.close_notebook_button.setFont(QFont("Arial", 20))
        self.close_notebook_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.close_notebook_button.setFixedSize(40, 40)
        self.close_notebook_button.move(1320, 240)
        self.close_notebook_button.hide()
        self.close_notebook_button.clicked.connect(self.toggle_notebook)

    def toggle_notebook(self):
        if self.is_notebook_active:
            self.notebook.hide()
            self.tabs_container.hide()
            self.close_notebook_button.hide()
            self.is_notebook_active = False
            print("Блокнот скрыт.")
        else:
            self.notebook.show()
            self.tabs_container.show()
            self.close_notebook_button.show()
            self.is_notebook_active = True
            print("Блокнот показан.")

            # Поднимаем блокнот над другими виджетами
            self.notebook.raise_()
            self.tabs_container.raise_()
            self.close_notebook_button.raise_()

    def switch_to_main_page(self):
        self.notebook.clear()
        self.notebook.setText("Это главная страница блокнота.\nЗдесь можно писать заметки.")

    def create_new_tab(self):
        input_field = QLineEdit(parent=self.tabs_container)
        input_field.setPlaceholderText("Введите название")
        input_field.setText("Новая заметка")
        input_field.setFixedSize(180, 40)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 5px;
            }
        """)

        delete_button = QPushButton("×", parent=self.tabs_container)
        delete_button.setFixedSize(20, 20)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_tab(input_field, delete_button))

        tab_widget = QWidget(parent=self.tabs_container)
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(input_field)
        tab_layout.addWidget(delete_button)
        tab_widget.setLayout(tab_layout)
        self.tabs_layout.addWidget(tab_widget)
        self.tabs.append((input_field, tab_widget))
        input_field.returnPressed.connect(lambda: self.switch_to_tab(input_field.text()))

    def delete_tab(self, input_field, delete_button):
        if self.tabs:
            last_input_field, last_tab_widget = self.tabs.pop()
            last_tab_widget.deleteLater()
            print(f"Вкладка '{last_input_field.text()}' удалена.")

    def switch_to_tab(self, tab_name):
        self.notebook.clear()
        self.notebook.setText(f"Это страница '{tab_name}'.\nЗдесь можно писать заметки.")

    def save_notes(self):
        for input_field, _ in self.tabs:
            tab_name = input_field.text()
            notes = self.notebook.toPlainText()
            with open(f"{tab_name}.txt", "w", encoding="utf-8") as file:
                file.write(notes)
        print("Заметки сохранены.")