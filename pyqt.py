import cv2
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import random
import threading
import pafy
import vlc
import time
import winsound
import ctypes
from video_manager import Video_Manager


class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.music = QtWidgets.QComboBox()
        self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        self.btn_start = QtWidgets.QPushButton('Game Start')

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()

        self.box_layout()
        self.background()
        self.window_style()
        self.button()

    def player_1(self, mode):
        vm = Video_Manager()

        # image_resizing
        img_width = vm.img_width
        img_height = vm.img_height

        # load_video
        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW + 0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            exit()

        while True:
            _, frame = vidcap.read()
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            if vm.game_finish == False:
                box_seed_num = vm.box_num // 90
                random.seed(box_seed_num)
                vm.box_num += 1

                detection_blue, detection_red = vm.tracking_ball(frame)
                coordinate_red, coordinate_blue = vm.random_box(mode, frame, is_one_player=True)

                if box_seed_num != vm.current_seed:
                    vm.is_answer_handled_red = False
                    vm.is_answer_handled_blue = False

                rectangle_seed_num = vm.rect_num % 3
                vm.rect_num += 1

                # 점수 계산
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = vm.score_calculation(frame,
                                                                                                              rectangle_seed_num,
                                                                                                              detection_blue,
                                                                                                              coordinate_blue,
                                                                                                              box_seed_num,
                                                                                                              detection_red,
                                                                                                              coordinate_red)

                # 정답 rect 그리기
                vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                       is_answer_handled_blue)

                # 점수 표기
                vm.PlayerGameStats(frame, red_score, blue_score, is_one_player=True)

                vm.frame_num = vm.frame_num + 1
                if vm.frame_num == 900:
                    vm.game_finish = True
            else:
                vm.Winner_effect(frame, red_score, blue_score, is_one_player=True)

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:
                ctypes.windll.user32.MessageBoxW(0, '게임을 종료합니다', '안내', 0)
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self, mode):
        vm = Video_Manager()

        # image_resizing
        img_width = vm.img_width
        img_height = vm.img_height

        # load_video
        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW + 0)

        if not vidcap.isOpened():
            print('카메라를 열 수 없습니다.')
            exit()

        while True:
            _, frame = vidcap.read()
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            if vm.game_finish == False:
                box_seed_num = vm.box_num // 90
                random.seed(box_seed_num)
                vm.box_num += 1

                detection_blue, detection_red = vm.tracking_ball(frame)
                coordinate_red, coordinate_blue = vm.random_box(mode, frame, is_one_player=False)

                if box_seed_num != vm.current_seed:
                    vm.is_answer_handled_red = False
                    vm.is_answer_handled_blue = False

                rectangle_seed_num = vm.rect_num % 3
                vm.rect_num += 1

                # 점수 계산
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue = vm.score_calculation(frame,
                                                                                                            rectangle_seed_num,
                                                                                                            detection_blue,
                                                                                                            coordinate_blue,
                                                                                                            box_seed_num,
                                                                                                            detection_red,
                                                                                                            coordinate_red)

                # 정답 rect 그리기
                vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                     is_answer_handled_blue)

                # 점수 표기
                vm.PlayerGameStats(frame, red_score, blue_score, is_one_player=False)

                vm.frame_num = vm.frame_num + 1
                if vm.frame_num == 900:
                    vm.game_finish = True
            else:
                vm.Winner_effect(frame, red_score, blue_score, is_one_player=False)

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:
                ctypes.windll.user32.MessageBoxW(0, '게임을 종료합니다', '안내', 0)
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def game_start_easy(self):
        if self.btn_player_1.isChecked():
            self.player_1('easy')
        elif self.btn_player_2.isChecked():
            self.player_2('easy')

    def game_start_normal(self):
        if self.btn_player_1.isChecked():
            self.player_1('normal')
        elif self.btn_player_2.isChecked():
            self.player_2('normal')

    def game_start_hard(self):
        if self.btn_player_1.isChecked():
            self.player_1('hard')
        elif self.btn_player_2.isChecked():
            self.player_2('hard')

    def game_start_hell(self):
        if self.btn_player_1.isChecked():
            self.player_1('hell')
        elif self.btn_player_2.isChecked():
            self.player_2('hell')

    def box_layout(self):
        self.btn_player_1.setToolTip('1인용 게임')
        self.btn_player_2.setToolTip('2인용 게임')
        self.btn_start.setToolTip('누르면 게임을 시작합니다')
        self.btn_start.setStyleSheet("QPushButton { background-color: rgb(255, 190, 11);}")

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.music)
        hbox.addWidget(self.btn_player_1)
        hbox.addWidget(self.btn_player_2)
        hbox.addWidget(self.btn_start)
        hbox.addStretch(1)

        self.vbox.addStretch(3)
        self.vbox.addLayout(hbox)
        self.vbox.addStretch(1)

    def background(self):
        bg_text = QtGui.QImage('bg.jpg')
        scaled_bg_text = bg_text.scaled(1280, 720)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg_text))
        app.setPalette(palette)

    def window_style(self):
        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.vbox)
        self.window.setGeometry(0, 0, 1280, 720)
        self.window.show()

    def youtube_play(self, url):
        try:
            audio = pafy.new(url)
            audio = audio.getbestaudio()
            play_url = audio.url

            instance = vlc.Instance()
            player = instance.media_player_new()
            media = instance.media_new(play_url)
            media.get_mrl()
            player.set_media(media)
            player.play()

            start = time.time()

            while True:
                if time.time() - start > 40:
                    player.pause()
                    break
                pass

        except KeyError as err:
            if err.args[0] == 'dislike_count':
                winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def button(self):
        self.music.move(200, 400)
        for i in self.music_list:
            self.music.addItem(i)
        self.music.setToolTip('배경음악을 선택하세요')
        self.music.setFixedSize(200, 30)

        self.btn_player_1.setStyleSheet(
            'QRadioButton{font: 15pt DOSMyungjo;} QRadioButton::indicator {width: 20px; height: 20px;};')
        self.btn_player_2.setStyleSheet(
            'QRadioButton{font: 15pt DOSMyungjo;} QRadioButton::indicator {width: 20px; height: 20px;};')

        self.btn_start.setFixedSize(150, 30)
        self.btn_start.setFont(QtGui.QFont('DOSMyungjo', 15))
        # self.btn_start.clicked.connect(self.game_start)

        self.music.currentIndexChanged.connect(self.music_play)

    def music_thread(self, url):
        thread = threading.Thread(target=lambda: self.youtube_play(url))
        thread.daemon = True
        thread.start()


