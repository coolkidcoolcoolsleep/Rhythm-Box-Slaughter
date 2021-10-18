import cv2
import sys


class Tracking:
    def track_and_draw(self, blue_lower, blue_upper, red_lower, red_upper):
        vidcap = cv2.VideoCapture(0)
        detection_blue = []
        detection_red = []

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

            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            blue_mask = cv2.erode(blue_mask, None, iterations=2)
            blue_mask = cv2.dilate(blue_mask, None, iterations=2)
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    detection_blue.append([x, y, w, h])

            red_mask = cv2.inRange(hsv, red_lower, red_upper)
            red_mask = cv2.erode(red_mask, None, iterations=2)
            red_mask = cv2.dilate(red_mask, None, iterations=2)
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    detection_red.append([x, y, w, h])

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(1) == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()

        return detection_blue, detection_red


if __name__ == '__main__':
    blue_lower = (100, 150, 0)
    blue_upper = (140, 255, 255)

    # red_lower = (0, 70, 50)
    # red_upper = (10, 255, 255)

    red_lower = (175, 70, 50)
    red_upper = (180, 255, 255)

    t = Tracking()
    t.track_and_draw(blue_lower, blue_upper, red_lower, red_upper)
