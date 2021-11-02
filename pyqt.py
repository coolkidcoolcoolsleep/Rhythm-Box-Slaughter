import cv2
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import random
import winsound
import threading
from video_manager import Video_Manager
import youtube_player


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.music = QtWidgets.QComboBox(self)
        self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        self.btn_start = QtWidgets.QPushButton('Game Start')

        self.button()
        self.background()
        self.label_text()
        self.window_style()

    def player_1(self):
        vm = Video_Manager()

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

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            box_seed_num = vm.box_num // 90
            random.seed(box_seed_num)
            vm.box_num += 1

            detection_blue, detection_red = vm.tracking_ball(frame)
            coordinate_red, coordinate_blue = vm.random_box('easy', frame, is_one_player=True)

            if box_seed_num != vm.current_seed:
                vm.is_answer_handled_red = False
                vm.is_answer_handled_blue = False

            rectangle_seed_num = vm.rect_num % 3
            vm.rect_num += 1

            blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = vm.score_calculation(frame,
                                                                                                        rectangle_seed_num,
                                                                                                        detection_blue,
                                                                                                        coordinate_blue,
                                                                                                        box_seed_num,
                                                                                                        detection_red,
                                                                                                        coordinate_red)

            vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                   is_answer_handled_blue)

            # vm.OnePlayerGameStats(frame, red_score, blue_score, vm.one_player_score, img_width, img_height)
            vm.TwoPlayerGameStats(frame, red_score, blue_score, vm.img_width, vm.img_height)

            cv2.imshow('Rhythm Box Slaughter', frame)
            # esc 키를 누르면 닫음 -> 후에 노래가 끝나면 종료로 수정해야 함

            if cv2.waitKey(15) == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self):
        vm = Video_Manager()

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

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            box_seed_num = vm.box_num // 90
            random.seed(box_seed_num)
            vm.box_num += 1

            detection_blue, detection_red = vm.tracking_ball(frame)
            coordinate_red, coordinate_blue = vm.random_box('easy', frame, is_one_player=False)

            if box_seed_num != vm.current_seed:
                vm.is_answer_handled_red = False
                vm.is_answer_handled_blue = False

            rectangle_seed_num = vm.rect_num % 3
            vm.rect_num += 1

            blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = vm.score_calculation(frame,
                                                                                                        rectangle_seed_num,
                                                                                                        detection_blue,
                                                                                                        coordinate_blue,
                                                                                                        box_seed_num,
                                                                                                        detection_red,
                                                                                                        coordinate_red)

            vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                   is_answer_handled_blue)

            # vm.OnePlayerGameStats(frame, red_score, blue_score, vm.one_player_score, img_width, img_height)
            vm.TwoPlayerGameStats(frame, red_score, blue_score, vm.img_width, vm.img_height)

            cv2.imshow('Rhythm Box Slaughter', frame)
            # esc 키를 누르면 닫음 -> 후에 노래가 끝나면 종료로 수정해야 함

            if cv2.waitKey(15) == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def game_start(self):
        if self.btn_player_1.isChecked():
            print('test: btn_player_1')
            self.player_1()
        elif self.btn_player_2.isChecked():
            print('test: btn_player_2')
            self.player_2()

    def youtube_play(self):
        youtube_player.player()

    def music_play(self):
        music_list = ['(음악을 선택하세요)',
                      'youtube music 1',
                      'cute',
                      'tenderness',
                      'acoustic breeze',
                      'better days']
        item = self.music.currentText()
        # index = self.music.findText(f'{item}', QtCore.Qt.MatchFixedString)    # findText: 인덱스를 return

        if item == music_list[0]:
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 1')

            thread = threading.Thread(target=self.youtube_play)
            thread.daemon = True
            thread.start()

        elif item == music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')

    def button(self):
        self.btn_player_1.setToolTip('1인용 게임')
        self.btn_player_2.setToolTip('2인용 게임')
        self.btn_start.setToolTip('누르면 게임을 시작합니다')

        self.music.move(200, 400)
        music_list = ['(음악을 선택하세요)',
                      'youtube music 1',
                      'cute',
                      'tenderness',
                      'acoustic breeze',
                      'better days']
        for i in music_list:
            self.music.addItem(i)
        self.music.setToolTip('배경음악을 선택하세요')

        vbox.addWidget(label)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.music)
        hbox.addWidget(self.btn_player_1)
        hbox.addWidget(self.btn_player_2)
        hbox.addWidget(self.btn_start)
        hbox.addStretch(1)

        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        # self.btn_player_1.clicked.connect(self.player_1)
        # self.btn_player_2.clicked.connect(self.player_2)
        # self.music.activated[str].connect(self.music_play)
        self.btn_start.clicked.connect(self.game_start)
        self.music.currentIndexChanged.connect(self.music_play)

    def background(self):
        bg = QtGui.QImage('mint_pink.png')
        scaled_bg = bg.scaled(400, 100)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg))
        app.setPalette(palette)

    def label_text(self):
        label.setText('리듬 박스 학살')
        label.setFont(QtGui.QFont('Arial', 15))
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def window_style(self):
        window.setWindowTitle('Rhythm Box Slaughter')
        window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        window.setLayout(vbox)
        window.setGeometry(0, 0, 400, 100)
        window.show()


def resources():
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())


if __name__ == '__main__':
    resources()

    app = QtWidgets.QApplication([])
    window = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout()
    label = QtWidgets.QLabel()

    app.setStyle('Fusion')

    main = MainWindow()

    sys.exit(app.exec_())
