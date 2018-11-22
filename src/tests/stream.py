import numpy as np
import cv2

camera_index = 0  # 0: built-in, 1: external
cap = cv2.VideoCapture(camera_index)

while True:
    is_correctly_setup, frame = cap.read()  # get next frame
    cv2.imshow("frame", frame)  # show frame on popup window
    if cv2.waitKey(1) & 0xFF == ord("q"):  # if user wants to close
        break

cap.release()  # kill capture
cv2.destroyAllWindows()  # kill windows