import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5 import uic
import time


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.f_go_to_place = False
        self.f = False
        uic.loadUi('test.ui', self)
        self.pushFollow.clicked.connect(self.follow)

    def follow(self):
        if not self.f:
            self.f = True
        else:
            self.f = False
        if self.f_go_to_place:
            self.pushFollow.move(120, 140)
            self.f = False
            self.f_go_to_place = False

    def mouseMoveEvent(self, event):
        if self.f:
            x, y = event.x(), event.y()
            x2, y2 = self.pushHere.x() + 25, self.pushHere.y() + 25
            self.pushFollow.move(x - 25, y - 25)
            x1, y1 = self.pushFollow.x() + 25, self.pushFollow.y() + 25
            if abs(x1 - x2) < 25 and abs(y1 - y2) < 25:
                self.pushFollow.move(x2 - 25, y2 - 25)
                self.f = False
                self.f_go_to_place = True
            print(x1, y1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
