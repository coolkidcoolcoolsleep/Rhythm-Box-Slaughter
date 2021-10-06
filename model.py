from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import numpy as np
import cv2
import sys


vidcap = cv2.VideoCapture(0)

if not vidcap.isOpened():
    print('카메라를 열 수 없습니다.')
    sys.exit()

while vidcap.isOpened():
    ret, frame = vidcap.read()

    frame = cv2.flip(frame, 1)
    count = 0
    if ret:
        cv2.imshow('Rhythm Box Slaughter', frame)
        if int(vidcap.get(1) % 100 == 0):
            cv2.imwrite('C:/%d.png' % count, frame)
            image = frame
            model = tf.keras.models.load_model('model/model.h5')

            count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

vidcap.release()
cv2.destroyAllWindows()
