import time
import json
import gtts
import datetime
import logging
import pygame
import sys

from HeadDetector.prediction_yolo import *
from FaceClassifier.detect_in_image import *


def get_time_of_day():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 13:
        return "Buenos días"
    if 13 <= hour < 19:
        return "Buenas tardes"
    return "Buenas noches"


def build_sentence(info):
    if info and info.get("company"):
        return "¡{} {name}! ¿Cómo está {company}? {sentence}".format(get_time_of_day(), **info)
    elif info:
        return "¡{} {name}! {sentence}".format(get_time_of_day(), **info)
    else:
        return "{}. No he podido reconocer tu rostro. Es la primera vez que vienes a BREIN?".format(get_time_of_day())


def save_audio(_id, sentence, spain=False):
    logging.info("\n- Making audio clip from text...")
    lang = "es-ES" if spain else "es-us"
    try:
        gtts.gTTS(text=sentence, lang=lang).save(f"./../data/greetings/{_id}.mp3")
    except Exception as e:
        logging.error("An exception occurred when trying to save audio.")
        logging.error(e)
        return False
    logging.info("- Audio clip saved correctly.")
    return True


def play_audio(file_path, seconds=15.0):
    logging.info("\n- Playing...")
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    time.sleep(seconds)
    logging.info("- Finished playing.")


def main(cheat=None):
    play_audio(f"./../data/sounds/loading.mp3", 0.1)
    people = json.loads(open("./../data/names.json", "r", encoding="utf-8").read())
    camera_index = 1  # 0: built-in, 1: external

    head = find_head(camera_index)

    play_audio(f"./../data/sounds/match.mp3", 0.1)
    _id = classify_face(head)

    if cheat:
        _id = cheat

    info = None
    try:
        info = people[_id]
    except KeyError:
        logging.error("Face didn't match someone that we know.")
        _id = "unknown"

    sentence = build_sentence(info)

    if _id == "melero":
        save_audio(_id, sentence, spain=True)
    else:
        save_audio(_id, sentence)

    play_audio(f"./../data/greetings/{_id}.mp3", 15.0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
