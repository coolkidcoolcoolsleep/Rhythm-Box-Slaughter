import numpy as np
import cv2
import sys


class Video:
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
                cv2.imshow('Rhythm Box Slaughter', frame)
                if int(vidcap.get(1) % 100 == 0):
                    cv2.imwrite('C:/%d.png' % count, frame)
                    count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            else:
                break

        vidcap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    vc = Video()
    vc.video_capture()
