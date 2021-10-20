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

        # face detection
        faces, _ = cv.detect_face(frame)

        # 얼굴이 인식되면 선글라스 이미지 띄우기
        for face in faces:
            x, y, w, h = face[0], face[1], face[2], face[3]
            glasses = cv2.imread('sunglasses.png', -1)

            glasses_height, glasses_width, _ = glasses.shape
            roi = frame[x:x + glasses_width, y:y + glasses_height]

            if x & y != 0 and roi.shape[0] & roi.shape[1] != 0:
                print('glasses shape: ', glasses.shape)
                frame = cvzone.overlayPNG(frame, glasses, [x + 50, y + 50])
            if roi.shape[0] <= glasses.shape[0] or roi.shape[1] <= glasses.shape[1]:
                print('roi shape:', roi.shape)

            else:
                print('x, y:', x, y)

        cv2.imshow('sunglasses', frame)

        if cv2.waitKey(1) == 27:    # ESC키 눌러서 빠져나가기
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sunglasses()
