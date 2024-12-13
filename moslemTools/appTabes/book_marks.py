import shutil,gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,webbrowser,functions,time,random,os,re
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
class book_marcks(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.Category_label=qt.QLabel(_("إختيار الفئة"))
        self.Category=qt.QComboBox()
        self.Category.addItem(_("القرآن الكريم"))
        self.Category.addItem(_("الأحاديث"))
        self.Category.setAccessibleName(_("إختيار الفئة"))
        self.results=guiTools.QListWidget()
        self.results.clicked.connect(self.onItemClicked)
        self.dl=guiTools.QPushButton(_("حذف العلامة المرجعية"))
        self.dl.clicked.connect(self.onRemove)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.Category_label)
        layout.addWidget(self.Category)
        layout.addWidget(self.results)
        layout.addWidget(self.dl)
        self.Category.currentIndexChanged.connect(self.onCategoryChanged)
        self.onCategoryChanged(0)
        qt1.QShortcut("delete",self).activated.connect(self.onRemove)
    def onItemClicked(self):
        if self.Category.currentIndex()==0:
            functions.bookMarksManager.openQuranByBookMarkName(self,self.results.currentItem().text())
        else:
            bookName,hadeethNumber=functions.bookMarksManager.GetHadeethBookByName(self.results.currentItem().text())
            gui.hadeeth_viewer(self,bookName,index=hadeethNumber).exec()
    def onRemove(self):
        try:
            if self.Category.currentIndex()==0:
                functions.bookMarksManager.removeQuranBookMark(self.results.currentItem().text())
            else:
                functions.bookMarksManager.removeAhadeethBookMark(self.results.currentItem().text())
            guiTools.speak(_("تم حذف العلامة المرجعية"))
            self.onCategoryChanged(self.Category.currentIndex())
        except:
            qt.QMessageBox.critical(self,_("تحذير"),_("حدث خطأ أثناء حذف العلامة المرجعية"))
    def onCategoryChanged(self,index):
        bookMarksData=functions.bookMarksManager.openBookMarksFile()
        if index==0:
            type="quran"
        else:
            type="ahadeeth"
        self.results.clear()
        for item in bookMarksData[type]:
            self.results.addItem(item["name"])
