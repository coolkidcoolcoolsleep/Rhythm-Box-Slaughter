# random_rhythm_box.py
import glob
from PIL import Image
import numpy as np
import cv2


class RandomRhythmBox:
    def __init__(self, dataset, img_res=(266, 126)):
        self.dataset = dataset
        self.img_res = img_res

    def load_data(self):
        path = glob.glob('data/image_input/*.jpg')
        images = []
        for file in path:
            img = Image.open(file)
            img = Image.fromarray(np.array(img)).resize(size=self.img_res)
            img = np.array(img)                 # (126, 266, 3)
            images.append(img)

        return images

    def split_display(self, is_one_player=True):
        images = self.load_data()
        display = []
        for image in images:
            if not is_one_player:
                display_size = (image[:63, :133], image[63:, 133:])
            else:
                display_size = image
            display.append(display_size)

        return display

    def random_box(self, level, is_one_player=True):
        if level == 'easy':
            pass
            # game_area =
        if level == 'norm':
            pass
        if level == 'hard':
            pass
        pass

    def bpm_per_song(self):
        pass

    def color_box(self):
        img = self.load_data()[0]
        red_color, blue_color = (0, 0, 255), (255, 0, 0)

        img = cv2.rectangle(img, (10, 10), (30, 30), blue_color, 3)
        img = cv2.rectangle(img, (100, 100), (120, 120), red_color, 3)
        cv2.imwrite('data/image_output/01.jpg', img)
        cv2.imshow('rectangle',img)
        cv2.waitKey(0)

if __name__ == '__main__':
    data = RandomRhythmBox('./data/image_input')
    test = data.color_box()
    # test = data.split_display(False)
    # ['./data/image_input\\sample01.jpg']








