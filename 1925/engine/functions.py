# game_functions.py

class Character:
    def __init__(self, name, color="#c8c8ff", who_outlines=None):
        self.name = name
        self.color = color
        self.who_outlines = who_outlines if who_outlines else []

    def speak(self, text):
        return f"{self.name}: {text}" if self.name else text


class Scene:
    def __init__(self, name, music=None):
        self.name = name
        self.music = music

    def display(self, game_window):
        game_window.change_background(f"assets/backgrounds/{self.name}.png")
        if self.music:
            game_window.play_music(f"assets/music/{self.music}")


class Dialogue:
    def __init__(self, character, text):
        self.character = character
        self.text = text

    def display(self, game_window):
        game_window.display_text(self.character, self.text)

class Choice:
    def __init__(self, text, result):
        self.text = text  # Текст пункта меню
        self.result = result  # Действие, которое будет выполнено при выборе

class Menu:
    def __init__(self, prompt, choices):
        self.prompt = prompt  # Текст перед меню
        self.choices = choices  # Список вариантов выбора (экземпляры Choice)


def narrator(text):
    return Dialogue(None, text)


def character(character, text):
    return Dialogue(character, text)