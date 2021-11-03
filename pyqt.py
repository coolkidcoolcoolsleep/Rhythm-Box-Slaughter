import cv2
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import random
import winsound
import threading
import pafy
import vlc
import time
from video_manager import Video_Manager


class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        self.music = QtWidgets.QComboBox()
        self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        self.btn_start = QtWidgets.QPushButton('Game Start')

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()

        self.box_layout()
        self.background()
        self.label_text()
        self.window_style()
        self.button()

    def player_1(self):
        vm = Video_Manager()

        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW+0)

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
            vm.TwoPlayerGameStats(frame, red_score, blue_score)

            cv2.imshow('Rhythm Box Slaughter', frame)
            # esc 키를 누르면 닫음 -> 후에 노래가 끝나면 종료로 수정해야 함

            if cv2.waitKey(15) == 27:
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self):
        vm = Video_Manager()

        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW+0)

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
            vm.TwoPlayerGameStats(frame, red_score, blue_score)

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

    def box_layout(self):
        self.btn_player_1.setToolTip('1인용 게임')
        self.btn_player_2.setToolTip('2인용 게임')
        self.btn_start.setToolTip('누르면 게임을 시작합니다')

        self.vbox.addWidget(self.label)
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
        bg = QtGui.QImage('mint_pink.png')
        scaled_bg = bg.scaled(400, 100)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg))
        app.setPalette(palette)

    def label_text(self):
        self.label.setText('리듬 박스 학살')
        self.label.setFont(QtGui.QFont('Arial', 15))
        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

    def window_style(self):
        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.vbox)
        self.window.setGeometry(0, 0, 400, 100)
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

        self.btn_start.clicked.connect(self.game_start)
        self.music.currentIndexChanged.connect(self.music_play)


class GameWindow1(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 1',
                  'cute',
                  'tenderness',
                  'acoustic breeze',
                  'better days']

    def __init__(self):
        super().__init__()
        Game.__init__(self)
        # self.button()
        # self.music = QtWidgets.QComboBox(self)
        # self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        # self.btn_start = QtWidgets.QPushButton('Game Start')
        #
        # self.window = QtWidgets.QWidget()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.label = QtWidgets.QLabel()
        #
        # self.background()
        # self.label_text()
        # self.window_style()

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 1')

            thread = threading.Thread(target=lambda: self.youtube_play('https://www.youtube.com/watch?v=lXDyWT3VlKg&ab_channel=M2'))
            thread.daemon = True
            thread.start()

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')


class GameWindow2(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 2',
                  'cute 2',
                  'tenderness 2',
                  'acoustic breeze 2',
                  'better days 2']

    def __init__(self):
        super().__init__()
        Game.__init__(self)
        # self.button()
        # self.music = QtWidgets.QComboBox(self)
        # self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        # self.btn_start = QtWidgets.QPushButton('Game Start')
        #
        # self.window = QtWidgets.QWidget()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.label = QtWidgets.QLabel()

        # self.background()
        # self.label_text()
        # self.window_style()

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 2')

            thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/2v5iWf2KDCw'))
            thread.daemon = True
            thread.start()

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')


class GameWindow3(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 3',
                  'cute 3',
                  'tenderness 3',
                  'acoustic breeze 3',
                  'better days 3']

    def __init__(self):
        super().__init__()
        Game.__init__(self)
        # self.button()
        # self.music = QtWidgets.QComboBox(self)
        # self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        # self.btn_start = QtWidgets.QPushButton('Game Start')
        #
        # self.window = QtWidgets.QWidget()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.label = QtWidgets.QLabel()

        # self.background()
        # self.label_text()
        # self.window_style()

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            # winsound.SND_FILENAME: wav file 이름
            # winsound.SND_ASYNC: 사운드 async 재생한다. 실행 시 바로 리턴되고 사운드는 재생된다.
            # winsound.PlaySound('bensound-jazzyfrenchy.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            pass
        elif item == self.music_list[1]:
            # winsound.PlaySound('bensound-ukulele.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

            print('test: youtube music 3')

            thread = threading.Thread(target=lambda: self.youtube_play('https://www.youtube.com/watch?v=cSvgRKsML7o'))
            thread.daemon = True
            thread.start()

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')


