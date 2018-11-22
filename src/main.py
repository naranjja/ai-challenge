import time
import json
import gtts
import logging
import pygame


def save_audio(_id, sentence, spain=False):
    lang = "es-ES" if spain else "es-us"
    try: gtts.gTTS(text=sentence, lang=lang).save(f"./../data/greetings/{_id}.mp3")
    except: return False
    return True


def play_audio(_id):
    pygame.mixer.init()
    pygame.mixer.music.load(f"./../data/greetings/{_id}.mp3")
    pygame.mixer.music.play()
    time.sleep(10)


def main():
    names = json.loads(open("./../data/names.json", "r", encoding="utf-8").read())
    
    # TODO: classify
    _id = "jose"

    try: info = names[_id]
    except KeyError: 
        logging.error("Face didn't match something that we know.")
        return

    sentence = info.get("sentence")
    
    if _id == "melero": save_audio(_id, sentence, spain=True)
    else: save_audio(_id, sentence)
    
    play_audio(_id)


if __name__ == "__main__":
    main()