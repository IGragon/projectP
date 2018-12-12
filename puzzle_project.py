import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog)
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter, QColor
from PIL import Image
import time
import os
import math


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('puzzle.ui', self)
        self.setFixedSize(1080, 720)
        self.fname = ''
        self.image = ''
        self.frame_to_hight = False
        self.frame_to_width = False
        self.image_have_taken = False
        self.fixedPoints = dict()
        self.get_image()
        self.make_puzzle()
        self.createBtns()

    def paintEvent(self, event):
        if self.image_have_taken:
            qp = QPainter()
            qp.begin(self)
            self.draw_frame(qp)
            qp.end()

    def draw_frame(self, qp):
        if self.frame_to_width:
            x_i, y_i = self.image.size
            x1, y1 = 385, 45
            x2, y2 = 995, 45
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            y2 = (600 * y_i) // x_i
            qp.drawLine(x1, y1, x2, y2)

    def get_image(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/')[0]
        self.image = Image.open(self.fname)
        x, y = self.image.size
        if x > y:
            pixmap = QPixmap(self.fname).scaledToWidth(600)
            self.frame_to_width = True
        else:
            pixmap = QPixmap(self.fname).scaledToHeight(600)
            self.frame_to_hight = True
        self.labelForArt.setPixmap(pixmap)
        self.labelForArt.resize(self.labelForArt.sizeHint())
        self.image_have_taken = True

    def make_puzzle(self):
        os.system('mkdir data')
        step_x, step_y = self.image.size
        step_x = step_x // 6
        step_y = step_y // 6
        self.btn_size_x = step_x
        self.btn_size_y = step_y
        for i in range(6):
            for j in range(6):
                croped = self.image.crop([j * step_x, i * step_y, (j + 1) * step_x, (i + 1) * step_y])
                self.fixedPoints[str(i) + str(j)] = (j * step_x + 390, i * step_y + 50)
                name = 'image' + str(i + 1) + str(j + 1) + '.jpg'
                croped.save('data/' + name)
        self.set_image(step_x, step_y)

    def set_image(self, x, y):
        x_im, y_im = self.image.size
        if x > y:
            sub = y_im - y
            # сделать преобразования


    def createBtns(self):
        for _ in range(36):
            pass


def wait(sec):
    t = time.time()
    while time.time() - t < sec:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
