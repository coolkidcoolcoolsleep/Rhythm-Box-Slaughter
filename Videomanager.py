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
        self.one_player_result = 0

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

        # box
        self.BoxThreshold = 6

        # score
        self.blue_score = 0
        self.red_score = 0
        self.sum_score = 0
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
        self.purple_gage_loc = [150, 30]
        self.gage_size = (820, 60)
        self.gage_size_1p = (1720, 60)
        self.text_loc = [850, 0]
        self.text_loc_1p = [30, 10]
        self.blue_text_loc = [self.img_width//2+5, 0]
        self.text_size = (100, 100)
        self.text_size_1p = (100, 100)


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

        self.red_fill_11 = cv2.imread('data/gage/red_fill_11.png', -1)
        self.red_fill_11 = cv2.resize(self.red_fill_11, self.gage_size, -1)

        self.red_fill_12 = cv2.imread('data/gage/red_fill_12.png', -1)
        self.red_fill_12 = cv2.resize(self.red_fill_12, self.gage_size, -1)

        self.red_fill_13 = cv2.imread('data/gage/red_fill_13.png', -1)
        self.red_fill_13 = cv2.resize(self.red_fill_13, self.gage_size, -1)

        self.red_fill_14 = cv2.imread('data/gage/red_fill_14.png', -1)
        self.red_fill_14 = cv2.resize(self.red_fill_14, self.gage_size, -1)

        self.red_fill_15 = cv2.imread('data/gage/red_fill_15.png', -1)
        self.red_fill_15 = cv2.resize(self.red_fill_15, self.gage_size, -1)

        self.red_fill_16 = cv2.imread('data/gage/red_fill_16.png', -1)
        self.red_fill_16 = cv2.resize(self.red_fill_16, self.gage_size, -1)

        self.red_fill_17 = cv2.imread('data/gage/red_fill_17.png', -1)
        self.red_fill_17 = cv2.resize(self.red_fill_17, self.gage_size, -1)

        self.red_fill_18 = cv2.imread('data/gage/red_fill_18.png', -1)
        self.red_fill_18 = cv2.resize(self.red_fill_18, self.gage_size, -1)

        self.red_fill_19 = cv2.imread('data/gage/red_fill_19.png', -1)
        self.red_fill_19 = cv2.resize(self.red_fill_19, self.gage_size, -1)

        self.red_fill_20 = cv2.imread('data/gage/red_fill_20.png', -1)
        self.red_fill_20 = cv2.resize(self.red_fill_20, self.gage_size, -1)

        self.red_fill_21 = cv2.imread('data/gage/red_fill_21.png', -1)
        self.red_fill_21 = cv2.resize(self.red_fill_21, self.gage_size, -1)

        self.red_fill_22 = cv2.imread('data/gage/red_fill_22.png', -1)
        self.red_fill_22 = cv2.resize(self.red_fill_22, self.gage_size, -1)

        self.red_fill_23 = cv2.imread('data/gage/red_fill_23.png', -1)
        self.red_fill_23 = cv2.resize(self.red_fill_23, self.gage_size, -1)

        self.red_fill_24 = cv2.imread('data/gage/red_fill_24.png', -1)
        self.red_fill_24 = cv2.resize(self.red_fill_24, self.gage_size, -1)

        self.red_fill_25 = cv2.imread('data/gage/red_fill_25.png', -1)
        self.red_fill_25 = cv2.resize(self.red_fill_25, self.gage_size, -1)

        self.red_fill_26 = cv2.imread('data/gage/red_fill_26.png', -1)
        self.red_fill_26 = cv2.resize(self.red_fill_26, self.gage_size, -1)

        self.red_fill_27 = cv2.imread('data/gage/red_fill_27.png', -1)
        self.red_fill_27 = cv2.resize(self.red_fill_27, self.gage_size, -1)

        self.red_fill_28 = cv2.imread('data/gage/red_fill_28.png', -1)
        self.red_fill_28 = cv2.resize(self.red_fill_28, self.gage_size, -1)

        self.red_fill_29 = cv2.imread('data/gage/red_fill_29.png', -1)
        self.red_fill_29 = cv2.resize(self.red_fill_29, self.gage_size, -1)

        self.red_fill_30 = cv2.imread('data/gage/red_fill_30.png', -1)
        self.red_fill_30 = cv2.resize(self.red_fill_30, self.gage_size, -1)

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

        # (80, 1500, 4)
        self.purple_fill_0 = cv2.imread('data/gage/purple_0.png', -1)
        self.purple_fill_0 = cv2.resize(self.purple_fill_0, self.gage_size_1p, -1)

        self.purple_fill_1 = cv2.imread('data/gage/purple_1.png', -1)
        self.purple_fill_1 = cv2.resize(self.purple_fill_1, self.gage_size_1p, -1)

        self.purple_fill_2 = cv2.imread('data/gage/purple_2.png', -1)
        self.purple_fill_2 = cv2.resize(self.purple_fill_2, self.gage_size_1p, -1)

        self.purple_fill_3 = cv2.imread('data/gage/purple_3.png', -1)
        self.purple_fill_3 = cv2.resize(self.purple_fill_3, self.gage_size_1p, -1)

        self.purple_fill_4 = cv2.imread('data/gage/purple_4.png', -1)
        self.purple_fill_4 = cv2.resize(self.purple_fill_4, self.gage_size_1p, -1)

        self.purple_fill_5 = cv2.imread('data/gage/purple_5.png', -1)
        self.purple_fill_5 = cv2.resize(self.purple_fill_5, self.gage_size_1p, -1)

        self.purple_fill_6 = cv2.imread('data/gage/purple_6.png', -1)
        self.purple_fill_6 = cv2.resize(self.purple_fill_6, self.gage_size_1p, -1)

        self.purple_fill_7 = cv2.imread('data/gage/purple_7.png', -1)
        self.purple_fill_7 = cv2.resize(self.purple_fill_7, self.gage_size_1p, -1)

        self.purple_fill_8 = cv2.imread('data/gage/purple_8.png', -1)
        self.purple_fill_8 = cv2.resize(self.purple_fill_8, self.gage_size_1p, -1)

        self.purple_fill_9 = cv2.imread('data/gage/purple_9.png', -1)
        self.purple_fill_9 = cv2.resize(self.purple_fill_9, self.gage_size_1p, -1)

        self.purple_fill_10 = cv2.imread('data/gage/purple_10.png', -1)
        self.purple_fill_10 = cv2.resize(self.purple_fill_10, self.gage_size_1p, -1)

        self.purple_fill_11 = cv2.imread('data/gage/purple_11.png', -1)
        self.purple_fill_11 = cv2.resize(self.purple_fill_11, self.gage_size_1p, -1)

        self.purple_fill_12 = cv2.imread('data/gage/purple_12.png', -1)
        self.purple_fill_12 = cv2.resize(self.purple_fill_12, self.gage_size_1p, -1)

        self.purple_fill_13 = cv2.imread('data/gage/purple_13.png', -1)
        self.purple_fill_13 = cv2.resize(self.purple_fill_13, self.gage_size_1p, -1)

        self.purple_fill_14 = cv2.imread('data/gage/purple_14.png', -1)
        self.purple_fill_14 = cv2.resize(self.purple_fill_14, self.gage_size_1p, -1)

        self.purple_fill_15 = cv2.imread('data/gage/purple_15.png', -1)
        self.purple_fill_15 = cv2.resize(self.purple_fill_15, self.gage_size_1p, -1)

        self.purple_fill_16 = cv2.imread('data/gage/purple_16.png', -1)
        self.purple_fill_16 = cv2.resize(self.purple_fill_16, self.gage_size_1p, -1)

        self.purple_fill_17 = cv2.imread('data/gage/purple_17.png', -1)
        self.purple_fill_17 = cv2.resize(self.purple_fill_17, self.gage_size_1p, -1)

        self.purple_fill_18 = cv2.imread('data/gage/purple_18.png', -1)
        self.purple_fill_18 = cv2.resize(self.purple_fill_18, self.gage_size_1p, -1)

        self.purple_fill_19 = cv2.imread('data/gage/purple_19.png', -1)
        self.purple_fill_19 = cv2.resize(self.purple_fill_19, self.gage_size_1p, -1)

        self.purple_fill_20 = cv2.imread('data/gage/purple_20.png', -1)
        self.purple_fill_20 = cv2.resize(self.purple_fill_20, self.gage_size_1p, -1)

        self.purple_fill_21 = cv2.imread('data/gage/purple_21.png', -1)
        self.purple_fill_21 = cv2.resize(self.purple_fill_21, self.gage_size_1p, -1)

        self.purple_fill_22 = cv2.imread('data/gage/purple_22.png', -1)
        self.purple_fill_22 = cv2.resize(self.purple_fill_22, self.gage_size_1p, -1)

        self.purple_fill_23 = cv2.imread('data/gage/purple_23.png', -1)
        self.purple_fill_23 = cv2.resize(self.purple_fill_23, self.gage_size_1p, -1)

        self.purple_fill_24 = cv2.imread('data/gage/purple_24.png', -1)
        self.purple_fill_24 = cv2.resize(self.purple_fill_24, self.gage_size_1p, -1)

        self.purple_fill_25 = cv2.imread('data/gage/purple_25.png', -1)
        self.purple_fill_25 = cv2.resize(self.purple_fill_25, self.gage_size_1p, -1)

        self.purple_fill_26 = cv2.imread('data/gage/purple_26.png', -1)
        self.purple_fill_26 = cv2.resize(self.purple_fill_26, self.gage_size_1p, -1)

        self.purple_fill_27 = cv2.imread('data/gage/purple_27.png', -1)
        self.purple_fill_27 = cv2.resize(self.purple_fill_27, self.gage_size_1p, -1)

        self.purple_fill_28 = cv2.imread('data/gage/purple_28.png', -1)
        self.purple_fill_28 = cv2.resize(self.purple_fill_28, self.gage_size_1p, -1)

        self.purple_fill_29 = cv2.imread('data/gage/purple_29.png', -1)
        self.purple_fill_29 = cv2.resize(self.purple_fill_29, self.gage_size_1p, -1)

        self.purple_fill_30 = cv2.imread('data/gage/purple_30.png', -1)
        self.purple_fill_30 = cv2.resize(self.purple_fill_30, self.gage_size_1p, -1)

        self.purple_fill_31 = cv2.imread('data/gage/purple_31.png', -1)
        self.purple_fill_31 = cv2.resize(self.purple_fill_31, self.gage_size_1p, -1)

        self.purple_fill_32 = cv2.imread('data/gage/purple_32.png', -1)
        self.purple_fill_32 = cv2.resize(self.purple_fill_32, self.gage_size_1p, -1)

        self.purple_fill_33 = cv2.imread('data/gage/purple_33.png', -1)
        self.purple_fill_33 = cv2.resize(self.purple_fill_33, self.gage_size_1p, -1)

        self.purple_fill_34 = cv2.imread('data/gage/purple_34.png', -1)
        self.purple_fill_34 = cv2.resize(self.purple_fill_34, self.gage_size_1p, -1)

        self.purple_fill_35 = cv2.imread('data/gage/purple_35.png', -1)
        self.purple_fill_35 = cv2.resize(self.purple_fill_35, self.gage_size_1p, -1)

        self.purple_fill_36 = cv2.imread('data/gage/purple_36.png', -1)
        self.purple_fill_36 = cv2.resize(self.purple_fill_36, self.gage_size_1p, -1)

        self.purple_fill_37 = cv2.imread('data/gage/purple_37.png', -1)
        self.purple_fill_37 = cv2.resize(self.purple_fill_37, self.gage_size_1p, -1)

        self.purple_fill_38 = cv2.imread('data/gage/purple_38.png', -1)
        self.purple_fill_38 = cv2.resize(self.purple_fill_38, self.gage_size_1p, -1)

        self.purple_fill_39 = cv2.imread('data/gage/purple_39.png', -1)
        self.purple_fill_39 = cv2.resize(self.purple_fill_39, self.gage_size_1p, -1)

        self.purple_fill_40 = cv2.imread('data/gage/purple_40.png', -1)
        self.purple_fill_40 = cv2.resize(self.purple_fill_40, self.gage_size_1p, -1)

        self.purple_fill_41 = cv2.imread('data/gage/purple_41.png', -1)
        self.purple_fill_41 = cv2.resize(self.purple_fill_41, self.gage_size_1p, -1)

        self.purple_fill_42 = cv2.imread('data/gage/purple_42.png', -1)
        self.purple_fill_42 = cv2.resize(self.purple_fill_42, self.gage_size_1p, -1)

        self.purple_fill_43 = cv2.imread('data/gage/purple_43.png', -1)
        self.purple_fill_43 = cv2.resize(self.purple_fill_43, self.gage_size_1p, -1)

        self.purple_fill_44 = cv2.imread('data/gage/purple_44.png', -1)
        self.purple_fill_44 = cv2.resize(self.purple_fill_44, self.gage_size_1p, -1)

        self.purple_fill_45 = cv2.imread('data/gage/purple_45.png', -1)
        self.purple_fill_45 = cv2.resize(self.purple_fill_45, self.gage_size_1p, -1)

        self.purple_fill_46 = cv2.imread('data/gage/purple_46.png', -1)
        self.purple_fill_46 = cv2.resize(self.purple_fill_46, self.gage_size_1p, -1)

        self.purple_fill_47 = cv2.imread('data/gage/purple_47.png', -1)
        self.purple_fill_47 = cv2.resize(self.purple_fill_47, self.gage_size_1p, -1)

        self.purple_fill_48 = cv2.imread('data/gage/purple_48.png', -1)
        self.purple_fill_48 = cv2.resize(self.purple_fill_48, self.gage_size_1p, -1)

        self.purple_fill_49 = cv2.imread('data/gage/purple_49.png', -1)
        self.purple_fill_49 = cv2.resize(self.purple_fill_49, self.gage_size_1p, -1)

        self.purple_fill_50 = cv2.imread('data/gage/purple_50.png', -1)
        self.purple_fill_50 = cv2.resize(self.purple_fill_50, self.gage_size_1p, -1)

        self.purple_fill_51 = cv2.imread('data/gage/purple_51.png', -1)
        self.purple_fill_51 = cv2.resize(self.purple_fill_51, self.gage_size_1p, -1)

        self.purple_fill_52 = cv2.imread('data/gage/purple_52.png', -1)
        self.purple_fill_52 = cv2.resize(self.purple_fill_52, self.gage_size_1p, -1)

        self.purple_fill_53 = cv2.imread('data/gage/purple_53.png', -1)
        self.purple_fill_53 = cv2.resize(self.purple_fill_53, self.gage_size_1p, -1)

        self.purple_fill_54 = cv2.imread('data/gage/purple_54.png', -1)
        self.purple_fill_54 = cv2.resize(self.purple_fill_54, self.gage_size_1p, -1)

        self.purple_fill_55 = cv2.imread('data/gage/purple_55.png', -1)
        self.purple_fill_55 = cv2.resize(self.purple_fill_55, self.gage_size_1p, -1)

        self.purple_fill_56 = cv2.imread('data/gage/purple_56.png', -1)
        self.purple_fill_56 = cv2.resize(self.purple_fill_56, self.gage_size_1p, -1)

        self.purple_fill_57 = cv2.imread('data/gage/purple_57.png', -1)
        self.purple_fill_57 = cv2.resize(self.purple_fill_57, self.gage_size_1p, -1)

        self.purple_fill_58 = cv2.imread('data/gage/purple_58.png', -1)
        self.purple_fill_58 = cv2.resize(self.purple_fill_58, self.gage_size_1p, -1)

        self.purple_fill_59 = cv2.imread('data/gage/purple_59.png', -1)
        self.purple_fill_59 = cv2.resize(self.purple_fill_59, self.gage_size_1p, -1)

        self.purple_fill_60 = cv2.imread('data/gage/purple_10.png', -1)
        self.purple_fill_60 = cv2.resize(self.purple_fill_60, self.gage_size_1p, -1)

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

        self.red_10 = cv2.imread('data/text/red_10.png', -1)
        self.red_10 = cv2.resize(self.red_10, self.text_size, -1)

        self.red_11 = cv2.imread('data/text/red_11.png', -1)
        self.red_11 = cv2.resize(self.red_11, self.text_size, -1)

        self.red_12 = cv2.imread('data/text/red_12.png', -1)
        self.red_12 = cv2.resize(self.red_12, self.text_size, -1)

        self.red_13 = cv2.imread('data/text/red_13.png', -1)
        self.red_13 = cv2.resize(self.red_13, self.text_size, -1)

        self.red_14 = cv2.imread('data/text/red_14.png', -1)
        self.red_14 = cv2.resize(self.red_14, self.text_size, -1)

        self.red_15 = cv2.imread('data/text/red_15.png', -1)
        self.red_15 = cv2.resize(self.red_15, self.text_size, -1)

        self.red_16 = cv2.imread('data/text/red_16.png', -1)
        self.red_16 = cv2.resize(self.red_16, self.text_size, -1)

        self.red_17 = cv2.imread('data/text/red_17.png', -1)
        self.red_17 = cv2.resize(self.red_17, self.text_size, -1)

        self.red_18 = cv2.imread('data/text/red_18.png', -1)
        self.red_18 = cv2.resize(self.red_18, self.text_size, -1)

        self.red_19 = cv2.imread('data/text/red_19.png', -1)
        self.red_19 = cv2.resize(self.red_19, self.text_size, -1)

        self.red_20 = cv2.imread('data/text/red_20.png', -1)
        self.red_20 = cv2.resize(self.red_20, self.text_size, -1)

        self.red_21 = cv2.imread('data/text/red_21.png', -1)
        self.red_21 = cv2.resize(self.red_21, self.text_size, -1)

        self.red_22 = cv2.imread('data/text/red_22.png', -1)
        self.red_22 = cv2.resize(self.red_22, self.text_size, -1)

        self.red_23 = cv2.imread('data/text/red_23.png', -1)
        self.red_23 = cv2.resize(self.red_23, self.text_size, -1)

        self.red_24 = cv2.imread('data/text/red_24.png', -1)
        self.red_24 = cv2.resize(self.red_24, self.text_size, -1)

        self.red_25 = cv2.imread('data/text/red_25.png', -1)
        self.red_25 = cv2.resize(self.red_25, self.text_size, -1)

        self.red_26 = cv2.imread('data/text/red_26.png', -1)
        self.red_26 = cv2.resize(self.red_26, self.text_size, -1)

        self.red_27 = cv2.imread('data/text/red_27.png', -1)
        self.red_27 = cv2.resize(self.red_27, self.text_size, -1)

        self.red_28 = cv2.imread('data/text/red_28.png', -1)
        self.red_28 = cv2.resize(self.red_28, self.text_size, -1)

        self.red_29 = cv2.imread('data/text/red_29.png', -1)
        self.red_29 = cv2.resize(self.red_29, self.text_size, -1)

        self.red_30 = cv2.imread('data/text/red_30.png', -1)
        self.red_30 = cv2.resize(self.red_30, self.text_size, -1)

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

        self.purple_0 = cv2.imread('data/text/blue_30.png', -1)
        self.blue_30 = cv2.resize(self.blue_30, self.text_size, -1)

        self.purple_0 = cv2.imread('data/text/purple_0.png', -1)
        self.purple_0 = cv2.resize(self.purple_0, self.text_size_1p, -1)

        self.purple_1 = cv2.imread('data/text/purple_1.png', -1)
        self.purple_1 = cv2.resize(self.purple_1, self.text_size_1p, -1)

        self.purple_2 = cv2.imread('data/text/purple_2.png', -1)
        self.purple_2 = cv2.resize(self.purple_2, self.text_size_1p, -1)

        self.purple_3 = cv2.imread('data/text/purple_3.png', -1)
        self.purple_3 = cv2.resize(self.purple_3, self.text_size_1p, -1)

        self.purple_4 = cv2.imread('data/text/purple_4.png', -1)
        self.purple_4 = cv2.resize(self.purple_4, self.text_size_1p, -1)

        self.purple_5 = cv2.imread('data/text/purple_5.png', -1)
        self.purple_5 = cv2.resize(self.purple_5, self.text_size_1p, -1)

        self.purple_6 = cv2.imread('data/text/purple_6.png', -1)
        self.purple_6 = cv2.resize(self.purple_6, self.text_size_1p, -1)

        self.purple_7 = cv2.imread('data/text/purple_7.png', -1)
        self.purple_7 = cv2.resize(self.purple_7, self.text_size_1p, -1)

        self.purple_8 = cv2.imread('data/text/purple_8.png', -1)
        self.purple_8 = cv2.resize(self.purple_8, self.text_size_1p, -1)

        self.purple_9 = cv2.imread('data/text/purple_9.png', -1)
        self.purple_9 = cv2.resize(self.purple_9, self.text_size_1p, -1)

        self.purple_10 = cv2.imread('data/text/purple_10.png', -1)
        self.purple_10 = cv2.resize(self.purple_10, self.text_size_1p, -1)

        self.purple_11 = cv2.imread('data/text/purple_11.png', -1)
        self.purple_11 = cv2.resize(self.purple_11, self.text_size_1p, -1)

        self.purple_12 = cv2.imread('data/text/purple_12.png', -1)
        self.purple_12 = cv2.resize(self.purple_12, self.text_size_1p, -1)

        self.purple_13 = cv2.imread('data/text/purple_13.png', -1)
        self.purple_13 = cv2.resize(self.purple_13, self.text_size_1p, -1)

        self.purple_14 = cv2.imread('data/text/purple_14.png', -1)
        self.purple_14 = cv2.resize(self.purple_14, self.text_size_1p, -1)

        self.purple_15 = cv2.imread('data/text/purple_15.png', -1)
        self.purple_15 = cv2.resize(self.purple_15, self.text_size_1p, -1)

        self.purple_16 = cv2.imread('data/text/purple_16.png', -1)
        self.purple_16 = cv2.resize(self.purple_16, self.text_size_1p, -1)

        self.purple_17 = cv2.imread('data/text/purple_17.png', -1)
        self.purple_17 = cv2.resize(self.purple_17, self.text_size_1p, -1)

        self.purple_18 = cv2.imread('data/text/purple_18.png', -1)
        self.purple_18 = cv2.resize(self.purple_18, self.text_size_1p, -1)

        self.purple_19 = cv2.imread('data/text/purple_19.png', -1)
        self.purple_19 = cv2.resize(self.purple_19, self.text_size_1p, -1)

        self.purple_20 = cv2.imread('data/text/purple_20.png', -1)
        self.purple_20 = cv2.resize(self.purple_20, self.text_size_1p, -1)

        self.purple_21 = cv2.imread('data/text/purple_21.png', -1)
        self.purple_21 = cv2.resize(self.purple_21, self.text_size_1p, -1)

        self.purple_22 = cv2.imread('data/text/purple_22.png', -1)
        self.purple_22 = cv2.resize(self.purple_22, self.text_size_1p, -1)

        self.purple_23 = cv2.imread('data/text/purple_23.png', -1)
        self.purple_23 = cv2.resize(self.purple_23, self.text_size_1p, -1)

        self.purple_24 = cv2.imread('data/text/purple_24.png', -1)
        self.purple_24 = cv2.resize(self.purple_24, self.text_size_1p, -1)

        self.purple_25 = cv2.imread('data/text/purple_25.png', -1)
        self.purple_25 = cv2.resize(self.purple_25, self.text_size_1p, -1)

        self.purple_26 = cv2.imread('data/text/purple_26.png', -1)
        self.purple_26 = cv2.resize(self.purple_26, self.text_size_1p, -1)

        self.purple_27 = cv2.imread('data/text/purple_27.png', -1)
        self.purple_27 = cv2.resize(self.purple_27, self.text_size_1p, -1)

        self.purple_28 = cv2.imread('data/text/purple_28.png', -1)
        self.purple_28 = cv2.resize(self.purple_28, self.text_size_1p, -1)

        self.purple_29 = cv2.imread('data/text/purple_29.png', -1)
        self.purple_29 = cv2.resize(self.purple_29, self.text_size_1p, -1)

        self.purple_30 = cv2.imread('data/text/purple_30.png', -1)
        self.purple_30 = cv2.resize(self.purple_30, self.text_size_1p, -1)

        self.purple_31 = cv2.imread('data/text/purple_31.png', -1)
        self.purple_31 = cv2.resize(self.purple_31, self.text_size_1p, -1)

        self.purple_32 = cv2.imread('data/text/purple_32.png', -1)
        self.purple_32 = cv2.resize(self.purple_32, self.text_size_1p, -1)

        self.purple_33 = cv2.imread('data/text/purple_33.png', -1)
        self.purple_33 = cv2.resize(self.purple_33, self.text_size_1p, -1)

        self.purple_34 = cv2.imread('data/text/purple_34.png', -1)
        self.purple_34 = cv2.resize(self.purple_34, self.text_size_1p, -1)

        self.purple_35 = cv2.imread('data/text/purple_35.png', -1)
        self.purple_35 = cv2.resize(self.purple_35, self.text_size_1p, -1)

        self.purple_36 = cv2.imread('data/text/purple_36.png', -1)
        self.purple_36 = cv2.resize(self.purple_36, self.text_size_1p, -1)

        self.purple_37 = cv2.imread('data/text/purple_37.png', -1)
        self.purple_37 = cv2.resize(self.purple_37, self.text_size_1p, -1)

        self.purple_38 = cv2.imread('data/text/purple_38.png', -1)
        self.purple_38 = cv2.resize(self.purple_38, self.text_size_1p, -1)

        self.purple_39 = cv2.imread('data/text/purple_39.png', -1)
        self.purple_39 = cv2.resize(self.purple_39, self.text_size_1p, -1)

        self.purple_40 = cv2.imread('data/text/purple_40.png', -1)
        self.purple_40 = cv2.resize(self.purple_40, self.text_size_1p, -1)

        self.purple_41 = cv2.imread('data/text/purple_41.png', -1)
        self.purple_41 = cv2.resize(self.purple_41, self.text_size_1p, -1)

        self.purple_42 = cv2.imread('data/text/purple_42.png', -1)
        self.purple_42 = cv2.resize(self.purple_42, self.text_size_1p, -1)

        self.purple_43 = cv2.imread('data/text/purple_43.png', -1)
        self.purple_43 = cv2.resize(self.purple_43, self.text_size_1p, -1)

        self.purple_44 = cv2.imread('data/text/purple_44.png', -1)
        self.purple_44 = cv2.resize(self.purple_44, self.text_size_1p, -1)

        self.purple_45 = cv2.imread('data/text/purple_45.png', -1)
        self.purple_45 = cv2.resize(self.purple_45, self.text_size_1p, -1)

        self.purple_46 = cv2.imread('data/text/purple_46.png', -1)
        self.purple_46 = cv2.resize(self.purple_46, self.text_size_1p, -1)

        self.purple_47 = cv2.imread('data/text/purple_47.png', -1)
        self.purple_47 = cv2.resize(self.purple_47, self.text_size_1p, -1)

        self.purple_48 = cv2.imread('data/text/purple_48.png', -1)
        self.purple_48 = cv2.resize(self.purple_48, self.text_size_1p, -1)

        self.purple_49 = cv2.imread('data/text/purple_49.png', -1)
        self.purple_49 = cv2.resize(self.purple_49, self.text_size_1p, -1)

        self.purple_50 = cv2.imread('data/text/purple_50.png', -1)
        self.purple_50 = cv2.resize(self.purple_50, self.text_size_1p, -1)

        self.purple_51 = cv2.imread('data/text/purple_51.png', -1)
        self.purple_51 = cv2.resize(self.purple_51, self.text_size_1p, -1)

        self.purple_52 = cv2.imread('data/text/purple_52.png', -1)
        self.purple_52 = cv2.resize(self.purple_52, self.text_size_1p, -1)

        self.purple_53 = cv2.imread('data/text/purple_53.png', -1)
        self.purple_53 = cv2.resize(self.purple_53, self.text_size_1p, -1)

        self.purple_54 = cv2.imread('data/text/purple_54.png', -1)
        self.purple_54 = cv2.resize(self.purple_54, self.text_size_1p, -1)

        self.purple_55 = cv2.imread('data/text/purple_55.png', -1)
        self.purple_55 = cv2.resize(self.purple_55, self.text_size_1p, -1)

        self.purple_56 = cv2.imread('data/text/purple_56.png', -1)
        self.purple_56 = cv2.resize(self.purple_56, self.text_size_1p, -1)

        self.purple_57 = cv2.imread('data/text/purple_57.png', -1)
        self.purple_57 = cv2.resize(self.purple_57, self.text_size_1p, -1)

        self.purple_58 = cv2.imread('data/text/purple_58.png', -1)
        self.purple_58 = cv2.resize(self.purple_58, self.text_size_1p, -1)

        self.purple_59 = cv2.imread('data/text/purple_59.png', -1)
        self.purple_59 = cv2.resize(self.purple_59, self.text_size_1p, -1)

        self.purple_60 = cv2.imread('data/text/purple_10.png', -1)
        self.purple_60 = cv2.resize(self.purple_60, self.text_size_1p, -1)

        # (200, 400, 4)
        self.red_win = cv2.imread('data/text/red_win.png', -1)

        self.red_lose = cv2.imread('data/text/red_lose.png', -1)

        self.red_draw = cv2.imread('data/text/red_draw.png', -1)

        self.blue_win = cv2.imread('data/text/blue_win.png', -1)

        self.blue_lose = cv2.imread('data/text/blue_lose.png', -1)

        self.blue_draw = cv2.imread('data/text/blue_draw.png', -1)

        self.peace_r = cv2.imread('data/text/peace_r.png', -1)
        self.peace_r = cv2.resize(self.peace_r, (200, 200), -1)
        self.peace_l = cv2.imread('data/text/peace_l.png', -1)
        self.peace_l = cv2.resize(self.peace_l, (200, 200), -1)

        self.clap_r = cv2.imread('data/text/clap_r.png', -1)
        self.clap_l = cv2.imread('data/text/clap_l.png', -1)

        # (600, 1000, 4)
        self.poor = cv2.imread('data/text/poor.png', -1)
        self.poor = cv2.resize(self.poor, (500, 300), -1)

        self.not_bad = cv2.imread('data/text/not_bad.png', -1)
        self.not_bad = cv2.resize(self.not_bad, (500, 300), -1)

        self.good = cv2.imread('data/text/good.png', -1)
        self.good = cv2.resize(self.good, (500, 300), -1)

        self.excellent = cv2.imread('data/text/excellent.png', -1)
        self.excellent = cv2.resize(self.excellent, (500, 300), -1)

        self.splendid = cv2.imread('data/text/splendid.png', -1)
        self.splendid = cv2.resize(self.splendid, (500, 300), -1)

    def load_video(self):
        # load_video
        # vidcap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
        vidcap = cv2.VideoCapture(0)
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
                coordinate_red, coordinate_blue = self.random_box('easy', frame, is_one_player=True)

                if box_seed_num != self.current_seed:
                    self.is_answer_handled_red = False
                    self.is_answer_handled_blue = False

                rectangle_seed_num = self.rect_num % 3
                self.rect_num += 1

                # 점수 계산
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue, sum_score = \
                    self.score_calculation(frame, rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num,
                          detection_red, coordinate_red)

                # 정답 rect 그리기
                self.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                  is_answer_handled_blue)

                # 점수 표기
                frame = self.PlayerGameStats(frame, red_score, blue_score, sum_score, is_one_player=True)

                self.frame_num = self.frame_num + 1
                if self.frame_num == 900:
                    self.game_finish = True

                # 승자 결정
                self.game_result(red_score, blue_score, sum_score, is_one_player=True)

            else:
                # 승자 효과
                frame = self.Winner_effect(frame, self.win_red, self.win_blue, self.all_draw, self.one_player_result, is_one_player=True)

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
            area1, area2 = area
            (xs1, ys1), (xe1, ye1) = area1
            (xs2, ys2), (xe2, ye2) = area2
            a1, b1 = random.randint(xs1, xe1), random.randint(ys1, ye1)
            a2, b2 = random.randint(xs2, xe2), random.randint(ys2, ye2)
            if not is_one_player:
                img = cv2.line(img, (self.img_width//2, 0), (self.img_width//2, self.img_height), self.white_color, 2)
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
            else:
                return False
        else:
            False

    def score_calculation(self, frame, rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num,
                          detection_red, coordinate_red):
        # if not is_one_player:
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
        return self.blue_score, self.red_score, self.is_answer_handled_red, self.is_answer_handled_blue, self.blue_score+self.red_score

    def Drawing_Rectangle(self, frame, coordinate_blue, coordinate_red, is_answer_handled_red, is_answer_handled_blue):
        if self.is_answer_handled_red:
            cv2.rectangle(frame, (coordinate_blue[0][0], coordinate_blue[0][1]),
                          (coordinate_blue[0][2], coordinate_blue[0][3]), self.green_color, 3)

        if self.is_answer_handled_blue:
            cv2.rectangle(frame, (coordinate_red[0][0], coordinate_red[0][1]),
                          (coordinate_red[0][2], coordinate_red[0][3]), self.green_color, 3)

    def PlayerGameStats(self, frame, red_score, blue_score, sum_score, is_one_player=False):
        if not is_one_player:
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
        else:
            if sum_score == 0:
                frame = cvzone.overlayPNG(frame, self.purple_fill_0, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_0, self.text_loc_1p)
            elif sum_score == 1:
                frame = cvzone.overlayPNG(frame, self.purple_fill_1, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_1, self.text_loc_1p)
            elif sum_score == 2:
                frame = cvzone.overlayPNG(frame, self.purple_fill_2, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_2, self.text_loc_1p)
            elif sum_score == 3:
                frame = cvzone.overlayPNG(frame, self.purple_fill_3, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_3, self.text_loc_1p)
            elif sum_score == 4:
                frame = cvzone.overlayPNG(frame, self.purple_fill_4, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_4, self.text_loc_1p)
            elif sum_score == 5:
                frame = cvzone.overlayPNG(frame, self.purple_fill_5, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_5, self.text_loc_1p)
            elif sum_score == 6:
                frame = cvzone.overlayPNG(frame, self.purple_fill_6, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_6, self.text_loc_1p)
            elif sum_score == 7:
                frame = cvzone.overlayPNG(frame, self.purple_fill_7, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_7, self.text_loc_1p)
            elif sum_score == 8:
                frame = cvzone.overlayPNG(frame, self.purple_fill_8, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_8, self.text_loc_1p)
            elif sum_score == 9:
                frame = cvzone.overlayPNG(frame, self.purple_fill_9, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_9, self.text_loc_1p)
            elif sum_score == 10:
                frame = cvzone.overlayPNG(frame, self.purple_fill_10, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_10, self.text_loc_1p)
            elif sum_score == 11:
                frame = cvzone.overlayPNG(frame, self.purple_fill_11, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_11, self.text_loc_1p)
            elif sum_score == 12:
                frame = cvzone.overlayPNG(frame, self.purple_fill_12, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_12, self.text_loc_1p)
            elif sum_score == 13:
                frame = cvzone.overlayPNG(frame, self.purple_fill_13, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_13, self.text_loc_1p)
            elif sum_score == 14:
                frame = cvzone.overlayPNG(frame, self.purple_fill_14, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_14, self.text_loc_1p)
            elif sum_score == 15:
                frame = cvzone.overlayPNG(frame, self.purple_fill_15, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_15, self.text_loc_1p)
            elif sum_score == 16:
                frame = cvzone.overlayPNG(frame, self.purple_fill_16, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_16, self.text_loc_1p)
            elif sum_score == 17:
                frame = cvzone.overlayPNG(frame, self.purple_fill_17, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_17, self.text_loc_1p)
            elif sum_score == 18:
                frame = cvzone.overlayPNG(frame, self.purple_fill_18, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_18, self.text_loc_1p)
            elif sum_score == 19:
                frame = cvzone.overlayPNG(frame, self.purple_fill_19, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_19, self.text_loc_1p)
            elif sum_score == 20:
                frame = cvzone.overlayPNG(frame, self.purple_fill_20, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_20, self.text_loc_1p)
            elif sum_score == 21:
                frame = cvzone.overlayPNG(frame, self.purple_fill_21, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_21, self.text_loc_1p)
            elif sum_score == 22:
                frame = cvzone.overlayPNG(frame, self.purple_fill_22, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_22, self.text_loc_1p)
            elif sum_score == 23:
                frame = cvzone.overlayPNG(frame, self.purple_fill_23, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_23, self.text_loc_1p)
            elif sum_score == 24:
                frame = cvzone.overlayPNG(frame, self.purple_fill_24, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_24, self.text_loc_1p)
            elif sum_score == 25:
                frame = cvzone.overlayPNG(frame, self.purple_fill_25, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_25, self.text_loc_1p)
            elif sum_score == 26:
                frame = cvzone.overlayPNG(frame, self.purple_fill_26, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_26, self.text_loc_1p)
            elif sum_score == 27:
                frame = cvzone.overlayPNG(frame, self.purple_fill_27, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_27, self.text_loc_1p)
            elif sum_score == 28:
                frame = cvzone.overlayPNG(frame, self.purple_fill_28, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_28, self.text_loc_1p)
            elif sum_score == 29:
                frame = cvzone.overlayPNG(frame, self.purple_fill_29, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_29, self.text_loc_1p)
            elif sum_score == 30:
                frame = cvzone.overlayPNG(frame, self.purple_fill_30, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_30, self.text_loc_1p)
            elif sum_score == 31:
                frame = cvzone.overlayPNG(frame, self.purple_fill_31, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_31, self.text_loc_1p)
            elif sum_score == 32:
                frame = cvzone.overlayPNG(frame, self.purple_fill_32, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_32, self.text_loc_1p)
            elif sum_score == 33:
                frame = cvzone.overlayPNG(frame, self.purple_fill_33, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_33, self.text_loc_1p)
            elif sum_score == 34:
                frame = cvzone.overlayPNG(frame, self.purple_fill_34, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_34, self.text_loc_1p)
            elif sum_score == 35:
                frame = cvzone.overlayPNG(frame, self.purple_fill_35, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_35, self.text_loc_1p)
            elif sum_score == 36:
                frame = cvzone.overlayPNG(frame, self.purple_fill_36, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_36, self.text_loc_1p)
            elif sum_score == 37:
                frame = cvzone.overlayPNG(frame, self.purple_fill_37, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_37, self.text_loc_1p)
            elif sum_score == 38:
                frame = cvzone.overlayPNG(frame, self.purple_fill_38, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_38, self.text_loc_1p)
            elif sum_score == 39:
                frame = cvzone.overlayPNG(frame, self.purple_fill_39, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_39, self.text_loc_1p)
            elif sum_score == 40:
                frame = cvzone.overlayPNG(frame, self.purple_fill_40, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_40, self.text_loc_1p)
            elif sum_score == 41:
                frame = cvzone.overlayPNG(frame, self.purple_fill_41, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_41, self.text_loc_1p)
            elif sum_score == 42:
                frame = cvzone.overlayPNG(frame, self.purple_fill_42, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_42, self.text_loc_1p)
            elif sum_score == 43:
                frame = cvzone.overlayPNG(frame, self.purple_fill_43, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_43, self.text_loc_1p)
            elif sum_score == 44:
                frame = cvzone.overlayPNG(frame, self.purple_fill_44, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_44, self.text_loc_1p)
            elif sum_score == 45:
                frame = cvzone.overlayPNG(frame, self.purple_fill_45, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_45, self.text_loc_1p)
            elif sum_score == 46:
                frame = cvzone.overlayPNG(frame, self.purple_fill_46, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_46, self.text_loc_1p)
            elif sum_score == 47:
                frame = cvzone.overlayPNG(frame, self.purple_fill_47, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_47, self.text_loc_1p)
            elif sum_score == 48:
                frame = cvzone.overlayPNG(frame, self.purple_fill_48, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_48, self.text_loc_1p)
            elif sum_score == 49:
                frame = cvzone.overlayPNG(frame, self.purple_fill_49, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_49, self.text_loc_1p)
            elif sum_score == 50:
                frame = cvzone.overlayPNG(frame, self.purple_fill_50, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_50, self.text_loc_1p)
            elif sum_score == 51:
                frame = cvzone.overlayPNG(frame, self.purple_fill_51, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_51, self.text_loc_1p)
            elif sum_score == 52:
                frame = cvzone.overlayPNG(frame, self.purple_fill_52, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_52, self.text_loc_1p)
            elif sum_score == 53:
                frame = cvzone.overlayPNG(frame, self.purple_fill_53, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_53, self.text_loc_1p)
            elif sum_score == 54:
                frame = cvzone.overlayPNG(frame, self.purple_fill_54, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_54, self.text_loc_1p)
            elif sum_score == 55:
                frame = cvzone.overlayPNG(frame, self.purple_fill_55, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_55, self.text_loc_1p)
            elif sum_score == 56:
                frame = cvzone.overlayPNG(frame, self.purple_fill_56, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_56, self.text_loc_1p)
            elif sum_score == 57:
                frame = cvzone.overlayPNG(frame, self.purple_fill_57, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_57, self.text_loc_1p)
            elif sum_score == 58:
                frame = cvzone.overlayPNG(frame, self.purple_fill_58, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_58, self.text_loc_1p)
            elif sum_score == 59:
                frame = cvzone.overlayPNG(frame, self.purple_fill_59, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_59, self.text_loc_1p)
            elif sum_score == 60:
                frame = cvzone.overlayPNG(frame, self.purple_fill_60, self.purple_gage_loc)
                frame = cvzone.overlayPNG(frame, self.purple_60, self.text_loc_1p)

                # while self.frame_num < 901:
                #     frame = cvzone.overlayPNG(frame, self.puple+sum_score, self.blue_gage_loc)
                #     frame = cvzone.overlayPNG(frame, self.blue_fill_27, self.blue_gage_loc)

        return frame

    def game_result(self, red_score, blue_score, sum_score, is_one_player=False):
        if not is_one_player:
            if red_score > blue_score:
                self.win_red = True
            elif red_score < blue_score:
                self.win_blue = True
            elif red_score == blue_score:
                self.all_draw = True
        else:
            if 0 <= sum_score < 10:
                self.one_player_result = 'Poor'
            elif 9 < sum_score < 30:
                self.one_player_result = 'Not Bad'
            elif 29 < sum_score < 50:
                self.one_player_result = 'Good'
            elif 49 < sum_score < 60:
                self.one_player_result = 'Excellent'
            elif sum_score == 60:
                self.one_player_result = 'Splendid'

    def Winner_effect(self, frame, win_red, win_blue, all_draw, one_player_result, is_one_player=False):
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
        else:
            # 0-19:Poor
            if self.one_player_result == 'Poor':
                frame = cvzone.overlayPNG(frame, self.poor, [self.img_width // 2, self.img_height // 2])
            # 20-29:Not Bad
            elif self.one_player_result == 'Not Bad':
                frame = cvzone.overlayPNG(frame, self.Not_Bad, [self.img_width // 2, self.img_height // 2])
            elif self.one_player_result == 'Good':
                frame = cvzone.overlayPNG(frame, self.Good, [self.img_width // 2, self.img_height // 2])
            elif self.one_player_result == 'Excellent':
                frame = cvzone.overlayPNG(frame, self.Excellent, [self.img_width // 2, self.img_height // 2])
            elif self.one_player_result == 'Splendid':
                frame = cvzone.overlayPNG(frame, self.Splendid, [self.img_width // 2, self.img_height // 2])

        return frame


if __name__ == '__main__':
    v = Video_Manager()
    v.load_video()