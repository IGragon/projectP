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
        self.is_piece_following = False
        self.places_for_Pieces = dict()
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
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'images/')[0]
        self.image = Image.open(self.fname)
        x, y = self.image.size
        if x >= y:
            self.pixmap = QPixmap(self.fname).scaledToWidth(600)
            self.frame_to_width = True
        else:
            self.pixmap = QPixmap(self.fname).scaledToHeight(600)
            self.frame_to_hight = True
        self.image_have_taken = True
        self.pixmap.save('data/main_pic.jpg')
        self.image = Image.open('data/main_pic.jpg')

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
        self.createBtns(step_x, step_y)

    def createBtns(self, x, y):
        x_im, y_im = self.image.size
        if x >= y:
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
        for l in self.buttons:
            for btn in l:
                btn.clicked.connect(self.move_piece)
        self.height_of_piece = y
        self.width_of_piece = x
        for x_n in range(6):
            for y_n in range(6):
                self.places_for_Pieces[str(x_n + 1) + str(y_n + 1)] = \
                    [390 + x_n * self.width_of_piece, 50 + y_n * self.height_of_piece]

    def move_piece(self):
        if self.is_piece_following:
            self.is_piece_following = False
            mid_x = self.moving_piece.x() + self.width_of_piece // 2
            mid_y = self.moving_piece.y() + self.height_of_piece // 2
            if 390 < mid_x < (390 + self.width_of_piece * 6) and \
                    50 < mid_y < (50 + self.height_of_piece * 6):
                open_places = list(filter(lambda place: len(place[1]) < 3 and
                                                   abs(place[1][0] - self.moving_piece.x()) < self.width_of_piece and
                                                   abs(place[1][1] - self.moving_piece.y()) < self.height_of_piece,
                                     self.places_for_Pieces.items()))
                if len(open_places):
                    n_in_Places_for_Pieces = min(open_places,
                        key = lambda place:
                        ((place[1][0] - self.moving_piece.x()) ** 2
                         + (place[1][1] - self.moving_piece.y()) ** 2)
                        ** 0.5)[0]
                    self.places_for_Pieces[n_in_Places_for_Pieces] += [self.moving_piece]
                    self.moving_piece.move(self.places_for_Pieces[n_in_Places_for_Pieces][0],
                                           self.places_for_Pieces[n_in_Places_for_Pieces][1])
        else:
            self.moving_piece = self.sender()
            if not ((self.moving_piece.x() - 390) % self.width_of_piece) and \
                    not ((self.moving_piece.y() - 50) % self.height_of_piece):
                coord_x_in_field = (self.moving_piece.x() - 390) // self.width_of_piece
                coord_y_in_field = (self.moving_piece.y() - 50) // self.height_of_piece
                n_coord = str(coord_x_in_field + 1) + str(coord_y_in_field + 1)
                if len(self.places_for_Pieces[n_coord]) > 2 and self.places_for_Pieces[n_coord][-1] == self.moving_piece:
                    del self.places_for_Pieces[n_coord][-1]
            self.is_piece_following = True

    def mouseMoveEvent(self, event):
        if self.is_piece_following:
            new_x = event.x() - self.width_of_piece // 2
            if new_x < 0:
                new_x = 0
            elif new_x + self.width_of_piece > 1080:
                new_x = 1080 - self.width_of_piece
            new_y = event.y() - self.height_of_piece // 2
            if new_y < 0:
                new_y = 0
            elif new_y + self.height_of_piece > 720:
                new_y = 720 - self.height_of_piece
            self.moving_piece.move(new_x, new_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
