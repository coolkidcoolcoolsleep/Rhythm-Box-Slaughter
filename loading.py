import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class LoadingGIF(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.window_loading = QtWidgets.QWidget()
        self.vbox_loading = QtWidgets.QVBoxLayout()
        self.loading = QtGui.QMovie('loading.gif')
        self.label_loading = QtWidgets.QLabel(self)
        self.label_loading.setMovie(self.loading)
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)

        self.loading_ui()

        timer = QtCore.QTimer()
        self.animation_start()
        timer.singleShot(3000, self.animation_stop)

    def loading_ui(self):
        # self.window_loading.setWindowTitle('Loading...')
        self.window_loading.setFixedSize(1280, 720)
        self.window_loading.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)

        self.vbox_loading.addWidget(self.label_loading)

        self.window_loading.setLayout(self.vbox_loading)
        self.window_loading.show()

    def animation_start(self):
        self.loading.start()

    def animation_stop(self):
        # self.loading.stop()
        self.window_loading.close()


def main():
    app = QtWidgets.QApplication([])
    load = LoadingGIF()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
