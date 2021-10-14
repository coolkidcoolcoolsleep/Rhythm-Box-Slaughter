import cv2
import numpy as np


def sunglasses():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Cannot open camera')
        exit()

    width, height = 266, 126
    img = cv2.imread('circular-sunglasses.png')
    img = cv2.resize(img, dsize=(width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Cannot receive frame from camera')
            break
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        # Blend the two images and show the result
        tr = 0.3    # transparency between 0-1, show camera if 0
        frame = ((1-tr) * frame.astype(np.float) + tr * img.astype(np.float)).astype(np.uint8)

        cv2.imshow('sunglasses', frame)
        if cv2.waitKey(1) == 27:    # press ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sunglasses()
