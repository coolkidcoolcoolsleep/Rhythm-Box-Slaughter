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

    def split_display(self, is_one_player=True):
        images = self.load_data()
        display = []
        for image in images:
            # if not is_one_player:
            #     display_size = (image[:, :133], image[:, 133:])         # (126, 133, 3)
            # else:
            #     display_size = image
            # display.append(display_size)
            display.append(image)
        return display

    def rhythm_box_display_area(self, level, is_one_player=True):
        if not is_one_player:
            if level == 'easy':
                game_areas = self.load_data()
                for image in game_areas:
                    x, y, _ = image.shape                                   # (126, 266, 3)
                    area = cv2.rectangle(image, (self.easy, self.easy), (x-self.easy, y//2-self.easy),
                                         self.green_color, 1)
                    area = cv2.rectangle(area, (x+self.easy, y+self.easy), (x-self.easy, y-self.easy),
                                         self.green_color, 1)
                    cv2.imshow('rectangle', area)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
            if level == 'norm':
                pass
            if level == 'hard':
                pass
        else:
            pass

    def bpm_per_song(self):
        pass

    def color_box(self):
        img = self.load_data()[0]

        img = cv2.rectangle(img, (10, 10), (30, 30), self.blue_color, 3)
        img = cv2.rectangle(img, (100, 100), (120, 120), self.red_color, 3)
        cv2.imwrite('data/image_output/01.jpg', img)
        cv2.imshow('rectangle', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    data = RandomRhythmBox('./data/image_input')
    data.rhythm_box_display_area('easy', False)
    # test = data.color_box()
    # test = data.split_display(True)
    # ['./data/image_input\\sample01.jpg']








