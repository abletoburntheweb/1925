# engine/screens/game_logic.py

from PyQt5.QtWidgets import QStackedWidget, QWidget, QApplication
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
        game_engine = self

        self.init_screens()

    def init_screens(self):
        # Инициализация экранов
        self.main_menu = MainMenu(self)
        self.addWidget(self.main_menu)   # Добавляем его в стек виджетов

        self.game_screen = GameScreen(self)
        self.addWidget(self.game_screen)
        self.setCurrentWidget(self.main_menu)  # Устанавливаем главное меню как текущий экран

    def clear_window(self):
        print("Очищаю все виджеты...")
        current_screen = self.currentWidget()

        for widget in self.findChildren(QWidget):
            if widget != current_screen:
                print(f"Удаляю виджет: {widget}")
                widget.deleteLater()

        print("Все виджеты удалены.")

    def start_script(self, script_path):
        print(f"Запускаю сценарий: {script_path}")

        #self.clear_window() было прекращено, так как текущая система стеков позволяет обойтись без этого

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

    def choice(options):
        game_engine.currentWidget().dialogues.append(("__CHOICE__", options))
        if len(game_engine.currentWidget().dialogues) == 1:
            game_engine.currentWidget().show_next_dialogue()

    def exit_game(self):
        # Закрытие игры
        self.close()
        QApplication.quit()

    def toggle_fullscreen(self, fullscreen):
        """
        Переключает между полноэкранным и оконным режимами.
        """
        if fullscreen:
            self.showFullScreen()  # Полноэкранный режим
        else:
            self.showNormal()  # Оконный режим
            self.setFixedSize(1920, 1080)  # Устанавливаем фиксированный размер

# Глобальные функции для использования в скриптах
def say(character, text):
    game_engine.currentWidget().say(character, text)

def show_scene(scene_name, effect="none"):
    game_engine.currentWidget().show_scene(scene_name, effect)

def play_music(file_name, loop=False):
    game_engine.currentWidget().play_music(file_name, loop)

def stop_music():
    game_engine.currentWidget().stop_music()

def play_sfx(file_name):
    game_engine.currentWidget().play_sfx(file_name)

def show_character(character_name, position="center"):
    game_engine.currentWidget().show_character(character_name, position)

def hide_character(character_name):
    game_engine.currentWidget().hide_character(character_name)

def clear_characters():
    game_engine.currentWidget().clear_characters()

def start_script(script_path):
    game_engine.start_script(script_path)

def show_chapter(chapter_title, effect="fade", next_script=None):
    game_engine.currentWidget().show_chapter(chapter_title, effect, next_script)
def choice(options):
    return game_engine.currentWidget().show_choices(options)
def exit_game():
    game_engine.exit_game()