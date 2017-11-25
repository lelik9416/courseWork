from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QMainWindow, QAction, QWidget, QFileDialog, QMdiSubWindow,
        QDesktopWidget, QMessageBox)
        
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys
from netCDF4 import Dataset

class App(QWidget):
 
    def __init__(self):
        super().__init__()

        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Model WRF')
        self.setGeometry(10, 10, 450, 300)
        self.setWindowIcon(QIcon('wrf.jpeg'))
        self.center()
        
        
        self.openFileNameDialog()

        mainLayout = QVBoxLayout()
        
        but1 = QPushButton('Показать список переменных')
        but2 = QPushButton('Показать информацию о переменной')
        but3 = QPushButton('Показать значения переменной')
        but4 = QPushButton('Сохранить значения переменной')
        but5 = QPushButton('Рассчитать параметры переменной')
        but6 = QPushButton('Загрузить второй файл')

        mainLayout.addWidget(but1)
        mainLayout.addWidget(but2)
        mainLayout.addWidget(but3)
        mainLayout.addWidget(but4)
        mainLayout.addWidget(but5)
        mainLayout.addWidget(but6)
        
        but1.clicked.connect(self.event_show_lists)

        self.setLayout(mainLayout)
        self.show()
 

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Input file", "","All Files (*);;Python Files (*.py)", options=options)
        
        self.data = Dataset(fileName, "r", format="NETCDF4")
        
        #self.data._isopen()
        #self.data.close()
        #with Dataset(fileName, "r", format="NETCDF4") as f:
        #    self.data = f


    def event_show_lists(self):
        self.data_keys_for_buts = []
        keys = []
        
        text = QTextEdit()
        #textEdit = self.window.setWindowModality(self, QTextEdit())
        
        #window.addWidget(text)
        
        with self.data:
            data_keys = self.data.variables.keys()
            for k in data_keys:
                self.lbl = k
                self.data_keys_for_buts.append(k)
                str_param = '\n'.join(self.data_keys_for_buts)
        
        text.setText(str_param)
        return  text.show()

    
    def event_show_information(self):

        self.textEdit = QTextEdit()
        
        with self.data:
            data_keys = self.data.variables.values()



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




class Description(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        
        
    def initUI(self):
        pass
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


