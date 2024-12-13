import shutil,gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,webbrowser,functions,time,random,os,re
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog

class protcasts(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list=guiTools.QListWidget()
        self.list.itemClicked.connect(self.play_procast)
        self.list.addItem(_("إذاعة القرآن الكريم من القاهرة"))                        
        self.list.addItem(_("إذاعة القرآن الكريم من السعودية"))
        self.list.addItem(_("إذاعة القرآن الكريم من دبي"))
        self.list.addItem(_("إذاعة للقرآن الكريم عبر الانترنيت"))
        self.list.addItem(_("إذاعة القرآن الكريم من نابلِس "))
        self.list.addItem(_("إذاعة الحرم المكي"))
        self.list.addItem(_("إذاعة القرآن الكريم من أستراليا"))
        self.list.addItem(_("إذاعة طيبة للقرآن الكريم من السودان"))
        self.list.addItem(_("إذاعة القرآن الكريم من مصر"))
        self.list.addItem(_("إذاعة القرآن الكريم من فَلَسطين"))
        self.list.addItem(_("تلاوات خاشعة"))
        self.list.addItem(_("إذاعة القُراء"))
        self.list.addItem(_("إذاعة عمر عبد الكافي"))
        self.list.addItem(_("فتاوى ابن عُثيمين"))
        self.list.addItem(_("إذاعة التفسير"))
        self.list.addItem(_("المختصر في التفسير"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list)
        self.setLayout(layout)        
        self.media=QMediaPlayer(self)
        self.audioOutput=QAudioOutput(self)
        self.media.setAudioOutput(self.audioOutput)
        self.media.setSource(qt2.QUrl.fromLocalFile("data/sounds/001001.mp3"))
        self.media.play()
        time.sleep(0.5)
        self.media.stop()
    def play_procast(self):
        if self.media.isPlaying():
            self.media.stop()
        else:
            if self.list.currentRow()==0:
                self.media.setSource(qt2.QUrl("https://stream.radiojar.com/8s5u5tpdtwzuv"))            
            elif self.list.currentRow()==1:
                self.media.setSource(qt2.QUrl("https://stream.radiojar.com/4wqre23fytzuv"))
            elif self.list.currentRow()==2:
                self.media.setSource(qt2.QUrl("https://uk5.internet-radio.com/proxy/dubaiholyquran?mp=/stream;"))
            elif self.list.currentRow()==3:
                self.media.setSource(qt2.QUrl("https://qurango.net/radio/tarateel"))
            elif self.list.currentRow()==4:
                self.media.setSource(qt2.QUrl("http://www.quran-radio.org:8002/;stream.mp3"))
            elif self.list.currentRow()==5:
                self.media.setSource(qt2.QUrl("http://r7.tarat.com:8004/;"))
            elif self.list.currentRow()==6:
                self.media.setSource(qt2.QUrl("http://listen.qkradio.com.au:8382/listen.mp3"))
            elif self.list.currentRow()==7:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:9960"))
            elif self.list.currentRow()==8:
                self.media.setSource(qt2.QUrl("http://66.45.232.131:9994/;stream"))
            elif self.list.currentRow()==9:
                self.media.setSource(qt2.QUrl("http://streamer.mada.ps:8029/quranfm"))
            elif self.list.currentRow()==10:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:9992"))
            elif self.list.currentRow()==11:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:8006"))
            elif self.list.currentRow()==12:
                self.media.setSource(qt2.QUrl("http://node-28.zeno.fm/66geh5zntp8uv?zs=u1rolhJRRS-k08Aw1jvY8Q&rj-tok=AAABgNAugTEAylkfGQGe4UQM-w&rj-ttl=5"))
            elif self.list.currentRow()==13:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:8014"))
            elif self.list.currentRow()==14:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:9718"))
            elif self.list.currentRow()==15:
                self.media.setSource(qt2.QUrl("http://live.mp3quran.net:9698"))
            self.media.play()
