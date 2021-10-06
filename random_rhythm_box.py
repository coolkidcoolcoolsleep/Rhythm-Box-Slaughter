# random_rhythm_box.py
import glob
from PIL import Image
import numpy as np
import cv2


class RandomRhythmBox:
    def __init__(self, dataset, img_width=266, img_height=126):
        self.dataset = dataset
        self.img_width = img_width
        self.img_height = img_height
        self.easy = 30
        self.norm = 20
        self.hard = 15
        self.red_color = (0, 0, 255)
        self.blue_color = (255, 0, 0)
        self.green_color = (0, 255, 0)

    def load_data(self):
        path = glob.glob('data/image_input/*.jpg')
        images = []
        for file in path:
            img = Image.open(file)
            img = Image.fromarray(np.array(img)).resize(size=(self.img_width, self.img_height))
            img = np.array(img)                 # (126, 266, 3)
            images.append(img)

        return images

    def rhythm_box_display_area(self, level, is_one_player=True):
        game_areas = self.load_data()
        display_areas = []
        if not is_one_player:
            if level == 'easy':
                for area in game_areas:
                    y, x, _ = area.shape                                                # (126, 266, 3)
                    area1 = (self.easy, self.easy), (x//2-self.easy, y-self.easy)       # (30, 30), (103, 96)
                    area2 = (x//2+self.easy, self.easy), (x-self.easy, y-self.easy)     # (163, 30), (236, 96)
                    display_areas.append((area1, area2))
            if level == 'norm':
                for area in game_areas:
                    y, x, _ = area.shape  # (126, 266, 3)
                    area1 = (self.norm, self.norm), (x//2-self.norm, y-self.norm)  # (20, 20), (113, 106)
                    area2 = (x//2+self.norm, self.norm), (x-self.norm, y-self.norm)  # (153, 20), (246, 106)
                    display_areas.append((area1, area2))
            if level == 'hard':
                for area in game_areas:
                    y, x, _ = area.shape  # (126, 266, 3)
                    area1 = (self.hard, self.hard), (x//2-self.hard, y-self.hard)  # (15, 15), (118, 111)
                    area2 = (x//2+self.hard, self.hard), (x-self.hard, y-self.hard)  # (148, 15), (251, 111)
                    display_areas.append((area1, area2))
        else:
            if level == 'easy':
                for area in game_areas:
                    y, x, _ = area.shape                                                # (126, 266, 3)
                    area1 = (self.easy, self.easy), (x-self.easy, y-self.easy)       # (30, 30), (236, 96)
                    display_areas.append(area1)
            if level == 'norm':
                for area in game_areas:
                    y, x, _ = area.shape  # (126, 266, 3)
                    area1 = (self.norm, self.norm), (x-self.norm, y-self.norm)  # (20, 20), (246, 106)
                    display_areas.append(area1)
            if level == 'hard':
                for area in game_areas:
                    y, x, _ = area.shape  # (126, 266, 3)
                    area1 = (self.hard, self.hard), (x-self.hard, y-self.hard)  # (15, 15), (251, 111)
                    display_areas.append(area1)
        return display_areas

    def bpm_per_song(self):
        pass

    def random_box(self, level, is_one_player=True):
        img = self.load_data()[0]
        areas = self.rhythm_box_display_area(level, is_one_player)
        # (((30, 30), (103, 96)), ((163, 30), (236, 96)))
        if not is_one_player:
            if level == 'easy':
                for area in areas:
                    area1, area2 = area
                    (xs1, ys1), (xe1, ye1) = area1
                    a, b = int(np.random.randint(xs1, xe1, 1)), int(np.random.randint(ys1, ye1, 1))
                    img = cv2.rectangle(img, (a, b), (a+self.easy, b+self.easy), self.red_color, 3)
                    (xs2, ys2), (xe2, ye2) = area2
                    a, b = int(np.random.randint(xs2, xe2, 1)), int(np.random.randint(ys2, ye2, 1))
                    img = cv2.rectangle(img, (a, b), (a+self.easy, b+self.easy), self.blue_color, 3)
                    cv2.imshow('rectangle', img)
                    cv2.waitKey(0)
        exit()
        # np.random.randint()
        img = cv2.rectangle(img, (10, 10), (30, 30), self.blue_color, 3)
        img = cv2.rectangle(img, (100, 100), (120, 120), self.red_color, 3)
        cv2.imwrite('data/image_output/01.jpg', img)
        cv2.imshow('rectangle', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    data = RandomRhythmBox('./data/image_input')
    data.random_box('easy', False)
    # data.rhythm_box_display_area('hard', False)
    # data.rhythm_box_display_area('hard', True)
    # test = data.color_box()
    # ['./data/image_input\\sample01.jpg']








