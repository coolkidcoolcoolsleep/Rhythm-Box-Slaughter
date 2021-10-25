import cv2
import cvlib as cv
import cvzone
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import threading
import sys
# from video_manager import Video_Manager


running = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.music_dialog = QtWidgets.QDialog()

    def run(self):
        global running
        cap = cv2.VideoCapture(0)
        width, height = 1330, 630

        if not cap.isOpened():
            print('카메라를 열 수 없습니다')
            exit()

        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)
                faces, _ = cv.detect_face(img)

                for face in faces:
                    x, y = face[0], face[1]
                    glasses = cv2.imread('sunglasses.png', -1)

                    try:
                        img = cvzone.overlayPNG(img, glasses, [x+50, y+50])

                    except:
                        pass

                h, w, c = img.shape
                q_img = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_img)
                label.setPixmap(pixmap)

            else:
                QtWidgets.QMessageBox.about(window, 'Error', '카메라를 불러올 수 없습니다')
                break

        cap.release()

    def player_1(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()

    def player_2(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()

    def select_music_window(self):
        self.music_dialog.setWindowTitle('select music')
        self.music_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.music_dialog.resize(300, 200)
        self.music_dialog.show()
        btn_music = QtWidgets.QPushButton('music', self.music_dialog)
        btn_music.clicked.connect(self.select_music)

    def select_music(self):
        music = QtWidgets.QComboBox(self)
        music.move(200, 400)
        music_list = [1, 2, 3, 4]
        for i in music_list:
            music.addItem(f'music{i}')
        music.showPopup()

    def close_event(self, event):
        close = QtWidgets.QMessageBox()
        close.setText('나가시겠습니까?')
        close.setWindowTitle('Exit')
        close.setWindowIcon(QtGui.QIcon('sunglasses.png'))
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()

        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def button(self):
        btn_player_1 = QtWidgets.QPushButton('1 Player')
        btn_player_1.setFixedSize(100, 20)

        btn_player_2 = QtWidgets.QPushButton('2 Player')
        btn_player_2.setFixedSize(100, 20)

        btn_stop = QtWidgets.QPushButton('Exit')
        btn_stop.setFixedSize(100, 20)

        music = QtWidgets.QComboBox(self)
        music.move(200, 400)
        music_list = [1, 2, 3, 4]
        for i in music_list:
            music.addItem(f'music{i}')

        vbox.addWidget(label)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_player_1)
        hbox.addWidget(btn_player_2)
        hbox.addWidget(music)
        hbox.addWidget(btn_stop)
        hbox.addStretch(1)

        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        btn_player_1.clicked.connect(self.player_1)
        btn_player_2.clicked.connect(self.player_2)
        btn_stop.clicked.connect(self.close_event)


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
