from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from image_processing_w2 import MyWindow
from image_classification import *


class Ui_MainWindow_1(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        
        MainWindow.setGeometry(170,25,587,475)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setStyleSheet("background-color: rgb(243, 227, 92);\n"
"font: italic 13pt \"Harlow Solid Italic\";\n"
"color: rgb(70, 170, 43);")

        
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.window2)
        self.pushButton.clicked.connect(MainWindow.close)
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap("background.png"))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Plate Food Guide"))
        self.pushButton.setText(_translate("MainWindow", "Open Our Application"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        
    
    def window2(self):
        self.ui = MyWindow()
        self.ui.show()
        
        
if __name__ == "__main__":
    import sys
    # svm_model = training()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_1()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())