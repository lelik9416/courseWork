from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QMainWindow, QAction, QWidget, QFileDialog, QMdiSubWindow,
        QDesktopWidget, QMessageBox, QStackedWidget, QListWidgetItem)
        
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys
from netCDF4 import Dataset



class App(QMainWindow): 
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._increment = True
        
        self.initUI()
        self._initSingnals()
        
 
    def initUI(self):
        
        self.text = QTextEdit()
        
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.setWindowTitle('Model WRF')
        self.setGeometry(10, 10, 320, 200)
        self.setMinimumSize(320, 200)
        self.setMaximumSize(320, 200)
        self.setWindowIcon(QIcon('wrf.jpeg'))
        #self.menubar = self.menuBar()
        #self.statusbar = self.statusBar()
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

        self.f = Dataset(fileName, "r", format="NETCDF4")
        
        
    
    def _initSingnals(self):
        self.btn.clicked.connect(self.onClick)
    
        
        
    def onClick(self):
        """Слот"""
        if self._increment:
            self.openFileNameDialog()
            
            self.buttons = Buttons(self)
            self.stack.addWidget(self.buttons)
            self.stack.setCurrentWidget(self.buttons)
            
            self.buttons.but1.clicked.connect(self.eventShowLists)
            self.buttons.but2.clicked.connect(self.eventShowInformation)
            
            self.buttons.but4.clicked.connect(self.eventSaveValues)



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
    
    
    def eventShowLists(self):
        self.data_keys_for_buts = []
        #self.c = []

        data_keys = self.f.variables.keys()
        #a = list(self.f.variables.values())
        
        for k in data_keys:
            self.data_keys_for_buts.append(k)
        """    
        for i in a:
            try:
                if 'description:':
                    c = i.description
                    self.c.append(c)
                    
            except:
                continue
                
        print(len(self.data_keys_for_buts))
        print(len(c))
        """            
        self.str_param_1 = '\n'.join(self.data_keys_for_buts)
        #str_param_2 = '\n'.join(self.c)
        #str_param_3 = str_param_1 + ' - ' + str_param_2
            
            
        self.text.setText(self.str_param_1)
        return self.text.show()
        
        
        
    def eventShowInformation(self):
        #self.lbl = QLabel(self)
        #self.combo = QComboBox(self)
        
        self.data_information = []
        
        self.data_keys_for_buts = []
        data_keys = self.f.variables.keys()
        for k in data_keys:
            self.data_keys_for_buts.append(k)
            
        
        self.data_values = list(self.f.variables.values())

        for k in self.data_values:
            self.data_information.append(str(k))
            str_param = ''.join(self.data_information)


        #self.combo.addItems(self.data_keys_for_buts)
        #self.combo.activated[str].connect(self.onActivated)
    
        #self.stack.addWidget(self.combo)
        #self.stack.setCurrentWidget(self.combo)
        
        self.text.setText(str_param)
        return self.text.show()
        #return self.lbl.show()
        
        
    def onActivated(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()
        
        
        
    def eventShowValues(self):
        pass
    
    
    def eventSaveValues(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _  = QFileDialog.getSaveFileName(self,"Input file", "","All Files (*);;Python Files (*.py)", options=options)
        
        with open(fileName, 'w') as f:
            f.write('ok')
        
    
    def eventCalculate(self):
        pass
        
        
    



class Buttons(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.initUI()
        
        
    def initUI(self):

        
        hbox = QVBoxLayout()
        hbox.addStretch(1)
        
        self.but1 = QPushButton('Показать список переменных', self)
        self.but2 = QPushButton('Показать информацию о переменной', self)
        self.but3 = QPushButton('Показать значения переменной', self)
        self.but4 = QPushButton('Сохранить значения переменной', self)
        self.but5 = QPushButton('Рассчитать параметры переменной', self)
        self.but6 = QPushButton('Загрузить второй файл', self)
        
        self.but1.resize(self.but1.sizeHint())
        self.but2.resize(self.but2.sizeHint())
        self.but3.resize(self.but3.sizeHint())
        self.but4.resize(self.but4.sizeHint())
        self.but5.resize(self.but5.sizeHint())
        self.but6.resize(self.but6.sizeHint())
        
        
        hbox.addWidget(self.but1)
        hbox.addWidget(self.but2)
        hbox.addWidget(self.but3)
        hbox.addWidget(self.but4)
        hbox.addWidget(self.but5)
        hbox.addWidget(self.but6)
        
        
        vbox = QHBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.show()
        
        
    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
