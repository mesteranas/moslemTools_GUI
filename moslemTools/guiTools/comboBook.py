import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
from settings import *
language.init_translation()
class comboBook(qt.QComboBox):
    def __init__(self,layout,text):
        super().__init__()
        self.layout=layout
        layout.addWidget(qt.QLabel(text))
        self.setAccessibleName(text)
        layout.addWidget(self)
        self.w=qt.QStackedWidget()
        layout.addWidget(self.w)
        self.currentIndexChanged.connect(self.changeI)
        qt1.QShortcut("ctrl+tab",self).activated.connect(self.Nexttab)
        qt1.QShortcut("ctrl+shift+tab",self).activated.connect(self.previousTab)

    def add(self,text,tabWidget):
        self.w.addWidget(tabWidget)
        self.addItem(text)
    def changeI(self,index):
        self.w.setCurrentIndex(index)
    def Nexttab(self):
        if self.currentIndex()==self.count()-1:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(int(self.currentIndex())+1)
    def previousTab(self):
        if self.currentIndex()==0:
            self.setCurrentIndex(self.count()-1)
        else:
            self.setCurrentIndex(self.currentIndex()-1)