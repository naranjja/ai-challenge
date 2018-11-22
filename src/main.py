import time
import json
import gtts
import datetime
import logging
import pygame


def get_time_of_day():
    hour = datetime.datetime.now().hour
    if hour >= 5 and hour < 13: return "Buenos días"
    if hour >= 13 and hour < 19: return "Buenas tardes"
    return "Buenas noches"


def build_sentence(info):
    if info and info.get("company"):
        return "¡{} {name}! ¿Cómo está {company}? {sentence}".format(get_time_of_day(), **info)
    elif info:
        return "¡{} {name}! {sentence}".format(get_time_of_day(), **info)
    else:
        return "¡{} persona desconocida! No te he podido reconocer correctamente.".format(get_time_of_day())


def save_audio(_id, sentence, spain=False):
    lang = "es-ES" if spain else "es-us"
    try: gtts.gTTS(text=sentence, lang=lang).save(f"./../data/greetings/{_id}.mp3")
    except: return False
    return True


def play_audio(_id):
    pygame.mixer.init()
    pygame.mixer.music.load(f"./../data/greetings/{_id}.mp3")
    pygame.mixer.music.play()
    time.sleep(15)


def main():
    names = json.loads(open("./../data/names.json", "r", encoding="utf-8").read())

    # TODO: classify and return _id as key from dict of names
    _id = "anapaula"

    info = None
    try: info = names[_id]
    except KeyError: 
        logging.error("Face didn't match something that we know.")
        _id = "unknown"

    sentence = build_sentence(info)
    
    if _id == "melero": save_audio(_id, sentence, spain=True)
    else: save_audio(_id, sentence)
    
    play_audio(_id)


if __name__ == "__main__":
    main()