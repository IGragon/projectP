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
        self.pushPiece11 = QPushButton('', self)
        self.buttons.append(self.pushPiece11)
        self.pushPiece12 = QPushButton('', self)
        self.buttons.append(self.pushPiece12)
        self.pushPiece13 = QPushButton('', self)
        self.buttons.append(self.pushPiece13)
        self.pushPiece14 = QPushButton('', self)
        self.buttons.append(self.pushPiece14)
        self.pushPiece15 = QPushButton('', self)
        self.buttons.append(self.pushPiece15)
        self.pushPiece16 = QPushButton('', self)
        self.buttons.append(self.pushPiece16)
        self.pushPiece21 = QPushButton('', self)
        self.buttons.append(self.pushPiece21)
        self.pushPiece22 = QPushButton('', self)
        self.buttons.append(self.pushPiece22)
        self.pushPiece23 = QPushButton('', self)
        self.buttons.append(self.pushPiece23)
        self.pushPiece24 = QPushButton('', self)
        self.buttons.append(self.pushPiece24)
        self.pushPiece25 = QPushButton('', self)
        self.buttons.append(self.pushPiece25)
        self.pushPiece26 = QPushButton('', self)
        self.buttons.append(self.pushPiece26)
        self.pushPiece31 = QPushButton('', self)
        self.buttons.append(self.pushPiece31)
        self.pushPiece32 = QPushButton('', self)
        self.buttons.append(self.pushPiece32)
        self.pushPiece33 = QPushButton('', self)
        self.buttons.append(self.pushPiece33)
        self.pushPiece34 = QPushButton('', self)
        self.buttons.append(self.pushPiece34)
        self.pushPiece35 = QPushButton('', self)
        self.buttons.append(self.pushPiece35)
        self.pushPiece36 = QPushButton('', self)
        self.buttons.append(self.pushPiece36)
        self.pushPiece41 = QPushButton('', self)
        self.buttons.append(self.pushPiece41)
        self.pushPiece42 = QPushButton('', self)
        self.buttons.append(self.pushPiece42)
        self.pushPiece43 = QPushButton('', self)
        self.buttons.append(self.pushPiece43)
        self.pushPiece44 = QPushButton('', self)
        self.buttons.append(self.pushPiece44)
        self.pushPiece45 = QPushButton('', self)
        self.buttons.append(self.pushPiece45)
        self.pushPiece46 = QPushButton('', self)
        self.buttons.append(self.pushPiece46)
        self.pushPiece51 = QPushButton('', self)
        self.buttons.append(self.pushPiece51)
        self.pushPiece52 = QPushButton('', self)
        self.buttons.append(self.pushPiece52)
        self.pushPiece53 = QPushButton('', self)
        self.buttons.append(self.pushPiece53)
        self.pushPiece54 = QPushButton('', self)
        self.buttons.append(self.pushPiece54)
        self.pushPiece55 = QPushButton('', self)
        self.buttons.append(self.pushPiece55)
        self.pushPiece56 = QPushButton('', self)
        self.buttons.append(self.pushPiece56)
        self.pushPiece61 = QPushButton('', self)
        self.buttons.append(self.pushPiece61)
        self.pushPiece62 = QPushButton('', self)
        self.buttons.append(self.pushPiece62)
        self.pushPiece63 = QPushButton('', self)
        self.buttons.append(self.pushPiece63)
        self.pushPiece64 = QPushButton('', self)
        self.buttons.append(self.pushPiece64)
        self.pushPiece65 = QPushButton('', self)
        self.buttons.append(self.pushPiece65)
        self.pushPiece66 = QPushButton('', self)
        self.buttons.append(self.pushPiece66)
        name_1, name_2 = 1, 1
        for btn in self.buttons:
            if name_2 == 7:
                name_1 += 1
                name_2 = 1
            btn.resize(x, y)
            btn.move(random.randint(0, 280 - x), random.randint(32, 720 - y))
            icon = QIcon('data/image' + str(name_1) + str(name_2))
            btn.setIcon(icon)
            btn.setIconSize(QSize(x, y))
            name_2 += 1


def wait(sec):
    t = time.time()
    while time.time() - t < sec:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
