import cv2
import time
import sys
import numpy as np


class Tracking:
    def track_and_draw(self, color_lower, color_upper, color):
        vidcap = cv2.VideoCapture(0)
        time.sleep(0.4)
        detections = []

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        while True:
            _, frame = vidcap.read()
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(266, 126))

            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, color_lower, color_upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

                    detections.append([x, y, w, h])

            cv2.imshow('Rhythm Box Slaughter', frame)
            cv2.moveWindow(winname='Rhythm Box Slaughter', x=300, y=200)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        vidcap.release()
        cv2.destroyAllWindows()

        return detections


if __name__ == '__main__':
    red_lower = (0, 70, 50)
    red_upper = (10, 255, 255)
    red = (0, 0, 255)

    blue_lower = (100, 150, 0)
    blue_upper = (140, 255, 255)
    blue = (255, 0, 0)

    t = Tracking()

    t.track_and_draw(red_lower, red_upper, red)
    # t.track_and_draw(blue_lower, blue_upper, blue)
