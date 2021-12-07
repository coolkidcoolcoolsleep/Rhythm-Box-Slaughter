import os
from PIL import Image
import cv2
import random
import time
from PIL import ImageFont, ImageDraw, Image
from imutils import resize
import numpy as np
import cvzone

class Video_Manager:
    def __init__(self):
        self.current_seed = 0
        self.is_answer_handled_red = False
        self.is_answer_handled_blue = False
        self.game_finish = False
        self.win_red = False
        self.win_blue = False
        self.all_draw = False

        # drawing_color
        self.blue_lower = (100, 150, 0)
        self.blue_upper = (140, 255, 255)
        self.red_lower = (-10, 100, 100)
        self.red_upper = (10, 255, 255)

        # 피부가 많이 잡힘
        # self.red_lower = (0, 70, 50)
        # self.red_upper = (10, 255, 255)

        # 살짝 피부 많이
        # self.red_lower = (0, 50, 20)
        # self.red_upper = (5, 255, 255)

        # level
        self.easy = 300
        self.norm = 250
        self.hard = 200
        self.hell = 170

        # color
        self.red_color = (203, 192, 255)
        self.blue_color = (223, 188, 80)
        self.green_color = (0, 255, 0)
        self.white_color = (255, 255, 255)

        self.red_gage_color = (199, 5, 0)
        self.blue_gage_color = (5, 75, 174)

        # score
        self.blue_score = 0
        self.red_score = 0

        # box
        self.BoxThreshold = 6

        # score
        self.blue_score = 0
        self.red_score = 0
        self.one_player_score = 0

        # area
        self.easy_min_area = self.easy * 30
        self.norm_min_area = self.norm * 30
        self.hard_min_area = self.hard * 30

        # display_size
        self.img_width = 1920
        self.img_height = 1080

        # player_num
        self.box_num = 0
        self.rect_num = 0
        self.frame_num = 0

        self.gage_loc = [20, 20]
        self.blue_gage_loc = [1075, 20]
        self.gage_size = (820, 60)
        self.text_loc = [845, 0]
        self.blue_text_loc = [self.img_width//2+5, 0]
        self.text_size = (100, 100)

        # 게이지 사이즈 (85, 920, 4)

        self.emtpy_gage = cv2.imread('data/gage/empty_gage.png', -1)
        self.emtpy_gage = cv2.resize(self.emtpy_gage, self.gage_size, -1)

        self.red_fill_1 = cv2.imread('data/gage/red_fill_1.png', -1)
        self.red_fill_1 = cv2.resize(self.red_fill_1, self.gage_size, -1)

        self.red_fill_2 = cv2.imread('data/gage/red_fill_2.png', -1)
        self.red_fill_2 = cv2.resize(self.red_fill_2, self.gage_size, -1)

        self.red_fill_3 = cv2.imread('data/gage/red_fill_3.png', -1)
        self.red_fill_3 = cv2.resize(self.red_fill_3, self.gage_size, -1)

        self.red_fill_4 = cv2.imread('data/gage/red_fill_4.png', -1)
        self.red_fill_4 = cv2.resize(self.red_fill_4, self.gage_size, -1)

        self.red_fill_5 = cv2.imread('data/gage/red_fill_5.png', -1)
        self.red_fill_5 = cv2.resize(self.red_fill_5, self.gage_size, -1)

        self.red_fill_6 = cv2.imread('data/gage/red_fill_6.png', -1)
        self.red_fill_6 = cv2.resize(self.red_fill_6, self.gage_size, -1)

        self.red_fill_7 = cv2.imread('data/gage/red_fill_7.png', -1)
        self.red_fill_7 = cv2.resize(self.red_fill_7, self.gage_size, -1)

        self.red_fill_8 = cv2.imread('data/gage/red_fill_8.png', -1)
        self.red_fill_8 = cv2.resize(self.red_fill_8, self.gage_size, -1)

        self.red_fill_9 = cv2.imread('data/gage/red_fill_9.png', -1)
        self.red_fill_9 = cv2.resize(self.red_fill_9, self.gage_size, -1)

        self.red_fill_10 = cv2.imread('data/gage/red_fill_10.png', -1)
        self.red_fill_10 = cv2.resize(self.red_fill_10, self.gage_size, -1)

        self.blue_fill_1 = cv2.imread('data/gage/blue_fill_1.png', -1)
        self.blue_fill_1 = cv2.resize(self.blue_fill_1, self.gage_size, -1)

        self.blue_fill_2 = cv2.imread('data/gage/blue_fill_2.png', -1)
        self.blue_fill_2 = cv2.resize(self.blue_fill_2, self.gage_size, -1)

        self.blue_fill_3 = cv2.imread('data/gage/blue_fill_3.png', -1)
        self.blue_fill_3 = cv2.resize(self.blue_fill_3, self.gage_size, -1)

        self.blue_fill_4 = cv2.imread('data/gage/blue_fill_4.png', -1)
        self.blue_fill_4 = cv2.resize(self.blue_fill_4, self.gage_size, -1)

        self.blue_fill_5 = cv2.imread('data/gage/blue_fill_5.png', -1)
        self.blue_fill_5 = cv2.resize(self.blue_fill_5, self.gage_size, -1)

        self.blue_fill_6 = cv2.imread('data/gage/blue_fill_6.png', -1)
        self.blue_fill_6 = cv2.resize(self.blue_fill_6, self.gage_size, -1)

        self.blue_fill_7 = cv2.imread('data/gage/blue_fill_7.png', -1)
        self.blue_fill_7 = cv2.resize(self.blue_fill_7, self.gage_size, -1)

        self.blue_fill_8 = cv2.imread('data/gage/blue_fill_8.png', -1)
        self.blue_fill_8 = cv2.resize(self.blue_fill_8, self.gage_size, -1)

        self.blue_fill_9 = cv2.imread('data/gage/blue_fill_9.png', -1)
        self.blue_fill_9 = cv2.resize(self.blue_fill_9, self.gage_size, -1)

        self.blue_fill_10 = cv2.imread('data/gage/blue_fill_10.png', -1)
        self.blue_fill_10 = cv2.resize(self.blue_fill_10, self.gage_size, -1)

        self.blue_fill_11 = cv2.imread('data/gage/blue_fill_11.png', -1)
        self.blue_fill_11 = cv2.resize(self.blue_fill_11, self.gage_size, -1)

        self.blue_fill_12 = cv2.imread('data/gage/blue_fill_12.png', -1)
        self.blue_fill_12 = cv2.resize(self.blue_fill_12, self.gage_size, -1)

        self.blue_fill_13 = cv2.imread('data/gage/blue_fill_13.png', -1)
        self.blue_fill_13 = cv2.resize(self.blue_fill_13, self.gage_size, -1)

        self.blue_fill_14 = cv2.imread('data/gage/blue_fill_14.png', -1)
        self.blue_fill_14 = cv2.resize(self.blue_fill_14, self.gage_size, -1)

        self.blue_fill_15 = cv2.imread('data/gage/blue_fill_15.png', -1)
        self.blue_fill_15 = cv2.resize(self.blue_fill_15, self.gage_size, -1)

        self.blue_fill_16 = cv2.imread('data/gage/blue_fill_16.png', -1)
        self.blue_fill_16 = cv2.resize(self.blue_fill_16, self.gage_size, -1)

        self.blue_fill_17 = cv2.imread('data/gage/blue_fill_17.png', -1)
        self.blue_fill_17 = cv2.resize(self.blue_fill_17, self.gage_size, -1)

        self.blue_fill_18 = cv2.imread('data/gage/blue_fill_18.png', -1)
        self.blue_fill_18 = cv2.resize(self.blue_fill_18, self.gage_size, -1)

        self.blue_fill_19 = cv2.imread('data/gage/blue_fill_19.png', -1)
        self.blue_fill_19 = cv2.resize(self.blue_fill_19, self.gage_size, -1)

        self.blue_fill_20 = cv2.imread('data/gage/blue_fill_20.png', -1)
        self.blue_fill_20 = cv2.resize(self.blue_fill_20, self.gage_size, -1)

        self.blue_fill_21 = cv2.imread('data/gage/blue_fill_21.png', -1)
        self.blue_fill_21 = cv2.resize(self.blue_fill_21, self.gage_size, -1)

        self.blue_fill_22 = cv2.imread('data/gage/blue_fill_22.png', -1)
        self.blue_fill_22 = cv2.resize(self.blue_fill_22, self.gage_size, -1)

        self.blue_fill_23 = cv2.imread('data/gage/blue_fill_23.png', -1)
        self.blue_fill_23 = cv2.resize(self.blue_fill_23, self.gage_size, -1)

        self.blue_fill_24 = cv2.imread('data/gage/blue_fill_24.png', -1)
        self.blue_fill_24 = cv2.resize(self.blue_fill_24, self.gage_size, -1)

        self.blue_fill_25 = cv2.imread('data/gage/blue_fill_25.png', -1)
        self.blue_fill_25 = cv2.resize(self.blue_fill_25, self.gage_size, -1)

        self.blue_fill_26 = cv2.imread('data/gage/blue_fill_26.png', -1)
        self.blue_fill_26 = cv2.resize(self.blue_fill_26, self.gage_size, -1)

        self.blue_fill_27 = cv2.imread('data/gage/blue_fill_27.png', -1)
        self.blue_fill_27 = cv2.resize(self.blue_fill_27, self.gage_size, -1)

        self.blue_fill_28 = cv2.imread('data/gage/blue_fill_28.png', -1)
        self.blue_fill_28 = cv2.resize(self.blue_fill_28, self.gage_size, -1)

        self.blue_fill_29 = cv2.imread('data/gage/blue_fill_29.png', -1)
        self.blue_fill_29 = cv2.resize(self.blue_fill_29, self.gage_size, -1)

        self.blue_fill_30 = cv2.imread('data/gage/blue_fill_30.png', -1)
        self.blue_fill_30 = cv2.resize(self.blue_fill_30, self.gage_size, -1)

        self.red_0 = cv2.imread('data/text/red_0.png', -1)
        self.red_0 = cv2.resize(self.red_0, self.text_size, -1)

        self.red_1 = cv2.imread('data/text/red_1.png', -1)
        self.red_1 = cv2.resize(self.red_1, self.text_size, -1)

        self.red_2 = cv2.imread('data/text/red_2.png', -1)
        self.red_2 = cv2.resize(self.red_2, self.text_size, -1)

        self.red_3 = cv2.imread('data/text/red_3.png', -1)
        self.red_3 = cv2.resize(self.red_3, self.text_size, -1)

        self.red_4 = cv2.imread('data/text/red_4.png', -1)
        self.red_4 = cv2.resize(self.red_4, self.text_size, -1)

        self.red_5 = cv2.imread('data/text/red_5.png', -1)
        self.red_5 = cv2.resize(self.red_5, self.text_size, -1)

        self.red_6 = cv2.imread('data/text/red_6.png', -1)
        self.red_6 = cv2.resize(self.red_6, self.text_size, -1)

        self.red_7 = cv2.imread('data/text/red_7.png', -1)
        self.red_7 = cv2.resize(self.red_7, self.text_size, -1)

        self.red_8 = cv2.imread('data/text/red_8.png', -1)
        self.red_8 = cv2.resize(self.red_8, self.text_size, -1)

        self.red_9 = cv2.imread('data/text/red_9.png', -1)
        self.red_9 = cv2.resize(self.red_9, self.text_size, -1)

        self.red_10 = cv2.imread('data/text/red_10.png', -1)
        self.red_10 = cv2.resize(self.red_10, self.text_size, -1)

        self.blue_0 = cv2.imread('data/text/blue_0.png', -1)
        self.blue_0 = cv2.resize(self.blue_0, self.text_size, -1)

        self.blue_1 = cv2.imread('data/text/blue_1.png', -1)
        self.blue_1 = cv2.resize(self.blue_1, self.text_size, -1)

        self.blue_2 = cv2.imread('data/text/blue_2.png', -1)
        self.blue_2 = cv2.resize(self.blue_2, self.text_size, -1)

        self.blue_3 = cv2.imread('data/text/blue_3.png', -1)
        self.blue_3 = cv2.resize(self.blue_3, self.text_size, -1)

        self.blue_4 = cv2.imread('data/text/blue_4.png', -1)
        self.blue_4 = cv2.resize(self.blue_4, self.text_size, -1)

        self.blue_5 = cv2.imread('data/text/blue_5.png', -1)
        self.blue_5 = cv2.resize(self.blue_5, self.text_size, -1)

        self.blue_6 = cv2.imread('data/text/blue_6.png', -1)
        self.blue_6 = cv2.resize(self.blue_6, self.text_size, -1)

        self.blue_7 = cv2.imread('data/text/blue_7.png', -1)
        self.blue_7 = cv2.resize(self.blue_7, self.text_size, -1)

        self.blue_8 = cv2.imread('data/text/blue_8.png', -1)
        self.blue_8 = cv2.resize(self.blue_8, self.text_size, -1)

        self.blue_9 = cv2.imread('data/text/blue_9.png', -1)
        self.blue_9 = cv2.resize(self.blue_9, self.text_size, -1)

        self.blue_10 = cv2.imread('data/text/blue_10.png', -1)
        self.blue_10 = cv2.resize(self.blue_10, self.text_size, -1)

        self.blue_11 = cv2.imread('data/text/blue_11.png', -1)
        self.blue_11 = cv2.resize(self.blue_11, self.text_size, -1)

        self.blue_12 = cv2.imread('data/text/blue_12.png', -1)
        self.blue_12 = cv2.resize(self.blue_12, self.text_size, -1)

        self.blue_13 = cv2.imread('data/text/blue_13.png', -1)
        self.blue_13 = cv2.resize(self.blue_13, self.text_size, -1)

        self.blue_14 = cv2.imread('data/text/blue_14.png', -1)
        self.blue_14 = cv2.resize(self.blue_14, self.text_size, -1)

        self.blue_15 = cv2.imread('data/text/blue_15.png', -1)
        self.blue_15 = cv2.resize(self.blue_15, self.text_size, -1)

        self.blue_16 = cv2.imread('data/text/blue_16.png', -1)
        self.blue_16 = cv2.resize(self.blue_16, self.text_size, -1)

        self.blue_17 = cv2.imread('data/text/blue_17.png', -1)
        self.blue_17 = cv2.resize(self.blue_17, self.text_size, -1)

        self.blue_18 = cv2.imread('data/text/blue_18.png', -1)
        self.blue_18 = cv2.resize(self.blue_18, self.text_size, -1)

        self.blue_19 = cv2.imread('data/text/blue_19.png', -1)
        self.blue_19 = cv2.resize(self.blue_19, self.text_size, -1)

        self.blue_20 = cv2.imread('data/text/blue_20.png', -1)
        self.blue_20 = cv2.resize(self.blue_20, self.text_size, -1)

        self.blue_21 = cv2.imread('data/text/blue_21.png', -1)
        self.blue_21 = cv2.resize(self.blue_21, self.text_size, -1)

        self.blue_22 = cv2.imread('data/text/blue_22.png', -1)
        self.blue_22 = cv2.resize(self.blue_22, self.text_size, -1)

        self.blue_23 = cv2.imread('data/text/blue_23.png', -1)
        self.blue_23 = cv2.resize(self.blue_23, self.text_size, -1)

        self.blue_24 = cv2.imread('data/text/blue_24.png', -1)
        self.blue_24 = cv2.resize(self.blue_24, self.text_size, -1)

        self.blue_25 = cv2.imread('data/text/blue_25.png', -1)
        self.blue_25 = cv2.resize(self.blue_25, self.text_size, -1)

        self.blue_26 = cv2.imread('data/text/blue_26.png', -1)
        self.blue_26 = cv2.resize(self.blue_26, self.text_size, -1)

        self.blue_27 = cv2.imread('data/text/blue_27.png', -1)
        self.blue_27 = cv2.resize(self.blue_27, self.text_size, -1)

        self.blue_28 = cv2.imread('data/text/blue_28.png', -1)
        self.blue_28 = cv2.resize(self.blue_28, self.text_size, -1)

        self.blue_29 = cv2.imread('data/text/blue_29.png', -1)
        self.blue_29 = cv2.resize(self.blue_29, self.text_size, -1)

        self.blue_30 = cv2.imread('data/text/blue_30.png', -1)
        self.blue_30 = cv2.resize(self.blue_30, self.text_size, -1)

        self.red_win = cv2.imread('data/text/red_win.png', -1)
        # self.red_win = cv2.resize(self.red_win, (500, 100), -1)

        self.red_lose = cv2.imread('data/text/red_lose.png', -1)
        # self.red_lose = cv2.resize(self.red_lose, (500, 100), -1)

        self.red_draw = cv2.imread('data/text/red_draw.png', -1)
        # self.red_draw = cv2.resize(self.red_draw, (500, 100), -1)

        self.blue_win = cv2.imread('data/text/blue_win.png', -1)
        # self.blue_win = cv2.resize(self.blue_win, (500, 100), -1)

        self.blue_lose = cv2.imread('data/text/blue_lose.png', -1)
        # self.blue_lose = cv2.resize(self.blue_lose, (500, 100), -1)

        self.blue_draw = cv2.imread('data/text/blue_draw.png', -1)
        # self.blue_draw = cv2.resize(self.blue_draw, (500, 100), -1)

        self.peace_r = cv2.imread('data/text/peace_r.png', -1)
        self.peace_r = cv2.resize(self.peace_r, (200, 200), -1)
        self.peace_l = cv2.imread('data/text/peace_l.png', -1)
        self.peace_l = cv2.resize(self.peace_l, (200, 200), -1)

        self.clap_r = cv2.imread('data/text/clap_r.png', -1)
        self.clap_l = cv2.imread('data/text/clap_l.png', -1)

    def load_video(self):
        # load_video
        # vidcap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
        vidcap = cv2.VideoCapture(0)

        # print(self.red_win.shape)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            exit()

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, (self.img_width, self.img_height))

            if self.game_finish == False:
                box_seed_num = self.box_num // 30
                random.seed(box_seed_num)
                self.box_num += 1

                detection_blue, detection_red = self.tracking_ball(frame)
                coordinate_red, coordinate_blue = self.random_box('easy', frame, is_one_player=False)

                if box_seed_num != self.current_seed:
                    self.is_answer_handled_red = False
                    self.is_answer_handled_blue = False

                rectangle_seed_num = self.rect_num % 3
                self.rect_num += 1

                # 점수 계산
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = self.score_calculation(frame,
                    rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num, detection_red, coordinate_red)

                # 정답 rect 그리기
                self.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                  is_answer_handled_blue)

                # 점수 표기
                frame = self.PlayerGameStats(frame, red_score, blue_score, is_one_player=False)

                self.frame_num = self.frame_num + 1
                if self.frame_num == 60:
                    self.game_finish = True
                if red_score > blue_score:
                    self.win_red = True
                elif red_score < blue_score:
                    self.win_blue = True
                elif red_score == blue_score:
                    self.all_draw = True
            else:
                frame = self.Winner_effect(frame, self.win_red, self.win_blue, self.all_draw, is_one_player=False)

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def tracking_ball(self, frame):
        detection_red = []
        detection_blue = []
        # GaussianBlur: 적용해서 노이즈와 이상치 줄임
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        blue_mask = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
        # erode: 개체 경계의 픽셀을 제거
        blue_mask = cv2.erode(blue_mask, None, iterations=2)
        # dilate: 공백으로 구분 된 연결 영역
        blue_mask = cv2.dilate(blue_mask, None, iterations=2)
        # 공의 윤곽선 찾기
        contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.easy_min_area: # easy 기준 6500
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                # detection_blue = [x, y, w, h]
                detection_blue.append([x, y, x + w, y + h])

        red_mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        # erode: 개체 경계의 픽셀을 제거
        red_mask = cv2.erode(red_mask, None, iterations=2)
        # dilate: 공백으로 구분 된 연결 영역
        red_mask = cv2.dilate(red_mask, None, iterations=2)
        # 공의 윤곽선 찾기
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.easy_min_area:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                # detection_red = [x, y, w, h]
                detection_red.append([x, y, x + w, y + h])
                # print("detection_red: ", x, y, w, h)

        return detection_blue[-1:], detection_red[-1:]

    def rhythm_box_display_area(self, level, frame):
        # game_areas = self.load_data()
        # game_areas = frame
        area = frame
        display_areas = []
        # for area in game_areas:
        # print(area.shape)
        y, x, _ = area.shape  # (1080, 1920, 3)
        if level == 'easy':
            area1 = (0, 80), (x // 2 - self.easy, y - self.easy)  # (0, 0), (760, 880)
            area2 = (x // 2, 80), (x - self.easy, y - self.easy)  # (960, 0), (1720, 880)
            # print(area1, area2)
            display_areas.append((area1, area2))
        if level == 'norm':
            area1 = (0, 80), (x // 2 - self.norm, y - self.norm)  # (0, 0), (113, 106)
            area2 = (x // 2, 80), (x - self.norm, y - self.norm)  # (133, 0), (246, 106)
            # print(area1, area2)
            display_areas.append((area1, area2))
        if level == 'hard':
            area1 = (0, 80), (x // 2 - self.hard, y - self.hard)  # (0, 0), (118, 111)
            area2 = (x // 2, 80), (x - self.hard, y - self.hard)  # (133, 0), (251, 111)
            # print(area1, area2)
            display_areas.append((area1, area2))
        return display_areas

    def random_box(self, level, frame, is_one_player=False):
        # img = self.load_data()[0]
        img = frame
        areas = self.rhythm_box_display_area(level, frame)
        coordinate_red, coordinate_blue = [], []
        # (((30, 30), (103, 96)), ((163, 30), (236, 96)))
        for area in areas:
            if not is_one_player:
                img = cv2.line(img, (self.img_width//2, 0), (self.img_width//2, self.img_height), self.white_color, 2)
            area1, area2 = area
            (xs1, ys1), (xe1, ye1) = area1
            (xs2, ys2), (xe2, ye2) = area2
            a1, b1 = random.randint(xs1, xe1), random.randint(ys1, ye1)
            a2, b2 = random.randint(xs2, xe2), random.randint(ys2, ye2)

            if level == 'easy':
                img = cv2.rectangle(img, (a1, b1), (a1 + self.easy, b1 + self.easy), self.red_color, 3)
                coordinate_red.append([a1, b1, a1 + self.easy, b1 + self.easy])
                img = cv2.rectangle(img, (a2, b2), (a2 + self.easy, b2 + self.easy), self.blue_color, 3)
                coordinate_blue.append([a2, b2, a2 + self.easy, b2 + self.easy])
            if level == 'norm':
                img = cv2.rectangle(img, (a1, b1), (a1 + self.norm, b1 + self.norm), self.red_color, 3)
                coordinate_red.append([a1, b1, a1 + self.norm, b1 + self.norm])
                img = cv2.rectangle(img, (a2, b2), (a2 + self.norm, b2 + self.norm), self.blue_color, 3)
                coordinate_blue.append([a2, b2, a2 + self.norm, b2 + self.norm])
            if level == 'hard':
                img = cv2.rectangle(img, (a1, b1), (a1 + self.hard, b1 + self.hard), self.red_color, 3)
                coordinate_red.append([a1, b1, a1 + self.hard, b1 + self.hard])
                img = cv2.rectangle(img, (a2, b2), (a2 + self.hard, b2 + self.hard), self.blue_color, 3)
                coordinate_blue.append([a2, b2, a2 + self.hard, b2 + self.hard])
        return coordinate_red, coordinate_blue

    def isRectangleOverlap(self, detection_rect, coordinate_rect, BoxThreshold):
        if detection_rect and coordinate_rect:
            if (coordinate_rect[0][0]-BoxThreshold <= detection_rect[0][0] <= coordinate_rect[0][2]+BoxThreshold) and \
                (coordinate_rect[0][0]-BoxThreshold <= detection_rect[0][2] <= coordinate_rect[0][2]+BoxThreshold) and \
                (coordinate_rect[0][1]-BoxThreshold <= detection_rect[0][1] <= coordinate_rect[0][3]+BoxThreshold) and \
                    (coordinate_rect[0][1]-BoxThreshold <= detection_rect[0][3] <= coordinate_rect[0][3]+BoxThreshold):
                return True
            else: return False
        else: False

    def score_calculation(self, frame, rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num,
                          detection_red, coordinate_red):
        if rectangle_seed_num == 0:
            if self.isRectangleOverlap(detection_blue, coordinate_blue,
                                       self.BoxThreshold) and not self.is_answer_handled_red:
                self.current_seed = box_seed_num
                self.is_answer_handled_red = True
                self.blue_score += 1

            if self.isRectangleOverlap(detection_red, coordinate_red,
                                       self.BoxThreshold) and not self.is_answer_handled_blue:
                self.current_seed = box_seed_num
                self.is_answer_handled_blue = True
                self.red_score += 1

        return self.blue_score, self.red_score, self.is_answer_handled_red, self.is_answer_handled_blue

    def Drawing_Rectangle(self, frame, coordinate_blue, coordinate_red, is_answer_handled_red, is_answer_handled_blue):
        if self.is_answer_handled_red:
            cv2.rectangle(frame, (coordinate_blue[0][0], coordinate_blue[0][1]),
                          (coordinate_blue[0][2], coordinate_blue[0][3]), self.green_color, 3)

        if self.is_answer_handled_blue:
            cv2.rectangle(frame, (coordinate_red[0][0], coordinate_red[0][1]),
                          (coordinate_red[0][2], coordinate_red[0][3]), self.green_color, 3)

    def Winner_effect(self, frame, win_red, win_blue, all_draw, is_one_player=False):
        if not is_one_player:
            img = frame
            img = cv2.line(img, (self.img_width // 2, 0), (self.img_width // 2, self.img_height), self.white_color, 2)
            if win_red:
                # red 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.red_win, [(1920 // 4) - 200, (1080 // 2) - 100])
                frame = cvzone.overlayPNG(frame, self.clap_l, [(1920 // 4) - 400, (1080 // 2) - 100])
                # blue 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.blue_lose, [(1920 // 2) + 200, (1080 // 2) - 100])
            elif win_blue:
                # red 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.red_lose, [(1920 // 4) - 200, (1080 // 2) - 100])
                # blue 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.blue_win, [(1920 // 2) + 200, (1080 // 2) - 100])
                frame = cvzone.overlayPNG(frame, self.clap_r, [(1920 // 4) + 600, (1080 // 2) - 100])
            elif all_draw:
                # red 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.red_draw, [(1920 // 4) - 200, (1080 // 2) - 100])
                frame = cvzone.overlayPNG(frame, self.peace_l, [self.img_width // 2-300, self.img_height // 2 - 200])
                # blue 영역 화면 출력
                frame = cvzone.overlayPNG(frame, self.blue_draw, [(1920 // 2) + 200, (1080 // 2) - 100])
                frame = cvzone.overlayPNG(frame, self.peace_r, [self.img_width // 2+100, self.img_height // 2 - 200])
        # else:
        #     # 0-19:Poor
        #     if 0 < self.sum_score < 20:
        #         frame = cvzone.overlayPNG(frame, self.poor, [self.img_width // 2, self.img_height // 2])
        #     # 20-29:Not Bad
        #     if 20 < self.sum_score < 29:
        #         frame = cvzone.overlayPNG(frame, self.not_bad, [self.img_width // 2, self.img_height // 2])
            # 30-49:Good
            # 50-59:Excellent
            # 60:Splendid
        return frame

    def PlayerGameStats(self, frame, red_score, blue_score, is_one_player=False):
        if red_score == 0:
            # 왼쪽 숫자
            frame = cvzone.overlayPNG(frame, self.emtpy_gage, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_0, self.text_loc)
        elif red_score == 1:
            frame = cvzone.overlayPNG(frame, self.red_fill_1, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_1, self.text_loc)
        elif red_score == 2:
            frame = cvzone.overlayPNG(frame, self.red_fill_2, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_2, self.text_loc)
        elif red_score == 3:
            frame = cvzone.overlayPNG(frame, self.red_fill_3, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_3, self.text_loc)
        elif red_score == 4:
            frame = cvzone.overlayPNG(frame, self.red_fill_4, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_4, self.text_loc)
        elif red_score == 5:
            frame = cvzone.overlayPNG(frame, self.red_fill_5, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_5, self.text_loc)
        elif red_score == 6:
            frame = cvzone.overlayPNG(frame, self.red_fill_6, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_6, self.text_loc)
        elif red_score == 7:
            frame = cvzone.overlayPNG(frame, self.red_fill_7, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_7, self.text_loc)
        elif red_score == 8:
            frame = cvzone.overlayPNG(frame, self.red_fill_8, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_8, self.text_loc)
        elif red_score == 9:
            frame = cvzone.overlayPNG(frame, self.red_fill_9, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_9, self.text_loc)
        elif red_score == 10:
            frame = cvzone.overlayPNG(frame, self.red_fill_10, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_10, self.text_loc)
        elif red_score == 11:
            frame = cvzone.overlayPNG(frame, self.red_fill_11, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_11, self.text_loc)
        elif red_score == 12:
            frame = cvzone.overlayPNG(frame, self.red_fill_12, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_12, self.text_loc)
        elif red_score == 13:
            frame = cvzone.overlayPNG(frame, self.red_fill_13, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_13, self.text_loc)
        elif red_score == 14:
            frame = cvzone.overlayPNG(frame, self.red_fill_14, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_14, self.text_loc)
        elif red_score == 15:
            frame = cvzone.overlayPNG(frame, self.red_fill_15, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_15, self.text_loc)
        elif red_score == 16:
            frame = cvzone.overlayPNG(frame, self.red_fill_16, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_16, self.text_loc)
        elif red_score == 17:
            frame = cvzone.overlayPNG(frame, self.red_fill_17, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_17, self.text_loc)
        elif red_score == 18:
            frame = cvzone.overlayPNG(frame, self.red_fill_18, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_18, self.text_loc)
        elif red_score == 19:
            frame = cvzone.overlayPNG(frame, self.red_fill_19, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_19, self.text_loc)
        elif red_score == 20:
            frame = cvzone.overlayPNG(frame, self.red_fill_20, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_20, self.text_loc)
        elif red_score == 21:
            frame = cvzone.overlayPNG(frame, self.red_fill_21, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_21, self.text_loc)
        elif red_score == 22:
            frame = cvzone.overlayPNG(frame, self.red_fill_22, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_22, self.text_loc)
        elif red_score == 23:
            frame = cvzone.overlayPNG(frame, self.red_fill_23, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_23, self.text_loc)
        elif red_score == 24:
            frame = cvzone.overlayPNG(frame, self.red_fill_24, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_24, self.text_loc)
        elif red_score == 25:
            frame = cvzone.overlayPNG(frame, self.red_fill_25, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_25, self.text_loc)
        elif red_score == 26:
            frame = cvzone.overlayPNG(frame, self.red_fill_26, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_26, self.text_loc)
        elif red_score == 27:
            frame = cvzone.overlayPNG(frame, self.red_fill_27, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_27, self.text_loc)
        elif red_score == 28:
            frame = cvzone.overlayPNG(frame, self.red_fill_28, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_28, self.text_loc)
        elif red_score == 29:
            frame = cvzone.overlayPNG(frame, self.red_fill_29, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_29, self.text_loc)
        elif red_score == 30:
            frame = cvzone.overlayPNG(frame, self.red_fill_30, self.gage_loc)
            frame = cvzone.overlayPNG(frame, self.red_30, self.text_loc)

        if blue_score == 0:
            frame = cvzone.overlayPNG(frame, self.emtpy_gage, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_0, self.blue_text_loc)
        elif blue_score == 1:
            frame = cvzone.overlayPNG(frame, self.blue_fill_1, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_1, self.blue_text_loc)
        elif blue_score == 2:
            frame = cvzone.overlayPNG(frame, self.blue_fill_2, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_2, self.blue_text_loc)
        elif blue_score == 3:
            frame = cvzone.overlayPNG(frame, self.blue_fill_3, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_3, self.blue_text_loc)
        elif blue_score == 4:
            frame = cvzone.overlayPNG(frame, self.blue_fill_4, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_4, self.blue_text_loc)
        elif blue_score == 5:
            frame = cvzone.overlayPNG(frame, self.blue_fill_5, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_5, self.blue_text_loc)
        elif blue_score == 6:
            frame = cvzone.overlayPNG(frame, self.blue_fill_6, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_6, self.blue_text_loc)
        elif blue_score == 7:
            frame = cvzone.overlayPNG(frame, self.blue_fill_7, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_7, self.blue_text_loc)
        elif blue_score == 8:
            frame = cvzone.overlayPNG(frame, self.blue_fill_8, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_8, self.blue_text_loc)
        elif blue_score == 9:
            frame = cvzone.overlayPNG(frame, self.blue_fill_9, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_9, self.blue_text_loc)
        elif blue_score == 10:
            frame = cvzone.overlayPNG(frame, self.blue_fill_10, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_10, self.blue_text_loc)
        elif blue_score == 11:
            frame = cvzone.overlayPNG(frame, self.blue_fill_11, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_11, self.blue_text_loc)
        elif blue_score == 12:
            frame = cvzone.overlayPNG(frame, self.blue_fill_12, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_12, self.blue_text_loc)
        elif blue_score == 13:
            frame = cvzone.overlayPNG(frame, self.blue_fill_13, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_13, self.blue_text_loc)
        elif blue_score == 14:
            frame = cvzone.overlayPNG(frame, self.blue_fill_14, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_14, self.blue_text_loc)
        elif blue_score == 15:
            frame = cvzone.overlayPNG(frame, self.blue_fill_15, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_15, self.blue_text_loc)
        elif blue_score == 16:
            frame = cvzone.overlayPNG(frame, self.blue_fill_16, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_16, self.blue_text_loc)
        elif blue_score == 17:
            frame = cvzone.overlayPNG(frame, self.blue_fill_17, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_17, self.blue_text_loc)
        elif blue_score == 18:
            frame = cvzone.overlayPNG(frame, self.blue_fill_18, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_18, self.blue_text_loc)
        elif blue_score == 19:
            frame = cvzone.overlayPNG(frame, self.blue_fill_19, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_19, self.blue_text_loc)
        elif blue_score == 20:
            frame = cvzone.overlayPNG(frame, self.blue_fill_20, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_20, self.blue_text_loc)
        elif blue_score == 21:
            frame = cvzone.overlayPNG(frame, self.blue_fill_21, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_21, self.blue_text_loc)
        elif blue_score == 22:
            frame = cvzone.overlayPNG(frame, self.blue_fill_22, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_22, self.blue_text_loc)
        elif blue_score == 23:
            frame = cvzone.overlayPNG(frame, self.blue_fill_23, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_23, self.blue_text_loc)
        elif blue_score == 24:
            frame = cvzone.overlayPNG(frame, self.blue_fill_24, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_24, self.blue_text_loc)
        elif blue_score == 25:
            frame = cvzone.overlayPNG(frame, self.blue_fill_25, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_25, self.blue_text_loc)
        elif blue_score == 26:
            frame = cvzone.overlayPNG(frame, self.blue_fill_26, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_26, self.blue_text_loc)
        elif blue_score == 27:
            frame = cvzone.overlayPNG(frame, self.blue_fill_27, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_27, self.blue_text_loc)
        elif blue_score == 28:
            frame = cvzone.overlayPNG(frame, self.blue_fill_28, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_28, self.blue_text_loc)
        elif blue_score == 29:
            frame = cvzone.overlayPNG(frame, self.blue_fill_29, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_29, self.blue_text_loc)
        elif blue_score == 30:
            frame = cvzone.overlayPNG(frame, self.blue_fill_30, self.blue_gage_loc)
            frame = cvzone.overlayPNG(frame, self.blue_30, self.blue_text_loc)

        return frame

if __name__ == '__main__':
    v = Video_Manager()
    v.load_video()