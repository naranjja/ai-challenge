import numpy as np
import os
import cv2
import logging
import json
import operator
import threading
import time

execution_path = None
try:
    from HeadDetector.preprocessing import parse_annotation
    from HeadDetector.utils import draw_boxes
    from HeadDetector.frontend import YOLO

    execution_path = "./HeadDetector"  # from src
except ModuleNotFoundError:
    from preprocessing import parse_annotation
    from utils import draw_boxes
    from frontend import YOLO

    execution_path = "."  # locally

config_path = f"{execution_path}/config.json"
weights_path = f"{execution_path}/model.h5"
image_path = f"{execution_path}/img/original.jpg"
output_path = f"{execution_path}/img/output.jpg"


def yolo_initialization():
    with open(config_path) as f:
        config = json.load(f)
        f.close()

    ###############################
    #   Make the model
    ###############################

    yolo = YOLO(backend=config["model"]["backend"],
                input_size=config["model"]["input_size"],
                labels=config["model"]["labels"],
                max_box_per_image=config["model"]["max_box_per_image"],
                anchors=config["model"]["anchors"])

    ###############################
    #   Load trained weights
    ###############################

    yolo.load_weights(weights_path)

    return yolo


def maximum_area(image_original, boxes):
    image_h, image_w, _ = image_original.shape
    areas = {}
    for i_box, box in enumerate(boxes):
        if (box.get_score() < 0.5):
            areas[i_box] = 0
            continue
        xmin = int(box.xmin * image_w)
        ymin = int(box.ymin * image_h)
        xmax = int(box.xmax * image_w)
        ymax = int(box.ymax * image_h)

        areas[i_box] = (ymax - ymin) * (xmax - xmin)

    return areas


def camera_thread(camera_index):
    cap = cv2.VideoCapture(camera_index)
    while True:
        is_correctly_setup, frame = cap.read()  # get next frame

        cv2.imshow("frame", frame)  # show frame on popup window
        cv2.imwrite(image_path, frame)

        cv2.waitKey(10)

        if not should_camera_stop:
            cap.release()  # kill capture
            cv2.destroyAllWindows()  # kill windows
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):  # if user wants to close
            break


def find_head(camera_index):
    logging.info("\n- Finding heads...")

    try:
        os.unlink(image_path)
        os.unlink(output_path)
    except FileNotFoundError:
        pass

    global should_camera_stop
    should_camera_stop = True

    yolo = yolo_initialization()
    t = threading.Thread(target=lambda: camera_thread(camera_index))
    t.start()

    found_head_counter = 0
    while True:
        try:
            image_original = cv2.imread(image_path)
            boxes = yolo.predict(image_original)
            # image = draw_boxes(image_original, boxes, config["model"]["labels"])

            areas = maximum_area(image_original, boxes)
            box_index = None
            try:
                box_index = max(areas.items(), key=operator.itemgetter(1))[0]
                logging.debug(f"- Found a head!")
                found_head_counter += 1
                logging.info(f"Frame: {found_head_counter}")
            except:
                logging.debug("No head found.")

            logging.debug("Area de foto:", areas[box_index])
            if areas[box_index] < 140 ** 2:
                logging.debug("Face too small.")
                continue

            image_h, image_w, _ = image_original.shape
            xmin = int(boxes[box_index].xmin * image_w)
            ymin = int(boxes[box_index].ymin * image_h)
            xmax = int(boxes[box_index].xmax * image_w)
            ymax = int(boxes[box_index].ymax * image_h)
            crop_img = image_original[ymin:ymax, xmin:xmax]

            if found_head_counter >= 2:
                logging.info(f"- Found a head!")
                cv2.imwrite(output_path, crop_img)
                return output_path
            else: continue

            if cv2.waitKey(1) & 0xFF == ord("q"):  # if user wants to close
                should_camera_stop = False
                logging.warn("Process stopped.")
                return

            time.sleep(0.1)

        except:
            logging.debug("No heads found.")
            continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    camera_index = 0  # 0: built-in, 1: external
    result = find_head(camera_index)
    logging.info(result)
