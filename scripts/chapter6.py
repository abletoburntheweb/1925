from engine.game_logic import define_character, say, show_scene, play_music, show_character, hide_character, choice, \
    show_chapter

narrator = define_character(None, color="#c8c8ff")
detective = define_character("Детектив", color="#ffcccb")
alan = define_character("Алан Хант", color="#ffcccb")
duke = define_character("Герцог",color="#ffcccb")
francis = define_character("Френсис Миллер", color="#ffcccb")
bartender = define_character("Бармен", color="#ffcccb")
evelyn = define_character("Эвелин", color="#ffcccb")
tennent = define_character("Миссис Теннонт",  color="#ffcccb")
stern = define_character("Стерн", color="#ffcccb")
woman = define_character("Женщина", color="#ffcccb")
agatha = define_character("Агата Блейк",color="#ffcccb" )
constable = define_character("Констебль",color="#ffcccb" )

def scene1():
    pass