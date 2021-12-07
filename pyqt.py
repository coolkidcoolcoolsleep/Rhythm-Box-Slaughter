import cv2
import os
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import random
import threading
import time
import winsound
import ctypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import shutil
import pyautogui
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

        # load_video
        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW+0)

        if not vidcap.isOpened():
            vidcap = cv2.VideoCapture(0)

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, (vm.img_width, vm.img_height))

            if vm.game_finish == False:
                box_seed_num = vm.box_num // 25
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
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue, sum_score = \
                    vm.score_calculation(frame, rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num,
                                           detection_red, coordinate_red)

                # 정답 rect 그리기
                vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                       is_answer_handled_blue)

                # 점수 표기
                frame = vm.PlayerGameStats(frame, red_score, blue_score, sum_score, is_one_player=True)

                vm.frame_num = vm.frame_num + 1
                if vm.frame_num == 750:
                    vm.game_finish = True

                # 승자 결정
                vm.game_result(red_score, blue_score, sum_score, is_one_player=True)

            else:
                # 승자 효과
                frame = vm.Winner_effect(frame, vm.one_player_result, vm.two_player_result,
                                           is_one_player=True)

            cv2.imshow('Rhythm Box Slaughter', frame)

            if cv2.waitKey(15) == 27:
                ctypes.windll.user32.MessageBoxW(0, '게임을 종료합니다', '안내', 0)
                break

        vidcap.release()
        cv2.destroyAllWindows()

    def player_2(self, mode):
        vm = Video_Manager()

        # load_video
        vidcap = cv2.VideoCapture(cv2.CAP_DSHOW + 0)

        if not vidcap.isOpened():
            vidcap = cv2.VideoCapture(0)

        while True:
            _, frame = vidcap.read()  # _: ret
            # print(_)
            # 영상 좌우 반전
            frame = cv2.flip(frame, 1)

            if frame is None:
                break

            frame = cv2.resize(frame, (vm.img_width, vm.img_height))
            if vm.game_finish == False:
                box_seed_num = vm.box_num // 20
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
                blue_score, red_score, is_answer_handled_red, is_answer_handled_blue, sum_score = \
                    vm.score_calculation(frame, rectangle_seed_num, detection_blue, coordinate_blue, box_seed_num,
                          detection_red, coordinate_red)

                # 정답 rect 그리기
                vm.Drawing_Rectangle(frame, coordinate_blue, coordinate_red, is_answer_handled_red,
                                  is_answer_handled_blue)

                # 점수 표기
                frame = vm.PlayerGameStats(frame, red_score, blue_score, sum_score, is_one_player=False)

                vm.frame_num = vm.frame_num + 1
                if vm.frame_num == 600:
                    vm.game_finish = True

                # 승자 결정
                vm.game_result(red_score, blue_score, sum_score, is_one_player=False)

            else:
                # 승자 효과
                frame = vm.Winner_effect(frame, vm.two_player_result, vm.one_player_result, is_one_player=False)

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

    def game_start_norm(self):
        if self.btn_player_1.isChecked():
            self.player_1('norm')
        elif self.btn_player_2.isChecked():
            self.player_2('norm')

    def game_start_hard(self):
        if self.btn_player_1.isChecked():
            self.player_1('hard')
        elif self.btn_player_2.isChecked():
            self.player_2('hard')

    def box_layout(self):
        self.btn_player_1.setToolTip('1인용 게임')
        self.btn_player_2.setToolTip('2인용 게임')
        self.btn_start.setToolTip('누르면 게임을 시작합니다')
        self.btn_start.setStyleSheet('QPushButton { background-color: rgb(255, 190, 11);}')

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
        self.window.setPalette(palette)

    def window_style(self):
        self.window.setWindowTitle('Rhythm Box Slaughter')
        self.window.setWindowIcon(QtGui.QIcon('sunglasses.png'))

        self.window.setLayout(self.vbox)
        self.window.setGeometry(0, 0, 1280, 720)
        self.window.show()

    def youtube_play(self, url):
        try:
            shutil.rmtree(r"C:\chrome_debugging")  # remove Cookie, Cache files

            subprocess.Popen(r'C:/Program Files/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 '
                             r'--user-data-dir="C:\chrome_debugging"')  # Open the debugger chrome

            option = Options()
            option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

            driver = webdriver.Chrome('./chromedriver.exe', options=option)

            driver.implicitly_wait(10)

            driver.get(
                url='https://accounts.google.com/ServiceLogin/identifier?service=youtube&uilel=3&passive=true&continue='
                    'https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dko%26next'
                    '%3Dhttps%253A%252F%252Fwww.youtube.com%252Fmusicpremium&hl=ko&ec=65620&flowName=GlifWebSignIn&flowEntry'
                    '=ServiceLogin')

            pyautogui.write('ID')  # Fill in your ID or E-mail
            pyautogui.press('tab', presses=3)  # Press the Tab key 3 times
            pyautogui.press('enter')
            time.sleep(3)  # wait a process
            pyautogui.write('PW')  # Fill in your PW
            pyautogui.press('enter')

            start = time.time()

            driver.get(url)
            time.sleep(3)

            while True:
                time.sleep(1)
                if time.time() - start > 60:
                    driver.close()
                    break

        except KeyError as err:
            if err.args[0] == 'dislike_count':
                winsound.PlaySound('bensound-tenderness.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    def button(self):
        self.music.move(200, 400)
        for i in self.music_list:
            self.music.addItem(i)
        self.music.setToolTip('배경음악을 선택하세요')
        self.music.setFixedSize(200, 30)
        self.music.setStyleSheet('QComboBox QAbstractItemView {background: white};')

        self.btn_player_1.setStyleSheet(
            'QRadioButton {font: 15pt DOSMyungjo;} QRadioButton::indicator {width: 20px; height: 20px;};')
        self.btn_player_2.setStyleSheet(
            'QRadioButton {font: 15pt DOSMyungjo;} QRadioButton::indicator {width: 20px; height: 20px;};')

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
                  '에이핑크 - Secret Garden : ★☆☆☆☆',
                  "NU'EST - Love Paint : ★★★★★",
                  '샤이니 - Wowowow : ★☆☆☆☆',
                  '샤이니 - One : ★★★★★',
                  "박효신 - It's You : ★★★★★",
                  '여자친구 - 시간을 달려서 : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', "비스트 - I'm sorry : ★☆☆☆☆", 'K.Will - 눈물이 뚝뚝 : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=DIjGzZgu_yY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow2(Game):
    music_list = ['(노래를 선택하세요)', '잔나비 - Goodnight (Intro) : ★★★★★', '샤이니 - One : ★★★★★', 'IU - 미운 오리 : ★☆☆☆☆', '양파&다비치&HANNA -  사랑이 다 그런거래요 : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '바람이 분다OST - 비밀의 방 : ★★★★★', 'f(x) - All Mine : ★★★★★', '곽연진 - 재회의 테마 : ★★★☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆', 'EXO - Heart Attack : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=NK3y5QJ1rp8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=bGKjOoAirdo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=GrtKiJt_xJg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=lZ6XG1JhsEk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow3(Game):
    music_list = ['(노래를 선택하세요)', '레드벨벳 - Ice Cream Cake : ★★★★★', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', "비스트 - I'm sorry : ★☆☆☆☆", '에이핑크 - Secret Garden : ★☆☆☆☆', '엠버 - Borders : ★☆☆☆☆', '샤이니 - One : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow4(Game):
    music_list = ['(노래를 선택하세요)', 'EXO - Monster : ★★★★★', '슈퍼주니어 - Shirt : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '연애말고 결혼 OST - Love Knots : ★★★★★', 'f(x) - All Mine : ★★★★★', '샤이니 - One : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', "비스트 - I'm sorry : ★☆☆☆☆", '에이핑크 - Secret Garden : ★☆☆☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Om8twVJM1is')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow5(Game):
    music_list = ['(노래를 선택하세요)', '아이유 - 스물셋 : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', '박세영 - 블루로드 : ★★★☆☆', '안녕하신가영 - 순간의 순간 : ★☆☆☆☆', "G.NA - Don't Cry : ★☆☆☆☆", '비투비 - Anymore : ★☆☆☆☆', '일레븐 - Pray For Korea : ★★★☆☆', '레드벨벳 - Automatic : ★☆☆☆☆', '에일리 - 그대도 같은가요 : ★★★★★', '최정우 - 어디선가 나의 노랠듣고 있을 너에게 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=OSaANCJsfXs')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=J3unOTNiDN8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=WtHuuFi7Lwk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=D1sTQc7FrVk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=9lpyAUDxT0c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=RVUv6Hw3WsE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=o5Vj8WCWGW4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=lxprNC-DqSM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow6(Game):
    music_list = ['(노래를 선택하세요)', '에이핑크 - Secret Garden : ★☆☆☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆', "박효신 - It's You : ★★★★★", '현아 - 빨개요 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', "바람이 분다OST - It's Over : ★★★★★", '인피니트 - Follow Me : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=qocyC5nvsH8&list=OLAK5uy_kfaAb-W2pQsUqp0x-VmmMlHrGyQhvD79k&index=15')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow7(Game):
    music_list = ['(노래를 선택하세요)', '비투비 - 두 번째 고백 : ★☆☆☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '제이민 - Song On My Guitar : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '블루베어스 & 택연 - 오늘 같은 밤 : ★★★★★', '레인보우 유아동요 - 숲 속의 음악가 : ★☆☆☆☆', '혁오 - Hooka : ★☆☆☆☆', '투하트 - Tell Me Why : ★☆☆☆☆', '인피니트 - Because : ★★★☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=H_rr4CCyACQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=uxhVy02aTqA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xl5an64ksKQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=OytSUJZNgL4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=qlEIui3xpUs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=q-tGcNE6nO8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow8(Game):
    music_list = ['(노래를 선택하세요)', '여자친구 - 시간을 달려서 : ★★★☆☆', '최준영 - 얼음심장 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '지훈 - 너만 생각나 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', "박효신 - It's You : ★★★★★", '지나유 - 처음사랑 : ★★★★★', '윤지훈 - 너밖에 몰라 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=leQ5P_1pNB8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow9(Game):
    music_list = ['(노래를 선택하세요)', 'f(x) - Lollipop : ★★★★★', '동방신기 - Humanoids : ★★★☆☆', '요조 - 바나나파티 : ★★★★★', '천둥 - Good : ★★★☆☆', "박효신 - It's You : ★★★★★", '이지수 - 너야 : ★☆☆☆☆', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', '인피니트 - Follow Me : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow10(Game):
    music_list = ['(노래를 선택하세요)', '여자친구 - 시간을 달려서 : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '샤이니 - One : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '엠버 - Borders : ★☆☆☆☆', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '양파&다비치&HANNA -  사랑이 다 그런거래요 : ★★★★★', '슈퍼주니어 - A-Oh! : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bGKjOoAirdo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=hoRbO-PiXgU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow11(Game):
    music_list = ['(노래를 선택하세요)', '여자친구 - 시간을 달려서 : ★★★☆☆', '보아 - One Dream : ★☆☆☆☆', '인피니트 - 내꺼하자 : ★★★★★', '다방 - Wanna Buy Love (여자친구 사주세요) (사랑을 살 수 있다면) : ★★★★★', '비스트 - Let It Snow : ★★★☆☆', '김나영 - 어땠을까 : ★★★★★', '장기하와 얼굴들 - 그러게 왜 그랬어 : ★★★★★', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '아이유 - 마쉬멜로우 : ★★★★★', '엠씨더맥스 - 어디에도 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/DeuejYoRbps')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/R69fQWVoZLk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/ZoJrqFPt1pk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/RrFq968fXd8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t9GYZ2InEq0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/XfvR4QJVVhU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/lbLeVCAqd7Y')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow12(Game):
    music_list = ['(노래를 선택하세요)', '시스타 - One More Day : ★★★★★', '샤이니 - 산소 같은 너 : ★☆☆☆☆', '엠버 - Borders : ★☆☆☆☆', '연애말고 결혼 OST - Love Knots : ★★★★★', '샤이니 - One : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆', '양파&다비치&HANNA -  사랑이 다 그런거래요 : ★★★★★', 'K.Will - 눈물이 뚝뚝 : ★☆☆☆☆', "비스트 - I'm sorry : ★☆☆☆☆"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=wvpknmu5UIY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bGKjOoAirdo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=DIjGzZgu_yY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow13(Game):
    music_list = ['(노래를 선택하세요)', '여자친구 - 시간을 달려서 : ★★★☆☆', '가인 - 피어나 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '천둥 - Good : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow14(Game):
    music_list = ['(노래를 선택하세요)', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '엠버 - Borders : ★☆☆☆☆', '샤이니 - One : ★★★★★', '연애말고 결혼 OST - Love Knots : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', "비스트 - I'm sorry : ★☆☆☆☆", 'f(x) - All Mine : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', '샤이니 - Wowowow : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow15(Game):
    music_list = ['(노래를 선택하세요)', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', 'NCT 127 - Switch : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow16(Game):
    music_list = ['(노래를 선택하세요)', '이지수 - 너야 : ★☆☆☆☆', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', 'VIXX - Love Me Do : ★★★★★', 'B1A4 - 몇 번을 : ★★★★★', '샤이니 - Hold You : ★☆☆☆☆', '여자친구 - 시간을 달려서 : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '안현정 - 그대와 나 : ★★★★★', '인피니트 - Follow Me : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=jqCIlPQ-sI8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/FmuOH_0UKVI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=H5hJreMo_f8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow17(Game):
    music_list = ['(노래를 선택하세요)', '에이핑크 - Secret Garden : ★☆☆☆☆', '보아 - Only One : ★☆☆☆☆', "비스트 - I'm sorry : ★☆☆☆☆", '연애말고 결혼 OST - Love Knots : ★★★★★', '샤이니 - One : ★★★★★', 'f(x) - All Mine : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', '엠버 - Borders : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow18(Game):
    music_list = ['(노래를 선택하세요)', '2NE1 - 안녕 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '블루베어스 & 택연 - 오늘 같은 밤 : ★★★★★', '규현 - Eternal Sunshine : ★★★★★', '여자친구 - 시간을 달려서 : ★★★☆☆', '길구봉구 - 달아 : ★★★☆☆', '주헌, 형원, I.M - 인터스텔라 (Interstellar) : ★★★★★', '타코 & 제이형 - 어떡하죠 : ★★★☆☆', '아이유 - 싫은 날 : ★★★★★', '백지영 - 사랑아 또 사랑아 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=uxhVy02aTqA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/3T7BH-7LiqM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/zgwix-rY_pU')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/dBUWcM2TBpM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/-jxLz7uQ3Uw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Tqudgg0aBAI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/wQZkM2ELDXA')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow19(Game):
    music_list = ['(노래를 선택하세요)', '여자친구 - 시간을 달려서 : ★★★☆☆', '휘성 - Night and Day : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '연애말고 결혼 OST - Love Knots : ★★★★★', '동방신기 - Humanoids : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '양파&다비치&HANNA -  사랑이 다 그런거래요 : ★★★★★', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '내 여자친구를 소개합니다 OST - 명우의 수난 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/RSh5akaaHXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=bGKjOoAirdo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/PgO9V6K4yrk')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow20(Game):
    music_list = ['(노래를 선택하세요)', '규현 - 우리가 사랑한 시간 : ★★★★★', "NU'EST - Love Paint : ★★★★★", 'EXO - Heart Attack : ★☆☆☆☆', '박재범 - When : ★☆☆☆☆', 'GOD - 길 : ★★★★★', 'IU - 미운 오리 : ★☆☆☆☆', '레드벨벳 - Light Me Up : ★★★☆☆', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '데미온 - Street of Dawn : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/73TIQLmFb4A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/5_4pSZX2wCM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=NK3y5QJ1rp8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/rRctWJReQFQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/dCdRIvqVGtA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow21(Game):
    music_list = ['(노래를 선택하세요)', '에이핑크 - Secret Garden : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "NU'EST - Love Paint : ★★★★★", "박효신 - It's You : ★★★★★", '레드벨벳 - Ice Cream Cake : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow22(Game):
    music_list = ['(노래를 선택하세요)', '지나유 - 처음사랑 : ★★★★★', '지훈 - 너만 생각나 : ★★★★★', '윤지훈 - 너밖에 몰라 : ★★★★★', '최준영 - 얼음심장 : ★★★★★', '가인 - Fxxk U : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', "NU'EST - Love Paint : ★★★★★", '4MINUTE - 팜므파탈 : ★★★☆☆', 'EXO - Monster : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=leQ5P_1pNB8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/VSAVsstaj4E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow23(Game):
    music_list = ['(노래를 선택하세요)', '린 - 이별주 : ★★★★★', "NU'EST - Love Paint : ★★★★★", '아이유 - 스물셋 : ★★★★★', 'EXO - Baby : ★☆☆☆☆', '크래용팝 - 1, 2, 3, 4 : ★★★★★', '비투비 - Anymore : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', '방탄소년단 - 고엽 : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '가비엔제이 - 연애소설 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/dw_QLwFb2z0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=D1sTQc7FrVk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/82Ocgy2Jsf4')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow24(Game):
    music_list = ['(노래를 선택하세요)', "NU'EST - Love Paint : ★★★★★", '잠비나이 - Connection : ★★★★★', '현아 - 빨개요 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow25(Game):
    music_list = ['(노래를 선택하세요)', "NU'EST - Love Paint : ★★★★★", '4MINUTE - 팜므파탈 : ★★★☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '에일리 - 노래가 늘었어 : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', '인피니트 - Follow Me : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow26(Game):
    music_list = ['(노래를 선택하세요)', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', "비스트 - I'm sorry : ★☆☆☆☆", '연애말고 결혼 OST - Love Knots : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', "NU'EST - Love Paint : ★★★★★", '동방신기 - Humanoids : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow27(Game):
    music_list = ['(노래를 선택하세요)', 'f(x) - Lollipop : ★★★★★', "NU'EST - Love Paint : ★★★★★", '이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '오빠친구동생 - 소보루빵 : ★★★★★', '지코 - 날 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '우주소녀 - Catch Me : ★★★★★', '모던다락방 - All I Want Is 바라만봐도 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/5bBh8fPirDk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/A6JrasjoyeY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/-tDld3F9xAA')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow28(Game):
    music_list = ['(노래를 선택하세요)', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '연애말고 결혼 OST - Love Knots : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '엠버 - Borders : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '샤이니 - One : ★★★★★', "비스트 - I'm sorry : ★☆☆☆☆", "NU'EST - Love Paint : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow29(Game):
    music_list = ['(노래를 선택하세요)', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', '요조 - 바나나파티 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '지나 - 싫어 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '보아 - One Dream : ★☆☆☆☆', "NU'EST - Love Paint : ★★★★★", '정동하 - Mystery (주군의 태양 OST) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow30(Game):
    music_list = ['(노래를 선택하세요)', '시스타 - One More Day : ★★★★★', "NU'EST - Love Paint : ★★★★★", '디아 - 날 위한 이별 : ★★★★★', "박효신 - It's You : ★★★★★", '솔뱅 - 함께 걷던 청계천 : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '방탄소년단 - We on : ★☆☆☆☆', '오빠친구동생 - 소보루빵 : ★★★★★', '팀 - Liquid : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=IyuUyIeyYCc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/p6CIxdvSl4E')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/i4kkDOk9PnM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow31(Game):
    music_list = ['(노래를 선택하세요)', '슈퍼주니어 - SUPERMAN : ★★★★★', '가인 - 피어나 : ★★★★★', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '지훈 - 너만 생각나 : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', "박효신 - It's You : ★★★★★", '정동하 - Mystery (주군의 태양 OST) : ★★★★★', "NU'EST - Love Paint : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow32(Game):
    music_list = ['(노래를 선택하세요)', '디아 - 날 위한 이별 : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '나플라 - 우 : ★☆☆☆☆', "NU'EST - Love Paint : ★★★★★", '스윙스 - 이겨낼거야 2 : ★★★☆☆', '지훈 - 너만 생각나 : ★★★★★', '박효신 - 야생화 : ★★★★★', "박효신 - It's You : ★★★★★", 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/isGDGhBsOT4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/DKQWuqsKXpM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow33(Game):
    music_list = ['(노래를 선택하세요)', 'NCT 127 - Switch : ★★★☆☆', '여은 - 사랑아 나의 사랑아 : ★★★☆☆', "NU'EST - Love Paint : ★★★★★", '동방신기 - Humanoids : ★★★☆☆', '안현정 - 그대와 나 : ★★★★★', '에이핑크 - 몰라요 : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆', '에일리 - 이제는 안녕 : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/eQJEGWQx_Lk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/qTI0TJUGDts')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow34(Game):
    music_list = ['(노래를 선택하세요)', '신용재 - 평범한 사랑 : ★★★☆☆', '인피니트 - 붙박이 별 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '오빠친구동생 - 소보루빵 : ★★★★★', 'VIXX - Love Me Do : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", "NU'EST - Love Paint : ★★★★★", '빅스 - 사슬 : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=jqCIlPQ-sI8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow35(Game):
    music_list = ['(노래를 선택하세요)', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '인피니트 - Follow Me : ★★★★★', "박효신 - It's You : ★★★★★", 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', "NU'EST - Love Paint : ★★★★★", '보아 - Only One : ★☆☆☆☆', '장나라 - 오월의 눈사람 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=3art4Cu-yqg')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow36(Game):
    music_list = ['(노래를 선택하세요)', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', 'VAV - 달빛 아래서 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', "NU'EST - Love Paint : ★★★★★", '2NE1 - 안녕 : ★★★★★', '일렉트로보이즈 - love (feat. 승희 from brave new girl group) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread(
            'https://www.youtube.com/watch?v=6HXnodVJhSI&list=OLAK5uy_kMSFXWnI5_OujCI0ON4-16F8ymMhufnY0&index=1')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/4bVF3W32oMc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow37(Game):
    music_list = ['(노래를 선택하세요)', '에일리 - 수줍은 내 사랑 : ★☆☆☆☆', '박재민 - 하루 : ★★★☆☆', "NU'EST - Love Paint : ★★★★★", "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', '휘성 - Night and Day : ★☆☆☆☆', '잠비나이 - Connection : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/s6I9S9mTt0o')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=XxEtFMDmcPE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=QTQhNI9NNQw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow38(Game):
    music_list = ['(노래를 선택하세요)', '에이핑크 - Secret Garden : ★☆☆☆☆', '엠버 - Borders : ★☆☆☆☆', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', 'GOD - 길 : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', 'f(x) - All Mine : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', '샤이니 - One : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/bNT-zFJKifI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow39(Game):
    music_list = ['(노래를 선택하세요)', 'EXO - Monster : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', 'GOD - 길 : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '틴탑 - 향수 뿌리지마 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'IU - 미운 오리 : ★☆☆☆☆', '레드벨벳 - Light Me Up : ★★★☆☆', '데미온 - Street of Dawn : ★★★☆☆', 'VAV - 달빛 아래서 : ★☆☆☆☆']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/TUZrerjUfIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=NK3y5QJ1rp8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/rRctWJReQFQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/dCdRIvqVGtA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=6HXnodVJhSI&list=OLAK5uy_kMSFXWnI5_OujCI0ON4-16F8ymMhufnY0&index=1')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow40(Game):
    music_list = ['(노래를 선택하세요)', 'EXO - Heart Attack : ★☆☆☆☆', '아이유 - 스물셋 : ★★★★★', '비투비 - 두 번째 고백 : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '헨리 - I Would : ★★★★★', '인피니트 - 맡겨 : ★★★☆☆', '빅뱅 - 맨정신 : ★★★★★', 'EXO - BEAUTIFUL : ★★★☆☆', '산들(B1A4) - 짝사랑 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/RXos9M66VbM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/NYanZjjfUw4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/MBNQgq56egk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ZPmnUSmzzno')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/osYmpohGBS8')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow41(Game):
    music_list = ['(노래를 선택하세요)', 'EXO - Heart Attack : ★☆☆☆☆', '클래지콰이 프로젝트 - Android : ★★★☆☆', '현아 - 빨개요 : ★★★★★', '셰인 - Be My Love : ★★★☆☆', '지나 - 싫어 : ★☆☆☆☆', '엠버 - Need To Feel Needed : ★☆☆☆☆', 'J-Min - Beautiful Days : ★★★★★', '뉴이스트 - 나의 천국 : ★★★★★', '한희정 - 러브레터 : ★★★☆☆', '엠블랙 - Again : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/OmfR14eBQQo')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/aHlYN3jIRMU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/iNPfFLmwyqM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/0GotOSuAO3U')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow42(Game):
    music_list = ['(노래를 선택하세요)', '4MINUTE - 팜므파탈 : ★★★☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '제이민 x 심은지 - 집 앞에서 : ★★★☆☆', 'EXO - Heart Attack : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '인피니트 - 불편한 진실 : ★★★☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '밍스 - shut up : ★☆☆☆☆', "백지영 - 아이캔't 드링크 : ★☆☆☆☆", '일렉트로보이즈 - love (feat. 승희 from brave new girl group) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/vllQcjG_au4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/IYyENijVcU4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/XwCDkRiJucw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/n7MUpj8VQeY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/4bVF3W32oMc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow43(Game):
    music_list = ['(노래를 선택하세요)', '이지수 - 너야 : ★☆☆☆☆', '레드벨벳 - Light Me Up : ★★★☆☆', '인피니트 - 내꺼하자 : ★★★★★', 'GOD - 길 : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', 'EXO - Heart Attack : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/rRctWJReQFQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow44(Game):
    music_list = ['(노래를 선택하세요)', "박효신 - It's You : ★★★★★", '아이오아이 - 내 말대로 해줘 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '에일리 - 얼음꽃 : ★★★★★', '임창정 - 그렇게 당해놓고 : ★★★☆☆', 'EXO - Heart Attack : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', 'f(x) - Lollipop : ★★★★★', 'RETA - Listen Now : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/5ParLiob-xw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Z8KzIpDqYoc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/XTSCvT7_dys')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow45(Game):
    music_list = ['(노래를 선택하세요)', '에이핑크 - Secret Garden : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '인피니트 - Follow Me : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', '잠비나이 - Connection : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow46(Game):
    music_list = ['(노래를 선택하세요)', '보아 - One Dream : ★☆☆☆☆', 'EXO - Heart Attack : ★☆☆☆☆', '아지아틱스 - Cold : ★★★★★', '비즈니즈 - 죽은 위인들의 사회 : ★★★☆☆', '슈퍼주니어 - Sexy, Free & Single : ★★★☆☆', "비프리 - fly (feat. loco & s'way.d) : ★★★★★", '인피니트 - Alone : ★☆☆☆☆', '현아 - Attention : ★★★☆☆', '칠전팔기 구해라 OST - 아로하 : ★★★★★', '박세영 - 블루로드 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/e8jXzim2hXk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/9PmvBKQOCCw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/gWIkiI_UmeE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/-e0FSXlQm4Q')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=AoS_cWcZB34')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=sV5cwqHw-p8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/u052eGvnQg0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=OSaANCJsfXs')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow47(Game):
    music_list = ['(노래를 선택하세요)', '시스타 - One More Day : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', '세븐틴 - BEAUTIFUL : ★★★★★', '미생 OST - Jordan Fantasy : ★★★★★', '윤도현 - 사랑했나봐 : ★☆☆☆☆', '미생 OST - 출근길 : ★★★☆☆', '블루베어스 & 택연 - 오늘 같은 밤 : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '이홍기 - Jump (뜨거운 안녕 OST) : ★★★★★', '시스타 - 이불 덮고 들어 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/TVaeTwHc2Lc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/MC7FxEOm5bo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=KeMbLY7ztDw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/uvatwry5tmA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=uxhVy02aTqA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/JJlFuj7WA9Q')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/sC0XKHDA-xM')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow48(Game):
    music_list = ['(노래를 선택하세요)','EXO - Heart Attack : ★☆☆☆☆', '케이윌 - 이러지마 제발 : ★☆☆☆☆', '시크릿 - Madonna : ★☆☆☆☆', '크라운제이 - The Best (feat. 서인영) : ★★★★★', '유미 - Last one (주군의 태양 OST) : ★★★☆☆', '요섭(비스트) - 나와 : ★★★★★', '가인 - 피어나 : ★★★★★', '비 - 30 SEXY (East4a deeptech mix) : ★★★☆☆', '시스타 - Say I Love You : ★★★★★', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/PdUiCJnRptk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/n2fM1yHE_Nc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/exqQ-a1UZfY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/XEk5Nrd3-Zs')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/61B2Ol6gzLc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/ZCLWXYCmeUcc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/nslMk8Vuw-0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow49(Game):
    music_list = ['(노래를 선택하세요)','김종국 - 눈물자국 : ★☆☆☆☆', '우주소녀 - Catch Me : ★★★★★', '지코 - 날 : ★☆☆☆☆', '윤도현 - 요즘 내 모습 : ★☆☆☆☆', 'EXO - Heart Attack : ★☆☆☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', "박효신 - It's You : ★★★★★", '박효신 - 야생화 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/0zMYllAzwM0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/A6JrasjoyeY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/5bBh8fPirDk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/M9jYuBrX0eUU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow50(Game):
    music_list = ['(노래를 선택하세요)','EXO - Heart Attack : ★☆☆☆☆', 'NCT 127 - Switch : ★★★☆☆', '스윗소로우 - 별 일 아니에요 (연애의 발견 OST) : ★★★☆☆', '황치열, 리싸 - 이 밤의 끝을 잡고 : ★☆☆☆☆', '비스트 - Easy : ★★★★★', '벤 - 안 괜찮아 : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '주군의 태양 OST - Ghost World : ★★★☆☆', '빅뱅 - Crazy Dog : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/GELnbRfJv3c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/23oVRoiu_dk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/cPTL-1ijmTI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/4b_ABHDG0Zg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/onAdqNddGpw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/c1nag-CoLpk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow51(Game):
    music_list = ['(노래를 선택하세요)','박재민 - 하루 : ★★★☆☆', 'VAV - 달빛 아래서 : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '데미온 - Street of Dawn : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '윤지훈 - 너밖에 몰라 : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆', 'GOD - 길 : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=XxEtFMDmcPE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread(
            'https://www.youtube.com/watch?v=6HXnodVJhSI&list=OLAK5uy_kMSFXWnI5_OujCI0ON4-16F8ymMhufnY0&index=1')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/dCdRIvqVGtA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow52(Game):
    music_list = ['(노래를 선택하세요)','EXO - Heart Attack : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', "바람이 분다OST - It's Over : ★★★★★", '에이핑크 - Secret Garden : ★☆☆☆☆', '슈가볼 - Cherish : ★★★☆☆', '보아 - Only One : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread(
            'https://www.youtube.com/watch?v=qocyC5nvsH8&list=OLAK5uy_kfaAb-W2pQsUqp0x-VmmMlHrGyQhvD79k&index=15')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=bq3-da4ENs4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow53(Game):
    music_list = ['(노래를 선택하세요)',"신데렐라와 네 명의 기사 OST - Let's Cheer Up! : ★☆☆☆☆", '이준기 - 하루만 : ★★★★★', '임창정 - 그렇게 당해놓고 : ★★★☆☆', '에이핑크 - Wanna Be : ★☆☆☆☆', '2NE1 - 안녕 : ★★★★★', '4MINUTE - BABABA : ★★★★★', '비스트 - Sad Movie : ★☆☆☆☆', '시스타 - Say I Love You : ★★★★★', 'EXO - Heart Attack : ★☆☆☆☆', '크라운제이 - The Best (feat. 서인영) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/r2md7i9Sra0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=w09-YIVqP5w')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=YFLnr9CUfJQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=4rD4yRIktTE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=eQxVA1wHF1Q')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/nslMk8Vuw-0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/exqQ-a1UZfY')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow54(Game):
    music_list = ['(노래를 선택하세요)','비스트 - Fiction : ★★★★★', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '캐스커 - Undo : ★★★★★', '인피니트 - Follow Me : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', '천둥 - Good : ★★★☆☆', '휘성 - Night and Day : ★☆☆☆☆', 'EXO - Heart Attack : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=whlVRDTobhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=tK_Cy1l3ASE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=17EC_xVcqC8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow55(Game):
    music_list = ['(노래를 선택하세요)','지훈 - 너만 생각나 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '봄바람 소년 - Only One : ★★★☆☆', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', 'EXO - Monster : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow56(Game):
    music_list = ['(노래를 선택하세요)','려욱 - 그대 : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', 'EXO - Let out the Beast : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '커피소년 - 바보 : ★★★★★', '방탄소년단 - 진격의 방탄 : ★★★☆☆', '레드벨벳 - Ice Cream Cake : ★★★★★', '아이유 - 스물셋 : ★★★★★', '현아 - Change : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/4BUQW4xwtAU')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Ac73vrPaKxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/KDBtuplAjRA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=7RsFNXsvusw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=fkBO1aq3a5E')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow57(Game):
    music_list = ['(노래를 선택하세요)','샤이니 - Runaway : ★★★★★', '슬리피 - 기분탓 : ★☆☆☆☆', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '신용재 - 평범한 사랑 : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '레드벨벳 - Ice Cream Cake : ★★★★★', '현아 - 빨개요 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=GNJrZOWa_E0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow58(Game):
    music_list = ['(노래를 선택하세요)','MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', 'GOD - 길 : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '데미온 - Street of Dawn : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', '장나라 - 오월의 눈사람 : ★★★★★', '레드벨벳 - Light Me Up : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=KgXtSx8ublA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/dCdRIvqVGtA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=3art4Cu-yqg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/rRctWJReQFQ')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow59(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '레드벨벳 - Ice Cream Cake : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', '인피니트 - 내꺼하자 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow60(Game):
    music_list = ['(노래를 선택하세요)','레드벨벳 - Ice Cream Cake : ★★★★★', 'f(x) - Lollipop : ★★★★★', '레드벨벳 - Huff n Puff : ★☆☆☆☆', '윤도현밴드 - 미스터리 : ★★★☆☆', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '딕펑스 - 요즘 젊은 것들 : ★★★☆☆', '방탄소년단 - 진격의 방탄 : ★★★☆☆', '스타러브피쉬 (with Jane) - Goodbye (연애의 발견 OST) : ★★★☆☆', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '안현정 - 그대와 나 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=9eINuufm6TY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/4DNf1ou59pY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=7RsFNXsvusw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/jPTM_yIP9-A')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow61(Game):
    music_list = ['(노래를 선택하세요)','레드벨벳 - Ice Cream Cake : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', '지나유 - 처음사랑 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '포맨 - 살다가 한번쯤 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow62(Game):
    music_list = ['(노래를 선택하세요)','보아 - One Dream : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', "박효신 - It's You : ★★★★★", '레드벨벳 - Ice Cream Cake : ★★★★★', '요조 - 바나나파티 : ★★★★★', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '지나 - 싫어 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow63(Game):
    music_list = ['(노래를 선택하세요)','더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '레드벨벳 - Ice Cream Cake : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow64(Game):
    music_list = ['(노래를 선택하세요)','디아 - 날 위한 이별 : ★★★★★', '요조 - 바나나파티 : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '가인 - 피어나 : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow65(Game):
    music_list = ['(노래를 선택하세요)','NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '박재민 - 하루 : ★★★☆☆', '오빠친구동생 - 소보루빵 : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★', '박효신 - 야생화 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '윤지훈 - 너밖에 몰라 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=XxEtFMDmcPE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow66(Game):
    music_list = ['(노래를 선택하세요)','레드벨벳 - Ice Cream Cake : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'NCT 127 - Switch : ★★★☆☆', "박효신 - It's You : ★★★★★", '봄바람 소년 - Only One : ★★★☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow67(Game):
    music_list = ['(노래를 선택하세요)','빅스 - 사슬 : ★☆☆☆☆', '지나유 - 처음사랑 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', "박효신 - It's You : ★★★★★", 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '레드벨벳 - Ice Cream Cake : ★★★★★', '윤지훈 - 너밖에 몰라 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow68(Game):
    music_list = ['(노래를 선택하세요)','보아 - Only One : ★☆☆☆☆', '레드벨벳 - Ice Cream Cake : ★★★★★', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '포맨 - 살다가 한번쯤 : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow69(Game):
    music_list = ['(노래를 선택하세요)','4MINUTE - 팜므파탈 : ★★★☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '일렉트로보이즈 - love (feat. 승희 from brave new girl group) : ★★★★★', '인피니트 - Follow Me : ★★★★★', "박효신 - It's You : ★★★★★", '레드벨벳 - Ice Cream Cake : ★★★★★', '2NE1 - Goodbye : ★★★★★', '이지수 - 너야 : ★☆☆☆☆']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/4bVF3W32oMc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow70(Game):
    music_list = ['(노래를 선택하세요)','휘성 - Night and Day : ★☆☆☆☆', '윤지훈 - 너밖에 몰라 : ★★★★★', '레드벨벳 - Ice Cream Cake : ★★★★★', "박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '인피니트 - Follow Me : ★★★★★', '잠비나이 - Connection : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=3zo4F0ZI5wE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow71(Game):
    music_list = ['(노래를 선택하세요)','유준상 - Love & Hate : ★★★★★', '좋아서하는밴드 - 우리 함께 하면 : ★★★☆☆', '한희정 - 러브레터 : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '임창정 - 그렇게 당해놓고 (feat.마부스 OF 일렉트로보이즈) (inst) : ★★★☆☆', '샤이니 - Your Number : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '아이유 - 스물셋 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=G3HHGDsrWR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=XQ7VV9V3cjs')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow72(Game):
    music_list = ['(노래를 선택하세요)','안혜은 - 그녀를 찾지마 : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '바스코 - Whoa Ha ! : ★★★☆☆', 'Lucia(심규선) - 녹여줘 : ★★★☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '현아 -Red : ★★★★★', '다방 - Wanna Buy Love (여자친구 사주세요) (사랑을 살 수 있다면) : ★★★★★', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '비스트 - Let It Snow : ★★★☆☆', '스윙스 - 이겨낼거야 2 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=BUIhCU0IaUA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=JpL691-pxuM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/cJ5ts0qjCaI')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/R69fQWVoZLk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ZoJrqFPt1pk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/DKQWuqsKXpM')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow73(Game):
    music_list = ['(노래를 선택하세요)','f(x) - All Mine : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '샤이니 - One : ★★★★★', '인피니트 - Follow Me : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', 'EXO - Monster : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow74(Game):
    music_list = ['(노래를 선택하세요)','인피니트 - 내꺼하자 : ★★★★★', 'EXO - Monster : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '에이핑크 - Secret Garden : ★☆☆☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '모던다락방 - All I Want Is 바라만봐도 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/-tDld3F9xAA')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow75(Game):
    music_list = ['(노래를 선택하세요)','Flower - 사랑은 알아도... : ★☆☆☆☆', 'f(x) - Lollipop : ★★★★★', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '오빠친구동생 - 소보루빵 : ★★★★★', '수지 - Ring My Bell : ★★★★★', 'EXO - Monster : ★★★★★', '인피니트 - 붙박이 별 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '딕펑스 - 요즘 젊은 것들 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=HVQ2WKhByMU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow76(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '인피니트 - Follow Me : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', 'EXO - Monster : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow77(Game):
    music_list = ['(노래를 선택하세요)','EXO - Monster : ★★★★★', '보아 - One Dream : ★☆☆☆☆', '시스타 - Say I Love You : ★★★★★', '오준성 - Enjoy Party : ★☆☆☆☆', '에이핑크 - It Girl : ★☆☆☆☆', '비스트 - 내가 아니야 : ★☆☆☆☆', '뉴이스트 - 나의 천국 : ★★★★★', '더 라임 그리워서 : ★★★☆☆', 'FTISLAND - 여자는 몰라 : ★☆☆☆☆', '틴탑 - Date : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/nslMk8Vuw-0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=JkRgGYEYERM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=nmcvXYrzPhM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=CU3wvWFpNvE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=fyaYx8M4DQk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=n25WFqxylKI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=K3esd7tIvPU')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow78(Game):
    music_list = ['(노래를 선택하세요)','딕펑스 - 요즘 젊은 것들 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', '시스타 - One More Day : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'EXO - Monster : ★★★★★', "박효신 - It's You : ★★★★★", '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow79(Game):
    music_list = ['(노래를 선택하세요)','가인 - 피어나 : ★★★★★', 'EXO - Monster : ★★★★★', '딕펑스 - 한강에서 놀아요 : ★★★☆☆', '딕펑스 - 요즘 젊은 것들 : ★★★☆☆', '인피니트 - 붙박이 별 : ★★★★★', "박효신 - It's You : ★★★★★", '이지수 - 너야 : ★☆☆☆☆', '요조 - 바나나파티 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow80(Game):
    music_list = ['(노래를 선택하세요)','인피니트 - Follow Me : ★★★★★', "박효신 - It's You : ★★★★★", '박효신 - 야생화 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '윤지훈 - 너밖에 몰라 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '지나유 - 처음사랑 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=IMQQbW33Vv0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow81(Game):
    music_list = ['(노래를 선택하세요)','윤미래 - 사랑이 맞을거야 : ★★★☆☆', 'NCT 127 - Switch : ★★★☆☆', 'Ailee - 폭풍속으로 : ★★★★★', '에일리 - 까꿍 : ★★★★★', '세븐틴 - 글쎄 : ★★★★★', '비투비 - 북 치고 장구 치고 : ★☆☆☆☆', '헨리(슈퍼주니어 M) - 1-4-3 (I Love You) : ★★★★★', '신용재 - 평범한 사랑 : ★★★☆☆', 'EXO - Monster : ★★★★★', '보아 - Kiss My Lips : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ijyPu476gqM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=2wOprvXwRRw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=2syb5fmZCy0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=LDd8sYs_Nos')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/iQPYeoWaYVo')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=aYJoNjk0G_Y')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=_HusM0Fhyn8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow82(Game):
    music_list = ['(노래를 선택하세요)','효린 - 널 사랑하겠어 : ★☆☆☆☆', '백지영 - 내 귀에 캔디 : ★★★★★', '김종국 - 눈물자국 : ★☆☆☆☆', '빅스 - 사슬 : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '오빠친구동생 - 소보루빵 : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', '레드벨벳 - Huff n Puff : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '산이 - Do It For Fun : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/CXETtH7hlkk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/rMG1YtxHLB8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/0zMYllAzwM0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=9eINuufm6TY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/VGEtxWb6b5w')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow83(Game):
    music_list = ['(노래를 선택하세요)','보아 - Only One : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '샤이니 - One : ★★★★★', "박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', 'f(x) - All Mine : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow84(Game):
    music_list = ['(노래를 선택하세요)','2NE1 - 안녕 : ★★★★★', '시크릿 - Madonna : ★☆☆☆☆', '비 - 널 붙잡을 노래 : ★★★★★', '태양 - Where U At : ★★★★★', '니엘 - 심쿵 : ★★★★★', '시스타 - 나혼자 : ★★★☆☆', 'EXO - Monster : ★★★★★', 'EXO - December, 2014 (The Winter’s Tale) : ★★★☆☆', '니엘 - 그런 날 : ★★★☆☆', '박재범 - Evolution (feat. Gray) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/n2fM1yHE_Nc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/2_tOh1AskFc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/btPF7HrPkyU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=1T3gndIBNbc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/E0ZHXVp_wUE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/iuY1y6bxKW0')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eKY7lZJPxQw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=lYPMh88RTLc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow85(Game):
    music_list = ['(노래를 선택하세요)','이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'EXO - Monster : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=VatHIJh4O0M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow86(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 스물셋 : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '용준형(비스트) - Caffeine : ★☆☆☆☆', '현아 -Red : ★★★★★', '박보람 - 연예할래 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '멜로디데이 - 마법의 성 : ★★★★★', '커피소년 - 바보 : ★★★★★', '성훈 - The Justice : ★★★★★', 'EXO - MY ANSWER : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=yL7MLE0ccB4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/1ELGunbuvqc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=UD6ZHSEVAJo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/KDBtuplAjRA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=fSgkA9gNFZo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=KC_nbsVUFtM')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow87(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 스물셋 : ★★★★★', '혁오 - Hooka : ★☆☆☆☆', '빅뱅 - Remember : ★★★★★', '이홍기 - Jump (뜨거운 안녕 OST) : ★★★★★', '아이유 - 입술 사이 (50cm) : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', "샤이니 - Don't Stop : ★★★☆☆", 'EXO - Thunder : ★☆☆☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=OytSUJZNgL4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=mEkY35ceP04')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/JJlFuj7WA9Q')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=sBVca5KOpkM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=o_3oHrQ14f4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Q62BG1hTpRg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow88(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 스물셋 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '인피니트 - 내꺼하자 : ★★★★★', "박효신 - It's You : ★★★★★", '이지수 - 너야 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow89(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 느리게 하는 일 : ★★★★★', 'f(x) - Lollipop : ★★★★★', '빅스 - Can’t say : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '업텐션 - Just Like That : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '나플라 - 우 : ★☆☆☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '아이유 - 스물셋 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=vmAIyJvVKhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/isGDGhBsOT4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow90(Game):
    music_list = ['(노래를 선택하세요)','규현 - Eternal Sunshine : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '아이유 - 스물셋 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', "박효신 - It's You : ★★★★★", '애프터스쿨 - 너 때문에 : ★★★★★', '요조 - 바나나파티 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/3T7BH-7LiqM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow91(Game):
    music_list = ['(노래를 선택하세요)','보아 - One Dream : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', 'AZIATIX - Lights : ★☆☆☆☆', '주영 - 들리나요 : ★★★★★', '비투비 - 두 번째 고백 : ★☆☆☆☆', '비투비 - For You : ★☆☆☆☆', '벤 - 안 괜찮아 : ★★★☆☆', '윤미래 - 사랑이 맞을거야 : ★★★☆☆', '아이유 - 스물셋 : ★★★★★', '현아 - 내 집에서 나가 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=hTUr660PMlU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=2LW4Ih_UZMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=G575vb5BYJY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/4b_ABHDG0Zg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ijyPu476gqM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=k69Q53y8skg')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow92(Game):
    music_list = ['(노래를 선택하세요)','제아 - 그대 바보 : ★★★★★', "연애말고결혼OST - What's Up : ★☆☆☆☆", '아이유 - 스물셋 : ★★★★★', '김희진 - 이별얘기 : ★★★★★', '거미 - 너를 사랑해 : ★★★★★', '안녕하신가영 - 순간의 순간 : ★☆☆☆☆', '인피니트 - Real Story : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', '채정아 - 죽어야 살까 : ★★★★★', '제시 - 쾌지나 칭칭나네 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=PActqzbihXY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=zsfpHGqswb4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=PSDfz_CjyiA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=OzfpeXFFe2I')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=J3unOTNiDN8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=fm384xbFBLk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread(
            'https://www.youtube.com/watch?v=gXeRqUt_gWU&list=OLAK5uy_lJKr97NHirogxAPddx7IkF4jWAJqRf93A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=uua52WTniBk')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow93(Game):
    music_list = ['(노래를 선택하세요)','가인 - 피어나 : ★★★★★', '아이유 - 스물셋 : ★★★★★', '비투비 - Anymore : ★☆☆☆☆', '크래용팝 - 1, 2, 3, 4 : ★★★★★', '가비엔제이 - 연애소설 : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '이승철 - 달링(프로듀사 OST) : ★★★☆☆', 'EXO - Baby : ★☆☆☆☆', '비스트 - Dance With U : ★★★★★', '린 - 이별주 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=D1sTQc7FrVk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/82Ocgy2Jsf4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/rCHEXMe0y_o')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/dw_QLwFb2z0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/0zGGPkNu9sw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow94(Game):
    music_list = ['(노래를 선택하세요)','4MINUTE - Sweet Suga Honey! : ★☆☆☆☆', '린 - 이별주 : ★★★★★', '아이유 - 스물셋 : ★★★★★', '크래용팝 - 1, 2, 3, 4 : ★★★★★', '인피니트 - Julia : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '비투비 - 스릴러 : ★★★★★', 'G.NA - 첫눈에 한눈에 : ★☆☆☆☆', '박재범 - 사실은 : ★☆☆☆☆', '엠블랙 - Y : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=hUIPuAWwhFs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Is4Ne0KeBGA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=eBVe1AUfT2w')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ptlOVdANVXA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=InmJJVsF9qU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/gyCss-xlMNA')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow95(Game):
    music_list = ['(노래를 선택하세요)','빅뱅 - 맨정신 : ★★★★★', '스윙스 - a real lady : ★☆☆☆☆', '세븐틴 - 어른이 되면 : ★☆☆☆☆', '아이유 - 스물셋 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '에일리 - 이제는 안녕 : ★★★★★', '업텐션 - Just Like That : ★☆☆☆☆', '이유성 - Butter Flying : ★★★☆☆', '아이유 - 느리게 하는 일 : ★★★★★', 'NCT 127 - Switch : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/MBNQgq56egk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=8H2OTYIHJvg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=DyJga7ny8jE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=HVqxQThIGgk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow96(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 스물셋 : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '바람이 분다OST - 비밀의 방 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '윤도현 - 요즘 내 모습 : ★☆☆☆☆', '빅스 - 사슬 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=GrtKiJt_xJg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/M9jYuBrX0eUU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow97(Game):
    music_list = ['(노래를 선택하세요)','아이유 - 스물셋 : ★★★★★', '보아 - Only One : ★☆☆☆☆', '산들(B1A4) - 짝사랑 : ★★★☆☆', '업텐션 - Just Like That : ★☆☆☆☆', '아이유 - 느리게 하는 일 : ★★★★★', '이유성 - Butter Flying : ★★★☆☆', '백지영 - 안해요 : ★★★★★', '셰인 - Be My Love : ★★★☆☆', '그린 카카오 - 언젠가 그대 다시 만나면 : ★★★★★', '유미 - Last one (주군의 태양 OST) : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/osYmpohGBS8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=HVqxQThIGgk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=sLY1xUdz9JU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=OXnA_Mz1BUE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/XEk5Nrd3-Zs')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow98(Game):
    music_list = ['(노래를 선택하세요)','2NE1 - 안녕 : ★★★★★', '아이유 - 스물셋 : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '산들(B1A4) - 짝사랑 : ★★★☆☆', '그린 카카오 - 언젠가 그대 다시 만나면 : ★★★★★', '오빠친구동생 - 소보루빵 : ★★★★★', "유성은 & 진영 - I'm In Love : ★★★★★", '인피니트 - 맡겨 : ★★★☆☆', '백지영 - 비라도 내렸으면 좋겠어 : ★★★☆☆', '비투비 - 두 번째 고백 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/osYmpohGBS8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=OXnA_Mz1BUE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=dy3vl_LTlrs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/NYanZjjfUw4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=0u51UhgzBk4')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow99(Game):
    music_list = ['(노래를 선택하세요)','산들 - 같이 걷는 길 : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆', '아이유 - 스물셋 : ★★★★★', '업텐션 - Just Like That : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '4MINUTE - BABABA : ★★★★★', '그린 카카오 - 언젠가 그대 다시 만나면 : ★★★★★', '몬스타엑스 - 출구는 없어 : ★☆☆☆☆', '라이너스의 담요 - Love Me : ★★★★★', '비투비 - 두 번째 고백 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=8YUp_kWhoXo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=NeeMfvMnYnE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=4rD4yRIktTE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=OXnA_Mz1BUE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=H9zSm887HDs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=AY10bU_rBu4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow100(Game):
    music_list = ['(노래를 선택하세요)','에일리 - 노래가 늘었어 : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '클래지콰이 프로젝트 - Android : ★★★☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '타루 - 세탁기 : ★★★☆☆', '한희정 - 러브레터 : ★★★☆☆', '예성 - 먹지 : ★★★★★', '4MINUTE - BABABA : ★★★★★', '이홍기 - Jump (뜨거운 안녕 OST) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/OmfR14eBQQo')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Xu-im-lBZsU')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/eofaEu1DZ_U')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=4rD4yRIktTE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/JJlFuj7WA9Q')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow101(Game):
    music_list = ['(노래를 선택하세요)','정동하 - Mystery (주군의 태양 OST) : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★', "박효신 - It's You : ★★★★★", '에이핑크 - Secret Garden : ★☆☆☆☆', '샤이니 - Wowowow : ★☆☆☆☆', '샤이니 - One : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '잠비나이 - Connection : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow102(Game):
    music_list = ['(노래를 선택하세요)','천둥 - Good : ★★★☆☆', '이지수 - 너야 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '인피니트 - Follow Me : ★★★★★', 'f(x) - Lollipop : ★★★★★', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '현아 - 빨개요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow103(Game):
    music_list = ['(노래를 선택하세요)','시스타 - Oh Baby : ★☆☆☆☆', '려욱 - 그대 : ★★★☆☆', '린 - 이별주 : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', '현아 - 빨개요 : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', "박효신 - It's You : ★★★★★", '슈퍼주니어 - SUPERMAN : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=XoMlXv1WK_g')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/4BUQW4xwtAU')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow104(Game):
    music_list = ['(노래를 선택하세요)','현아 - 빨개요 : ★★★★★', '알파벳 - 답정너 : ★★★★★', '보아 - One Dream : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '지나 - 싫어 : ★☆☆☆☆', 'We are the night - 흐려도 좋아 : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '더 라임 그리워서 : ★★★☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/A1WTC2kzz4s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=XNRo2MEMALQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=fyaYx8M4DQk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow105(Game):
    music_list = ['(노래를 선택하세요)','샤이니 - Runaway : ★★★★★', '시스타 - One More Day : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆', '현아 - 빨개요 : ★★★★★', "박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '천둥 - Good : ★★★☆☆', '동방신기 - Humanoids : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow106(Game):
    music_list = ['(노래를 선택하세요)','박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '린 - 이별주 : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★', '인피니트 - Julia : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '려욱 - 그대 : ★★★☆☆', '현아 - Change : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Is4Ne0KeBGA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/4BUQW4xwtAU')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=fkBO1aq3a5E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow107(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", '디아 - 날 위한 이별 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '현아 - 빨개요 : ★★★★★', '박효신 - 야생화 : ★★★★★', '샤이니 - Runaway : ★★★★★', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow108(Game):
    music_list = ['(노래를 선택하세요)','더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', 'Beta89 - 청춘아 : ★☆☆☆☆', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '코코소리 - 다크서클 : ★★★★★', '딕펑스 - 요즘 젊은 것들 : ★★★☆☆', '지나 - 싫어 : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★', '아우라 - 커졌다 작아졌다 : ★★★☆☆', 'NCT 127 - Switch : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=veaz-t0e2Fg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=eM8A0q8GQrc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/MuJUPCqRM1c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow109(Game):
    music_list = ['(노래를 선택하세요)','세븐틴 - 어른이 되면 : ★☆☆☆☆', '헨리 - Butterfly : ★☆☆☆☆', '시크릿 - POISON : ★☆☆☆☆', '민효린 & 진영 - 당신과 만난 이날 : ★★★☆☆', '이유성 - Butter Flying : ★★★☆☆', '현아 - 빨개요 : ★★★★★', '비스트 - 일하러 가야 돼 : ★☆☆☆☆', '블락비 - 몇 년 후에 : ★☆☆☆☆', '빅스 - 사슬 : ★☆☆☆☆', '오준성 - Out Of The Ghost : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=DyJga7ny8jE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=zbIND35CRgw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/TP56DuUpKBE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=R_WB0dPw6VE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=HVqxQThIGgk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=1BhbmhWMwC0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=3q6oEyVi9Dk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Ik_c8iCCw3M')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow110(Game):
    music_list = ['(노래를 선택하세요)','어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '업텐션 - Just Like That : ★☆☆☆☆', '비투비 - 두 번째 고백 : ★☆☆☆☆', '셰인 - Be My Love : ★★★☆☆', '아이유 - 느리게 하는 일 : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '악동뮤지션 - 매력있어 : ★★★★★', '현아 - 빨개요 : ★★★★★', '보아 - Only One : ★☆☆☆☆', '헨리(슈퍼주니어 M) - 1-4-3 (I Love You) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=i7ZZ7bAw0s4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=aYJoNjk0G_Y')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow111(Game):
    music_list = ['(노래를 선택하세요)','앤츠 - 예쁜 너니까 : ★☆☆☆☆', "유성은 & 진영 - I'm In Love : ★★★★★", '2NE1 - 안녕 : ★★★★★', '비투비 - 두 번째 고백 : ★☆☆☆☆', '틴탑 - 우린 문제없어 : ★☆☆☆☆', '인피니트 - Amazing : ★★★☆☆', '에이핑크 - 하늘 높이 : ★★★★★', '씨잼 - 걍 음악이다 : ★★★☆☆', '릴보이 - 돈돈돈 : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=dy3vl_LTlrs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Mdc9Y4NvGog')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ZLIqOjKWPvg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=TnIXDeM7jAw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=smx44t360ng')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=6rbt3DjYoOg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow112(Game):
    music_list = ['(노래를 선택하세요)','잠비나이 - Connection : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆', '미 - 온도 : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '현아 - 빨개요 : ★★★★★', "박효신 - It's You : ★★★★★", '디아 - 날 위한 이별 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/IqnF2Rps05Y')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=taSWFpvWOag')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow113(Game):
    music_list = ['(노래를 선택하세요)','비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '이지수 - 너야 : ★☆☆☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '모던다락방 - All I Want Is 바라만봐도 : ★★★☆☆', '인피니트 - 내꺼하자 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/-tDld3F9xAA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow114(Game):
    music_list = ['(노래를 선택하세요)','이지수 - 너야 : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', 'MBLAQ - 유령(같이 사랑했잖아) : ★☆☆☆☆', "박효신 - It's You : ★★★★★", 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '비스트 - Fiction : ★★★★★', '인피니트 - Follow Me : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '요조 - 바나나파티 : ★★★★★', 'f(x) - Lollipop : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=3uWlDF40QMc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=whlVRDTobhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow115(Game):
    music_list = ['(노래를 선택하세요)',"바람이 분다OST - It's Over : ★★★★★", 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '인피니트 - Follow Me : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '봄바람 소년 - Only One : ★★★☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', "박효신 - It's You : ★★★★★", '애프터스쿨 - 너 때문에 : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=qocyC5nvsH8&list=OLAK5uy_kfaAb-W2pQsUqp0x-VmmMlHrGyQhvD79k&index=15')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow116(Game):
    music_list = ['(노래를 선택하세요)','4MINUTE - BABABA : ★★★★★', '동방신기 - Humanoids : ★★★☆☆', '아이유 - 느리게 하는 일 : ★★★★★', '알레그로 - 우리가 스쳐온 서울 밤하늘엔 : ★★★☆☆', '보아 - One Dream : ★☆☆☆☆', '업텐션 - Just Like That : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '백지영 - 안해요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=4rD4yRIktTE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/0LvBVFnX1Vk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/rJgxdF_tCtw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=sLY1xUdz9JU')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow117(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", '잔나비 - Goodnight (Intro) : ★★★★★', 'f(x) - All Mine : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '인피니트 - Follow Me : ★★★★★', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '샤이니 - One : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow118(Game):
    music_list = ['(노래를 선택하세요)','에일리 - 노래가 늘었어 : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', 'Ra.L - 잠을 좀 자고싶어요 : ★☆☆☆☆', '이유림 - 이런 기분 : ★★★☆☆', 'EXO - Let Out The Beast : ★★★★★', 'EXO - Cloud 9 : ★☆☆☆☆', '바이브 - 외로운 놈 : ★★★☆☆', '보경, 셰인 - Summer Love : ★★★☆☆', '백지영 - 사랑아 또 사랑아 : ★☆☆☆☆', 'B.A.P - 빗소리 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=vISAh4A8s4M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Bnc3O7OkQlQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Ac73vrPaKxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=iEVaw0Ooh9E')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=bTx8pv_VhCk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/L9GPT1opU44')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/wQZkM2ELDXA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=mnt9rMqwjkA')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow119(Game):
    music_list = ['(노래를 선택하세요)','에일리 - 노래가 늘었어 : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', "박효신 - It's You : ★★★★★", 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '인피니트 - Follow Me : ★★★★★', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow120(Game):
    music_list = ['(노래를 선택하세요)','비스트 - Fiction : ★★★★★', '프롬 - 달의 뒤편으로 와요 : ★★★☆☆', "박효신 - It's You : ★★★★★", '레드벨벳 - 장미꽃 향기는 바람에 날리고 : ★★★★★', '천둥 - Good : ★★★☆☆', '임창정 - 그렇게 당해놓고 : ★★★☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '스윗소로우 - 별 일 아니에요 (연애의 발견 OST) : ★★★☆☆', 'NCT 127 - Switch : ★★★☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=whlVRDTobhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=hLiTZkvm8kY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=oYQHPSNlo5M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/GELnbRfJv3c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow121(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '지훈 - 너만 생각나 : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow122(Game):
    music_list = ['(노래를 선택하세요)','딕펑스 - 니가보여 : ★☆☆☆☆', '아이유 - 무릎 : ★★★★★', '참깨와 솜사탕 - 키스미 : ★★★☆☆', '샤이니 - Hold You : ★☆☆☆☆', '세븐틴 - 이 놈의 인기 : ★☆☆☆☆', 'B1A4 - Chu Chu Chu : ★☆☆☆☆', '한희정 - 러브레터 : ★★★☆☆', '보아 - Only One : ★☆☆☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '악뮤 - 다리꼬지마 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=4BhRyfa18cI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/SfeaTW4bcAw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/xHAoLgkbETY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=H5hJreMo_f8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=F6CkLk_ioRk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=BIhIbV3Qa8k')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/nnPY7l1LrMQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow123(Game):
    music_list = ['(노래를 선택하세요)','라디(Ra.D) - Lovesome : ★★★★★', '4MINUTE - Sweet Suga Honey! : ★☆☆☆☆', '시스타 - Give It To Me (Reno Remix) : ★★★★★', '방탄소년단 - Intro: Skool Luv Affair : ★☆☆☆☆', '멜로디데이 - Lake Wave (주군의 태양 OST) : ★☆☆☆☆', 'DEAN - And You? (Outro) : ★☆☆☆☆', 'f(x) - MILK : ★★★☆☆', '비스트 - 예이 : ★★★★★', '에일리 - 노래가 늘었어 : ★☆☆☆☆', '2NE1 - 안녕 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=XGD_YHFd2DI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=hUIPuAWwhFs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=QR8zSrx9tiQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=37167fMEw5c')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/w-rMc-AiNig')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=zic408dm4tc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/8uL-tSyMkyw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=K9VO1Iutggw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow124(Game):
    music_list = ['(노래를 선택하세요)','세븐틴 - 이 놈의 인기 : ★☆☆☆☆', '태양 - 기도 (feat. Teddy) : ★★★★★', '요조 - 뒹굴뒹굴 : ★★★★★', '정은지 - 하늘바라기 : ★☆☆☆☆', '딕펑스 - 니가보여 : ★☆☆☆☆', '샤이니 - Hold You : ★☆☆☆☆', '휘성 - Night and Day : ★☆☆☆☆', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '스윗소로우 - 별 일 아니에요 (연애의 발견 OST) : ★★★☆☆', '에일리 - 노래가 늘었어 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=F6CkLk_ioRk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/vWKrcboMteo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=7r8lcIuFBRM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Oe6z4yyja1w')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=4BhRyfa18cI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=H5hJreMo_f8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/GELnbRfJv3c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=S122aFkcOiw')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow125(Game):
    music_list = ['(노래를 선택하세요)','슈퍼주니어 - SUPERMAN : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '천둥 - Good : ★★★☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', "박효신 - It's You : ★★★★★", '잠비나이 - Connection : ★★★★★', '연애말고 결혼 OST - Love Knots : ★★★★★', 'f(x) - Lollipop : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow126(Game):
    music_list = ['(노래를 선택하세요)','N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '잠비나이 - Connection : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '디아 - 날 위한 이별 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow127(Game):
    music_list = ['(노래를 선택하세요)','인피니트 - 내꺼하자 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '잠비나이 - Connection : ★★★★★', '에일리 - 여인의 향기 : ★★★★★', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '보아 - One Dream : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '엠블랙 - Y : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=08sUMoBWBoY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/gyCss-xlMNA')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow128(Game):
    music_list = ['(노래를 선택하세요)','슈퍼주니어 - SUPERMAN : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '천둥 - Good : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', '4MINUTE - 팜므파탈 : ★★★☆☆', '시스타 - One More Day : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow129(Game):
    music_list = ['(노래를 선택하세요)','이지수 - 너야 : ★☆☆☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '인피니트 - Follow Me : ★★★★★', '동방신기 - Humanoids : ★★★☆☆', "박효신 - It's You : ★★★★★", '인피니트 - 내꺼하자 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '가인 - 피어나 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=42z1_1QteCg')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow130(Game):
    music_list = ['(노래를 선택하세요)','포맨 - 살다가 한번쯤 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', "박효신 - It's You : ★★★★★", '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '신용재 - 평범한 사랑 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow131(Game):
    music_list = ['(노래를 선택하세요)','인피니트 - 내꺼하자 : ★★★★★', 'NCT 127 - Switch : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '신용재 - 평범한 사랑 : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '샤이니 - Runaway : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆', '규현 - Eternal Sunshine : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/3T7BH-7LiqM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow132(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", '안혜은 - 그녀를 찾지마 : ★☆☆☆☆', '윤도현 - 요즘 내 모습 : ★☆☆☆☆', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '김종국 - 눈물자국 : ★☆☆☆☆', '빅스 - 사슬 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=BUIhCU0IaUA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/M9jYuBrX0eUU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/0zMYllAzwM0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow133(Game):
    music_list = ['(노래를 선택하세요)','Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '이지수 - 너야 : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '보아 - Only One : ★☆☆☆☆', '인피니트 - 내꺼하자 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '인피니트 - Follow Me : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow134(Game):
    music_list = ['(노래를 선택하세요)','윤미래 - Who : ★☆☆☆☆', '미(MIIII) - Not-Boyfriend : ★☆☆☆☆', '엠블랙 - Again : ★★★★★', '어쿠루브 - 그날 : ★☆☆☆☆', '뉴이스트 - 나의 천국 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '2NE1 - 안녕 : ★★★★★', '인피니트 - 내꺼하자 : ★★★★★', '한희정 - 러브레터 : ★★★☆☆', '여자친구 - 나침반 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=0U91paqy_TQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Zo5WP7kpe04')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/0GotOSuAO3U')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/tgigW1AnV0E')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=EV0y8HZW8Qs')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow135(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '잠비나이 - Connection : ★★★★★', '인피니트 - Follow Me : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆', '인피니트 - 내꺼하자 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=YnubLDYNNfQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow136(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '방탄소년단 - 고엽 : ★☆☆☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '유준상 - Love & Hate : ★★★★★', '린 - 이별주 : ★★★★★', '비투비 - 자리비움 : ★☆☆☆☆', 'f(x) - Lollipop : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=G3HHGDsrWR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/18jtm9s1J20')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow137(Game):
    music_list = ['(노래를 선택하세요)','f(x) - Lollipop : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '지코 - 날 : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '동방신기 - 아테나 : ★★★★★', 'YoungAh - 이별통보 : ★★★★★', '셰인 - Be My Love : ★★★☆☆', "The K2 OST - Anna's Appassionata : ★☆☆☆☆", '오빠친구동생 - 소보루빵 : ★★★★★', '보아 - One Dream : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/5bBh8fPirDk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/3QbUsUUNMwg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=CIPU4oHcM7o')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=aI9j9XcUGM8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow138(Game):
    music_list = ['(노래를 선택하세요)','천둥 - Good : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '비투비 - Killing Me : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆', '샤이니 - Your Number : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', '시스타 - One More Day : ★★★★★', 'f(x) - Lollipop : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=pL6G2PUOmwQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow139(Game):
    music_list = ['(노래를 선택하세요)','안현정 - 그대와 나 : ★★★★★', '여은 - 사랑아 나의 사랑아 : ★★★☆☆', '가인 - 피어나 : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '에일리 - 이제는 안녕 : ★★★★★', '비투비 - Killing Me : ★★★★★', '에이핑크 - 몰라요 : ★★★★★', 'f(x) - Lollipop : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '방탄소년단 - 고엽 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/eQJEGWQx_Lk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=pL6G2PUOmwQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/qTI0TJUGDts')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow140(Game):
    music_list = ['(노래를 선택하세요)',"박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '잠비나이 - Connection : ★★★★★', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', 'f(x) - Lollipop : ★★★★★', '지나유 - 처음사랑 : ★★★★★', '박효신 - 야생화 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/ujqVQBgDttc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow141(Game):
    music_list = ['(노래를 선택하세요)','보아 - Home : ★☆☆☆☆', 'f(x) - Lollipop : ★★★★★', '에이핑크 - 몰라요 : ★★★★★', '안현정 - 그대와 나 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', 'NCT 127 - Switch : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '시크릿 - POISON : ★☆☆☆☆', '천둥 - Good : ★★★☆☆', '참깨와 솜사탕 - 키스미 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/igTvMcvm35s')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/qTI0TJUGDts')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/TP56DuUpKBE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/xHAoLgkbETY')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow142(Game):
    music_list = ['(노래를 선택하세요)','디아 - 날 위한 이별 : ★★★★★', "박효신 - It's You : ★★★★★", '악뮤 - 다리꼬지마 : ★★★★★', '슬리피 - 기분탓 : ★☆☆☆☆', '에일리 - 이제는 안녕 : ★★★★★', '인피니트 - 붙박이 별 : ★★★★★', '오빠친구동생 - 소보루빵 : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆', '레드벨벳 - Huff n Puff : ★☆☆☆☆', 'f(x) - Lollipop : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/nnPY7l1LrMQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=GNJrZOWa_E0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=9eINuufm6TY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow143(Game):
    music_list = ['(노래를 선택하세요)','보아 - Only One : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '코코소리 - 다크서클 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', 'Beta89 - 청춘아 : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', "박효신 - It's You : ★★★★★", 'f(x) - Lollipop : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=eM8A0q8GQrc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=veaz-t0e2Fg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow144(Game):
    music_list = ['(노래를 선택하세요)','유성은 - 500일의 Summer : ★☆☆☆☆', '레인보우 유아동요 - 숲 속의 음악가 : ★☆☆☆☆', 'f(x) - MILK : ★★★☆☆', 'HUS - Space Loves Disco : ★★★★★', 'f(x) - Lollipop : ★★★★★', '효린 - 미치게 만들어 : ★★★★★', '백지영 - 사랑아 또 사랑아 : ★☆☆☆☆', '2NE1 - 안녕 : ★★★★★', '악동뮤지션 - 외국인의 고백 : ★★★☆☆', 'FTISLAND - 새들처럼 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=S9GYqowJ9oM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xl5an64ksKQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/8uL-tSyMkyw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=1xo0Ah5mGcA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=bztNjL76goE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/wQZkM2ELDXA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=_lip7tyMQmQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=JWV_VuWn_n8')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow145(Game):
    music_list = ['(노래를 선택하세요)','Flower - 사랑은 알아도... : ★☆☆☆☆', '디아 - 날 위한 이별 : ★★★★★', '이지수 - 너야 : ★☆☆☆☆', '샤이니 - Your Number : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '천둥 - Good : ★★★☆☆', 'f(x) - Lollipop : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '휘성 - Night and Day : ★☆☆☆☆', '인피니트 - 붙박이 별 : ★★★★★']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=bcYxNusTPrw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow146(Game):
    music_list = ['(노래를 선택하세요)','더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', '방탄소년단 - 고엽 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', "박효신 - It's You : ★★★★★", '봄바람 소년 - Only One : ★★★☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', '보아 - One Dream : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow147(Game):
    music_list = ['(노래를 선택하세요)','에이핑크 - Secret Garden : ★☆☆☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', '시스타 - One More Day : ★★★★★', "비스트 - I'm sorry : ★☆☆☆☆", '샤이니 - Wowowow : ★☆☆☆☆', '샤이니 - One : ★★★★★', '연애말고 결혼 OST - Love Knots : ★★★★★', '잔나비 - Goodnight (Intro) : ★★★★★', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow148(Game):
    music_list = ['(노래를 선택하세요)','정동하 - Mystery (주군의 태양 OST) : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', "박효신 - It's You : ★★★★★", '포맨 - 살다가 한번쯤 : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow149(Game):
    music_list = ['(노래를 선택하세요)','오빠친구동생 - 소보루빵 : ★★★★★', '애프터스쿨 - 너 때문에 : ★★★★★', '박효신 - 야생화 : ★★★★★', "박효신 - It's You : ★★★★★", 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '스트레이 - Tonight : ★★★☆☆']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Dr_6ktsvnHU')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow150(Game):
    music_list = ['(노래를 선택하세요)','Flower - 사랑은 알아도... : ★☆☆☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', '에일리 - 이제는 안녕 : ★★★★★', '김장훈 - 어머니는 내 마음을 아세요 : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '유준상 - Love & Hate : ★★★★★', 'NCT 127 - Switch : ★★★☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=LsQKeNhdda8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=G3HHGDsrWR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow151(Game):
    music_list = ['(노래를 선택하세요)','디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '빅스 - 사슬 : ★☆☆☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', '지훈 - 너만 생각나 : ★★★★★', '지나유 - 처음사랑 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', 'N(엔) (VIXX) X 여은 (MelodyDay) - 니가 없는 난 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=G0wjfcufRDk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=-oAMQNxxM0k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=FMIqLQR0CYI')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow152(Game):
    music_list = ['(노래를 선택하세요)',"비스트 - I'm sorry : ★☆☆☆☆", '애프터스쿨 - 너 때문에 : ★★★★★', 'f(x) - All Mine : ★★★★★', '에이핑크 - Secret Garden : ★☆☆☆☆', '비투비 블루 - 내 곁에 서 있어줘 : ★★★★★', '보아 - Only One : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '잔나비 - Goodnight (Intro) : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '샤이니 - One : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=bLALIv5C7Q8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow153(Game):
    music_list = ['(노래를 선택하세요)','애프터스쿨 - 너 때문에 : ★★★★★', '2NE1 - 안녕 : ★★★★★', 'f(x) - Beautiful Goodbye : ★☆☆☆☆', '제이스 - 라디오 스타 : ★★★☆☆', '타코 & 제이형 - 어떡하죠 : ★★★☆☆', '크래용팝 - 1, 2, 3, 4 : ★★★★★', '시스타 - 니까짓게 : ★★★★★', '최가람 - Broken Heart : ★☆☆☆☆', '비 - 30 SEXY (East4a deeptech mix) : ★★★☆☆', '지놉 - 여기봐요 : ★★★☆☆']
    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=UgO8wlKgdOc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=_mlER1d944U')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/-jxLz7uQ3Uw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=7M47xbruU_M')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=tf0pYYi5WJ0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ZCLWXYCmeUcc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=2ehqBe0SYlo')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow154(Game):
    music_list = ['(노래를 선택하세요)','봄바람 소년 - Only One : ★★★☆☆', '애프터스쿨 - 너 때문에 : ★★★★★', '인피니트 - Follow Me : ★★★★★', '디아 - 날 위한 이별 : ★★★★★', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '슈퍼주니어 - SUPERMAN : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', "박효신 - It's You : ★★★★★", '휘성 - Night and Day : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=cllEoGTbPIM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow155(Game):
    music_list = ['(노래를 선택하세요)','틴탑 - Date : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '시스타 - One More Day : ★★★★★', 'K.Will - 눈물이 뚝뚝 : ★☆☆☆☆', '셰인 - Be My Love : ★★★☆☆', '블루베어스 & 택연 - 오늘 같은 밤 : ★★★★★', '윤도현 - 사랑했나봐 : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '창민 & 다희 - 한 사람만 보여요 (최고다 이순신 OST) : ★★★★★', '보아 - One Dream : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=K3esd7tIvPU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=DIjGzZgu_yY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=uxhVy02aTqA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=KeMbLY7ztDw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/xl46idovwQM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow156(Game):
    music_list = ['(노래를 선택하세요)','에일리 - 이제는 안녕 : ★★★★★', '여은 - 사랑아 나의 사랑아 : ★★★☆☆', '샤이니 - Runaway : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆', '보아 - One Dream : ★☆☆☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', '지나 - 싫어 : ★☆☆☆☆', '방탄소년단 - 고엽 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/eQJEGWQx_Lk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow157(Game):
    music_list = ['(노래를 선택하세요)','개리 - 둥둥 : ★☆☆☆☆', '최철호 - Der Rosenkavalier : ★★★★★', '보아 - One Dream : ★☆☆☆☆', '지나 - 싫어 : ★☆☆☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '샤이니 - Runaway : ★★★★★', "박효신 - It's You : ★★★★★", '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', '박효신 - 야생화 : ★★★★★', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass


        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=GYkOUX0fDP8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=StZqbmSHJMY')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/n2Ux_MX7qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow158(Game):
    music_list = ['(노래를 선택하세요)','보아 - One Dream : ★☆☆☆☆', '산들(B1A4) - 짝사랑 : ★★★☆☆', '스윙스 - a real lady : ★☆☆☆☆', '박재범 - Forever : ★★★★★', '샤이니 - 너의 노래가 되어 : ★★★★★', '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆', '지나 - 싫어 : ★☆☆☆☆', 'We are the night - 흐려도 좋아 : ★☆☆☆☆', '임창정 - 그렇게 당해놓고 (feat.마부스 OF 일렉트로보이즈) (inst) : ★★★☆☆', 'NCT 127 - Switch : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/osYmpohGBS8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=8H2OTYIHJvg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=EMj7hPy4wJ8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=5mhDiHyFE3g')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=XNRo2MEMALQ')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow159(Game):
    music_list = ['(노래를 선택하세요)','인피니트 - 붙박이 별 : ★★★★★', '샤이니 - Your Number : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '봄바람 소년 - Only One : ★★★☆☆', 'Flower - 사랑은 알아도... : ★☆☆☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆', '보아 - One Dream : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=DD5ZGsP3VsM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow160(Game):
    music_list = ['(노래를 선택하세요)',
                  '보아 - Only One : ★☆☆☆☆', '유미 - Last one (주군의 태양 OST) : ★★★☆☆', '슈퍼주니어 - Let’s Dance : ★★★★★', '알레그로 - 우리가 스쳐온 서울 밤하늘엔 : ★★★☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '몬스타엑스 - 히어로 : ★★★★★', '에일리 - Live or Die : ★☆☆☆☆', '악뮤 - 다리꼬지마 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '보아 - One Dream : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/XEk5Nrd3-Zs')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=I1-q8mrnpDU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/0LvBVFnX1Vk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=jzYU7nCNR4c')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=w6yUYGd5M3M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/nnPY7l1LrMQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow161(Game):
    music_list = ['(노래를 선택하세요)',
                  '제이켠 - 나쁜 X : ★★★☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '거미 - 너를 사랑해 : ★★★★★', 'AZIATIX - Lights : ★☆☆☆☆', '비투비 - 두 번째 고백 : ★☆☆☆☆', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '에이핑크 - 하늘 높이 : ★★★★★', '2NE1 - 안녕 : ★★★★★', '보아 - One Dream : ★☆☆☆☆', '릴보이 - 돈돈돈 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Pr4JowItzOM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=OzfpeXFFe2I')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=hTUr660PMlU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=rxl9cIbBHrc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=TnIXDeM7jAw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=6rbt3DjYoOg')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow162(Game):
    music_list = ['(노래를 선택하세요)',
                  '보아 - One Dream : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '에이핑크 - BUBIBU : ★★★☆☆', '엠블랙 - Y : ★★★★★', '지나 - 싫어 : ★☆☆☆☆', '시스타 - Sunshine : ★★★★★', '주영 - 들리나요 : ★★★★★', '앤츠 - 예쁜 너니까 : ★☆☆☆☆', '휘성 - Night and Day : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=EOAxIz7VQU8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=eNcn4vA-9sE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/gyCss-xlMNA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=5tK8627wCtw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=2LW4Ih_UZMw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=8shnOlfd1wY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow163(Game):
    music_list = ['(노래를 선택하세요)',
                  '가인 - 피어나 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '김남주 & 육성재 - 사진 : ★★★☆☆', '뉴이스트 - 나의 천국 : ★★★★★', '한희정 - 러브레터 : ★★★☆☆', '참깨와 솜사탕 - 키스미 : ★★★☆☆', '이홍기 - Jump (뜨거운 안녕 OST) : ★★★★★', '시스타 - One More Day : ★★★★★', '클래지콰이 프로젝트 - Android : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/mBEJ18AV8gE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/xHAoLgkbETY')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/JJlFuj7WA9Q')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/OmfR14eBQQo')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow164(Game):
    music_list = ['(노래를 선택하세요)',
                  '시스타 - One More Day : ★★★★★', 'Beta89 - 청춘아 : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '형돈이와 대준이 - 안좋을때 들으면 더 안좋은 노래 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', 'EXO - MY ANSWER : ★★★★★', '코코소리 - 다크서클 : ★★★★★', '요조 - 바나나파티 : ★★★★★', '샤이니 - Last Christmas : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=veaz-t0e2Fg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/KJSXolyj4DM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=KC_nbsVUFtM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=eM8A0q8GQrc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=V5PLNMn3Wfg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow165(Game):
    music_list = ['(노래를 선택하세요)',
                  '에일리 - 이제는 안녕 : ★★★★★', '에이핑크 - 몰라요 : ★★★★★', '안현정 - 그대와 나 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '시크릿 - POISON : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', 'NCT 127 - Switch : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '샤이니 - Evil : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/qTI0TJUGDts')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/TP56DuUpKBE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/t81DgI79p8A')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow166(Game):
    music_list = ['(노래를 선택하세요)',
                  '에이핑크 - Secret Garden : ★☆☆☆☆', '비스트 - Fiction : ★★★★★', '모던다락방 - All I Want Is 바라만봐도 : ★★★☆☆',
                  '디아 - 날 위한 이별 : ★★★★★', 'Flower - 사랑은 알아도... : ★☆☆☆☆', 'DICKPUNKS - 지금을 잃고 싶지 않아 : ★★★★★',
                  '이지수 - 너야 : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', '빅스 - 사슬 : ★☆☆☆☆', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=whlVRDTobhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/-tDld3F9xAA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=WmLGy3ebLnM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow167(Game):
    music_list = ['(노래를 선택하세요)',
                  '샤이니 - One : ★★★★★', '시스타 - One More Day : ★★★★★', "비스트 - I'm sorry : ★☆☆☆☆", '연애말고 결혼 OST - Love Knots : ★★★★★', '샤이니 - Wowowow : ★☆☆☆☆', '에이핑크 - Secret Garden : ★☆☆☆☆', '비스트 - Fiction : ★★★★★', 'K.Will - 눈물이 뚝뚝 : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', '보아 - Only One : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=grPy2KJYZ9M')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=whlVRDTobhs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=DIjGzZgu_yY')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow168(Game):
    music_list = ['(노래를 선택하세요)',
                  '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '딕펑스 - 들리지 않겠죠 : ★☆☆☆☆', '안현정 - 그대와 나 : ★★★★★', '뉴이스트 - 나의 천국 : ★★★★★',
                  '엠블랙 - Y : ★★★★★', 'B1A4 - 몇 번을 : ★★★★★', '박재범 - Evolution (feat. Gray) : ★★★★★', '더 라임 그리워서 : ★★★☆☆',
                  '2NE1 - 안녕 : ★★★★★', '시스타 - One More Day : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=gJzAmWLrJFU')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/gyCss-xlMNA')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/FmuOH_0UKVI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=lYPMh88RTLc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=fyaYx8M4DQk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow169(Game):
    music_list = ['(노래를 선택하세요)',
                  '휘성 - Night and Day : ★☆☆☆☆', '시스타 - One More Day : ★★★★★', '샤이니 - One : ★★★★★', "비스트 - I'm sorry : ★☆☆☆☆", '에이핑크 - Secret Garden : ★☆☆☆☆', '잔나비 - Goodnight (Intro) : ★★★★★', 'f(x) - All Mine : ★★★★★', '천둥 - Good : ★★★☆☆', '연애말고 결혼 OST - Love Knots : ★★★★★', "박효신 - It's You : ★★★★★"]

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=zdoB2TPqWxs')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=et9u7hPESCo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=7d_cdW-k6pE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=f4_3dWqu6kM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow170(Game):
    music_list = ['(노래를 선택하세요)',
                  '박효신 - 야생화 : ★★★★★', '가인 - 피어나 : ★★★★★', 'B1A4 - 둘만 있으면 : ★☆☆☆☆', 'Second Moon - 다음 이시간에 : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', 'NS 윤지 - 니가 뭘 알아 : ★☆☆☆☆', '포맨 - 살다가 한번쯤 : ★★★★★', '클래지콰이 프로젝트 - Madly : ★★★☆☆', '지나 - 싫어 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=7A_tJZblEP4')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=e38Ijf-MMYI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/K6fzVQ7KKXM')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=g9iUDKeokIw')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/Grv0k1dXz3U')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow171(Game):
    music_list = ['(노래를 선택하세요)',
                  '뉴클리어스 - 깃길 : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '크래용팝 - 1, 2, 3, 4 : ★★★★★', '샤이니 - Evil : ★★★★★', '보아 - Home : ★☆☆☆☆', 'NCT 127 - Switch : ★★★☆☆', '김남주 & 육성재 - 사진 : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '태양 - 기도 (feat. Teddy) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=lSBbLQXAUZs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t81DgI79p8A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/igTvMcvm35s')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/mBEJ18AV8gE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/vWKrcboMteo')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow172(Game):
    music_list = ['(노래를 선택하세요)',
                  '크래용팝 - 1, 2, 3, 4 : ★★★★★', '방탄소년단 - 고엽 : ★☆☆☆☆', '샤이니 - Evil : ★★★★★', '비투비 - 자리비움 : ★☆☆☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '빅스 - 사슬 : ★☆☆☆☆', '에이프릴 - 스노우맨 : ★★★☆☆', '홍대광 - 아닌가요 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/Q8QDrGxGmy8')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/t81DgI79p8A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/18jtm9s1J20')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=RYQS3YmhO_8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=BETXd_AUeAg')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow173(Game):
    music_list = ['(노래를 선택하세요)',
                  '아이유 - 느리게 하는 일 : ★★★★★', '한희정 - 러브레터 : ★★★☆☆', '뉴이스트 - 나의 천국 : ★★★★★', '안현정 - 그대와 나 : ★★★★★', '황치열, 리싸 - 이 밤의 끝을 잡고 : ★☆☆☆☆', '이유성 - Butter Flying : ★★★☆☆', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '가인 - 피어나 : ★★★★★', '유미 - Last one (주군의 태양 OST) : ★★★☆☆', '보아 - Only One : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/S_8B6x89Uoo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/23oVRoiu_dk')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=HVqxQThIGgk')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/XEk5Nrd3-Zs')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow174(Game):
    music_list = ['(노래를 선택하세요)',
                  '안현정 - 그대와 나 : ★★★★★', '뉴이스트 - 나의 천국 : ★★★★★', 'B1A4 - 몇 번을 : ★★★★★', '2NE1 - 안녕 : ★★★★★', '수지 - Ring My Bell : ★★★★★', '멜로디데이 - Lake Wave (주군의 태양 OST) : ★☆☆☆☆', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆', '주헌, 형원, I.M - 인터스텔라 (Interstellar) : ★★★★★', '더 케이투 OST - The K2 Main Theme : ★★★☆☆', '가인 - 피어나 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/FmuOH_0UKVI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=HVQ2WKhByMU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/w-rMc-AiNig')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/dBUWcM2TBpM')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/zOE7y0iCmG8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow175(Game):
    music_list = ['(노래를 선택하세요)',
                  "박효신 - It's You : ★★★★★", '천둥 - Good : ★★★☆☆', '가인 - 피어나 : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆',
                  'Flower - 사랑은 알아도... : ★☆☆☆☆', '이지수 - 너야 : ★☆☆☆☆', '정동하 - Mystery (주군의 태양 OST) : ★★★★★',
                  '디아 - 날 위한 이별 : ★★★★★', '4MINUTE - 팜므파탈 : ★★★☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=kFLNAB5-qsQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=r39Sufgf7Pc')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow176(Game):
    music_list = ['(노래를 선택하세요)',
                  'NCT 127 - Switch : ★★★☆☆', '박효신 - 야생화 : ★★★★★', '태양 - 기도 (feat. Teddy) : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '샤이니 - Evil : ★★★★★', '김남주 & 육성재 - 사진 : ★★★☆☆', '안현정 - 그대와 나 : ★★★★★', '한희정 - 러브레터 : ★★★☆☆', '뉴클리어스 - 깃길 : ★☆☆☆☆', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/vWKrcboMteo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/t81DgI79p8A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/mBEJ18AV8gE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/4eRNIS6zMeo')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=lSBbLQXAUZs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow177(Game):
    music_list = ['(노래를 선택하세요)',
                  '빅스 - 사슬 : ★☆☆☆☆', '슈퍼주니어 - SUPERMAN : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', '샤이니 - Last Christmas : ★★★☆☆', '박효신 - 야생화 : ★★★★★', '코코소리 - 다크서클 : ★★★★★', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', 'Lucia(심규선) - 녹여줘 : ★★★☆☆', "박효신 - It's You : ★★★★★", 'Beta89 - 청춘아 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Fdw1DkgWZC8')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=eM8A0q8GQrc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/cJ5ts0qjCaI')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=veaz-t0e2Fg')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow178(Game):
    music_list = ['(노래를 선택하세요)',
                  '보아 - Only One : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '포맨 - 살다가 한번쯤 : ★★★★★', "박효신 - It's You : ★★★★★", '슈퍼주니어 - SUPERMAN : ★★★★★', '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆', 'Lucia(심규선) - 녹여줘 : ★★★☆☆', 'Beta89 - 청춘아 : ★☆☆☆☆', '바스코 - Whoa Ha ! : ★★★☆☆', '코코소리 - 다크서클 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/eV0RwwijHGw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/IdFeKj798hU')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/cJ5ts0qjCaI')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=veaz-t0e2Fg')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=JpL691-pxuM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=eM8A0q8GQrc')
            self.btn_start.clicked.connect(self.game_start_hard)

class GameWindow179(Game):
    music_list = ['(노래를 선택하세요)',
                  '박효신 - 야생화 : ★★★★★', '니엘 - 심쿵 : ★★★★★', '에이핑크 - 하늘 높이 : ★★★★★', '시크릿 - Madonna : ★☆☆☆☆', '태민 - One By One : ★★★☆☆', '송지은 - 예쁜 나이 25살 : ★★★☆☆', '디아 - 날 위한 이별 : ★★★★★', '민연재 - 비행소녀 : ★★★★★', '2NE1 - 안녕 : ★★★★★', 'We are the night - 흐려도 좋아 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=1T3gndIBNbc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TnIXDeM7jAw')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/n2fM1yHE_Nc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=3wQWOKQX8NE')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=dMEZMHpWTSM')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=TCHXoRYwjVQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=XNRo2MEMALQ')
            self.btn_start.clicked.connect(self.game_start_easy)


class GameWindow180(Game):
    music_list = ['(노래를 선택하세요)',
                  '김예림 - 행복한 나를 : ★★★★★', 'DEAN - Bonnie & Clyde : ★☆☆☆☆', 'f(x) - Stand Up : ★★★☆☆', 'B.A.P - 0 (Zero) : ★☆☆☆☆', 'B.A.P - Fermata : ★★★★★', '니엘 - 아포카토 : ★☆☆☆☆', '박효신 - 야생화 : ★★★★★', '휘성 - Night and Day : ★☆☆☆☆', '셰인 - Be My Love : ★★★☆☆', '4minute - 이름이 뭐예요? : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Plc5V1ANWtE')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=QKcJa8dKg_A')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Px_TaS30Cb0')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=W4EHYKFQvns')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=dGERGbN7VYg')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=QgU5CVZQoEs')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=ZtcM3KhgF-s')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=nD5ferh1_eE')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow181(Game):
    music_list = ['(노래를 선택하세요)',
                  'NCT 127 - Switch : ★★★☆☆', '빅스 - 사슬 : ★☆☆☆☆', '시크릿 - POISON : ★☆☆☆☆', '악뮤 - 다리꼬지마 : ★★★★★', 'B1A4 - 몇 번을 : ★★★★★', '어반자카파 - Rainbow Ride (Prelude) : ★★★★★', '보경, 셰인 - Summer Love : ★★★☆☆', '방탄소년단 - Intro: Never Mind : ★☆☆☆☆', '샤이니 - Evil : ★★★★★', '이오공감 - 한 사람을 위한 마음 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass

        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/TP56DuUpKBE')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/nnPY7l1LrMQ')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/FmuOH_0UKVI')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/L9GPT1opU44')
            self.btn_start.clicked.connect(self.game_start_norm)

        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)

        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/t81DgI79p8A')
            self.btn_start.clicked.connect(self.game_start_hard)

        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/DokABcA8Iy8')
            self.btn_start.clicked.connect(self.game_start_norm)


class GameWindow182(Game):
    music_list = ['(노래를 선택하세요)',
                  '샤이니 - Your Number : ★☆☆☆☆',
                  '임창정 - 그렇게 당해놓고 (feat.마부스 OF 일렉트로보이즈) (inst) : ★★★☆☆',
                  '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆',
                  '태양 - 기도 (feat. Teddy) : ★★★★★',
                  '황치열, 리싸 - 이 밤의 끝을 잡고 : ★☆☆☆☆',
                  '에일리 - 이제는 안녕 : ★★★★★',
                  '보아 - Only One (Instrumental) : ★☆☆☆☆',
                  '김남주 & 육성재 - 사진 : ★★★☆☆',
                  '방탄소년단 - Intro: Never Mind : ★☆☆☆☆',
                  'NCT 127 - Switch : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/t1gRKVgghKY')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/vWKrcboMteo')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/23oVRoiu_dk')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/yvU8KRQRfbQ')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/mBEJ18AV8gE')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)

class GameWindow183(Game):
    music_list = ['(노래를 선택하세요)',
                  '김현우 - Love Blowing : ★★★☆☆',
                  'NCT 127 - Switch : ★★★☆☆',
                  '한희정 - 입맞춤, 입술의 춤 : ★★★★★',
                  '2NE1 - Goodbye : ★★★★★',
                  '오준성 - The Chorus Of Knights : ★☆☆☆☆',
                  '악동뮤지션 - 사람들이 움직이는 게 : ★★★★★',
                  '인피니트 - 붙박이 별 : ★★★★★',
                  '딕펑스 - 요즘 젊은 것들 : ★★★☆☆',
                  '백지영 - 사랑아 또 사랑아 : ★☆☆☆☆',
                  '이지수 - 너야 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/pdLtYmWDoq8')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=gtAiZ8ONgpU')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=_XDUam4-pis')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=MWROa7V4FqA')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/nwHnJT-AXR0')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/wQZkM2ELDXA')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)

class GameWindow184(Game):
    music_list = ['(노래를 선택하세요)',
                  '휘성 - Night and Day : ★☆☆☆☆',
                  '방탄소년단 - Intro: Never Mind : ★☆☆☆☆',
                  '딕펑스 - 요즘 젊은 것들 : ★★★☆☆',
                  '샤이니 - Your Number : ★☆☆☆☆',
                  '천둥 - Good : ★★★☆☆',
                  '황치열, 리싸 - 이 밤의 끝을 잡고 : ★☆☆☆☆',
                  '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆',
                  'NCT 127 - Switch : ★★★☆☆',
                  '어반자카파 - Rainbow Ride (Prelude) : ★★★★★',
                  '정동하 - Mystery (주군의 태양 OST) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/xq3NB3U0Ps8')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=X7eMeU7JiIA')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/23oVRoiu_dk')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=jAhJl87fEOQ')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/9JpxslQR-zc')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow185(Game):
    music_list = ['(노래를 선택하세요)',
                  '오빠친구동생 - 소보루빵 : ★★★★★',
                  '딕펑스 - 한강에서 놀아요 : ★★★☆☆',
                  '이지수 - 너야 : ★☆☆☆☆',
                  '스트레이 - Tonight : ★★★☆☆',
                  "박효신 - It's You : ★★★★★",
                  '디아 - 날 위한 이별 : ★★★★★',
                  '보아 - Only One (Instrumental) : ★☆☆☆☆',
                  'Flower - 사랑은 알아도... : ★☆☆☆☆',
                  '빅스 - 사슬 : ★☆☆☆☆',
                  '딕펑스 - 요즘 젊은 것들 : ★★★☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=TutGX4fTXMw')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/B3qAHL_dXXk')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=TBddTpXl-uA')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/Dr_6ktsvnHU')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=Q33ftKGy3vk')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=xc3iDjbYSG8')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/OwNJJf2yM04')
            self.btn_start.clicked.connect(self.game_start_norm)

class GameWindow186(Game):
    music_list = ['(노래를 선택하세요)',
                  '2NE1 - Goodbye : ★★★★★',
                  '멜로디데이 - Lake Wave (주군의 태양 OST) : ★☆☆☆☆',
                  '빅스 - 사슬 : ★☆☆☆☆',
                  '에이핑크 - Wanna Be : ★☆☆☆☆',
                  '주헌, 형원, I.M - 인터스텔라 (Interstellar) : ★★★★★',
                  '태양 - 기도 (feat. Teddy) : ★★★★★',
                  '종현 - 그래도 되지 않아? : ★★★★★',
                  '팀 - River Flows in You : ★★★☆☆',
                  '백지영 - 사랑아 또 사랑아 : ★☆☆☆☆',
                  '4minute - 안 줄래 : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[2]:
            self.music_thread('https://youtu.be/w-rMc-AiNig')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[3]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=YFLnr9CUfJQ')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/dBUWcM2TBpM')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/vWKrcboMteo')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=GDY0f2sb9yE')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/Xcc87nlXEnI')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/wQZkM2ELDXA')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=UAOghR-YRYQ')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow187(Game):
    music_list = ['(노래를 선택하세요)',
                  '더 콰이엇 - 진흙 속에서 피는 꽃 : ★☆☆☆☆',
                  '비하트 - 필요없어 : ★☆☆☆☆',
                  '비투비 - 자리비움 : ★☆☆☆☆',
                  '린 - 이별주 : ★★★★★',
                  '방탄소년단 - 고엽 : ★☆☆☆☆',
                  '박수진 & 일렉트로보이즈 - 떨려요 : ★★★☆☆',
                  '방탄소년단 - Intro: Never Mind : ★☆☆☆☆',
                  '휘성 - Night and Day : ★☆☆☆☆',
                  '정동하 - Mystery (주군의 태양 OST) : ★★★★★',
                  '빅스 - 사슬 : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=Gf-P9UvVWqw')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=3nmvvZtvXDc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/18jtm9s1J20')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/QGQqh_jCWwc')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/cljJCtXYvuI')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=7arTRoqY3QA')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[7]:
            self.music_thread('https://youtu.be/ugrXP_YT9j0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[9]:
            self.music_thread('https://youtu.be/WZ2rdYNbndc')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=pMkIfldadUc')
            self.btn_start.clicked.connect(self.game_start_easy)




class GameWindow188(Game):
    music_list = ['(노래를 선택하세요)',
                  '클래지콰이 프로젝트 - Android : ★★★☆☆',
                  '2NE1 - Goodbye : ★★★★★',
                  '셰인 - Be My Love : ★★★☆☆',
                  '에이핑크 - Wanna Be : ★☆☆☆☆',
                  '한희정 - 러브레터 : ★★★☆☆',
                  '뉴이스트 - 나의 천국 : ★★★★★',
                  '헨리(슈퍼주니어 M) - My Everything : ★★★★★',
                  '티어라이너 - Einfühlung : ★★★★★',
                  '보아 - Only One (Instrumental) : ★☆☆☆☆',
                  '성시경 - Winter Wonderland : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://youtu.be/OmfR14eBQQo')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/UmC0cfwSKks')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=YFLnr9CUfJQ')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/sCpFPdavYII')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[6]:
            self.music_thread('https://youtu.be/6390tjodZ5k')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=Mbm5PldbeWY')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=rqHEhhnWfqY')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://youtu.be/4y2j_Z0IuI0')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow189(Game):
    music_list = ['(노래를 선택하세요)',
                  '보아 - Only One (Instrumental) : ★☆☆☆☆',
                  "비스트 - I'm sorry : ★☆☆☆☆",
                  '일렉트로보이즈 - love (feat. 승희 from brave new girl group) : ★★★★★',
                  '인피니트 - Follow Me : ★★★★★',
                  '프롬 - 달의 뒤편으로 와요 : ★★★☆☆',
                  '휘성 - Night and Day : ★☆☆☆☆',
                  "박효신 - It's You : ★★★★★",
                  '연애말고 결혼 OST - Love Knots : ★★★★★',
                  'K.Will - 눈물이 뚝뚝 : ★☆☆☆☆',
                  '잔나비 - Goodnight (Intro) : ★★★★★']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=ty-88JATqxc')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=ZpRlIVImgnM')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/4bVF3W32oMc')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[4]:
            self.music_thread('https://youtu.be/mb1J6xz1ME0')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[5]:
            self.music_thread('https://www.youtube.com/watch?v=hLiTZkvm8kY')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=xXlS6-V5ec0')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[8]:
            self.music_thread('https://www.youtube.com/watch?v=lk5QWPq1K6E')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=DIjGzZgu_yY')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=1Xr5IhcE2pE')
            self.btn_start.clicked.connect(self.game_start_hard)


class GameWindow190(Game):
    music_list = ['(노래를 선택하세요)',
                  '2NE1 - Goodbye : ★★★★★',
                  '에이핑크 - 끌려 : ★☆☆☆☆',
                  '신용재 - 평범한 사랑 : ★★★☆☆',
                  '슈퍼주니어 - Oops!! : ★★★★★',
                  '유미 - Last one (주군의 태양 OST) : ★★★☆☆',
                  'LOCO - 높아 2 : ★★★★★',
                  '조권 & 니엘 & 지오 & 양요섭 & 우현 - 눈물나게 아름다운 : ★★★★★',
                  '기리보이, 매드클라운, 주영 - 0 (YOUNG) : ★★★★★',
                  '오준성 - Enjoy Party : ★☆☆☆☆',
                  '휘성 - Night and Day : ★☆☆☆☆']

    def __init__(self):
        super().__init__()
        Game.__init__(self)

    def music_play(self):
        item = self.music.currentText()

        if item == self.music_list[0]:
            pass
        elif item == self.music_list[1]:
            self.music_thread('https://www.youtube.com/watch?v=o3hMsjMkOB4')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[2]:
            self.music_thread('https://www.youtube.com/watch?v=IdBLtbfnlHM')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[3]:
            self.music_thread('https://youtu.be/7o2SvZhpp8c')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[4]:
            self.music_thread('https://www.youtube.com/watch?v=PFeIiLbOiK8')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[5]:
            self.music_thread('https://youtu.be/XEk5Nrd3-Zs')
            self.btn_start.clicked.connect(self.game_start_norm)
        elif item == self.music_list[6]:
            self.music_thread('https://www.youtube.com/watch?v=dVYLEvYsnDU')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[7]:
            self.music_thread('https://www.youtube.com/watch?v=fHw3CJp9ckk')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[8]:
            self.music_thread('https://youtu.be/FeDeDnwJlB0')
            self.btn_start.clicked.connect(self.game_start_hard)
        elif item == self.music_list[9]:
            self.music_thread('https://www.youtube.com/watch?v=JkRgGYEYERM')
            self.btn_start.clicked.connect(self.game_start_easy)
        elif item == self.music_list[10]:
            self.music_thread('https://www.youtube.com/watch?v=eV1KawA_5Q0')
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

    def box_layout(self):
        self.vbox.addWidget(self.label_1)
        self.vbox.addWidget(self.label_2)

        self.btn_go.setFont(QtGui.QFont('DOSMyungjo', 30))
        self.btn_go.setFixedSize(QtCore.QSize(150, 50))
        self.btn_go.setStyleSheet(
            'QPushButton {color: black; background-color: rgb(255, 190, 11); border-radius: 5px;}')

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
