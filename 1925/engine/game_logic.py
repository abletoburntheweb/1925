# engine/screens/game_logic.py

from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt, QTimer
from engine.screens.game_screen import GameScreen
from engine.screens.main_menu import MainMenu
import importlib

# Глобальные переменные
music_player = None
game_engine = None

class Character:
    def __init__(self, name, color="#ffffff", who_outlines=None):
        self.name = name
        self.color = color
        self.who_outlines = who_outlines or []

def define_character(name, color="#ffffff", who_outlines=None):
    return Character(name, color, who_outlines)

class GameEngine(QStackedWidget):
    def __init__(self):
        super().__init__()
        global game_engine
        game_engine = self  # Сохраняем экземпляр в глобальной переменной

        self.init_screens()

    def init_screens(self):
        # Инициализация экранов
        self.main_menu = MainMenu(self)  # Создаем экземпляр главного меню
        self.addWidget(self.main_menu)   # Добавляем его в стек виджетов
        self.setCurrentWidget(self.main_menu)  # Устанавливаем главное меню как текущий экран

    def clear_window(self):
        """
        Очищает все виджеты в окне, кроме активного игрового экрана.
        """
        print("Очищаю все виджеты...")  # Отладка
        current_screen = self.currentWidget()  # Получаем текущий экран

        for widget in self.findChildren(QWidget):
            if widget != current_screen:
                print(f"Удаляю виджет: {widget}")
                widget.deleteLater()

        print("Все виджеты удалены.")  # Отладка

    def start_script(self, script_path):
        print(f"Запускаю сценарий: {script_path}")

        self.clear_window()  # Очищаем интерфейс

        try:
            module_name, function_name = script_path.split(":")
            module = importlib.import_module(module_name)
            script_function = getattr(module, function_name)

            game_screen = GameScreen(self)
            self.addWidget(game_screen)
            self.setCurrentWidget(game_screen)

            # Запускаем сценарий через 100 мс, чтобы интерфейс обновился
            QTimer.singleShot(100, script_function)
        except Exception as e:
            print(f"Ошибка при запуске сценария: {e}")

    def exit_game(self):
        # Закрытие игры
        self.close()

# Глобальные функции для использования в скриптах
def say(character, text):
    game_engine.currentWidget().say(character, text)

def show_scene(scene_name, effect="none"):
    game_engine.currentWidget().show_scene(scene_name, effect)

def play_music(file_name, loop=False):
    game_engine.currentWidget().play_music(file_name, loop)

def start_script(script_path):
    game_engine.start_script(script_path)

def exit_game():
    game_engine.exit_game()