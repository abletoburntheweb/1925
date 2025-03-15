# engine/scripts/chapter1.py
from engine.game_logic import define_character, say, show_scene, play_music

def start():
    # Определяем персонажей
    narrator = define_character(None, color="#c8c8ff")
    police = define_character("Полицейский", color="#ffcccb")

    # Начинаем сцену
    show_scene("hall", effect="fade")
    play_music("intro.mp3", loop=True)

    # Повествование
    say(narrator, "В мире, где пороки общества кажутся повседневной нормой...")
    say(police, "Вы не видели её сегодня?")