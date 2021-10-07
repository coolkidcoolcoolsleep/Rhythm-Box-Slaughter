from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import numpy as np
import cv2
import sys


class BallTracking:
    def selective_search(self, image, method='fast'):
        ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
        ss.setBaseImage(image)

        if method == 'fast':
            ss.switchToSelectiveSearchFast()
        else:
            ss.switchToSelectiveSearchQuality()

        rects = ss.process()
        return rects

    def box(self, image):
        H, W = image.shape[:2]
        rects = self.selective_search(image)

        proposals, boxes = [], []

        for (x, y, w, h) in rects:
            if w / float(W) < 0.1 or h / float(H) < 0.1:
                continue

            roi = image[y:y + h, x:x + w]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(roi, (64, 64))

            roi = img_to_array(roi)
            roi = preprocess_input(roi)

            proposals.append(roi)
            boxes.append((x, y, w, h))

        proposals = np.array(proposals)

        model = tf.keras.models.load_model('model/model.h5')
        preds = model.predict(proposals)
        preds_arg = np.argmax(preds, axis=1)

        labels = {}

        for i, (l, p) in enumerate(zip(preds_arg, preds)):
            label, prob = l, np.max(p)

            if prob >= 0.9:
                (x, y, w, h) = boxes[i]
                box = (x, y, x + w, y + h)

                L = labels.get(label[i], [])
                L.append((box, prob))
                labels[label[i]] = L

        for label in labels.keys():
            clone = image.copy()

            for (box, prob) in labels[label]:
                (startX, startY, endX, endY) = box
                cv2.rectangle(clone, (startX, startY), (endX, endY), (0, 255, 0), 2)

            cv2.imshow('Rhythm Box Slaughter', clone)

    def video_capture(self):
        vidcap = cv2.VideoCapture(0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        while vidcap.isOpened():
            ret, frame = vidcap.read()

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, dsize=(266, 126))

            count = 0
            if ret:
                if int(vidcap.get(1) % 10 == 0):
                    cv2.imwrite('C:/%d.png' % count, frame)
                    image = frame
                    self.box(image)
                    count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                break

        vidcap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    bt = BallTracking()
    bt.video_capture()
