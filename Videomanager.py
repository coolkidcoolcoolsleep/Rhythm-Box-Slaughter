import glob, os
from PIL import Image
import cv2, sys
import random


class Video_Manager:
    def load_video(self):

        # drawing_color
        self.blue_lower = (100, 150, 0)
        self.blue_lower = (100, 150, 0)
        self.blue_upper = (140, 255, 255)
        self.red_lower = (170, 120, 120)
        self.red_upper = (180, 255, 255)

        # level
        self.easy = 200
        self.norm = 40
        self.hard = 30

        self.red_color = (203, 192, 255)
        self.blue_color = (223, 188, 80)
        self.green_color = (0, 255, 0)
        self.white_color = (255, 255, 255)

        # score
        self.blue_score = 0
        self.red_score = 0

        # load_video
        vidcap = cv2.VideoCapture(0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        num = 0

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(665, 315))

            seed_num = num // 90
            random.seed(seed_num)
            num = num + 1

            # detection_blue와 red도 연속해서 끊어서 나와야 함
            detection_blue, detection_red = self.tracking_ball(frame)
            coordinate_red, coordinate_blue = self.random_box('easy', frame, is_one_player=True)

            # 좌표 비교
            # if self.isRectangleOverlap_blue(detection_blue, coordinate_blue):
            print("coordinate_blue: ", coordinate_blue)
            print("coordinate_red: ", coordinate_red)
            print("detection_blue: ", detection_blue)
            print("detection_red: ", detection_red)
            print(self.isRectangleOverlap_blue(detection_blue, coordinate_blue))

            # print(self.isRectangleOverlap_blue(detection_blue, coordinate_blue))
            # self.isRectangleOverlap_red(detection_red)

            # 점수 합산

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
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
            if area > 800:
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
            if area > 800:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                # detection_red = [x, y, w, h]
                detection_red.append([x, y, x + w, y + h])
                # print("detection_red: ", x, y, w, h)

        return detection_blue[-1:], detection_red[-1:]

    def rhythm_box_display_area(self, level, frame, is_one_player=True):
        # game_areas = self.load_data()
        # game_areas = frame
        area = frame
        display_areas = []
        # for area in game_areas:
        y, x, _ = area.shape  # (126, 266, 3)
        if not is_one_player:
            if level == 'easy':
                area1 = (0, 0), (x // 2 - self.easy, y - self.easy)  # (0, 0), (103, 96)
                area2 = (x // 2, 0), (x - self.easy, y - self.easy)  # (133, 0), (236, 96)
                # print(area1, area2)
                display_areas.append((area1, area2))
            if level == 'norm':
                area1 = (0, 0), (x // 2 - self.norm, y - self.norm)  # (0, 0), (113, 106)
                area2 = (x // 2, 0), (x - self.norm, y - self.norm)  # (133, 0), (246, 106)
                # print(area1, area2)
                display_areas.append((area1, area2))
            if level == 'hard':
                area1 = (0, 0), (x // 2 - self.hard, y - self.hard)  # (0, 0), (118, 111)
                area2 = (x // 2, 0), (x - self.hard, y - self.hard)  # (133, 0), (251, 111)
                # print(area1, area2)
                display_areas.append((area1, area2))
        else:
            if level == 'easy':
                area1 = (0, 0), (x - self.easy, y - self.easy)  # (0, 0), (236, 96)
                # print(area1)
                display_areas.append(area1)
            if level == 'norm':
                area1 = (0, 0), (x - self.norm, y - self.norm)  # (0, 0), (246, 106)
                # print(area1)
                display_areas.append(area1)
            if level == 'hard':
                area1 = (0, 0), (x - self.hard, y - self.hard)  # (0, 0), (251, 111)
                # print(area1)
                display_areas.append(area1)
        return display_areas

    def random_box(self, level, frame, is_one_player=True):
        # img = self.load_data()[0]

        img = frame
        areas = self.rhythm_box_display_area(level, frame, is_one_player)
        coordinate_red, coordinate_blue = [], []
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
                    img = cv2.rectangle(img, (a1, b1), (a1 + self.easy, b1 + self.easy), self.red_color, 3)
                    coordinate_red.append([a1, b1, a1 + self.easy, b1 + self.easy])
                    img = cv2.rectangle(img, (a2, b2), (a2 + self.easy, b2 + self.easy), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])
                if level == 'norm':
                    img = cv2.rectangle(img, (a1, b1), (a1 + self.norm, b1 + self.norm), self.red_color, 3)
                    coordinate_red.append([a, b, a + self.easy, b + self.easy])
                    img = cv2.rectangle(img, (a2, b2), (a2 + self.norm, b2 + self.norm), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])
                if level == 'hard':
                    img = cv2.rectangle(img, (a1, b1), (a1 + self.hard, b1 + self.hard), self.red_color, 3)
                    coordinate_red.append([a, b, a + self.easy, b + self.easy])
                    img = cv2.rectangle(img, (a2, b2), (a2 + self.hard, b2 + self.hard), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])

            else:
                (xs1, ys1), (xe1, ye1) = area
                a, b = random.randint(xs1, xe1), random.randint(ys1, ye1)
                c, d = random.randint(xs1, xe1), random.randint(ys1, ye1)
                if level == 'easy':
                    img = cv2.rectangle(img, (a, b), (a + self.easy, b + self.easy), self.red_color, 3)
                    coordinate_red.append([a, b, a + self.easy, b + self.easy])
                    img = cv2.rectangle(img, (c, d), (c + self.easy, d + self.easy), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])
                if level == 'norm':
                    img = cv2.rectangle(img, (a, b), (a + self.norm, b + self.norm), self.red_color, 3)
                    coordinate_red.append([a, b, a + self.easy, b + self.easy])
                    img = cv2.rectangle(img, (c, d), (c + self.norm, d + self.norm), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])
                if level == 'hard':
                    img = cv2.rectangle(img, (a, b), (a + self.hard, b + self.hard), self.red_color, 3)
                    coordinate_red.append([a, b, a + self.easy, b + self.easy])
                    img = cv2.rectangle(img, (c, d), (c + self.hard, d + self.hard), self.blue_color, 3)
                    coordinate_blue.append([c, d, c + self.easy, d + self.easy])

        return coordinate_red, coordinate_blue

    def isRectangleOverlap_blue(self, detection_blue, coordinate_blue):
        if (detection_blue[0][0] >= coordinate_blue[0][2]) or (detection_blue[0][2] <= coordinate_blue[0][0]) \
                or (detection_blue[0][3] <= coordinate_blue[0][1]) or (detection_blue[0][1] >= coordinate_blue[0][3]):
            return False
        else: return True

        # h1 = detection_blue[2] - detection_blue[0]
        # v1 = detection_blue[3] - detection_blue[1]
        # h2 = coordinate_blue[2] - coordinate_blue[0]
        # v2 = coordinate_blue[3] - coordinate_blue[1]
        #
        # hflag = False
        # vflag = False
        #
        # if detection_blue[0] <= coordinate_blue[0]:
        #     if coordinate_blue[0] - detection_blue[0] < h1:
        #         hflag = True
        # else:
        #     if detection_blue[0] - coordinate_blue[0] < h2:
        #         hflag = True
        #
        # if detection_blue[1] <= coordinate_blue[1]:
        #     if coordinate_blue[1] - detection_blue[1] < v1:
        #         vflag = True
        # else:
        #     if detection_blue[1] - coordinate_blue[1] < v2:
        #         vflag = True
        #
        # print(hflag, vflag)
        # return hflag and vflag

        # def isRectangleOverlap_red(self, detection_red, coordinate_red):
        #
        #     h1 = detection_red[2] - detection_red[0]
        #     v1 = detection_red[3] - detection_red[1]
        #     h2 = coordinate_red[2] - coordinate_red[0]
        #     v2 = coordinate_red[3] - coordinate_red[1]
        #
        #     hflag = False
        #     vflag = False
        #
        #     if detection_red[0] <= coordinate_red[0]:
        #         if coordinate_red[0] - detection_red[0] < h1:
        #             hflag = True
        #     else:
        #         if detection_red[0] - coordinate_red[0] < h2:
        #             hflag = True
        #
        #     if detection_red[1] <= coordinate_red[1]:
        #         if coordinate_red[1] - detection_red[1] < v1:
        #             vflag = True
        #     else:
        #         if detection_red[1] - coordinate_red[1] < v2:
        #             vflag = True
        #
        #     print(hflag, vflag)
        #     return hflag and vflag

    # def setScore(score):
    #     if
    #     pass
    #     self.isRectangleOverlap_blue


v = Video_Manager()
v.load_video()