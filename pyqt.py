import cv2
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import sys
import random
import winsound
from video_manager import Video_Manager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.music = QtWidgets.QComboBox(self)

    def player_1(self):
        vm = Video_Manager()

        vidcap = cv2.VideoCapture(0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        box_num = 0
        rect_num = 0

        while True:
            _, frame = vidcap.read()  # _: ret
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(665, 315))

            # 90 프레임마다 몫이 바뀌니까
            box_seed_num = box_num // 90
            random.seed(box_seed_num)
            box_num = box_num + 1

            detection_blue, detection_red = vm.tracking_ball(frame)
            coordinate_red, coordinate_blue = vm.random_box('easy', frame, is_one_player=True)

            # 좌표 비교
            rectangle_seed_num = rect_num % 3
            if rectangle_seed_num == 0:
                if vm.isRectangleOverlap(detection_blue, coordinate_blue, vm.load_video().BoxThreshold):
                    cv2.rectangle(frame, (coordinate_blue[0][0], coordinate_blue[0][1]),
                                  (coordinate_blue[0][2], coordinate_blue[0][3]), vm.green_color, 3)
                if vm.isRectangleOverlap(detection_red, coordinate_red, vm.BoxThreshold):
                    cv2.rectangle(frame, (coordinate_red[0][0], coordinate_red[0][1]),
                                  (coordinate_red[0][2], coordinate_red[0][3]), vm.green_color, 3)
            rect_num = rect_num + 1

            # 점수 합산

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self):
        vm = Video_Manager()

        vidcap = cv2.VideoCapture(0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            sys.exit()

        box_num = 0
        rect_num = 0

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(665, 315))

            # 90 프레임마다 몫이 바뀌니까
            box_seed_num = box_num // 90
            random.seed(box_seed_num)
            box_num = box_num + 1

            detection_blue, detection_red = vm.tracking_ball(frame)
            coordinate_red, coordinate_blue = vm.random_box('easy', frame, is_one_player=False)

            # 좌표 비교
            rectangle_seed_num = rect_num % 3
            if rectangle_seed_num == 0:
                if vm.isRectangleOverlap(detection_blue, coordinate_blue, vm.load_video().BoxThreshold):
                    cv2.rectangle(frame, (coordinate_blue[0][0], coordinate_blue[0][1]),
                                  (coordinate_blue[0][2], coordinate_blue[0][3]), vm.green_color, 3)
                if vm.isRectangleOverlap(detection_red, coordinate_red, vm.BoxThreshold):
                    cv2.rectangle(frame, (coordinate_red[0][0], coordinate_red[0][1]),
                                  (coordinate_red[0][2], coordinate_red[0][3]), vm.green_color, 3)
            rect_num = rect_num + 1

            # 점수 합산

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:  # esc 키를 누르면 닫음
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def music_play(self):
        winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def button(self):
        btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # btn_player_1.setFixedSize(100, 20)

        btn_player_2 = QtWidgets.QRadioButton('2 Player')
        # btn_player_2.setFixedSize(100, 20)

        self.music.move(200, 400)
        music_list = [1, 2, 3, 4]
        for i in music_list:
            self.music.addItem(f'music{i}')

        btn_start = QtWidgets.QPushButton('Game Start')

        vbox.addWidget(label)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_player_1)
        hbox.addWidget(btn_player_2)
        hbox.addWidget(self.music)
        hbox.addWidget(btn_start)
        hbox.addStretch(1)

        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        btn_player_1.clicked.connect(self.player_1)
        btn_player_2.clicked.connect(self.player_2)
        self.music.activated[str].connect(self.music_play)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()
    window.setWindowTitle('Rhythm Box Slaughter')
    window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

    main = MainWindow()
    main.button()

    window.setLayout(vbox)
    window.setGeometry(0, 0, 1330, 630)
    window.show()

    sys.exit(app.exec_())