class Congratulations(QWidget):
    def __init__(self, t):
        super().__init__()
        uic.loadUi('congrat.ui', self)
        self.setFixedSize(800, 560)
        self.setPicture()
        self.pushClose.clicked.connect(self.close)
        self.labelTime.setText(self.labelTime.text() + str(round(time.time() - t, 2)) + ' секунд')

    def setPicture(self):
        pixmap = QPixmap('data/congratulations.jpg')
        self.labelCon.setPixmap(pixmap)
        self.labelCon.resize(self.labelCon.sizeHint())


'''В то место, которое определяет победу пишешь:
self.congrat = Congratulations()
self.congrat.show()
ну, ещё можешь сделать какой-нибудь флаг,
 чтобы после закрытия больше не вызывалось'''