class GameWindow1(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 1',
                  'cute',
                  'tenderness',
                  'acoustic breeze',
                  'better days',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=lXDyWT3VlKg&ab_channel=M2')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow2(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 2',
                  'cute 2',
                  'tenderness 2',
                  'acoustic breeze 2',
                  'better days 2',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/2v5iWf2KDCw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow3(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 3',
                  'cute 3',
                  'tenderness 3',
                  'acoustic breeze 3',
                  'better days 3',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=cSvgRKsML7o')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow4(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 4',
                  'cute 4',
                  'tenderness 4',
                  'acoustic breeze 4',
                  'better days 4',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/Y-JQ-RCyPpQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow5(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 5',
                  'cute 5',
                  'tenderness 5',
                  'acoustic breeze 5',
                  'better days 5',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/_sI_Ps7JSEk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow6(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 6',
                  'cute 6',
                  'tenderness 6',
                  'acoustic breeze 6',
                  'better days 6',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/sjkrrmBnpGE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow7(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 7',
                  'cute 7',
                  'tenderness 7',
                  'acoustic breeze 7',
                  'better days 7',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/CfPxlb8-ZQ0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow8(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 8',
                  'cute 8',
                  'tenderness 8',
                  'acoustic breeze 8',
                  'better days 8',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/IRyJe-0Uie0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow9(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 9',
                  'cute 9',
                  'tenderness 9',
                  'acoustic breeze 9',
                  'better days 9',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/bbxXdASyLQw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow10(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 10',
                  'cute 10',
                  'tenderness 10',
                  'acoustic breeze 10',
                  'better days 10',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/Hq2yWd5wG_M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow11(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 11',
                  'cute 11',
                  'tenderness 11',
                  'acoustic breeze 11',
                  'better days 11',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow12(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 12',
                  'cute 12',
                  'tenderness 12',
                  'acoustic breeze 12',
                  'better days 12',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow13(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 13',
                  'cute 13',
                  'tenderness 13',
                  'acoustic breeze 13',
                  'better days 13',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow14(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 14',
                  'cute 14',
                  'tenderness 14',
                  'acoustic breeze 14',
                  'better days 14',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow15(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 15',
                  'cute 15',
                  'tenderness 15',
                  'acoustic breeze 15',
                  'better days 15',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow16(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 16',
                  'cute 16',
                  'tenderness 16',
                  'acoustic breeze 16',
                  'better days 16',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow17(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 17',
                  'cute 17',
                  'tenderness 17',
                  'acoustic breeze 17',
                  'better days 17',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow18(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 18',
                  'cute 18',
                  'tenderness 18',
                  'acoustic breeze 18',
                  'better days 18',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow19(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 19',
                  'cute 19',
                  'tenderness 19',
                  'acoustic breeze 19',
                  'better days 19',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow20(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 20',
                  'cute 20',
                  'tenderness 20',
                  'acoustic breeze 20',
                  'better days 20',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow21(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 21',
                  'cute 21',
                  'tenderness 21',
                  'acoustic breeze 21',
                  'better days 21',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow22(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 22',
                  'cute 22',
                  'tenderness 22',
                  'acoustic breeze 22',
                  'better days 22',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow23(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 23',
                  'cute 23',
                  'tenderness 23',
                  'acoustic breeze 23',
                  'better days 23',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow24(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 24',
                  'cute 24',
                  'tenderness 24',
                  'acoustic breeze 24',
                  'better days 24',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow25(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 25',
                  'cute 25',
                  'tenderness 25',
                  'acoustic breeze 25',
                  'better days 25',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow26(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 26',
                  'cute 26',
                  'tenderness 26',
                  'acoustic breeze 26',
                  'better days 26',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow27(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 27',
                  'cute 27',
                  'tenderness 27',
                  'acoustic breeze 27',
                  'better days 27',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow28(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 28',
                  'cute 28',
                  'tenderness 28',
                  'acoustic breeze 28',
                  'better days 28',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow29(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 29',
                  'cute 29',
                  'tenderness 29',
                  'acoustic breeze 29',
                  'better days 29',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow30(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 30',
                  'cute 30',
                  'tenderness 30',
                  'acoustic breeze 30',
                  'better days 30',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow31(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 31',
                  'cute 31',
                  'tenderness 31',
                  'acoustic breeze 31',
                  'better days 31',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow32(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 32',
                  'cute 32',
                  'tenderness 32',
                  'acoustic breeze 32',
                  'better days 32',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow33(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 33',
                  'cute 33',
                  'tenderness 33',
                  'acoustic breeze 33',
                  'better days 33',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow34(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 34',
                  'cute 34',
                  'tenderness 34',
                  'acoustic breeze 34',
                  'better days 34',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow35(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 35',
                  'cute 35',
                  'tenderness 35',
                  'acoustic breeze 35',
                  'better days 35',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow36(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 36',
                  'cute 36',
                  'tenderness 36',
                  'acoustic breeze 36',
                  'better days 36',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow37(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 37',
                  'cute 37',
                  'tenderness 37',
                  'acoustic breeze 37',
                  'better days 37',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow38(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 38',
                  'cute 38',
                  'tenderness 38',
                  'acoustic breeze 38',
                  'better days 38',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow39(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 39',
                  'cute 39',
                  'tenderness 39',
                  'acoustic breeze 39',
                  'better days 39',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow40(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 40',
                  'cute 40',
                  'tenderness 40',
                  'acoustic breeze 40',
                  'better days 40',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow41(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 41',
                  'cute 41',
                  'tenderness 41',
                  'acoustic breeze 41',
                  'better days 41',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow42(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 42',
                  'cute 42',
                  'tenderness 42',
                  'acoustic breeze 42',
                  'better days 42',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow43(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 43',
                  'cute 43',
                  'tenderness 43',
                  'acoustic breeze 43',
                  'better days 43',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow44(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 44',
                  'cute 44',
                  'tenderness 44',
                  'acoustic breeze 44',
                  'better days 44',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow45(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 45',
                  'cute 45',
                  'tenderness 45',
                  'acoustic breeze 45',
                  'better days 45',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow46(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 46',
                  'cute 46',
                  'tenderness 46',
                  'acoustic breeze 46',
                  'better days 46',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow47(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 47',
                  'cute 47',
                  'tenderness 47',
                  'acoustic breeze 47',
                  'better days 47',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow48(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 48',
                  'cute 48',
                  'tenderness 48',
                  'acoustic breeze 48',
                  'better days 48',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow49(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 49',
                  'cute 49',
                  'tenderness 49',
                  'acoustic breeze 49',
                  'better days 49',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow50(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 50',
                  'cute 50',
                  'tenderness 50',
                  'acoustic breeze 50',
                  'better days 50',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow51(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 51',
                  'cute 51',
                  'tenderness 51',
                  'acoustic breeze 51',
                  'better days 51',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow52(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 52',
                  'cute 52',
                  'tenderness 52',
                  'acoustic breeze 52',
                  'better days 52',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow53(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 53',
                  'cute 53',
                  'tenderness 53',
                  'acoustic breeze 53',
                  'better days 53',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow54(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 54',
                  'cute 54',
                  'tenderness 54',
                  'acoustic breeze 54',
                  'better days 54',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow55(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 55',
                  'cute 55',
                  'tenderness 55',
                  'acoustic breeze 55',
                  'better days 55',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow56(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 56',
                  'cute 56',
                  'tenderness 56',
                  'acoustic breeze 56',
                  'better days 56',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow57(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 57',
                  'cute 57',
                  'tenderness 57',
                  'acoustic breeze 57',
                  'better days 57',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow58(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 58',
                  'cute 58',
                  'tenderness 58',
                  'acoustic breeze 58',
                  'better days 58',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow59(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 59',
                  'cute 59',
                  'tenderness 59',
                  'acoustic breeze 59',
                  'better days 59',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow60(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 60',
                  'cute 60',
                  'tenderness 60',
                  'acoustic breeze 60',
                  'better days 60',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow61(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 61',
                  'cute 61',
                  'tenderness 61',
                  'acoustic breeze 61',
                  'better days 61',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow62(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 62',
                  'cute 62',
                  'tenderness 62',
                  'acoustic breeze 62',
                  'better days 62',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow63(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 63',
                  'cute 63',
                  'tenderness 63',
                  'acoustic breeze 63',
                  'better days 63',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow64(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 64',
                  'cute 64',
                  'tenderness 64',
                  'acoustic breeze 64',
                  'better days 64',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow65(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 65',
                  'cute 65',
                  'tenderness 65',
                  'acoustic breeze 65',
                  'better days 65',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow66(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 66',
                  'cute 66',
                  'tenderness 66',
                  'acoustic breeze 66',
                  'better days 66',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow67(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 67',
                  'cute 67',
                  'tenderness 67',
                  'acoustic breeze 67',
                  'better days 67',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow68(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 68',
                  'cute 68',
                  'tenderness 68',
                  'acoustic breeze 68',
                  'better days 68',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow69(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 69',
                  'cute 69',
                  'tenderness 69',
                  'acoustic breeze 69',
                  'better days 69',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow70(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 70',
                  'cute 70',
                  'tenderness 70',
                  'acoustic breeze 70',
                  'better days 70',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow71(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 71',
                  'cute 71',
                  'tenderness 71',
                  'acoustic breeze 71',
                  'better days 71',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow72(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 72',
                  'cute 72',
                  'tenderness 72',
                  'acoustic breeze 72',
                  'better days 72',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow73(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 73',
                  'cute 73',
                  'tenderness 73',
                  'acoustic breeze 73',
                  'better days 73',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow74(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 74',
                  'cute 74',
                  'tenderness 74',
                  'acoustic breeze 74',
                  'better days 74',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow75(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 75',
                  'cute 75',
                  'tenderness 75',
                  'acoustic breeze 75',
                  'better days 75',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow76(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 76',
                  'cute 76',
                  'tenderness 76',
                  'acoustic breeze 76',
                  'better days 76',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow77(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 77',
                  'cute 77',
                  'tenderness 77',
                  'acoustic breeze 77',
                  'better days 77',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow78(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 78',
                  'cute 78',
                  'tenderness 78',
                  'acoustic breeze 78',
                  'better days 78',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow79(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 79',
                  'cute 79',
                  'tenderness 79',
                  'acoustic breeze 79',
                  'better days 79',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow80(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 80',
                  'cute 80',
                  'tenderness 80',
                  'acoustic breeze 80',
                  'better days 80',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow81(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 81',
                  'cute 81',
                  'tenderness 81',
                  'acoustic breeze 81',
                  'better days 81',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow82(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 82',
                  'cute 82',
                  'tenderness 82',
                  'acoustic breeze 82',
                  'better days 82',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow83(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 83',
                  'cute 83',
                  'tenderness 83',
                  'acoustic breeze 83',
                  'better days 83',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow84(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 84',
                  'cute 84',
                  'tenderness 84',
                  'acoustic breeze 84',
                  'better days 84',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow85(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 85',
                  'cute 85',
                  'tenderness 85',
                  'acoustic breeze 85',
                  'better days 85',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow86(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 86',
                  'cute 86',
                  'tenderness 86',
                  'acoustic breeze 86',
                  'better days 86',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow87(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 87',
                  'cute 87',
                  'tenderness 87',
                  'acoustic breeze 87',
                  'better days 87',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow88(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 88',
                  'cute 88',
                  'tenderness 88',
                  'acoustic breeze 88',
                  'better days 88',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow89(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 89',
                  'cute 89',
                  'tenderness 89',
                  'acoustic breeze 89',
                  'better days 89',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow90(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 90',
                  'cute 90',
                  'tenderness 90',
                  'acoustic breeze 90',
                  'better days 90',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow91(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 91',
                  'cute 91',
                  'tenderness 91',
                  'acoustic breeze 91',
                  'better days 91',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow92(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 92',
                  'cute 92',
                  'tenderness 92',
                  'acoustic breeze 92',
                  'better days 92',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow93(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 93',
                  'cute 93',
                  'tenderness 93',
                  'acoustic breeze 93',
                  'better days 93',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow94(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 94',
                  'cute 94',
                  'tenderness 94',
                  'acoustic breeze 94',
                  'better days 94',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow95(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 95',
                  'cute 95',
                  'tenderness 95',
                  'acoustic breeze 95',
                  'better days 95',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow96(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 96',
                  'cute 96',
                  'tenderness 96',
                  'acoustic breeze 96',
                  'better days 96',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow97(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 97',
                  'cute 97',
                  'tenderness 97',
                  'acoustic breeze 97',
                  'better days 97',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow98(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 98',
                  'cute 98',
                  'tenderness 98',
                  'acoustic breeze 98',
                  'better days 98',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow99(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 99',
                  'cute 99',
                  'tenderness 99',
                  'acoustic breeze 99',
                  'better days 99',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow100(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 100',
                  'cute 100',
                  'tenderness 100',
                  'acoustic breeze 100',
                  'better days 100',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow101(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 101',
                  'cute 101',
                  'tenderness 101',
                  'acoustic breeze 101',
                  'better days 101',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow102(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 102',
                  'cute 102',
                  'tenderness 102',
                  'acoustic breeze 102',
                  'better days 102',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow103(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 103',
                  'cute 103',
                  'tenderness 103',
                  'acoustic breeze 103',
                  'better days 103',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow104(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 104',
                  'cute 104',
                  'tenderness 104',
                  'acoustic breeze 104',
                  'better days 104',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow105(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 105',
                  'cute 105',
                  'tenderness 105',
                  'acoustic breeze 105',
                  'better days 105',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow106(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 106',
                  'cute 106',
                  'tenderness 106',
                  'acoustic breeze 106',
                  'better days 106',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow107(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 107',
                  'cute 107',
                  'tenderness 107',
                  'acoustic breeze 107',
                  'better days 107',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow108(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 108',
                  'cute 108',
                  'tenderness 108',
                  'acoustic breeze 108',
                  'better days 108',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow109(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 109',
                  'cute 109',
                  'tenderness 109',
                  'acoustic breeze 109',
                  'better days 109',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow110(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 110',
                  'cute 110',
                  'tenderness 110',
                  'acoustic breeze 110',
                  'better days 110',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow111(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 111',
                  'cute 111',
                  'tenderness 111',
                  'acoustic breeze 111',
                  'better days 111',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow112(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 112',
                  'cute 112',
                  'tenderness 112',
                  'acoustic breeze 112',
                  'better days 112',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow113(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 113',
                  'cute 113',
                  'tenderness 113',
                  'acoustic breeze 113',
                  'better days 113',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow114(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 114',
                  'cute 114',
                  'tenderness 114',
                  'acoustic breeze 114',
                  'better days 114',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow115(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 115',
                  'cute 115',
                  'tenderness 115',
                  'acoustic breeze 115',
                  'better days 115',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow116(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 116',
                  'cute 116',
                  'tenderness 116',
                  'acoustic breeze 116',
                  'better days 116',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow117(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 117',
                  'cute 117',
                  'tenderness 117',
                  'acoustic breeze 117',
                  'better days 117',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow118(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 118',
                  'cute 118',
                  'tenderness 118',
                  'acoustic breeze 118',
                  'better days 118',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow119(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 119',
                  'cute 119',
                  'tenderness 119',
                  'acoustic breeze 119',
                  'better days 119',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow120(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 120',
                  'cute 120',
                  'tenderness 120',
                  'acoustic breeze 120',
                  'better days 120',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow121(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 121',
                  'cute 121',
                  'tenderness 121',
                  'acoustic breeze 121',
                  'better days 121',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow122(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 122',
                  'cute 122',
                  'tenderness 122',
                  'acoustic breeze 122',
                  'better days 122',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow123(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 123',
                  'cute 123',
                  'tenderness 123',
                  'acoustic breeze 123',
                  'better days 123',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow124(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 124',
                  'cute 124',
                  'tenderness 124',
                  'acoustic breeze 124',
                  'better days 124',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow125(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 125',
                  'cute 125',
                  'tenderness 125',
                  'acoustic breeze 125',
                  'better days 125',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow126(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 126',
                  'cute 126',
                  'tenderness 126',
                  'acoustic breeze 126',
                  'better days 126',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow127(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 127',
                  'cute 127',
                  'tenderness 127',
                  'acoustic breeze 127',
                  'better days 127',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow128(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 128',
                  'cute 128',
                  'tenderness 128',
                  'acoustic breeze 128',
                  'better days 128',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow129(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 129',
                  'cute 129',
                  'tenderness 129',
                  'acoustic breeze 129',
                  'better days 129',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow130(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 130',
                  'cute 130',
                  'tenderness 130',
                  'acoustic breeze 130',
                  'better days 130',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow131(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 131',
                  'cute 131',
                  'tenderness 131',
                  'acoustic breeze 131',
                  'better days 131',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow132(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 132',
                  'cute 132',
                  'tenderness 132',
                  'acoustic breeze 132',
                  'better days 132',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow133(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 133',
                  'cute 133',
                  'tenderness 133',
                  'acoustic breeze 133',
                  'better days 133',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow134(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 134',
                  'cute 134',
                  'tenderness 134',
                  'acoustic breeze 134',
                  'better days 134',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow135(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 135',
                  'cute 135',
                  'tenderness 135',
                  'acoustic breeze 135',
                  'better days 135',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow136(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 136',
                  'cute 136',
                  'tenderness 136',
                  'acoustic breeze 136',
                  'better days 136',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow137(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 137',
                  'cute 137',
                  'tenderness 137',
                  'acoustic breeze 137',
                  'better days 137',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow138(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 138',
                  'cute 138',
                  'tenderness 138',
                  'acoustic breeze 138',
                  'better days 138',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow139(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 139',
                  'cute 139',
                  'tenderness 139',
                  'acoustic breeze 139',
                  'better days 139',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow140(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 140',
                  'cute 140',
                  'tenderness 140',
                  'acoustic breeze 140',
                  'better days 140',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow141(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 141',
                  'cute 141',
                  'tenderness 141',
                  'acoustic breeze 141',
                  'better days 141',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow142(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 142',
                  'cute 142',
                  'tenderness 142',
                  'acoustic breeze 142',
                  'better days 142',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow143(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 143',
                  'cute 143',
                  'tenderness 143',
                  'acoustic breeze 143',
                  'better days 143',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow144(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 144',
                  'cute 144',
                  'tenderness 144',
                  'acoustic breeze 144',
                  'better days 144',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow145(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 145',
                  'cute 145',
                  'tenderness 145',
                  'acoustic breeze 145',
                  'better days 145',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow146(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 146',
                  'cute 146',
                  'tenderness 146',
                  'acoustic breeze 146',
                  'better days 146',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow147(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 147',
                  'cute 147',
                  'tenderness 147',
                  'acoustic breeze 147',
                  'better days 147',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow148(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 148',
                  'cute 148',
                  'tenderness 148',
                  'acoustic breeze 148',
                  'better days 148',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow149(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 149',
                  'cute 149',
                  'tenderness 149',
                  'acoustic breeze 149',
                  'better days 149',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow150(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 150',
                  'cute 150',
                  'tenderness 150',
                  'acoustic breeze 150',
                  'better days 150',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow151(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 151',
                  'cute 151',
                  'tenderness 151',
                  'acoustic breeze 151',
                  'better days 151',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow152(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 152',
                  'cute 152',
                  'tenderness 152',
                  'acoustic breeze 152',
                  'better days 152',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow153(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 153',
                  'cute 153',
                  'tenderness 153',
                  'acoustic breeze 153',
                  'better days 153',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow154(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 154',
                  'cute 154',
                  'tenderness 154',
                  'acoustic breeze 154',
                  'better days 154',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow155(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 155',
                  'cute 155',
                  'tenderness 155',
                  'acoustic breeze 155',
                  'better days 155',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow156(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 156',
                  'cute 156',
                  'tenderness 156',
                  'acoustic breeze 156',
                  'better days 156',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow157(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 157',
                  'cute 157',
                  'tenderness 157',
                  'acoustic breeze 157',
                  'better days 157',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow158(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 158',
                  'cute 158',
                  'tenderness 158',
                  'acoustic breeze 158',
                  'better days 158',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow159(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 159',
                  'cute 159',
                  'tenderness 159',
                  'acoustic breeze 159',
                  'better days 159',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow160(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 160',
                  'cute 160',
                  'tenderness 160',
                  'acoustic breeze 160',
                  'better days 160',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow161(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 161',
                  'cute 161',
                  'tenderness 161',
                  'acoustic breeze 161',
                  'better days 161',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow162(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 162',
                  'cute 162',
                  'tenderness 162',
                  'acoustic breeze 162',
                  'better days 162',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow163(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 163',
                  'cute 163',
                  'tenderness 163',
                  'acoustic breeze 163',
                  'better days 163',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow164(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 164',
                  'cute 164',
                  'tenderness 164',
                  'acoustic breeze 164',
                  'better days 164',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow165(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 165',
                  'cute 165',
                  'tenderness 165',
                  'acoustic breeze 165',
                  'better days 165',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow166(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 166',
                  'cute 166',
                  'tenderness 166',
                  'acoustic breeze 166',
                  'better days 166',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow167(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 167',
                  'cute 167',
                  'tenderness 167',
                  'acoustic breeze 167',
                  'better days 167',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow168(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 168',
                  'cute 168',
                  'tenderness 168',
                  'acoustic breeze 168',
                  'better days 168',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow169(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 169',
                  'cute 169',
                  'tenderness 169',
                  'acoustic breeze 169',
                  'better days 169',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow170(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 170',
                  'cute 170',
                  'tenderness 170',
                  'acoustic breeze 170',
                  'better days 170',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow171(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 171',
                  'cute 171',
                  'tenderness 171',
                  'acoustic breeze 171',
                  'better days 171',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow172(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 172',
                  'cute 172',
                  'tenderness 172',
                  'acoustic breeze 172',
                  'better days 172',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow173(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 173',
                  'cute 173',
                  'tenderness 173',
                  'acoustic breeze 173',
                  'better days 173',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow174(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 174',
                  'cute 174',
                  'tenderness 174',
                  'acoustic breeze 174',
                  'better days 174',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow175(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 175',
                  'cute 175',
                  'tenderness 175',
                  'acoustic breeze 175',
                  'better days 175',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow176(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 176',
                  'cute 176',
                  'tenderness 176',
                  'acoustic breeze 176',
                  'better days 176',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow177(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 177',
                  'cute 177',
                  'tenderness 177',
                  'acoustic breeze 177',
                  'better days 177',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow178(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 178',
                  'cute 178',
                  'tenderness 178',
                  'acoustic breeze 178',
                  'better days 178',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow179(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 179',
                  'cute 179',
                  'tenderness 179',
                  'acoustic breeze 179',
                  'better days 179',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow180(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 180',
                  'cute 180',
                  'tenderness 180',
                  'acoustic breeze 180',
                  'better days 180',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow181(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 181',
                  'cute 181',
                  'tenderness 181',
                  'acoustic breeze 181',
                  'better days 181',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow182(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 182',
                  'cute 182',
                  'tenderness 182',
                  'acoustic breeze 182',
                  'better days 182',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow183(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 183',
                  'cute 183',
                  'tenderness 183',
                  'acoustic breeze 183',
                  'better days 183',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow184(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 184',
                  'cute 184',
                  'tenderness 184',
                  'acoustic breeze 184',
                  'better days 184',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow185(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 185',
                  'cute 185',
                  'tenderness 185',
                  'acoustic breeze 185',
                  'better days 185',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow186(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 186',
                  'cute 186',
                  'tenderness 186',
                  'acoustic breeze 186',
                  'better days 186',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow187(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 187',
                  'cute 187',
                  'tenderness 187',
                  'acoustic breeze 187',
                  'better days 187',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow188(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 188',
                  'cute 188',
                  'tenderness 188',
                  'acoustic breeze 188',
                  'better days 188',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow189(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 189',
                  'cute 189',
                  'tenderness 189',
                  'acoustic breeze 189',
                  'better days 189',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow190(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 190',
                  'cute 190',
                  'tenderness 190',
                  'acoustic breeze 190',
                  'better days 190',
                  '6',
                  '7',
                  '8',
                  '9',
                  '10']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7TO_oHxuk6c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t902Fc_gABM')
            self.btn_start.clicked.connect(self.game_start_easy)


class FindSongs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()

        self.label_1 = QtWidgets.QLabel()
        self.label_2 = QtWidgets.QLabel()
        self.btn_go = QtWidgets.QPushButton('선택')

        self.song_img_1 = QtWidgets.QRadioButton('GFRIEND - 시간을 달려서 (Rough)')
        self.song_img_2 = QtWidgets.QRadioButton("NU'EST - Love Paint (every afternoon)")
        self.song_img_3 = QtWidgets.QRadioButton('EXO - Heart Attack')
        self.song_img_4 = QtWidgets.QRadioButton('Red Velvet - Ice Cream Cake')
        self.song_img_5 = QtWidgets.QRadioButton('EXO - Monster')
        self.song_img_6 = QtWidgets.QRadioButton('IU - 스물셋')
        self.song_img_7 = QtWidgets.QRadioButton('현아 - 빨개요')
        self.song_img_8 = QtWidgets.QRadioButton('에일리 - 노래가 늘었어')
        self.song_img_9 = QtWidgets.QRadioButton('INFINITE - 내꺼하자')
        self.song_img_10 = QtWidgets.QRadioButton('f(x) - Lollipop (feat. SHINee)')
        self.song_img_11 = QtWidgets.QRadioButton('After School - 너 때문에')
        self.song_img_12 = QtWidgets.QRadioButton('BoA - One Dream (Feat. HENRY&&KEY)')
        self.song_img_13 = QtWidgets.QRadioButton('STSTAR - One More Day')
        self.song_img_14 = QtWidgets.QRadioButton('가인 - 피어나')
        self.song_img_15 = QtWidgets.QRadioButton('박효신 - 야생화')
        self.song_img_16 = QtWidgets.QRadioButton('NCT 127 - Switch')
        self.song_img_17 = QtWidgets.QRadioButton('VIXX - 사슬 (Chained up)')
        self.song_img_18 = QtWidgets.QRadioButton('BoA - Only One')
        self.song_img_19 = QtWidgets.QRadioButton('2NE1 - 안녕')
        self.song_img_20 = QtWidgets.QRadioButton('휘성 - Night and Day')

        self.box_layout()
        self.match()
        self.background()
        self.text_style()
        self.msg_box()

        self.w = None

    def vbox_style(self, song_img):
        song_img.setIconSize(QtCore.QSize(100, 100))
        song_img.setAutoExclusive(False)
        # shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        # song_img.setGraphicsEffect(shadow)

    def box_layout(self):
        self.vbox.addWidget(self.label_1)
        self.vbox.addWidget(self.label_2)

        self.btn_go.setFont(QtGui.QFont('DOSMyungjo', 30))
        self.btn_go.setFixedSize(QtCore.QSize(150, 50))
        self.btn_go.setStyleSheet(
            "QPushButton {color: black; background-color: rgb(255, 190, 11); border-radius: 5px;}")

        vbox_img_1 = QtWidgets.QVBoxLayout()

        vbox_img_1.addWidget(self.song_img_1)
        self.song_img_1.setIcon(QtGui.QIcon('rough.jpg'))
        self.vbox_style(self.song_img_1)

        vbox_img_1.addWidget(self.song_img_2)
        self.song_img_2.setIcon(QtGui.QIcon('love_paint.jpg'))
        self.vbox_style(self.song_img_2)

        vbox_img_1.addWidget(self.song_img_3)
        self.song_img_3.setIcon(QtGui.QIcon('heart_attack.jpg'))
        self.vbox_style(self.song_img_3)

        vbox_img_1.addWidget(self.song_img_4)
        self.song_img_4.setIcon(QtGui.QIcon('ice_cream_cake.jpg'))
        self.vbox_style(self.song_img_4)

        vbox_img_1.addWidget(self.song_img_5)
        self.song_img_5.setIcon(QtGui.QIcon('monster.jpg'))
        self.vbox_style(self.song_img_5)

        vbox_img_2 = QtWidgets.QVBoxLayout()

        vbox_img_2.addWidget(self.song_img_6)
        self.song_img_6.setIcon(QtGui.QIcon('23.jpg'))
        self.vbox_style(self.song_img_6)

        vbox_img_2.addWidget(self.song_img_7)
        self.song_img_7.setIcon(QtGui.QIcon('red.jpg'))
        self.vbox_style(self.song_img_7)

        vbox_img_2.addWidget(self.song_img_8)
        self.song_img_8.setIcon(QtGui.QIcon('ailee.jpg'))
        self.vbox_style(self.song_img_8)

        vbox_img_2.addWidget(self.song_img_9)
        self.song_img_9.setIcon(QtGui.QIcon('be_mine.jpg'))
        self.vbox_style(self.song_img_9)

        vbox_img_2.addWidget(self.song_img_10)
        self.song_img_10.setIcon(QtGui.QIcon('lollipop.jpg'))
        self.vbox_style(self.song_img_10)

        vbox_img_3 = QtWidgets.QVBoxLayout()

        vbox_img_3.addWidget(self.song_img_11)
        self.song_img_11.setIcon(QtGui.QIcon('after_school.jpg'))
        self.vbox_style(self.song_img_11)

        vbox_img_3.addWidget(self.song_img_12)
        self.song_img_12.setIcon(QtGui.QIcon('one_dream.jpg'))
        self.vbox_style(self.song_img_12)

        vbox_img_3.addWidget(self.song_img_13)
        self.song_img_13.setIcon(QtGui.QIcon('sistar.jpg'))
        self.vbox_style(self.song_img_13)

        vbox_img_3.addWidget(self.song_img_14)
        self.song_img_14.setIcon(QtGui.QIcon('gain.jpg'))
        self.vbox_style(self.song_img_14)

        vbox_img_3.addWidget(self.song_img_15)
        self.song_img_15.setIcon(QtGui.QIcon('wild_flower.jpg'))
        self.vbox_style(self.song_img_15)

        vbox_img_4 = QtWidgets.QVBoxLayout()

        vbox_img_4.addWidget(self.song_img_16)
        self.song_img_16.setIcon(QtGui.QIcon('switch.jpg'))
        self.vbox_style(self.song_img_16)

        vbox_img_4.addWidget(self.song_img_17)
        self.song_img_17.setIcon(QtGui.QIcon('chained_up.jpg'))
        self.vbox_style(self.song_img_17)

        vbox_img_4.addWidget(self.song_img_18)
        self.song_img_18.setIcon(QtGui.QIcon('only_one.jpg'))
        self.vbox_style(self.song_img_18)

        vbox_img_4.addWidget(self.song_img_19)
        self.song_img_19.setIcon(QtGui.QIcon('goodbye.jpg'))
        self.vbox_style(self.song_img_19)

        vbox_img_4.addWidget(self.song_img_20)
        self.song_img_20.setIcon(QtGui.QIcon('night_and_day.jpg'))
        self.vbox_style(self.song_img_20)

        self.hbox.addLayout(vbox_img_1)
        self.hbox.addLayout(vbox_img_2)
        self.hbox.addLayout(vbox_img_3)
        self.hbox.addLayout(vbox_img_4)

        self.grid_layout.addLayout(self.vbox, 0, 0)
        self.grid_layout.addLayout(self.hbox, 1, 0)
        self.grid_layout.addWidget(self.btn_go, 2, 0, alignment=QtCore.Qt.AlignCenter)

        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.grid_layout)
        self.window.setGeometry(0, 0, 1550, 800)
        self.window.show()

    def match(self):
        self.song_img_1.clicked.connect(self.current_index)
        self.song_img_2.clicked.connect(self.current_index)
        self.song_img_3.clicked.connect(self.current_index)
        self.song_img_4.clicked.connect(self.current_index)
        self.song_img_5.clicked.connect(self.current_index)
        self.song_img_6.clicked.connect(self.current_index)
        self.song_img_7.clicked.connect(self.current_index)
        self.song_img_8.clicked.connect(self.current_index)
        self.song_img_9.clicked.connect(self.current_index)
        self.song_img_10.clicked.connect(self.current_index)
        self.song_img_11.clicked.connect(self.current_index)
        self.song_img_12.clicked.connect(self.current_index)
        self.song_img_13.clicked.connect(self.current_index)
        self.song_img_14.clicked.connect(self.current_index)
        self.song_img_15.clicked.connect(self.current_index)
        self.song_img_16.clicked.connect(self.current_index)
        self.song_img_17.clicked.connect(self.current_index)
        self.song_img_18.clicked.connect(self.current_index)
        self.song_img_19.clicked.connect(self.current_index)
        self.song_img_20.clicked.connect(self.current_index)

    def current_index(self):
        if self.song_img_1.isChecked():
            if self.song_img_2.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_1)
            elif self.song_img_3.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_2)
            elif self.song_img_4.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_3)
            elif self.song_img_5.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_4)
            elif self.song_img_6.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_5)
            elif self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_6)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_7)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_8)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_9)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_10)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_11)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_12)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_13)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_14)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_15)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_16)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_17)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_18)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_19)

        elif self.song_img_2.isChecked():
            if self.song_img_3.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_20)
            elif self.song_img_4.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_21)
            elif self.song_img_5.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_22)
            elif self.song_img_6.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_23)
            elif self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_24)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_25)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_26)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_27)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_28)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_29)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_30)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_31)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_32)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_33)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_34)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_35)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_36)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_37)

        elif self.song_img_3.isChecked():
            if self.song_img_4.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_38)
            elif self.song_img_5.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_39)
            elif self.song_img_6.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_40)
            elif self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_41)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_42)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_43)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_44)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_45)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_46)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_47)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_48)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_49)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_50)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_51)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_52)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_53)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_54)

        elif self.song_img_4.isChecked():
            if self.song_img_5.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_55)
            elif self.song_img_6.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_56)
            elif self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_57)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_58)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_59)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_60)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_61)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_62)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_63)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_64)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_65)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_66)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_67)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_68)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_69)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_70)

        elif self.song_img_5.isChecked():
            if self.song_img_6.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_71)
            elif self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_72)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_73)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_74)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_75)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_76)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_77)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_78)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_79)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_80)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_81)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_82)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_83)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_84)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_85)

        elif self.song_img_6.isChecked():
            if self.song_img_7.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_86)
            elif self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_87)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_88)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_89)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_90)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_91)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_92)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_93)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_94)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_95)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_96)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_97)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_98)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_99)

        elif self.song_img_7.isChecked():
            if self.song_img_8.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_100)
            elif self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_101)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_102)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_103)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_104)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_105)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_106)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_107)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_108)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_109)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_110)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_111)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_112)

        elif self.song_img_8.isChecked():
            if self.song_img_9.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_113)
            elif self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_114)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_115)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_116)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_117)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_118)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_119)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_120)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_121)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_122)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_123)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_124)

        elif self.song_img_9.isChecked():
            if self.song_img_10.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_125)
            elif self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_126)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_127)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_128)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_129)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_130)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_131)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_132)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_133)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_134)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_135)

        elif self.song_img_10.isChecked():
            if self.song_img_11.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_136)
            elif self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_137)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_138)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_139)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_140)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_141)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_142)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_143)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_144)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_145)

        elif self.song_img_11.isChecked():
            if self.song_img_12.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_146)
            elif self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_147)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_148)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_149)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_150)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_151)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_152)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_153)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_154)

        elif self.song_img_12.isChecked():
            if self.song_img_13.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_155)
            elif self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_156)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_157)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_158)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_159)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_160)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_161)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_162)

        elif self.song_img_13.isChecked():
            if self.song_img_14.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_163)
            elif self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_164)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_165)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_166)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_167)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_168)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_169)

        elif self.song_img_14.isChecked():
            if self.song_img_15.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_170)
            elif self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_171)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_172)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_173)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_174)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_175)

        elif self.song_img_15.isChecked():
            if self.song_img_16.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_176)
            elif self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_177)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_178)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_179)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_180)

        elif self.song_img_16.isChecked():
            if self.song_img_17.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_181)
            elif self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_182)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_183)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_184)

        elif self.song_img_17.isChecked():
            if self.song_img_18.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_185)
            elif self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_186)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_187)

        elif self.song_img_18.isChecked():
            if self.song_img_19.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_188)
            elif self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_189)

        elif self.song_img_19.isChecked():
            if self.song_img_20.isChecked():
                self.btn_go.clicked.connect(self.btn_go_clicked_190)

    def background(self):
        bg = QtGui.QImage('bg_no_text.jpg')
        scaled_bg = bg.scaled(1550, 800)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg))
        app.setPalette(palette)

    def text_style(self):
        self.label_1.setText('리듬 박스 학살')
        self.label_1.setFont(QtGui.QFont('DOSMyungjo', 50, weight=QtGui.QFont.Bold))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)

        self.label_2.setText('노래를 2곡 선택한 뒤 선택 버튼을 눌러주세요')
        self.label_2.setFont(QtGui.QFont('DOSMyungjo'))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

    def msg_box(self):
        QtWidgets.QMessageBox.about(self, '안내', '노래를 2곡 선택한 뒤 선택 버튼을 눌러주세요')

    def new_window(self, game_window):
        if self.w is None:
            self.w = game_window

        else:
            self.w.close()
            self.w = None

    def btn_go_clicked_1(self):
        self.new_window(GameWindow1())

    def btn_go_clicked_2(self):
        self.new_window(GameWindow2())

    def btn_go_clicked_3(self):
        self.new_window(GameWindow3())

    def btn_go_clicked_4(self):
        self.new_window(GameWindow4())

    def btn_go_clicked_5(self):
        self.new_window(GameWindow5())

    def btn_go_clicked_6(self):
        self.new_window(GameWindow6())

    def btn_go_clicked_7(self):
        self.new_window(GameWindow7())

    def btn_go_clicked_8(self):
        self.new_window(GameWindow8())

    def btn_go_clicked_9(self):
        self.new_window(GameWindow9())

    def btn_go_clicked_10(self):
        self.new_window(GameWindow10())

    def btn_go_clicked_11(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_12(self):
        self.new_window(GameWindow12())

    def btn_go_clicked_13(self):
        self.new_window(GameWindow13())

    def btn_go_clicked_14(self):
        self.new_window(GameWindow14())

    def btn_go_clicked_15(self):
        self.new_window(GameWindow15())

    def btn_go_clicked_16(self):
        self.new_window(GameWindow16())

    def btn_go_clicked_17(self):
        self.new_window(GameWindow17())

    def btn_go_clicked_18(self):
        self.new_window(GameWindow18())

    def btn_go_clicked_19(self):
        self.new_window(GameWindow19())

    def btn_go_clicked_20(self):
        self.new_window(GameWindow20())

    def btn_go_clicked_21(self):
        self.new_window(GameWindow21())

    def btn_go_clicked_22(self):
        self.new_window(GameWindow22())

    def btn_go_clicked_23(self):
        self.new_window(GameWindow23())

    def btn_go_clicked_24(self):
        self.new_window(GameWindow24())

    def btn_go_clicked_25(self):
        self.new_window(GameWindow25())

    def btn_go_clicked_26(self):
        self.new_window(GameWindow26())

    def btn_go_clicked_27(self):
        self.new_window(GameWindow27())

    def btn_go_clicked_28(self):
        self.new_window(GameWindow28())

    def btn_go_clicked_29(self):
        self.new_window(GameWindow29())

    def btn_go_clicked_30(self):
        self.new_window(GameWindow30())

    def btn_go_clicked_31(self):
        self.new_window(GameWindow31())

    def btn_go_clicked_32(self):
        self.new_window(GameWindow32())

    def btn_go_clicked_33(self):
        self.new_window(GameWindow33())

    def btn_go_clicked_34(self):
        self.new_window(GameWindow34())

    def btn_go_clicked_35(self):
        self.new_window(GameWindow35())

    def btn_go_clicked_36(self):
        self.new_window(GameWindow36())

    def btn_go_clicked_37(self):
        self.new_window(GameWindow37())

    def btn_go_clicked_38(self):
        self.new_window(GameWindow38())

    def btn_go_clicked_39(self):
        self.new_window(GameWindow39())

    def btn_go_clicked_40(self):
        self.new_window(GameWindow40())

    def btn_go_clicked_41(self):
        self.new_window(GameWindow41())

    def btn_go_clicked_42(self):
        self.new_window(GameWindow42())

    def btn_go_clicked_43(self):
        self.new_window(GameWindow43())

    def btn_go_clicked_44(self):
        self.new_window(GameWindow44())

    def btn_go_clicked_45(self):
        self.new_window(GameWindow45())

    def btn_go_clicked_46(self):
        self.new_window(GameWindow46())

    def btn_go_clicked_47(self):
        self.new_window(GameWindow47())

    def btn_go_clicked_48(self):
        self.new_window(GameWindow48())

    def btn_go_clicked_49(self):
        self.new_window(GameWindow49())

    def btn_go_clicked_50(self):
        self.new_window(GameWindow50())

    def btn_go_clicked_51(self):
        self.new_window(GameWindow51())

    def btn_go_clicked_52(self):
        self.new_window(GameWindow52())

    def btn_go_clicked_53(self):
        self.new_window(GameWindow53())

    def btn_go_clicked_54(self):
        self.new_window(GameWindow54())

    def btn_go_clicked_55(self):
        self.new_window(GameWindow55())

    def btn_go_clicked_56(self):
        self.new_window(GameWindow56())

    def btn_go_clicked_57(self):
        self.new_window(GameWindow57())

    def btn_go_clicked_58(self):
        self.new_window(GameWindow58())

    def btn_go_clicked_59(self):
        self.new_window(GameWindow59())

    def btn_go_clicked_60(self):
        self.new_window(GameWindow60())

    def btn_go_clicked_61(self):
        self.new_window(GameWindow61())

    def btn_go_clicked_62(self):
        self.new_window(GameWindow62())

    def btn_go_clicked_63(self):
        self.new_window(GameWindow63())

    def btn_go_clicked_64(self):
        self.new_window(GameWindow64())

    def btn_go_clicked_65(self):
        self.new_window(GameWindow65())

    def btn_go_clicked_66(self):
        self.new_window(GameWindow66())

    def btn_go_clicked_67(self):
        self.new_window(GameWindow67())

    def btn_go_clicked_68(self):
        self.new_window(GameWindow68())

    def btn_go_clicked_69(self):
        self.new_window(GameWindow69())

    def btn_go_clicked_70(self):
        self.new_window(GameWindow70())

    def btn_go_clicked_71(self):
        self.new_window(GameWindow71())

    def btn_go_clicked_72(self):
        self.new_window(GameWindow72())

    def btn_go_clicked_73(self):
        self.new_window(GameWindow73())

    def btn_go_clicked_74(self):
        self.new_window(GameWindow74())

    def btn_go_clicked_75(self):
        self.new_window(GameWindow75())

    def btn_go_clicked_76(self):
        self.new_window(GameWindow76())

    def btn_go_clicked_77(self):
        self.new_window(GameWindow77())

    def btn_go_clicked_78(self):
        self.new_window(GameWindow78())

    def btn_go_clicked_79(self):
        self.new_window(GameWindow79())

    def btn_go_clicked_80(self):
        self.new_window(GameWindow80())

    def btn_go_clicked_81(self):
        self.new_window(GameWindow81())

    def btn_go_clicked_82(self):
        self.new_window(GameWindow82())

    def btn_go_clicked_83(self):
        self.new_window(GameWindow83())

    def btn_go_clicked_84(self):
        self.new_window(GameWindow84())

    def btn_go_clicked_85(self):
        self.new_window(GameWindow85())

    def btn_go_clicked_86(self):
        self.new_window(GameWindow86())

    def btn_go_clicked_87(self):
        self.new_window(GameWindow87())

    def btn_go_clicked_88(self):
        self.new_window(GameWindow88())

    def btn_go_clicked_89(self):
        self.new_window(GameWindow89())

    def btn_go_clicked_90(self):
        self.new_window(GameWindow90())

    def btn_go_clicked_91(self):
        self.new_window(GameWindow91())

    def btn_go_clicked_92(self):
        self.new_window(GameWindow92())

    def btn_go_clicked_93(self):
        self.new_window(GameWindow93())

    def btn_go_clicked_94(self):
        self.new_window(GameWindow94())

    def btn_go_clicked_95(self):
        self.new_window(GameWindow95())

    def btn_go_clicked_96(self):
        self.new_window(GameWindow96())

    def btn_go_clicked_97(self):
        self.new_window(GameWindow97())

    def btn_go_clicked_98(self):
        self.new_window(GameWindow98())

    def btn_go_clicked_99(self):
        self.new_window(GameWindow99())

    def btn_go_clicked_100(self):
        self.new_window(GameWindow100())

    def btn_go_clicked_101(self):
        self.new_window(GameWindow101())

    def btn_go_clicked_102(self):
        self.new_window(GameWindow102())

    def btn_go_clicked_103(self):
        self.new_window(GameWindow103())

    def btn_go_clicked_104(self):
        self.new_window(GameWindow104())

    def btn_go_clicked_105(self):
        self.new_window(GameWindow105())

    def btn_go_clicked_106(self):
        self.new_window(GameWindow106())

    def btn_go_clicked_107(self):
        self.new_window(GameWindow107())

    def btn_go_clicked_108(self):
        self.new_window(GameWindow108())

    def btn_go_clicked_109(self):
        self.new_window(GameWindow109())

    def btn_go_clicked_110(self):
        self.new_window(GameWindow110())

    def btn_go_clicked_111(self):
        self.new_window(GameWindow111())

    def btn_go_clicked_112(self):
        self.new_window(GameWindow112())

    def btn_go_clicked_113(self):
        self.new_window(GameWindow113())

    def btn_go_clicked_114(self):
        self.new_window(GameWindow114())

    def btn_go_clicked_115(self):
        self.new_window(GameWindow115())

    def btn_go_clicked_116(self):
        self.new_window(GameWindow116())

    def btn_go_clicked_117(self):
        self.new_window(GameWindow117())

    def btn_go_clicked_118(self):
        self.new_window(GameWindow118())

    def btn_go_clicked_119(self):
        self.new_window(GameWindow119())

    def btn_go_clicked_120(self):
        self.new_window(GameWindow120())

    def btn_go_clicked_121(self):
        self.new_window(GameWindow121())

    def btn_go_clicked_122(self):
        self.new_window(GameWindow122())

    def btn_go_clicked_123(self):
        self.new_window(GameWindow123())

    def btn_go_clicked_124(self):
        self.new_window(GameWindow124())

    def btn_go_clicked_125(self):
        self.new_window(GameWindow125())

    def btn_go_clicked_126(self):
        self.new_window(GameWindow126())

    def btn_go_clicked_127(self):
        self.new_window(GameWindow127())

    def btn_go_clicked_128(self):
        self.new_window(GameWindow128())

    def btn_go_clicked_129(self):
        self.new_window(GameWindow129())

    def btn_go_clicked_130(self):
        self.new_window(GameWindow130())

    def btn_go_clicked_131(self):
        self.new_window(GameWindow131())

    def btn_go_clicked_132(self):
        self.new_window(GameWindow132())

    def btn_go_clicked_133(self):
        self.new_window(GameWindow133())

    def btn_go_clicked_134(self):
        self.new_window(GameWindow134())

    def btn_go_clicked_135(self):
        self.new_window(GameWindow135())

    def btn_go_clicked_136(self):
        self.new_window(GameWindow136())

    def btn_go_clicked_137(self):
        self.new_window(GameWindow137())

    def btn_go_clicked_138(self):
        self.new_window(GameWindow138())

    def btn_go_clicked_139(self):
        self.new_window(GameWindow139())

    def btn_go_clicked_140(self):
        self.new_window(GameWindow140())

    def btn_go_clicked_141(self):
        self.new_window(GameWindow141())

    def btn_go_clicked_142(self):
        self.new_window(GameWindow142())

    def btn_go_clicked_143(self):
        self.new_window(GameWindow143())

    def btn_go_clicked_144(self):
        self.new_window(GameWindow144())

    def btn_go_clicked_145(self):
        self.new_window(GameWindow145())

    def btn_go_clicked_146(self):
        self.new_window(GameWindow146())

    def btn_go_clicked_147(self):
        self.new_window(GameWindow147())

    def btn_go_clicked_148(self):
        self.new_window(GameWindow148())

    def btn_go_clicked_149(self):
        self.new_window(GameWindow149())

    def btn_go_clicked_150(self):
        self.new_window(GameWindow150())

    def btn_go_clicked_151(self):
        self.new_window(GameWindow151())

    def btn_go_clicked_152(self):
        self.new_window(GameWindow152())

    def btn_go_clicked_153(self):
        self.new_window(GameWindow153())

    def btn_go_clicked_154(self):
        self.new_window(GameWindow154())

    def btn_go_clicked_155(self):
        self.new_window(GameWindow155())

    def btn_go_clicked_156(self):
        self.new_window(GameWindow156())

    def btn_go_clicked_157(self):
        self.new_window(GameWindow157())

    def btn_go_clicked_158(self):
        self.new_window(GameWindow158())

    def btn_go_clicked_159(self):
        self.new_window(GameWindow159())

    def btn_go_clicked_160(self):
        self.new_window(GameWindow160())

    def btn_go_clicked_161(self):
        self.new_window(GameWindow161())

    def btn_go_clicked_162(self):
        self.new_window(GameWindow162())

    def btn_go_clicked_163(self):
        self.new_window(GameWindow163())

    def btn_go_clicked_164(self):
        self.new_window(GameWindow64())

    def btn_go_clicked_165(self):
        self.new_window(GameWindow165())

    def btn_go_clicked_166(self):
        self.new_window(GameWindow166())

    def btn_go_clicked_167(self):
        self.new_window(GameWindow167())

    def btn_go_clicked_168(self):
        self.new_window(GameWindow168())

    def btn_go_clicked_169(self):
        self.new_window(GameWindow169())

    def btn_go_clicked_170(self):
        self.new_window(GameWindow170())

    def btn_go_clicked_171(self):
        self.new_window(GameWindow171())

    def btn_go_clicked_172(self):
        self.new_window(GameWindow172())

    def btn_go_clicked_173(self):
        self.new_window(GameWindow173())

    def btn_go_clicked_174(self):
        self.new_window(GameWindow174())

    def btn_go_clicked_175(self):
        self.new_window(GameWindow175())

    def btn_go_clicked_176(self):
        self.new_window(GameWindow176())

    def btn_go_clicked_177(self):
        self.new_window(GameWindow177())

    def btn_go_clicked_178(self):
        self.new_window(GameWindow178())

    def btn_go_clicked_179(self):
        self.new_window(GameWindow179())

    def btn_go_clicked_180(self):
        self.new_window(GameWindow180())

    def btn_go_clicked_181(self):
        self.new_window(GameWindow181())

    def btn_go_clicked_182(self):
        self.new_window(GameWindow182())

    def btn_go_clicked_183(self):
        self.new_window(GameWindow183())

    def btn_go_clicked_184(self):
        self.new_window(GameWindow184())

    def btn_go_clicked_185(self):
        self.new_window(GameWindow185())

    def btn_go_clicked_186(self):
        self.new_window(GameWindow186())

    def btn_go_clicked_187(self):
        self.new_window(GameWindow187())

    def btn_go_clicked_188(self):
        self.new_window(GameWindow188())

    def btn_go_clicked_189(self):
        self.new_window(GameWindow189())

    def btn_go_clicked_190(self):
        self.new_window(GameWindow190())


def resources():
    try:
        os.chdir(sys._MEIPASS)

    except:
        os.chdir(os.getcwd())


if __name__ == '__main__':
    # exe 파일 생성 시 이미지 포함
    resources()

    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')

    font_db = QtGui.QFontDatabase()
    font_db.addApplicationFont('DOSMyungjo.ttf')
    app.setFont(QtGui.QFont('DOSMyungjo'))

    song = FindSongs()
    sys.exit(app.exec_())
