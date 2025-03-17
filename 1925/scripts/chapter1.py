from engine.game_logic import define_character, say, show_scene, play_music, show_character, hide_character

def start():
    narrator = define_character(None, color="#c8c8ff")
    police = define_character("Полицейский", color="#ffcccb")

    show_scene("hall", effect="fade")
    play_music("intro.mp3", loop=True)

    say(narrator, "В мире, где пороки общества кажутся повседневной нормой...")

    show_character("man2", position="left")
    say(police, "Вы не видели её сегодня?")

    # Меняем сцену перед показом нового персонажа
    show_scene("door", effect="dissolve")

    show_character("man", position="right")
    say(police, "Вы видели её сегодня?")
