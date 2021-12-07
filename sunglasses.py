import cv2
import cvlib as cv
import cvzone


def sunglasses():
    width, height = 1330, 630

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Cannot open camera')
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Cannot receive frame from camera')
            break

        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        faces, _ = cv.detect_face(frame)
        # 얼굴이 인식되면 선글라스 이미지 띄우기
        for face in faces:
            x, y = face[0], face[1]
            glasses = cv2.imread('sunglasses.png', -1)

            try:
                frame = cvzone.overlayPNG(frame, glasses, [x+50, y+50])

            except:
                pass

        cv2.imshow('sunglasses', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sunglasses()
