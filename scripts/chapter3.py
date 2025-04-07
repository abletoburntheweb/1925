from engine.game_logic import define_character, say, show_scene, play_music, show_character, hide_character, choice, \
    show_chapter

narrator = define_character(None, color="#c8c8ff")
detective = define_character("Детектив", color="#ffcccb")
alan = define_character("Алан Хант", color="#ffcccb")
francis = define_character("Френсис Миллер", color="#ffcccb")
boy = define_character("Мальчик", color="#ffcccb")
bartender = define_character("Бармен", color="#ffcccb")


def scene1():
    pass