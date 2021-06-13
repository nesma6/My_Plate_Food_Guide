from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
import sys
#from image_processing_w3 import MainWindow_3
import cv2
from PIL import Image
from image_classification import *
from Calories import *


stylesheet = """
    MyWindow {
        background-color: #f3e35c; 
        background-repeat: no-repeat; 
        background-position: center;
    }
    QPushButton{
background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey);
border-style: solid;
border-color: #964b70;
border-width: 0.5px;
border-radius: 10px;
font: italic 13pt \"Harlow Solid Italic\";
height: 30;
}
QLabel{
border-width: 1px;
border-style: solid;
border-color:  #964b70;
font: italic 13pt \"Harlow Solid Italic\";
color:#964b70;
}
 """ 
class Ui_MainWindow_2(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(686, 293)
        MainWindow.setGeometry(170,25,587,475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
       
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(60)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_3.setStretch(0, 5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.setStyleSheet("background-color: #bebebe;\n"
            "color : #964b70;\n"    "border-color:#964b70;\n"  "border-width:1px;" )

        self.pushButton_2.setStyleSheet("background-color: #bebebe;\n"
            "color : #964b70;\n"     "border-color:#964b70;\n"  "border-width:1px;")
        self.pushButton_3.setStyleSheet("background-color: #bebebe;\n"
        "color : #964b70;\n"   "border-color:#964b70;\n"  "border-width:1px;")
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Plate Food Guide"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "Select Food "))
        
        self.label_3.setText(_translate("MainWindow", "Food"))
        #self.label_4.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Calorie"))
        #self.label_5.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", "Estimate The Calorie"))
        self.pushButton_3.setText(_translate("MainWindow", "Show Food Analysis"))
        self.pushButton_3.clicked.connect(MainWindow.close)
    

       
        

class MyWindow(QtWidgets.QMainWindow , Ui_MainWindow_2):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.file_path = None
        #self.svm_model = training()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.getfiles)
        self.pushButton_2.clicked.connect(self.estimate)
        self.setStyleSheet(stylesheet)
        self.show()
        self.food = ""
        self.calorie = ""
        self.label_3.setText("Food                       " + str(self.food))
        self.label_2.setText("Calorie                    " + str(self.calorie))
        self.pushButton_3.clicked.connect(self.window3)
        
    def getfiles(self):
        fname = QFileDialog.getOpenFileName(self, 'SELECT FOOD','c\\', "Image files (*.jpg *.PNG *.jpeg)")
        self.file_path = fname[0]
        image = Image.open(self.file_path)
        image = image.resize((400,350))
        image = image.convert('RGB')
        image.save('selected_food.jpeg')
        pixmap = QPixmap('selected_food.jpeg')
        self.label.setPixmap(QPixmap(pixmap))
        self.class_image, self.fruit_area, self.finger_area, self.fruit_contour, self.pix_to_cm_multiplier = classify_image(self.file_path)
        

    def estimate(self):
        self.label_3.setText("Food                       " + str(get_food_Name(self.class_image)))
        volume = Get_Volume(self.class_image, self.fruit_area, self.finger_area, self.pix_to_cm_multiplier, self.fruit_contour)
        _, calories, _ = Get_Calories(self.class_image, volume)
        self.label_2.setText("Calorie                    " + str(calories))

    def window3(self):
        self.ui = MainWindow_3(self.class_image)
        self.ui.show()


import sys, random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter


protein = {1:'0.26',  #apple
            2:'1.1',  #banana
            3:'21',   #beans
            4:'0.9',  #carrot
            5:'25',   #cheese
            6:'0.9',
            7:'1.1',
            8:'5',
            9:'0.9',
            10:'0.7',
            11:'1.3',
            12:'1.1',
            13:'1.9',
            14:'0.6'
}

Fats = {1:'0.17',  #apple
        2:'0.3',
        3:'1.2',
        4:'0.2',
        5:'33',
        6:'0.1',
        7:'0.1',
        8:'1.1',
        9:'0.2',
        10:'0.1',
        11:'0.2',
        12:'0.5',
        13:'0.4',
        14:'0.2'

 }
Carbos = {1: '13.81',  #apple
        2:'23',
        3:'63',
        4:'10',
        5:'1.3',
        6:'12',
        7:'9',
        8:'25',
        9:'3.9',
        10:'3.6',
        11:'26',
        12:'15',
        13:'9',
        14:'8'
}



Fiber = {1: '2.4',
        2:'2.6',
        3:'16',
        4:'2.8',
        5:'0',
        6:'2.4',
        7:'1.7',
        8:'1.2',
        9:'1.2',
        10:'0.5',
        11:'0.3',
        12:'3',
        13:'1.5',
        14:'0.4'

}



Calcium = { 1: '0.006',
            2:'0.005',
            3:'0.113',
            4:'0.033',
            5:'0.721',
            6:'0.04',
            7:'0.023',
            8:'0.006',
            9:'0.01',
            10:'0.014',
            11:'0.016',
            12:'0.034',
            13:'0.014',
            14:'0.007'
}


Potassium = {1: '0.107',
        2:'0.358',
        3:'0.001393',
        4:'0.320',
        5:'0.098',
        6:'0.181',
        7:'0.146',
        8:'0.024',
        9:'0.237',
        10:'0.147',
        11:'0.315',
        12:'0.312',
        13:'0.322',
        14:'0.112'
}

foods = {
    1 : "Apple",
    2 : "Banana",
    3 : "Bean", 
    4 : "Carrot",
    5 : "Cheese",
    6 : "Orange",
    7 : "Onion",
    8 : "Pasta",
    9 : "Tomato",
    10: "Cucumber",
    11: "Souce",
    12: "Kiwi",
    13: "Pepper",
    14: "Watermelon"
}


stylesheet2 = """
    MainWindow {
        background-image: url("image4.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
 """    
class MainWindow_3(QMainWindow):
        def __init__(self , class_image):
            super().__init__()
            #self.resize(500, 400)
            self.setGeometry(170,25,587,475)
            self.setWindowTitle("My Plate Food Guide")
            food_lable = class_image
            food_elements = []
            food_elements.append(str(protein[food_lable]))
            food_elements.append(str(Fats[food_lable]))
            food_elements.append(str(Carbos[food_lable]))
            food_elements.append(str(Fiber[food_lable]))
            food_elements.append(str(Calcium[food_lable]))
            food_elements.append(str(Potassium[food_lable]))

            set0 = QBarSet('Food Elements')
           
            for i in range(6):
                set0.append(float(food_elements[i]))
            

            series = QBarSeries()
            series.append(set0)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle(foods[food_lable] + '  Elements Per 100 Grams')
            chart.setAnimationOptions(QChart.SeriesAnimations)

            Food_Elements = ('protein', 'Fats', 'Carbos', 'Fiber', 'Calcium', 'Potassium')


            axisX = QBarCategoryAxis()
            axisX.append(Food_Elements)

            axisY = QValueAxis()
            max_num = max(food_elements)
            axisY.setRange(0,float(max_num)+0.5)

            chart.addAxis(axisX, Qt.AlignBottom)
            chart.addAxis(axisY, Qt.AlignLeft)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)

            chartView = QChartView(chart)
            self.setCentralWidget(chartView)
            p = QPushButton('previous',self)
            p.setGeometry(10,440,100,25)
            p.setStyleSheet("background-color: #bebebe;\n"
            "color : #964b70;\n"    "border-color:#964b70;\n"  "border-width:1px;" )
            p.clicked.connect(self.close)
            p.clicked.connect(self.go_to_window2)
            
            
            
            
        def go_to_window2(self):
            self.ui = MyWindow()
            self.ui.show()
            
            
    

