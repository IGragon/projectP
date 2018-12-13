import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QPushButton)
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtCore import QSize
from PIL import Image
import time
import os
import random
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
        self.t_start = time.time()

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
            y2 = (600 * y_i) // x_i + 55
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            x2 = 385
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            x2, y2 = 385, 45
            qp.drawLine(x1, y1, x2, y2)
        elif self.frame_to_hight:
            x_i, y_i = self.image.size
            x1, y1 = 385, 45
            x2, y2 = 385, 655
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            x2 = (600 * x_i) // y_i + 395
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            y2 = 45
            qp.drawLine(x1, y1, x2, y2)
            x1, y1 = x2, y2
            x2, y2 = 385, 45
            qp.drawLine(x1, y1, x2, y2)
        if self.checkShowPicture.isChecked():
            self.labelForArt.setPixmap(self.pixmap)
            self.labelForArt.resize(self.labelForArt.sizeHint())
        else:
            pixmap = QPixmap('')
            self.labelForArt.setPixmap(pixmap)
            self.labelForArt.resize(self.labelForArt.sizeHint())

    def get_image(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:/')[0]
        self.image = Image.open(self.fname)
        x, y = self.image.size
        if x >= y:
            self.pixmap = QPixmap(self.fname).scaledToWidth(600)
            self.frame_to_width = True
        else:
            self.pixmap = QPixmap(self.fname).scaledToHeight(600)
            self.frame_to_hight = True
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
        self.createBtns(step_x, step_y)

    def set_image(self, x, y):
        x_im, y_im = self.image.size
        pix = self.image.load()
        if x > y:
            sub = y_im - y * 6
            new_im = Image.new('RGB', (x_im, y * 6), (0, 0, 0))
            new_pix = new_im.load()
            for i in range(x_im - 1):
                for j in range(y_im - sub):
                    new_pix[i, j] = pix[i, j]
            new_im.save('data/main_pic.jpg')
            self.image = Image.open('data/main_pic.jpg')
            self.pixmap = QPixmap(self.fname).scaledToWidth(600)
        elif y > x:
            sub = x_im - x * 6
            new_im = Image.new('RGB', (x * 6, y_im), (0, 0, 0))
            new_pix = new_im.load()
            for i in range(x_im - sub):
                for j in range(y_im - 1):
                    new_pix[i, j] = pix[i, j]
            new_im.save('data/main_pic.jpg')
            self.image = Image.open('data/main_pic.jpg')
            self.pixmap = QPixmap(self.fname).scaledToHeight(600)

    def createBtns(self, x, y):
        x_im, y_im = self.image.size
        if x > y:
            y = ((600 * y_im) // x_im) // 6
            x = 100
        if y > x:
            x = ((600 * x_im) // y_im) // 6
            y = 100
        self.buttons = []
        for i in range(6):
            part = []
            for j in range(6):
                btn = QPushButton('', self)
                btn.resize(x, y)
                btn.move(random.randint(0, 280 - x), random.randint(32, 720 - y))
                icon = QIcon('data/image' + str(i + 1) + str(j + 1))
                btn.setIcon(icon)
                btn.setIconSize(QSize(x, y))
                part.append(btn)
            self.buttons.append(part)


def wait(sec):
    t = time.time()
    while time.time() - t < sec:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
