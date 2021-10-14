import cv2


def sunglasses():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Cannot open camera')
        exit()

    width, height = 266, 126
    img = cv2.imread('sunglasses.png', -1)     # -1: 투명 영역 불러오기
    img = cv2.resize(img, dsize=(width, height))

    # RGBA이미지로부터 alpha mask 추출해서 RGB로 전환하기
    b, g, r, a = cv2.split(img)
    overlay_color = cv2.merge((b, g, r))

    mask = cv2.medianBlur(a, 5)

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Cannot receive frame from camera')
            break
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

        # 배경: 선글라스 뒤의 영역 black out 처리하기
        img_bg = cv2.bitwise_and(frame.copy(), frame.copy(), mask=cv2.bitwise_not(mask))

        # 전경: 선글라스 이미지에서 선글라스 mask out 처리하기
        img_fg = cv2.bitwise_and(overlay_color, overlay_color, mask=mask)

        frame = cv2.add(img_bg, img_fg)
        cv2.imshow('sunglasses', frame)

        if cv2.waitKey(1) == 27:    # ESC키 눌러서 빠져나가기
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sunglasses()
