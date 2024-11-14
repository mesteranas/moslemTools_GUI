from .translationViewer import translationViewer
from .tafaseerViewer import TafaseerViewer
import time,winsound,pyperclip,gettext,os,json
_=gettext.gettext
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import guiTools,settings,functions
with open("data/json/files/all_reciters.json","r",encoding="utf-8-sig") as file:
    reciters=json.load(file)
class QuranPlayer(qt.QDialog):
    def __init__(self,p,text,index:int):
        super().__init__(p)        
        self.showFullScreen()
        self.media=QMediaPlayer(self)
        self.audioOutput=QAudioOutput(self)
        self.media.setAudioOutput(self.audioOutput)
        self.media.setSource(qt2.QUrl.fromLocalFile("data/sounds/001001.mp3"))
        self.media.play()
        time.sleep(0.5)
        self.media.stop()
        self.media.mediaStatusChanged.connect(self.on_state)
        self.index=index-1
        self.quranText=text.split("\n")
        self.text=guiTools.QReadOnlyTextEdit()
        self.text.setText(text[index-1])
        self.text.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        qt1.QShortcut("space",self).activated.connect(self.on_play)
        qt1.QShortcut("ctrl+g",self).activated.connect(self.gotoayah)
        qt1.QShortcut("alt+right",self).activated.connect(self.onNextAyah)
        qt1.QShortcut("alt+left",self).activated.connect(self.onPreviousAyah)
        qt1.QShortcut("escape",self).activated.connect(self.close)
        self.on_play()
    def on_set(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        if int(surah)<10:
            surah="00" + surah
        elif int(surah)<100:
            surah="0" + surah
        else:
            surah=str(surah)
        if Ayah<10:
            Ayah="00" + str(Ayah)
        elif Ayah<100:
            Ayah="0" + str(Ayah)
        else:
            Ayah=str(Ayah)
        return surah+Ayah+".mp3"
    def on_play(self):
        if not self.media.isPlaying():
            if os.path.exists("data/reciters/" + settings.settings_handler.get("g","reciter") + "/" + self.on_set()):
                path=qt2.QUrl.fromLocalFile("data/reciters/" + settings.settings_handler.get("g","reciter") + "/" + self.on_set())
            else:
                path=qt2.QUrl(reciters[self.getCurrentReciter()] + self.on_set())
            if not self.media.source()==path:
                self.media.setSource(path)
            self.media.play()
        else:
            self.media.pause()
    def onNextAyah(self):
        if self.index+1==len(self.quranText):
            self.index=0
        else:
            self.index+=1
        self.text.setText(self.quranText[self.index])
        self.media.stop()
        self.on_play()
    def onPreviousAyah(self):
        if self.index==0:
            self.index=len(self.quranText)-1
        else:
            self.index-=1
        self.text.setText(self.quranText[self.index])
        self.media.stop()
        self.on_play()
    def getcurrentAyahText(self):
        return self.text.toPlainText()
    def on_state(self,state):
        if state==QMediaPlayer.MediaStatus.EndOfMedia:
            self.onNextAyah()
    def getCurrentReciter(self):
        index=int(settings.settings_handler.get("g","reciter"))
        name=list(reciters.keys())[index]
        return name
    def getCurentAyahTafseer(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        TafaseerViewer(self,AyahNumber,AyahNumber).exec()
    def closeEvent(self,event):
        self.media.stop()
        self.close()
    def getCurentAyahIArab(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        result=functions.iarab.getIarab(AyahNumber,AyahNumber)
        guiTools.TextViewer(self,_("إعراب"),result)
    def getCurrentAyahTanzel(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        result=functions.tanzil.gettanzil(AyahNumber)
        if result:
            guiTools.TextViewer(self,_("اسباب النزول"),result)
        else:
            qt.QMessageBox.information(self,_("تنبيه"),_("لا توجد أسباب نزول متاحة لهذه الآية"))
    def getAyahInfo(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        sajda=""
        if juz[3]:
            sajda=_("الآية تحتوي على سجدة")
        qt.QMessageBox.information(self,_("معلومة"),_("رقم الآية {} رقم السورة {} {} رقم الآية في المصحف {} الجزء {} الربع {} الصفحة {} {}").format(str(Ayah),surah,juz[1],AyahNumber,juz[0],juz[2],page,sajda))
    def getCurentAyahTranslation(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        translationViewer(self,AyahNumber,AyahNumber).exec()
    def gotoayah(self):
        self.media.stop()
        number,ok=qt.QInputDialog.getInt(self,_("الذهاب إلى آية"),_("أكتب رقم الآية"),self.index+1,1,len(self.quranText),1)
        if ok:
            self.index=number-1
            self.text.setText(self.quranText[self.index])
            self.on_play()