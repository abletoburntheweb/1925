from engine.game_logic import define_character, say, show_scene, play_music, show_character, hide_character, choice


def start():
    narrator = define_character(None, color="#c8c8ff")
    detective = define_character("Детектив", color="#ffcccb")
    francis = define_character("Френсис Миллер", color="#ffcccb")
    alan = define_character("Алан Хант", color="#ffcccb")

    show_scene("office", effect="fade")
    play_music("tense_music.mp3", loop=True)

    say(detective, "Господин, вам не кажется, что всё в нашем мире циклично?")

    show_character("francis", position="right")
    say(francis, "Что… что вы имеете в виду?")
    say(francis, "Давайте, пожалуйста, приступим к рассмотрению моего заявления.")

    say(narrator, "Парень отчаянно пытался изобразить уверенность, но его поза выдавала страх.")

    show_scene("newspaper", effect="hpunch")
    say(narrator, "Мужчина швырнул газету на стол. На развороте красовался заголовок о ночном убийстве.")

    say(francis, "По-моему, вы переходите все границы, господин детектив!")

    say(detective, "Я считаю, что всё что происходит в данный момент, произойдёт снова. История мира — это циклы.")
    say(detective,
        "Наш мир жесток, поэтому вам впредь следует вести себя осторожнее, пока я не выясню, что происходит на самом деле.")

    show_scene("street", effect="fade")
    say(narrator, "Френсис вышел на улицу, но его не покидало ощущение, что детектив что-то знает.")

    show_character("alan", position="left")
    say(alan, "Здоров! Ты как?")
    say(alan, "Я слышал, что произошло этой ночью — это ужасно.")

    # Выбор: рассказать подробности или промолчать
    decision = choice([
        ("Поинтересоваться", "ask_about_it"),
        ("Промолчать", "stay_silent")
    ])

    if decision == "ask_about_it":
        say(alan, "Как это произошло?")
        say(narrator, "Эти слова ударили в него, как холодная волна. Френсис быстро огляделся.")
    else:
        say(narrator, "В воздухе повисло напряжённое молчание.")

    say(francis, "Могу тебе всё рассказать, но не здесь и не сейчас. Приходи ко мне в 7, я буду ждать.")

    say(alan, "Обещаю, что точно буду под окнами твоего дома в срок.")

    show_scene("newspaper_piece", effect="dissolve")
    say(narrator, "Френсис передал другу обрывок газеты с заголовком: 'Убийство Кассиуса Ханта'.")

    # Выбор: прочесть статью или проигнорировать
    article_choice = choice([
        ("Прочесть статью", "read_article"),
        ("Пропустить", "ignore_article")
    ])

    if article_choice == "read_article":
        say(francis, "Интересно... Как могла произойти такая смерть?")
    else:
        say(narrator, "Френсис не стал углубляться в детали.")

    show_scene("clock", effect="fade")
    say(narrator, "До встречи оставалось два часа. Нужно чем-то занять себя...")

    # Выбор, как провести время
    time_choice = choice([
        ("Посмотреть записи", "review_notes"),
        ("Прогуляться", "take_a_walk")
    ])

    if time_choice == "review_notes":
        say(narrator, "Френсис решил изучить свои старые записи.")
    else:
        say(narrator, "Френсис отправился на прогулку, чтобы развеяться.")

    show_scene("house", effect="dissolve")
    say(narrator, "Френсис пришёл раньше назначенного времени.")

    # Выбор: дождаться 7 часов или войти сразу
    wait_choice = choice([
        ("Дождаться 7 часов", "wait_for_time"),
        ("Войти сразу", "enter_now")
    ])

    if wait_choice == "wait_for_time":
        say(narrator, "Он поднял взгляд на часы и дождался момента.")
    else:
        say(narrator, "Френсис вошёл в дом раньше времени.")

    show_character("alan", position="center")
    say(alan, "Не задерживайся, проходи.")

    show_scene("apartment", effect="fade")
    say(narrator, "Френсис почувствовал резкий запах химии, наполняющий квартиру.")

    # Последний выбор: осмотреться или сразу перейти к делу
    apartment_choice = choice([
        ("Осмотреться", "look_around"),
        ("Сразу начать разговор", "start_talking")
    ])

    if apartment_choice == "look_around":
        say(narrator, "Френсис заметил выброшенные сигареты...")
    else:
        say(narrator, "Френсис сразу приступил к разговору.")

    say(narrator, "От этого разговора зависит многое...")
