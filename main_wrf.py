from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QMainWindow, QAction, QWidget, QFileDialog, QMdiSubWindow,
        QDesktopWidget, QMessageBox, QStackedWidget)
        
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from netCDF4 import Dataset



class App(QMainWindow):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._increment = True
        
        self.initUI()
        self._initSingnals()
        
 
    def initUI(self):
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.setWindowTitle('Model WRF')
        self.setGeometry(10, 10, 320, 200)
        self.setMinimumSize(320, 200)
        self.setMaximumSize(320, 200)
        self.setWindowIcon(QIcon('wrf.jpeg'))
        self.statusbar = self.statusBar()
        self.center()
        
        self.btn = QPushButton('Загрузить файл', self)
        self.btn.move(100, 70)
        self.btn.resize(self.btn.sizeHint())
        
        self.stack.addWidget(self.btn)
        self.stack.setCurrentWidget(self.btn)

        
        self.show()
        
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Input file", "","All Files (*);;Python Files (*.py)", options=options)

        f = Dataset(fileName, "r", format="NETCDF4")
        
        with f:
           self.data = f

        

    
    def _initSingnals(self):
        self.btn.clicked.connect(self.onClick)
    
        
        
    def onClick(self):
        """Слот"""
        if self._increment:
            self.openFileNameDialog()
            
            self.buttons = Buttons(self)
            self.stack.addWidget(self.buttons)
            self.stack.setCurrentWidget(self.buttons)
            


    @staticmethod
    def getData(self):
        
        #f = Dataset(self.openFileNameDialog.fileName, "r", format="NETCDF4")
        
        #with f:
            #cls.data = f.variables
        
        #print(self.data)
        return self.data


    def closeEvent(self, event):
        #переопределяем обработчик события закрытия окна
        #название окна, вопрос в окне, кнопка | кнопка, кнопка на которой курсор по умолчанию
        reply = QMessageBox.question(self, 'Exit message',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
           
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    
    #центрирование окна на рабочем столе
    def center(self):
        
        #получаем прямоугольник, определяющий геометрию главного окна
        qr = self.frameGeometry()
        #получаем разрешение экрана нашего монитора и центральную точку
        cp = QDesktopWidget().availableGeometry().center()
        #устанавливаем центр прямоугольника в центр экрана
        qr.moveCenter(cp)
        #двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, 
        #таким образом, центрируя окно на нашем экране
        self.move(qr.topLeft())








class Buttons(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.initUI()
        
        
    def initUI(self):

        self.windows = Windows(self)
        
        hbox = QVBoxLayout()
        hbox.addStretch(1)
        
        self.but1 = QPushButton('Показать список переменных', self)
        self.but2 = QPushButton('Показать информацию о переменной', self)
        self.but3 = QPushButton('Показать значения переменной', self)
        self.but4 = QPushButton('Сохранить значения переменной', self)
        self.but5 = QPushButton('Рассчитать параметры переменной', self)
        #self.but6 = QPushButton('Загрузить второй файл', self)
        
        self.but1.resize(self.but1.sizeHint())
        self.but2.resize(self.but2.sizeHint())
        self.but3.resize(self.but3.sizeHint())
        self.but4.resize(self.but4.sizeHint())
        self.but5.resize(self.but5.sizeHint())
        #self.but6.resize(self.but6.sizeHint())
        
        
        hbox.addWidget(self.but1)
        hbox.addWidget(self.but2)
        hbox.addWidget(self.but3)
        hbox.addWidget(self.but4)
        hbox.addWidget(self.but5)
        #hbox.addWidget(self.but6)
 
        self.but1.clicked.connect(self.windows.eventShowLists)
        
        
        vbox = QHBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.show()



    
    


class Windows(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                
        self.data = None
        
        
    def eventShowLists(self):
        self.data_keys_for_buts = []
        
        text = QTextEdit()
        
        self.got_data = App().getData(self)

        print(self.got_data)

        #with self.got_data:
        data_keys = self.got_data.variables.keys()
        
        text.setLabelText(str_param)
        return  text.show()
        



    def eventShowInformation(self):
     
        self.textEdit = QTextEdit()
        
        #with self.got_data:
        #    data_keys = self.got_data.variables.values()

    
    def eventShowValues(self):
        pass
        
    
    
    def eventSaveValues(self):
        pass
        
    
    def eventCalculate(self):
        pass
    
    
    





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
