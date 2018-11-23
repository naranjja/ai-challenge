import tensorflow as tf
import numpy as np

import scipy
import pickle
import logging
import json
import cv2
import os

execution_path = None
try:
    from FaceClassifier import detect_face
    from FaceClassifier import facenet

    execution_path = "./FaceClassifier"  # from src
except ModuleNotFoundError:
    import detect_face
    import facenet

    execution_path = "."  # locally


def classify_face(face):
    logging.info("\n- Classifying face...")

    # disable tf logging
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))

        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, f"{execution_path}/d_npy")

            minsize = 20  # minimum size of face
            threshold = [0.6, 0.7, 0.7]  # three steps threshold
            factor = 0.709  # scale factor
            image_size = 182
            input_image_size = 160

            people = json.loads(open(f"{execution_path}/../../data/names.json", "r", encoding="utf-8").read())
            names = list(people.keys())

            logging.info("- Loading feature extraction model...")
            modeldir = f"{execution_path}/pre_model/20180408-102900.pb"
            facenet.load_model(modeldir)

            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            embedding_size = embeddings.get_shape()[1]

            classifier_filename = f"{execution_path}/my_class/my_classifier.pkl"
            classifier_filename_exp = os.path.expanduser(classifier_filename)

            with open(classifier_filename_exp, "rb") as f:
                (model, class_names) = pickle.load(f)
                logging.debug(f"Classifier filename: {classifier_filename_exp}")
                f.close()

            logging.debug("Starting recognition...")

            frame = cv2.imread(face)
            try:
                logging.debug("size image1: ", frame.shape)
            except AttributeError:
                logging.debug("No face found!")

            try:
                frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            except:
                logging.debug("Found a head, but not a face!")
                return "unknown"

            frame = frame[:, :, 0:3]
            bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
            logging.debug("bounding", bounding_boxes)
            num_faces = bounding_boxes.shape[0]
            logging.debug("Detected_FaceNum: %d" % num_faces)

            if num_faces > 0:
                det = bounding_boxes[:, 0:4]

                cropped = []
                scaled = []
                scaled_reshape = []
                bb = np.zeros((num_faces, 4), dtype=np.int32)

                for i in range(num_faces):
                    emb_array = np.zeros((1, embedding_size))

                    bb[i][0] = det[i][0]
                    bb[i][1] = det[i][1]
                    bb[i][2] = det[i][2]
                    bb[i][3] = det[i][3]

                    # inner exception
                    if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
                        logging.debug("face is inner of range!")
                        continue

                    cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                    cropped[i] = facenet.flip(cropped[i], False)
                    scaled.append(scipy.misc.imresize(cropped[i], (image_size, image_size), interp="bilinear"))
                    scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
                                           interpolation=cv2.INTER_CUBIC)
                    scaled[i] = facenet.prewhiten(scaled[i])
                    scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
                    feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                    emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                    predictions = model.predict_proba(emb_array)

                    best_class_indices = np.argmax(predictions, axis=1)
                    logging.debug("Best class indice")
                    logging.debug(best_class_indices)
                    best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                    logging.debug("best class probabilities")
                    logging.debug(best_class_probabilities)
                    cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)  # boxing face

                    # plot result idx under box
                    text_x = bb[i][0]
                    text_y = bb[i][3] + 20
                    # print("result: ", best_class_indices[0])
                    # print(best_class_indices)
                    val = int(best_class_indices[0])
                    for H_i in names:
                        # print(H_i)
                        try:
                            if names[best_class_indices[0]] == H_i:
                                result_names = names[best_class_indices[0]]
                                cv2.putText(frame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                            1, (0, 0, 255), thickness=1, lineType=4)
                                # cv2.putText(frame, str, ("", text_fps_y),cv2.FONT_HERSHEY_COMPLEX_SMALL, 
                                #             1, (0, 0, 0), thickness=1, lineType=2)
                                try:
                                    os.unlink("result.jpg")
                                except FileNotFoundError:
                                    pass
                                cv2.imwrite("result.jpg", frame)
                        except:
                            pass
                    _id = None
                    try:
                        _id = names[val].lower()
                        logging.info(f"- Found: {_id}")
                        return _id
                    except:
                        logging.warning(f"- Could not find class {_id} (position {val}) in list of names.")
                        return "unknown"
            else:
                logging.warning(f"- Could not classify face.")
                return "unknown"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    classify_face("./test_face.jpg")
