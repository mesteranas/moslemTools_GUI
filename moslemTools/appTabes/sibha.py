import shutil,gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,webbrowser,functions,time,random,os,re
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
language.init_translation()

class sibha(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("ctrl+s",self).activated.connect(self.speak_number)
        self.reset=qt.QPushButton(_("إعادة تعين"))
        self.reset.setDefault(True)
        self.reset.clicked.connect(self.reset_count)
        self.numbers=qt.QLabel("0")
        self.numbers.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.numbers.setStyleSheet("font-size:300px;")
        self.add=qt.QPushButton(_("التسبيح"))
        self.add.setDefault(True)
        self.add.clicked.connect(self.increment_count)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.reset)
        layout.addWidget(self.numbers)
        layout.addWidget(self.add)
        self.setLayout(layout)                
    def reset_count(self):
        self.numbers.setText("0")
        guiTools.speak(_("تم إعادة التعيين الى 0"))
    def increment_count(self):
        current_count=int(self.numbers.text())
        current_count += 1
        self.numbers.setText(str(current_count))
        guiTools.speak(str(current_count))
    def speak_number(self):
        current_number=self.numbers.text()
        guiTools.speak(current_number)
