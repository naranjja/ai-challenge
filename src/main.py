import time
import json
import gtts
import datetime
import logging
import pygame


def find_face():
    logging.info("\n- Finding face...")
    # TODO
    logging.info("- Face found correctly.")
    return None  # testing


def classify_face(face):
    logging.info("\n- Classifying face...")
    # TODO
    _id = "rodrigo"
    logging.info(f"- Found: {_id}")
    return _id  # testing


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
    logging.info("\n- Making audio clip from text...")
    lang = "es-ES" if spain else "es-us"
    try: gtts.gTTS(text=sentence, lang=lang).save(f"./../data/greetings/{_id}.mp3")
    except Exception as e:
        logging.error("An exception occurred when trying to save audio.")
        logging.error(e) 
        return False
    logging.info("- Audio clip saved correctly.")
    return True

    
def play_audio(_id):
    logging.info("\n- Playing...")
    pygame.mixer.init()
    pygame.mixer.music.load(f"./../data/greetings/{_id}.mp3")
    pygame.mixer.music.play()
    time.sleep(15)
    logging.info("- Finished playing.")


def main():
    names = json.loads(open("./../data/names.json", "r", encoding="utf-8").read())

    face = find_face()
    _id = classify_face(face)

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
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()