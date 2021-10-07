# random_rhythm_box.py
import glob, os
from PIL import Image
import numpy as np
import cv2, sys
import random


class RandomRhythmBox:
    def __init__(self, dataset, img_width=266, img_height=126):
        self.dataset = dataset
        self.img_width = img_width
        self.img_height = img_height
        self.easy = 50
        self.norm = 40
        self.hard = 30
        self.red_color = (0, 0, 255)
        self.blue_color = (255, 0, 0)
        self.green_color = (0, 255, 0)
        self.white_color = (255, 255, 255)

    def load_video(self, level, is_one_player=True):
        cap = cv2.VideoCapture()
        cap.open(0)
        if not cap.isOpened():
            print('Camera open falied')
            sys.exit()

        fps = cap.get(cv2.CAP_PROP_FPS)
        # print(fps)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        # delay = round(1000/fps)

        if not os.path.exists('data/video'):
            os.makedirs('data/video')

        out = cv2.VideoWriter(f'data/video/{level}_{is_one_player}.mp4',
                              fourcc, fps, (self.img_width, self.img_height))

        if not out.isOpened():
            print('File open failed!')
            cap.release()
            sys.exit()

        num = 0
        while True:
            ret, frame = cap.read()             # bool, numpy

            if not ret:
                break
            flip_frame = cv2.flip(frame, 0)
            resize_frame = cv2.resize(flip_frame, dsize=(266, 126))
            # print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))       # 480.0
            # print(resize_frame.shape)                       # (126, 266, 3)
            seed_num = num // 10
            random.seed(seed_num)
            num = num + 1

            self.random_box(level, resize_frame, is_one_player)

            out.write(resize_frame)
            cv2.imshow('camera', resize_frame)

            if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def load_data(self):
        path = glob.glob('data/image_input/*.jpg')
        images = []
        for file in path:
            img = Image.open(file)
            img = Image.fromarray(np.array(img)).resize(size=(self.img_width, self.img_height))
            img = np.array(img)                 # (126, 266, 3)
            images.append(img)

        return images

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

    def bpm_per_song(self):
        pass

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


if __name__ == '__main__':
    data = RandomRhythmBox('./data/image_input')
    data.load_video('easy', True)
    # data.load_video('norm', True)
    # data.load_video('hard', True)
    # data.load_video('easy', False)
    # data.load_video('norm', False)
    # data.load_video('hard', False)
    # data.load_video('hard', False)








