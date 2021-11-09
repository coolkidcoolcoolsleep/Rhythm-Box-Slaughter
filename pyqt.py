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
from video_manager import Video_Manager


class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # QtWidgets.QWidget.__init__(self)
        self.music = QtWidgets.QComboBox()
        self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        self.btn_start = QtWidgets.QPushButton('Game Start')

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.label_empty = QtWidgets.QLabel()
        self.label = QtWidgets.QLabel()

        self.box_layout()
        self.background()
        self.label_text()
        self.window_style()
        self.button()

    def player_1(self):
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
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            if vm.game_finish == False:
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
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self):
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
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, dsize=(vm.img_width, vm.img_height))

            if vm.game_finish == False:
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
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def game_start(self):
        if self.btn_player_1.isChecked():
            self.player_1()
        elif self.btn_player_2.isChecked():
            self.player_2()

    def box_layout(self):
        self.btn_player_1.setToolTip('1인용 게임')
        self.btn_player_2.setToolTip('2인용 게임')
        self.btn_start.setToolTip('누르면 게임을 시작합니다')

        # self.vbox.addWidget(self.label_empty)
        # self.vbox.addWidget(self.label_empty)
        # self.vbox.addWidget(self.label_empty)
        # self.vbox.addWidget(self.label_empty)
        # self.vbox.addWidget(self.label_empty)
        #
        # self.vbox.addWidget(self.label)
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
        bg = QtGui.QImage('bg.jpg')
        scaled_bg = bg.scaled(1280, 720)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg))
        app.setPalette(palette)

    def label_text(self):
        self.label_empty.setText(' ')
        self.label.setFont(QtGui.QFont('Arial', 45))

        self.label.setText('리듬 박스 학살')
        self.label.setFont(QtGui.QFont('웰컴체 Regular', 45, weight=QtGui.QFont.Bold))
        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def window_style(self):
        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.vbox)
        self.window.setGeometry(0, 0, 1280, 720)
        self.window.show()

    def youtube_play(self, url):
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
            # stop = input('Type "s" to stop; "p" to pause; "" to play; : ')
            # if stop == 's':
            #     player.pause()
            #     break
            # elif stop == 'p':
            #     player.pause()
            # elif stop == '':
            #     player.play()

    def button(self):
        self.music.move(200, 400)
        for i in self.music_list:
            self.music.addItem(i)
        self.music.setToolTip('배경음악을 선택하세요')
        self.music.setFixedSize(200, 30)

        self.btn_player_1.setStyleSheet(
            'QRadioButton{font: 15pt 웰컴체 Regular;} QRadioButton::indicator { width: 20px; height: 20px;};')
        self.btn_player_2.setStyleSheet(
            'QRadioButton{font: 15pt 웰컴체 Regular;} QRadioButton::indicator { width: 20px; height: 20px;};')

        self.btn_start.setFixedSize(150, 30)
        self.btn_start.setFont(QtGui.QFont('웰컴체 Regular', 15))
        self.btn_start.clicked.connect(self.game_start)

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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:

            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 4')

            # thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/Y-JQ-RCyPpQ'))
            # thread.daemon = True
            # thread.start()
            self.music_thread('https://youtu.be/Y-JQ-RCyPpQ')

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            print('music 6')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            print('music 7')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            print('music 8')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            print('music 9')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            print('music 10')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 5')

            # thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/_sI_Ps7JSEk'))
            # thread.daemon = True
            # thread.start()
            self.music_thread('https://youtu.be/_sI_Ps7JSEk')

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            print('music 6')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            print('music 7')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            print('music 8')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            print('music 9')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            print('music 10')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 6')

            # thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/sjkrrmBnpGE'))
            # thread.daemon = True
            # thread.start()
            self.music_thread('https://youtu.be/sjkrrmBnpGE')

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            print('music 6')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            print('music 7')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            print('music 8')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            print('music 9')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            print('music 10')
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow12(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow13(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow14(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow15(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow16(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow17(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow18(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow19(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow20(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow21(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow22(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow23(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow24(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow25(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow26(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow27(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow28(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow29(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow30(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow31(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow32(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow33(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow34(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow35(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow36(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow37(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow38(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow39(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow40(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow41(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow42(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow43(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow44(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow45(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow46(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow47(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow48(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow49(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow50(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow51(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow52(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow53(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow54(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow55(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow56(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow57(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow58(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow59(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow60(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow61(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow62(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow63(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow64(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow65(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow66(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow67(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow68(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow69(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow70(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow71(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow72(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow73(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow74(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow75(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow76(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow77(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow78(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow79(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow80(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow81(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow82(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow83(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow84(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow85(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow86(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow87(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow88(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow89(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow90(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow91(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow92(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow93(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow94(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow95(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow96(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow97(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow98(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow99(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow100(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow101(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow102(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow103(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow104(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow105(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow106(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow107(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow108(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow109(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow110(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow111(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow112(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow113(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow114(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow115(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow116(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow117(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow118(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow119(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow120(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow121(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow122(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow123(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow124(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow125(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow126(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow127(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow128(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow129(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow130(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow131(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow132(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow133(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow134(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow135(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow136(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow137(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow138(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow139(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow140(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow141(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow142(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow143(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow144(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow145(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow146(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow147(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow148(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow149(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow150(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow151(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow152(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow153(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow154(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow155(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow156(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow157(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow158(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow159(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow160(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow161(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow162(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow163(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow164(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow165(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow166(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow167(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow168(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow169(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow170(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow171(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow172(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow173(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow174(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow175(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow176(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow177(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow178(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow179(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow180(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow181(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow182(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow183(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow184(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow185(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow186(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow187(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow188(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow189(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class GameWindow190(Game):
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

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Gg8pB9-6T8g')


class FindSongs(QtWidgets.QWidget):
    select_favorite_list_1 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 study coffee jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    select_favorite_list_2 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 study coffee jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    # select_favorite_list_3 = ['(좋아하는 노래를 선택하세요)',
    #                           '1',
    #                           '2 study coffee jazz',
    #                           '3 After The Rain',
    #                           '4 Relaxing Bossa Nova & Jazz',
    #                           '5 New York Jazz Lounge',
    #                           '6',
    #                           '7',
    #                           '8',
    #                           '9',
    #                           '10']
    #
    # select_favorite_list_4 = ['(좋아하는 노래를 선택하세요)',
    #                           '1',
    #                           '2 study coffee jazz',
    #                           '3 After The Rain',
    #                           '4 Relaxing Bossa Nova & Jazz',
    #                           '5 New York Jazz Lounge',
    #                           '6',
    #                           '7',
    #                           '8',
    #                           '9',
    #                           '10']
    #
    # select_favorite_list_5 = ['(좋아하는 노래를 선택하세요)',
    #                           '1',
    #                           '2 study coffee jazz',
    #                           '3 After The Rain',
    #                           '4 Relaxing Bossa Nova & Jazz',
    #                           '5 New York Jazz Lounge',
    #                           '6',
    #                           '7',
    #                           '8',
    #                           '9',
    #                           '10']

    def __init__(self):
        super().__init__()
        # QtWidgets.QWidget.__init__(self)
        # self.final_matching = []

        # dropdown style
        # self.select_song_1 = QtWidgets.QComboBox(self)
        # self.select_song_2 = QtWidgets.QComboBox(self)
        # self.select_song_3 = QtWidgets.QComboBox(self)
        # self.select_song_4 = QtWidgets.QComboBox(self)
        # self.select_song_5 = QtWidgets.QComboBox(self)

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel()
        self.label_2 = QtWidgets.QLabel()
        self.btn_go = QtWidgets.QPushButton('선택')
        self.msg = QtWidgets.QMessageBox()

        self.song_img_1 = QtWidgets.QRadioButton("안 되는데 - 4Men")
        self.song_img_2 = QtWidgets.QRadioButton('너와 나 그리고 우리 (You & I) - 이민호')
        self.song_img_3 = QtWidgets.QRadioButton('보여(still) - Sunday x 김태현(딕펑스)')
        self.song_img_4 = QtWidgets.QRadioButton('그대 (My Love) - Honey G')
        self.song_img_5 = QtWidgets.QRadioButton('Punchlines - The Quiett')
        self.song_img_6 = QtWidgets.QRadioButton('슬피 우는 새 - 아웃사이더')
        self.song_img_7 = QtWidgets.QRadioButton('비 따라 - 앤츠')
        self.song_img_8 = QtWidgets.QRadioButton('바보 - Gavy NJ')
        self.song_img_9 = QtWidgets.QRadioButton('하루라도 - MIO')
        self.song_img_10 = QtWidgets.QRadioButton('떠오르다 (INTRO) - Noel')
        self.song_img_11 = QtWidgets.QRadioButton('너와 나의 크리스마스 - PD BLUE')
        self.song_img_12 = QtWidgets.QRadioButton('Do - Urban Zakapa')
        self.song_img_13 = QtWidgets.QRadioButton('INTRO - HAHA')
        self.song_img_14 = QtWidgets.QRadioButton('YA MAN!! - SKULL&HAHA')
        self.song_img_15 = QtWidgets.QRadioButton('길 - 김나영')
        self.song_img_16 = QtWidgets.QRadioButton('썩은 미소 - 미생 OST')
        self.song_img_17 = QtWidgets.QRadioButton('예쁘게 하고 나와 - Boys Republic')
        self.song_img_18 = QtWidgets.QRadioButton("너의 마음을 내게 준다면 - Girl's Day")
        self.song_img_19 = QtWidgets.QRadioButton('끝 - 브로콜리 너마저')
        self.song_img_20 = QtWidgets.QRadioButton("소심한K씨의대범한사랑고백 - T-Ok")

        self.box_layout()
        self.match()
        self.background()
        self.text_style()
        self.current_index()

        self.w = None

    # dropdown style
    # def add_item_in_combobox(self, select_song, select_favorite_list):
    #     select_song.move(200, 400)
    #     for i in select_favorite_list:
    #         select_song.addItem(i)

    # song img style vbox
    def vbox_style(self, song_img):
        song_img.setIconSize(QtCore.QSize(100, 100))
        song_img.setAutoExclusive(False)

    def box_layout(self):
        # index = self.music.findText('sample 1', QtCore.Qt.MatchFixedString)    # findText: 인덱스를 return

        # dropdown style
        # self.add_item_in_combobox(self.select_song_1, self.select_favorite_list_1)
        # self.add_item_in_combobox(self.select_song_2, self.select_favorite_list_2)
        # self.add_item_in_combobox(self.select_song_3, self.select_favorite_list_3)
        # self.add_item_in_combobox(self.select_song_4, self.select_favorite_list_4)
        # self.add_item_in_combobox(self.select_song_5, self.select_favorite_list_5)

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.label_2)

        self.btn_go.setMaximumWidth(100)

        vbox_img_1 = QtWidgets.QVBoxLayout()

        vbox_img_1.addWidget(self.song_img_1)
        self.song_img_1.setIcon(QtGui.QIcon('four_men.jpg'))
        self.vbox_style(self.song_img_1)

        vbox_img_1.addWidget(self.song_img_2)
        self.song_img_2.setIcon(QtGui.QIcon('you_and_i.jpg'))
        self.vbox_style(self.song_img_2)

        vbox_img_1.addWidget(self.song_img_3)
        self.song_img_3.setIcon(QtGui.QIcon('still.jpg'))
        self.vbox_style(self.song_img_3)

        vbox_img_1.addWidget(self.song_img_4)
        self.song_img_4.setIcon(QtGui.QIcon('my_love.jpg'))
        self.vbox_style(self.song_img_4)

        vbox_img_1.addWidget(self.song_img_5)
        self.song_img_5.setIcon(QtGui.QIcon('punchlines.jpg'))
        self.vbox_style(self.song_img_5)

        vbox_img_3 = QtWidgets.QVBoxLayout()

        vbox_img_3.addWidget(self.song_img_6)
        self.song_img_6.setIcon(QtGui.QIcon('outsider.jpg'))
        self.vbox_style(self.song_img_6)

        vbox_img_3.addWidget(self.song_img_7)
        self.song_img_7.setIcon(QtGui.QIcon('ants.jpg'))
        self.vbox_style(self.song_img_7)

        vbox_img_3.addWidget(self.song_img_8)
        self.song_img_8.setIcon(QtGui.QIcon('fool.jpg'))
        self.vbox_style(self.song_img_8)

        vbox_img_3.addWidget(self.song_img_9)
        self.song_img_9.setIcon(QtGui.QIcon('mio.jpg'))
        self.vbox_style(self.song_img_9)

        vbox_img_3.addWidget(self.song_img_10)
        self.song_img_10.setIcon(QtGui.QIcon('noel.jpg'))
        self.vbox_style(self.song_img_10)

        vbox_img_2 = QtWidgets.QVBoxLayout()

        vbox_img_2.addWidget(self.song_img_11)
        self.song_img_11.setIcon(QtGui.QIcon('pd.jpg'))
        self.vbox_style(self.song_img_11)

        vbox_img_2.addWidget(self.song_img_12)
        self.song_img_12.setIcon(QtGui.QIcon('do.jpg'))
        self.vbox_style(self.song_img_12)

        vbox_img_2.addWidget(self.song_img_13)
        self.song_img_13.setIcon(QtGui.QIcon('haha.jpg'))
        self.vbox_style(self.song_img_13)

        vbox_img_2.addWidget(self.song_img_14)
        self.song_img_14.setIcon(QtGui.QIcon('ya_man.jpg'))
        self.vbox_style(self.song_img_14)

        vbox_img_2.addWidget(self.song_img_15)
        self.song_img_15.setIcon(QtGui.QIcon('kim_na_young.jpg'))
        self.vbox_style(self.song_img_15)

        vbox_img_4 = QtWidgets.QVBoxLayout()

        vbox_img_4.addWidget(self.song_img_16)
        self.song_img_16.setIcon(QtGui.QIcon('rotten_smile.jpg'))
        self.vbox_style(self.song_img_16)

        vbox_img_4.addWidget(self.song_img_17)
        self.song_img_17.setIcon(QtGui.QIcon('boys_republic.jpg'))
        self.vbox_style(self.song_img_17)

        vbox_img_4.addWidget(self.song_img_18)
        self.song_img_18.setIcon(QtGui.QIcon('girls_day.jpg'))
        self.vbox_style(self.song_img_18)

        vbox_img_4.addWidget(self.song_img_19)
        self.song_img_19.setIcon(QtGui.QIcon('broccoli.jpg'))
        self.vbox_style(self.song_img_19)

        vbox_img_4.addWidget(self.song_img_20)
        self.song_img_20.setIcon(QtGui.QIcon('t-ok.jpg'))
        self.vbox_style(self.song_img_20)

        self.hbox.addLayout(vbox_img_1)
        self.hbox.addLayout(vbox_img_3)
        self.hbox.addLayout(vbox_img_2)
        self.hbox.addLayout(vbox_img_4)

        self.grid_layout.addLayout(self.vbox, 0, 0)
        self.grid_layout.addLayout(self.hbox, 1, 0)
        self.grid_layout.addWidget(self.btn_go, 100, 100, alignment=QtCore.Qt.AlignCenter)

        # dropdown style
        # hbox = QtWidgets.QHBoxLayout()
        # hbox.addWidget(self.select_song_1)
        # hbox.addWidget(self.select_song_2)
        # # hbox.addWidget(self.select_song_3)
        # # hbox.addWidget(self.select_song_4)
        # # hbox.addWidget(self.select_song_5)
        # hbox.addWidget(self.btn_go)
        # self.vbox.addLayout(hbox)

        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.grid_layout)
        self.window.setLayout(self.hbox)
        self.window.setLayout(self.vbox)

        self.window.setGeometry(0, 0, 1280, 720)
        self.window.show()

    def match(self):
        # select_songs_lists = [self.select_song_1, self.select_song_2, self.select_song_3,
        #                       self.select_song_4, self.select_song_5]
        # select_songs_lists = [self.select_song_1, self.select_song_2]

        # dropdown style
        # self.select_song_2.currentIndexChanged.connect(self.current_index)

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
        # matched_musics = (self.select_song_1.currentIndex(), self.select_song_2.currentIndex(),
        #                   self.select_song_3.currentIndex(), self.select_song_4.currentIndex(),
        #                   self.select_song_5.currentIndex())

        # matched_musics = (self.select_song_1.currentIndex(), self.select_song_2.currentIndex())
        #
        # print(matched_musics)
        #
        # def test_list(number):
        #     test_list = [(number, i) for i in range(1, 11)]
        #
        #     return test_list

        # dropdown style 테스트 버전
        # if matched_musics in test_list(1):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_1)
        #     print('success: currentIndex 1')
        #
        # elif matched_musics in test_list(2):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_2)
        #     print('success: currentIndex 2')
        #
        # elif matched_musics in test_list(3):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_3)
        #     print('success: currentIndex 3')
        #
        # elif matched_musics in test_list(4):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_4)
        #     print('success: currentIndex 4')
        #
        # elif matched_musics in test_list(5):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_5)
        #     print('success: currentIndex 5')
        #
        # elif matched_musics in test_list(6):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_6)
        #     print('success: currentIndex 6')
        #
        # elif matched_musics in test_list(7):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_7)
        #     print('success: currentIndex 7')
        #
        # elif matched_musics in test_list(8):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_8)
        #     print('success: currentIndex 8')
        #
        # elif matched_musics in test_list(9):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_9)
        #     print('success: currentIndex 9')
        #
        # elif matched_musics in test_list(10):
        #     self.btn_go.clicked.connect(self.btn_go_clicked_10)
        #     print('success: currentIndex 10')
        #
        # else:
        #     self.btn_go.clicked.connect(self.btn_go_clicked_1)

        # song img 버전
        if self.song_img_1.isChecked():
            print('test: song_img_1')
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
        # scaled_bg = bg.scaled(400, 100)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(bg))
        app.setPalette(palette)

    def text_style(self):
        self.label.setText('*리듬 박스 학살*')
        self.label.setFont(QtGui.QFont('웰컴체 Regular', 45, weight=QtGui.QFont.Bold))
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_2.setText('왼쪽부터 순서대로 노래를 선택한 뒤 선택 버튼을 눌러주세요')
        self.label_2.setText('노래를 2곡 선택한 뒤 선택 버튼을 눌러주세요')
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)

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
        self.new_window(GameWindow11())

    def btn_go_clicked_13(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_14(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_15(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_16(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_17(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_18(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_19(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_20(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_21(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_22(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_23(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_24(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_25(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_26(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_27(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_28(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_29(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_30(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_31(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_32(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_33(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_34(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_35(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_36(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_37(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_38(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_39(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_40(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_41(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_42(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_43(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_44(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_45(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_46(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_47(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_48(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_49(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_50(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_51(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_52(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_53(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_54(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_55(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_56(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_57(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_58(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_59(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_60(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_61(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_62(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_63(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_64(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_65(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_66(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_67(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_68(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_69(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_70(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_71(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_72(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_73(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_74(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_75(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_76(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_77(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_78(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_79(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_80(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_81(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_82(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_83(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_84(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_85(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_86(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_87(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_88(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_89(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_90(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_91(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_92(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_93(self):
        self.new_window(GameWindow11())

        def btn_go_clicked_90(self):
            self.new_window(GameWindow11())

    def btn_go_clicked_94(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_95(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_96(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_97(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_98(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_99(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_100(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_101(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_102(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_103(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_104(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_105(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_106(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_107(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_108(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_109(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_110(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_111(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_112(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_113(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_114(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_115(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_116(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_117(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_118(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_119(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_120(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_121(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_122(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_123(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_124(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_125(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_126(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_127(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_128(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_129(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_130(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_131(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_132(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_133(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_134(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_135(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_136(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_137(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_138(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_139(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_140(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_141(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_142(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_143(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_144(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_145(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_146(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_147(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_148(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_149(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_150(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_151(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_152(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_153(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_154(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_155(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_156(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_157(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_158(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_159(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_160(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_161(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_162(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_163(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_164(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_165(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_166(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_167(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_168(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_169(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_170(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_171(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_172(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_173(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_174(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_175(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_176(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_177(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_178(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_179(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_180(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_181(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_182(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_183(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_184(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_185(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_186(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_187(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_188(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_189(self):
        self.new_window(GameWindow11())

    def btn_go_clicked_190(self):
        self.new_window(GameWindow11())


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
    font_db.addApplicationFont('웰컴체 Regular.ttf')
    app.setFont(QtGui.QFont('웰컴체 Regular'))

    song = FindSongs()
    sys.exit(app.exec_())