class GameWindow4(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 4',
                  'cute 4',
                  'tenderness 4',
                  'acoustic breeze 4',
                  'better days 4']

    def __init__(self):
        super().__init__()
        Game.__init__(self)
        # self.button()
        # self.music = QtWidgets.QComboBox(self)
        # self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        # self.btn_start = QtWidgets.QPushButton('Game Start')
        #
        # self.window = QtWidgets.QWidget()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.label = QtWidgets.QLabel()

        # self.background()
        # self.label_text()
        # self.window_style()

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

            thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/Y-JQ-RCyPpQ'))
            thread.daemon = True
            thread.start()

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')


class GameWindow5(Game):
    music_list = ['(노래를 선택하세요)',
                  'youtube music 5',
                  'cute 5',
                  'tenderness 5',
                  'acoustic breeze 5',
                  'better days 5']

    def __init__(self):
        super().__init__()
        Game.__init__(self)
        # self.button()
        # self.music = QtWidgets.QComboBox(self)
        # self.btn_player_1 = QtWidgets.QRadioButton('1 Player')
        # self.btn_player_2 = QtWidgets.QRadioButton('2 Players')
        # self.btn_start = QtWidgets.QPushButton('Game Start')
        #
        # self.window = QtWidgets.QWidget()
        # self.vbox = QtWidgets.QVBoxLayout()
        # self.label = QtWidgets.QLabel()

        # self.background()
        # self.label_text()
        # self.window_style()

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

            thread = threading.Thread(target=lambda: self.youtube_play('https://youtu.be/_sI_Ps7JSEk'))
            thread.daemon = True
            thread.start()

        elif item == self.music_list[2]:
            # winsound.PlaySound('bensound-cute.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-cute.wav')
        elif item == self.music_list[3]:
            # winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-tenderness.wav')
        elif item == self.music_list[4]:
            # winsound.PlaySound('bensound-acousticbreeze.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-acousticbreeze.wav')
        elif item == self.music_list[5]:
            # winsound.PlaySound('bensound-betterdays.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
            print('test: bensound-betterdays.wav')


