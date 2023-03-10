import sys
from csv import excel

import PIL.Image
import cv2
import numpy as np
from PIL import Image, ImageOps
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from keras.models import load_model
from NewTest import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        # Khai bao nut load
        self.uic.btnload.clicked.connect(self.linkto)
        # Khai bao nut phan loai
        self.uic.btnPhanTich.clicked.connect(self.Scanpic)

    def Scanpic(self):
         try:
            # Load the model

            model = load_model('model_brain.h5')


            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            image = Image.open(linkchange)

            size = (224, 224)
            image = ImageOps.fit(image, size, method=0, bleed=0.0, centering=(0.5, 0.5))

            # turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 255.0)
            # Load the image into the array

            data[0] = normalized_image_array


            # run the inference
            prediction = model.predict(data)

            print(prediction)

            # Khai bao thu vien
            name = ['Tumor', ' No Tumor']
            position_1 = np.argmax(prediction)
            # Tim so lon nhat trong mang
            max_value_1 = np.amax(prediction)

            # Lay ten con vat dung
            self.uic.lblkq.setText(name[position_1])
            # lay phan tram chinh xac
            self.uic.lblPhanTram.setText(str(round(max_value_1 * 100, 2)) + ' %')
         except:
             self.uic.lblkq.setText('Error')

    def linkto(self):
        # Tim duong dan
        link = QFileDialog.getOpenFileName(filter='*.jpg *.png *.jpeg')
        # load hinh len
        self.uic.imageload.setPixmap(QPixmap(link[0]))
        # hien link hinh
        self.uic.lineEdit.setText(link[0])
        # lay link hinh tren edit text
        global linkchange
        linkpic = self.uic.lineEdit.text()
        # thay the ky tu link
        linkchange = linkpic.replace('/', '//')

    def show(self):
        self.main_win.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
