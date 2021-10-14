import glob, os
from PIL import Image
import numpy as np
import cv2, sys
import random

# 2. random_box 좌표 끌고오고
# 3. ball_tracking 좌표 끌고와서
# 4. 2안에 3이 들어가나 비교
# 5. 들어가면 +10, 안 들어가면 -1
# ------------------------- 여기까지가 player1일 때
# 5. 1p와 2p 총점수 비교
# 6. 점수 더 높은 사람이 winner

# 랜덤하게 생성된 좌표와 tracking 돼서 나온 좌표값이 일치할 때 + 10
# 랜덤하게 생성된 좌표에 tracking 돼서 나온 좌표값이 일치하지 않을 때 -1

class Video_Manager:
    def __init__(self, img_width=266, img_height=126):
        self.img_width = img_width
        self.img_height = img_height
        self.easy = 50
        self.norm = 40
        self.hard = 30
        self.red_color = (0, 0, 255)
        self.blue_color = (255, 0, 0)
        self.green_color = (0, 255, 0)
        self.white_color = (255, 255, 255)

    def track_and_draw(self, blue_lower, blue_upper, red_lower, red_upper, level, is_one_player=True):
        # 카메라를 VideoCapture 타입의 객체로 얻어옴
        #  영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
        vidcap = cv2.VideoCapture(0)
        detection_blue = []
        detection_red = []

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        num = 0
        while True:
            _, frame = vidcap.read()    # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(266, 126))

            seed_num = num // 10
            random.seed(seed_num)
            num = num + 1

            # GaussianBlur: 적용해서 노이즈와 이상치 줄임
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            # erode: 개체 경계의 픽셀을 제거
            blue_mask = cv2.erode(blue_mask, None, iterations=2)
            # dilate: 공백으로 구분 된 연결 영역
            blue_mask = cv2.dilate(blue_mask, None, iterations=2)
            # 공의 윤곽선 찾기
            contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    detection_blue.append([x, y, w, h])
                    # print(x, y, w, h)

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
                    # print(x, y, w, h)

            self.random_box(level, frame, is_one_player)

            cv2.imshow('Rhythm Box Slaughter', frame)

            # if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
            #     break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        vidcap.release()
        cv2.destroyAllWindows()

        return detection_blue, detection_red
        # 리턴값으로 좌표를 받는 건???


    def rhythm_box_display_area(self, level, frame, is_one_player=True):
        # game_areas = self.load_data()
        # game_areas = frame
        area = frame
        display_areas = []
        # for area in game_areas:
        y, x, _ = area.shape  # (126, 266, 3)
        if not is_one_player:
            if level == 'easy':
                area1 = (0, 0), (x//2-self.easy, y-self.easy)       # (0, 0), (103, 96)
                area2 = (x//2, 0), (x-self.easy, y-self.easy)       # (133, 0), (236, 96)
                # print(area1, area2)
                display_areas.append((area1, area2))
            if level == 'norm':
                area1 = (0, 0), (x//2-self.norm, y-self.norm)       # (0, 0), (113, 106)
                area2 = (x//2, 0), (x-self.norm, y-self.norm)       # (133, 0), (246, 106)
                # print(area1, area2)
                display_areas.append((area1, area2))
            if level == 'hard':
                area1 = (0, 0), (x//2-self.hard, y-self.hard)       # (0, 0), (118, 111)
                area2 = (x//2, 0), (x-self.hard, y-self.hard)       # (133, 0), (251, 111)
                # print(area1, area2)
                display_areas.append((area1, area2))
        else:
            if level == 'easy':
                area1 = (0, 0), (x-self.easy, y-self.easy)          # (0, 0), (236, 96)
                # print(area1)
                display_areas.append(area1)
            if level == 'norm':
                area1 = (0, 0), (x-self.norm, y-self.norm)          # (0, 0), (246, 106)
                # print(area1)
                display_areas.append(area1)
            if level == 'hard':
                area1 = (0, 0), (x-self.hard, y-self.hard)          # (0, 0), (251, 111)
                # print(area1)
                display_areas.append(area1)
        return display_areas

    def random_box(self, level, frame, is_one_player=True):
        # img = self.load_data()[0]

        img = frame
        areas = self.rhythm_box_display_area(level, frame, is_one_player)
        # (((30, 30), (103, 96)), ((163, 30), (236, 96)))
        for area in areas:
            if not is_one_player:
                img = cv2.line(img, (133, 0), (133, 126), self.white_color, 2)
                area1, area2 = area
                (xs1, ys1), (xe1, ye1) = area1
                (xs2, ys2), (xe2, ye2) = area2
                a1, b1 = random.randint(xs1, xe1), random.randint(ys1, ye1)
                a2, b2 = random.randint(xs2, xe2), random.randint(ys2, ye2)

                if level == 'easy':
                    img = cv2.rectangle(img, (a1, b1), (a1+self.easy, b1+self.easy), self.red_color, 3)
                    img = cv2.rectangle(img, (a2, b2), (a2+self.easy, b2+self.easy), self.blue_color, 3)
                if level == 'norm':
                    img = cv2.rectangle(img, (a1, b1), (a1+self.norm, b1+self.norm), self.red_color, 3)
                    img = cv2.rectangle(img, (a2, b2), (a2+self.norm, b2+self.norm), self.blue_color, 3)
                if level == 'hard':
                    img = cv2.rectangle(img, (a1, b1), (a1+self.hard, b1+self.hard), self.red_color, 3)
                    img = cv2.rectangle(img, (a2, b2), (a2+self.hard, b2+self.hard), self.blue_color, 3)
            else:
                (xs1, ys1), (xe1, ye1) = area
                a, b = random.randint(xs1, xe1), random.randint(ys1, ye1)
                c, d = random.randint(xs1, xe1), random.randint(ys1, ye1)
                if level == 'easy':
                    img = cv2.rectangle(img, (a, b), (a + self.easy, b + self.easy), self.red_color, 3)
                    img = cv2.rectangle(img, (c, d), (c + self.easy, d + self.easy), self.blue_color, 3)
                if level == 'norm':
                    img = cv2.rectangle(img, (a, b), (a + self.norm, b + self.norm), self.red_color, 3)
                    img = cv2.rectangle(img, (c, d), (c + self.norm, d + self.norm), self.blue_color, 3)
                if level == 'hard':
                    img = cv2.rectangle(img, (a, b), (a + self.hard, b + self.hard), self.red_color, 3)
                    img = cv2.rectangle(img, (c, d), (c + self.hard, d + self.hard), self.blue_color, 3)
        # cv2.imshow('rhythm_box', img)
        # cv2.waitKey(0)
        # cv2.imwrite(f'data/image_output/01.jpg', img)

    # 사각형 표현 방법 : (x1, y1, x2, y2)
    # def overlap(rect1, rect2):
    # 두 개의 사각형이 겹쳐지는지 확인하는 함수
    # :param rect1: 첫번째 사각형
    # :param rect2: 두번째 사각형
    # :return: overlap이 되면 True, 아니면 False

    # return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[1] > rect2[3] or rect1[3] < rect2[1])

if __name__ == '__main__':
    blue_lower = (100, 150, 0)
    blue_upper = (140, 255, 255)

    red_lower = (0, 70, 50)
    red_upper = (10, 255, 255)

    t = Video_Manager()

    t.track_and_draw(blue_lower, blue_upper, red_lower, red_upper, 'easy', is_one_player=True)