class FindSongs(QtWidgets.QWidget):
    select_favorite_list_1 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 jazz',
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
                              '2 jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    select_favorite_list_3 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    select_favorite_list_4 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    select_favorite_list_5 = ['(좋아하는 노래를 선택하세요)',
                              '1',
                              '2 jazz',
                              '3 After The Rain',
                              '4 Relaxing Bossa Nova & Jazz',
                              '5 New York Jazz Lounge',
                              '6',
                              '7',
                              '8',
                              '9',
                              '10']

    def __init__(self):
        super().__init__()
        QtWidgets.QWidget.__init__(self)
        self.final_matching = []

        self.select_song_1 = QtWidgets.QComboBox(self)
        self.select_song_2 = QtWidgets.QComboBox(self)
        self.select_song_3 = QtWidgets.QComboBox(self)
        self.select_song_4 = QtWidgets.QComboBox(self)
        self.select_song_5 = QtWidgets.QComboBox(self)

        self.window = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.btn_go = QtWidgets.QPushButton('선택')
        self.msg = QtWidgets.QMessageBox()

        self.box_layout()
        self.match()
        self.background()
        self.text_style()

        self.w = None

    def add_item_in_combobox(self, select_song, select_favorite_list):
        select_song.move(200, 400)
        for i in select_favorite_list:
            select_song.addItem(i)

    def box_layout(self):
        # index = self.music.findText('sample 1', QtCore.Qt.MatchFixedString)    # findText: 인덱스를 return

        self.add_item_in_combobox(self.select_song_1, self.select_favorite_list_1)
        self.add_item_in_combobox(self.select_song_2, self.select_favorite_list_2)
        self.add_item_in_combobox(self.select_song_3, self.select_favorite_list_3)
        self.add_item_in_combobox(self.select_song_4, self.select_favorite_list_4)
        self.add_item_in_combobox(self.select_song_5, self.select_favorite_list_5)

        self.vbox.addWidget(self.label)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.select_song_1)
        hbox.addWidget(self.select_song_2)
        hbox.addWidget(self.select_song_3)
        hbox.addWidget(self.select_song_4)
        hbox.addWidget(self.select_song_5)
        hbox.addWidget(self.btn_go)
        self.vbox.addLayout(hbox)

        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.vbox)
        self.window.setGeometry(0, 0, 400, 100)
        self.window.show()

    def match(self):
        select_songs_lists = [self.select_song_1, self.select_song_2, self.select_song_3,
                              self.select_song_4, self.select_song_5]

        matching = []
        idx = 0
        for songs in select_songs_lists:
            all_items = [songs.itemText(i) for i in range(songs.count())]
            for _ in all_items:
                while idx < 5:
                    match = [j for j in range(1, 11)]
                    matching.append(match)
                    idx += 1
        # print(matching)

        i = 0
        while i < 5:
            for j in matching[i]:
                for k in matching[i]:
                    for l in matching[i]:
                        for m in matching[i]:
                            for n in matching[i]:
                                self.final_matching.append((j, k, l, m, n))
            i += 1
        # print(self.final_matching)

        self.select_song_5.currentIndexChanged.connect(self.current_index)
        # self.select_song_5.activated[str].connect(self.current_index)

    def current_index(self):
        matched_musics = (self.select_song_1.currentIndex(), self.select_song_2.currentIndex(),
                          self.select_song_3.currentIndex(), self.select_song_4.currentIndex(),
                          self.select_song_5.currentIndex())

        print(matched_musics)

        # (in final_matching) 테스트 버전
        if matched_musics in [(i, 1, 1, 1, 1) for i in range(1, 11)]:
            self.btn_go.clicked.connect(self.btn_go_clicked_1)
            print('success: currentIndex')
            # if self.select_song_1.currentIndex() == 0 or self.select_song_2.currentIndex() == 0 or \
            #     self.select_song_3.currentIndex() == 0 or self.select_song_4.currentIndex() == 0 or \
            #         self.select_song_5.currentIndex() == 0:
            #     pass

        elif matched_musics in [(2, 2, 2, 2, 2)]:
            self.btn_go.clicked.connect(self.btn_go_clicked_2)
            print('success: currentIndex 2')

        elif matched_musics in [(3, 3, 3, 3, 3)]:
            self.btn_go.clicked.connect(self.btn_go_clicked_3)

        elif matched_musics in [(4, 4, 4, 4, 4)]:
            self.btn_go.clicked.connect(self.btn_go_clicked_4)

        elif matched_musics in [(5, 5, 5, 5, 5)]:
            self.btn_go.clicked.connect(self.btn_go_clicked_5)

        else:
            self.btn_go.clicked.connect(self.btn_go_clicked_1)
            # self.btn_go.clicked.connect(self.open_msg)
            # print('매칭되는 목록이 없습니다')

    def open_msg(self):
        self.msg.setText('매칭되는 목록이 없습니다\n다시 선택해주세요')
        self.msg.setWindowTitle('알림')
        self.msg.setWindowIcon(QtGui.QIcon('sunglasses.png'))
        self.msg.StandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.exec_()

    def background(self):
        bg = QtGui.QImage('mint_pink.png')
        scaled_bg = bg.scaled(400, 100)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(scaled_bg))
        app.setPalette(palette)

    def text_style(self):
        self.label.setText('왼쪽부터 순서대로 노래를 선택한 뒤 선택 버튼을 눌러주세요')
        self.label.setFont(QtGui.QFont('Arial', 15))
        self.label.setAlignment(QtCore.Qt.AlignCenter)

    def new_window(self, game_window):
        if self.w is None:
            self.w = game_window
            # self.w.show()

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


def resources():
    try:
        os.chdir(sys._MEIPASS)
        print(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())


if __name__ == '__main__':
    # exe 파일 생성 시 이미지 포함
    resources()

    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')

    song = FindSongs()
    sys.exit(app.exec_())
