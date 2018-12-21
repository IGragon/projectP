import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QPushButton, QMessageBox, QWidget)
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtCore import QSize, QEvent
from PIL import Image
import time
import os
import random
import math


class Example(QMainWindow):
    def __init__(self, fname, parts_width, parts_hight):
        super().__init__()
        uic.loadUi('puzzle.ui', self)
        self.setFixedSize(1080, 720)
        icon = QIcon("sys_im/icon.png")
        self.setWindowIcon(icon)
        self.fname = fname
        self.image = ''
        self.x_pieces = int(parts_width)
        self.y_pieces = int(parts_hight)
        self.frame_to_hight = False
        self.frame_to_width = False
        self.image_have_taken = False
        self.is_piece_following = False
        self.count_of_good_placed_Pieces = 0
        self.places_for_Pieces = dict()
        self.fixedPoints = dict()
        self.get_image(fname)
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

    def get_image(self, fname):
        self.image = Image.open(fname)
        x, y = self.image.size
        if x >= y:
            self.pixmap = QPixmap(fname).scaledToWidth(600)
            self.frame_to_width = True
        else:
            self.pixmap = QPixmap(fname).scaledToHeight(600)
            self.frame_to_hight = True
        self.image_have_taken = True
        self.pixmap.save('data/main_pic.jpg')
        self.cut_useless_pixels(Image.open('data/main_pic.jpg'))
        self.image = Image.open('data/main_pic.jpg')
        self.make_puzzle()

    def cut_useless_pixels(self, image):
        pixels = image.load()
        x, y = image.size
        cut_image = Image.new('RGB', (x - (x % self.x_pieces), y - (y % self.y_pieces)), (0, 0, 0))
        new_pixels = cut_image.load()
        x_new, y_new = cut_image.size
        for i in range(x_new):
            for j in range(y_new):
                new_pixels[i, j] = pixels[i, j]
        cut_image.save('data/main_pic.jpg')

    def make_puzzle(self):
        os.system('mkdir data')
        step_x, step_y = self.image.size
        step_x = step_x // self.x_pieces
        step_y = step_y // self.y_pieces
        self.btn_size_x = step_x
        self.btn_size_y = step_y
        for i in range(self.x_pieces):
            for j in range(self.y_pieces):
                croped = self.image.crop([i * step_x, j * step_y, (i + 1) * step_x, (j + 1) * step_y])
                self.fixedPoints[str(i) + str(j)] = (i * step_x + 390, j * step_y + 50)
                name = 'image' + str(i + 1) + str(j + 1) + '.jpg'
                croped.save('data/' + name)
        self.createBtns(step_x, step_y)

    def createBtns(self, x, y):
        x_im, y_im = self.image.size
        if x > y:
            y = ((600 * y_im) // x_im) // self.y_pieces
            x = 600 // self.x_pieces
        if y >= x:
            x = ((600 * x_im) // y_im) // self.x_pieces
            y = 600 // self.y_pieces
        self.buttons = []
        for i in range(self.x_pieces):
            for j in range(self.y_pieces):
                btn = QPushButton('', self)
                btn.resize(x, y)
                btn.move(random.randint(0, 300 - x), random.randint(32, 720 - y))
                icon = QIcon('data/image' + str(i + 1) + str(j + 1))
                btn.setIcon(icon)
                btn.setIconSize(QSize(x, y))
                btn.setMouseTracking(True)
                btn.setObjectName(str(i + 1) + str(j + 1))
                btn.clicked.connect(self.move_piece)
                self.buttons.append(btn)
        self.height_of_piece = y
        self.width_of_piece = x
        for x_n in range(self.x_pieces):
            for y_n in range(self.y_pieces):
                self.places_for_Pieces[str(x_n + 1) + str(y_n + 1)] = \
                    [390 + x_n * self.width_of_piece, 50 + y_n * self.height_of_piece]

    def move_piece(self):
        if self.is_piece_following:
            self.is_piece_following = False
            mid_x = self.moving_piece.x() + self.width_of_piece // 2
            mid_y = self.moving_piece.y() + self.height_of_piece // 2
            if 390 < mid_x < (390 + self.width_of_piece * self.x_pieces) and \
                    50 < mid_y < (50 + self.height_of_piece * self.y_pieces):
                open_places = list(filter(lambda place: len(place[1]) < 3 and
                                                        abs(place[1][
                                                                0] - self.moving_piece.x()) < self.width_of_piece and
                                                        abs(place[1][1] - self.moving_piece.y()) < self.height_of_piece,
                                          self.places_for_Pieces.items()))
                if len(open_places):
                    n_in_Places_for_Pieces = min(open_places,
                                                 key=lambda place:
                                                 ((place[1][0] - self.moving_piece.x()) ** 2
                                                  + (place[1][1] - self.moving_piece.y()) ** 2)
                                                 ** 0.5)[0]
                    self.places_for_Pieces[n_in_Places_for_Pieces] += [self.moving_piece]
                    self.moving_piece.move(self.places_for_Pieces[n_in_Places_for_Pieces][0],
                                           self.places_for_Pieces[n_in_Places_for_Pieces][1])
                    if self.moving_piece.objectName() == n_in_Places_for_Pieces:
                        self.count_of_good_placed_Pieces += 1
                if self.count_of_good_placed_Pieces == self.x_pieces * self.y_pieces:
                    self.win()


        else:
            self.moving_piece = self.sender()
            if not ((self.moving_piece.x() - 390) % self.width_of_piece) and \
                    not ((self.moving_piece.y() - 50) % self.height_of_piece):
                coord_x_in_field = (self.moving_piece.x() - 390) // self.width_of_piece
                coord_y_in_field = (self.moving_piece.y() - 50) // self.height_of_piece
                n_coord = str(coord_x_in_field + 1) + str(coord_y_in_field + 1)
                if len(self.places_for_Pieces[n_coord]) > 2 and self.places_for_Pieces[n_coord][
                    -1] == self.moving_piece:
                    if self.moving_piece.objectName() == n_coord:
                        self.count_of_good_placed_Pieces -= 1
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

    def win(self):
        self.congrat = Congratulations(self.t_start)
        self.congrat.show()

    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self, 'Quit?', "Хотите выйти?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            os.system('del data /Q')
            self.close()
        else:
            event.ignore()


class Congratulations(QWidget):
    def __init__(self, t):
        super().__init__()
        uic.loadUi('congrat.ui', self)
        self.setFixedSize(800, 560)
        self.setPicture()
        self.pushClose.clicked.connect(self.close)
        game_time = time.time() - t
        min = game_time // 60
        sec = game_time - min * 60
        self.labelTime.setText(self.labelTime.text() + str(int(min)) + ':' + str(round(sec, 2)))

    def setPicture(self):
        pixmap = QPixmap('sys_im/congratulations.jpg')
        self.labelCon.setPixmap(pixmap)
        self.labelCon.resize(self.labelCon.sizeHint())


class StartSettings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('start.ui', self)
        self.setFixedSize(400, 600)
        icon = QIcon("sys_im/icon_start.png")
        self.setWindowIcon(icon)
        self.im = ''
        self.fname = ''
        self.pushStart.clicked.connect(self.close)
        self.pushSelect.clicked.connect(self.get_image)
        self.labelHello.setPixmap(QPixmap("sys_im/pyzzle.jpg").scaledToWidth(370))

    def closeEvent(self, event):
        if (self.lineWidth.text().isdigit() and self.lineHeight.text().isdigit()
            and int(self.lineWidth.text()) > 1 and int(self.lineHeight.text()) > 1) and self.fname:
            if self.fname:
                self.main_window = Example(self.fname, self.lineWidth.text(), self.lineHeight.text())
                self.main_window.show()
                self.close()
        else:
            if not self.fname and not (self.lineWidth.text().isdigit() and self.lineHeight.text().isdigit()
                                       and 12 > int(self.lineWidth.text()) > 1 and 12 > int(
                        self.lineHeight.text()) > 1):
                text = 'Неверное количество элементов и невыбрана картинка'
            elif not (12 > int(self.lineWidth.text()) > 1 and 12 > int(self.lineHeight.text()) > 1):
                text = 'Неверное количество элементов'
            else:
                text = 'Невыбрана картинка'
            dialog = QMessageBox.question(self, 'Что-то не так', text + '\nА может Вы хотите выйти?',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if dialog == QMessageBox.Yes:
                self.close()
            else:
                event.ignore()

    def get_image(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', 'images/')[0]
        self.im = Image.open(self.fname)
        x, y = self.im.size
        if x >= y:
            pixmap = QPixmap(self.fname).scaledToWidth(100)
        else:
            pixmap = QPixmap(self.fname).scaledToHeight(100)
        self.labelPreview.setPixmap(pixmap)

    def mouseMoveEvent(self, QMouseEvent):
        try:
            if self.checkSettings.isChecked():
                self.lineWidth.setEnabled(True)
                self.lineHeight.setEnabled(True)
                if not (self.lineWidth.text().isdigit() and self.lineHeight.text().isdigit()
                        and 12 > int(self.lineWidth.text()) > 1 and 12 > int(self.lineHeight.text()) > 1):
                    self.labelWarning.setStyleSheet("color: red;")
                else:
                    self.labelWarning.setStyleSheet("color: black;")
            else:
                self.lineWidth.setEnabled(False)
                self.lineHeight.setEnabled(False)
                self.lineWidth.setText('6')
                self.lineHeight.setText('6')
                self.labelWarning.setStyleSheet("color: black;")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = StartSettings()
    settings.show()
    sys.exit(app.exec())
