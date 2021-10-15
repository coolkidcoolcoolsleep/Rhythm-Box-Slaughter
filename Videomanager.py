import glob, os
from PIL import Image
import cv2, sys
import random


class Video_Manager:
    # def __init__(self, img_width=1330, img_height=126):
    #     self.img_width = img_width
    #     self.img_height = img_height
    #     self.easy = 50
    #     self.norm = 40
    #     self.hard = 30
    #     self.red_color = (0, 0, 255)
    #     self.blue_color = (255, 0, 0)
    #     self.green_color = (0, 255, 0)
    #     self.white_color = (255, 255, 255)


    def video_load(self):
        # 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
        # 카메라를 VideoCapture 타입의 객체로 얻어옴
        vidcap = cv2.VideoCapture(0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전

            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(1330, 630))

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
                break

        vidcap.release()
        cv2.destroyAllWindows()

        return frame


    def ball_tracking(self):

    #     # num = 0
    #     # # 10 프레임당 1개의 박스 생성
    #     # seed_num = num // 10
    #     # random.seed(seed_num)
    #     # num = num + 1

        blue_lower = (100, 150, 0)
        blue_upper = (140, 255, 255)

        red_lower = (0, 70, 50)
        red_upper = (10, 255, 255)

        frame = self.video_load()
        detection_blue, detection_red = [], []

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
                detection_blue.append((x, y, w, h))
                print("blue: ", detection_blue)

        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        red_mask = cv2.erode(red_mask, None, iterations=2)
        red_mask = cv2.dilate(red_mask, None, iterations=2)
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                x, y, w, h = cv2.boundingRect(cnt)
                detection_red.append((x, y, w, h))
                print("red: ", detection_red)

        return detection_blue, detection_red

    # def ball_drawing(self):
    #
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
    #
    #     self.random_box(level, frame, is_one_player)
    #
    #     cv2.imshow('Rhythm Box Slaughter', frame)
    #
    #     pass


    # def rhythm_box_display_area(self, level, frame, is_one_player=True):
    #     # game_areas = self.load_data()
    #     # game_areas = frame
    #     area = frame
    #     display_areas = []
    #     # for area in game_areas:
    #     y, x, _ = area.shape  # (126, 266, 3)
    #     if not is_one_player:
    #         if level == 'easy':
    #             area1 = (0, 0), (x//2-self.easy, y-self.easy)       # (0, 0), (103, 96)
    #             area2 = (x//2, 0), (x-self.easy, y-self.easy)       # (133, 0), (236, 96)
    #             # print(area1, area2)
    #             display_areas.append((area1, area2))
    #         if level == 'norm':
    #             area1 = (0, 0), (x//2-self.norm, y-self.norm)       # (0, 0), (113, 106)
    #             area2 = (x//2, 0), (x-self.norm, y-self.norm)       # (133, 0), (246, 106)
    #             # print(area1, area2)
    #             display_areas.append((area1, area2))
    #         if level == 'hard':
    #             area1 = (0, 0), (x//2-self.hard, y-self.hard)       # (0, 0), (118, 111)
    #             area2 = (x//2, 0), (x-self.hard, y-self.hard)       # (133, 0), (251, 111)
    #             # print(area1, area2)
    #             display_areas.append((area1, area2))
    #     else:
    #         if level == 'easy':
    #             area1 = (0, 0), (x-self.easy, y-self.easy)          # (0, 0), (236, 96)
    #             # print(area1)
    #             display_areas.append(area1)
    #         if level == 'norm':
    #             area1 = (0, 0), (x-self.norm, y-self.norm)          # (0, 0), (246, 106)
    #             # print(area1)
    #             display_areas.append(area1)
    #         if level == 'hard':
    #             area1 = (0, 0), (x-self.hard, y-self.hard)          # (0, 0), (251, 111)
    #             # print(area1)
    #             display_areas.append(area1)
    #
    #     return display_areas

    # def random_box(self, level, frame, is_one_player=True):
    #     # img = self.load_data()[0]
    #
    #     img = frame
    #     areas = self.rhythm_box_display_area(level, frame, is_one_player)
    #     # (((30, 30), (103, 96)), ((163, 30), (236, 96)))
    #     cor_red, cor_blue = [], []
    #
    #     for area in areas:
    #         if not is_one_player:
    #             img = cv2.line(img, (133, 0), (133, 126), self.white_color, 2)
    #             area1, area2 = area
    #             (xs1, ys1), (xe1, ye1) = area1
    #             (xs2, ys2), (xe2, ye2) = area2
    #             a1, b1 = random.randint(xs1, xe1), random.randint(ys1, ye1)
    #             a2, b2 = random.randint(xs2, xe2), random.randint(ys2, ye2)
    #
    #             if level == 'easy':
    #                 cor_red.append((a1, b1, self.easy, self.easy))
    #                 cor_blue.append((a2, b2, self.easy, self.easy))
    #                 img = cv2.rectangle(img, (a1, b1), (a1+self.easy, b1+self.easy), self.red_color, 3)
    #                 img = cv2.rectangle(img, (a2, b2), (a2+self.easy, b2+self.easy), self.blue_color, 3)
    #             if level == 'norm':
    #                 img = cv2.rectangle(img, (a1, b1), (a1+self.norm, b1+self.norm), self.red_color, 3)
    #                 img = cv2.rectangle(img, (a2, b2), (a2+self.norm, b2+self.norm), self.blue_color, 3)
    #             if level == 'hard':
    #                 img = cv2.rectangle(img, (a1, b1), (a1+self.hard, b1+self.hard), self.red_color, 3)
    #                 img = cv2.rectangle(img, (a2, b2), (a2+self.hard, b2+self.hard), self.blue_color, 3)
    #         else:
    #             (xs1, ys1), (xe1, ye1) = area
    #             a, b = random.randint(xs1, xe1), random.randint(ys1, ye1)
    #             c, d = random.randint(xs1, xe1), random.randint(ys1, ye1)
    #             if level == 'easy':
    #                 img = cv2.rectangle(img, (a, b), (a + self.easy, b + self.easy), self.red_color, 3)
    #                 img = cv2.rectangle(img, (c, d), (c + self.easy, d + self.easy), self.blue_color, 3)
    #             if level == 'norm':
    #                 img = cv2.rectangle(img, (a, b), (a + self.norm, b + self.norm), self.red_color, 3)
    #                 img = cv2.rectangle(img, (c, d), (c + self.norm, d + self.norm), self.blue_color, 3)
    #             if level == 'hard':
    #                 img = cv2.rectangle(img, (a, b), (a + self.hard, b + self.hard), self.red_color, 3)
    #                 img = cv2.rectangle(img, (c, d), (c + self.hard, d + self.hard), self.blue_color, 3)
    #
    #     return cor_red, cor_blue
    #
    #     # cv2.imshow('rhythm_box', img)
    #     # cv2.waitKey(0)
    #     # cv2.imwrite(f'data/image_output/01.jpg', img)

    # 사각형 표현 방법 : (x1, y1, x2, y2)
    # 두 개의 사각형이 겹쳐지는지 확인
    # def overlap(rect1, rect2):
    # :param rect1: 랜덤으로 생성된 사각형
    # :param rect2: detection
    # :return: overlap이 되면 True, 아니면 False
    # return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or rect1[1] > rect2[3] or rect1[3] < rect2[1])

if __name__ == '__main__':

    v = Video_Manager()
    v.ball_tracking()
    # print(det_blue, det_red)