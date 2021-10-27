import os
from PIL import Image
import cv2
import random
import time



class Video_Manager:
    def __init__(self):
        self.current_seed = 0
        self.is_answer_handled_red = False
        self.is_answer_handled_blue = False

        # drawing_color
        self.blue_lower = (100, 150, 0)
        self.blue_upper = (140, 255, 255)
        self.red_lower = (-10, 100, 100)
        self.red_upper = (10, 255, 255)

        # (0, 50, 20), (5, 255, 255)
        # (0, 70, 50), (10, 255, 255)
        # (175, 70, 50), (180, 255, 255)
        # (170, 120, 120), (180, 255, 255)
        # (0, 50, 20), (5, 255, 255)
        # (153, 46, 82), (166, 33, 55)

        # level
        self.easy = 200
        self.norm = 40
        self.hard = 30

        # color
        self.red_color = (203, 192, 255)
        self.blue_color = (223, 188, 80)
        self.green_color = (0, 255, 0)
        self.white_color = (255, 255, 255)

        # score
        self.blue_score = 0
        self.red_score = 0

        # box
        self.BoxThreshold = 6

        # score
        self.blue_score = 0
        self.red_score = 0

        # area
        self.easy_min_area = self.easy * 30
        self.norm_min_area = self.norm * 30
        self.hard_min_area = self.hard * 30

        # display_size
        self.img_width = 1330
        self.img_height = 630

        self.box_num = 0
        self.rect_num = 0

        # time
        # self.num_of_secs = 30

    def load_video(self):
        # image_resizing
        img_width = self.img_width
        img_height = self.img_height

        # load_video
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

            # frame = cv2.resize(frame, dsize=(665, 315))
            frame = cv2.resize(frame, dsize=(self.img_width, self.img_height))

            box_seed_num = self.box_num // 90
            random.seed(box_seed_num)
            self.box_num += 1

            # 볼 트래킹, 리듬박스 좌표 가져오기
            detection_blue, detection_red = self.tracking_ball(frame)
            coordinate_red, coordinate_blue = self.random_box('easy', frame, is_one_player=False)

            if box_seed_num != self.current_seed:
                self.is_answer_handled_red = False
                self.is_answer_handled_blue = False

            rectangle_seed_num = self.rect_num % 3
            self.rect_num += 1

            # 좌표, 점수 계산
            blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = self.score_calculation(frame,
                rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num, detection_red, coordinate_red)

            self.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                              is_answer_handled_blue)

            blue_score = str(blue_score)
            red_score = str(red_score)

            # (0, 100) : 문자열이 표시될 좌표 x = 0, y = 100
            # cv2.FONT_HERSHEY_SCRIPT_SIMPLEX : 폰트 형태
            # 1 : 문자열 크기(scale) 소수점 사용가능
            # (0, 255, 0) : 문자열 색상 (r,g,b)

            cv2.putText(frame, red_score, (30, 40), cv2.FONT_HERSHEY_PLAIN,  3, (0, 0, 0))
            cv2.putText(frame, blue_score, (570, 40), cv2.FONT_HERSHEY_PLAIN,  3, (0, 0, 0))

            cv2.imshow('Rhythm Box Slaughter', frame)
            # esc 키를 누르면 닫음 -> 후에 노래가 끝나면 종료로 수정해야 함

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

if __name__ == '__main__':
    v = Video_Manager()
    v.load_video()