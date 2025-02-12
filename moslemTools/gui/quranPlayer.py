from .translationViewer import translationViewer
from .tafaseerViewer import TafaseerViewer
import time,gettext,os,json
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import guiTools,settings,functions
with open("data/json/files/all_reciters.json","r",encoding="utf-8-sig") as file:
    reciters=json.load(file)
class QuranPlayer(qt.QDialog):
    def __init__(self,p,text,index:int,type,category):
        super().__init__(p)                        
        self.resize(1200,600)
        self.type=type
        self.times=int(settings.settings_handler.get("quranPlayer","times"))
        self.currentTime=1
        self.category=category
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
        self.text.customContextMenuRequested.connect(self.OnContextMenu)
        self.text.setFocus()
        self.font_size=12
        font=self.font()
        font.setPointSize(self.font_size)
        self.text.setFont(font)        
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))        
        self.N_aya=qt.QPushButton(_("الآيا التالية"))
        self.N_aya.clicked.connect(self.onNextAyah)
        self.PPS=qt.QPushButton(_("تشغيل"))
        self.PPS.clicked.connect(self.on_play)
        self.P_aya=qt.QPushButton(_("الآيا السابقة"))
        self.P_aya.clicked.connect(self.onPreviousAyah)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        layout.addWidget(self.N_aya)
        layout.addWidget(self.PPS)
        layout.addWidget(self.P_aya)
        qt1.QShortcut("space",self).activated.connect(self.on_play)
        qt1.QShortcut("ctrl+g",self).activated.connect(self.gotoayah)
        qt1.QShortcut("alt+right",self).activated.connect(self.onNextAyah)
        qt1.QShortcut("alt+left",self).activated.connect(self.onPreviousAyah)
        qt1.QShortcut("escape",self).activated.connect(self.close)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        self.on_play()
    def OnContextMenu(self):
        if self.media.isPlaying():
            self.media.stop()
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        aya=qt.QMenu(_("خيارات الآية"),self)
        GoToAya=qt1.QAction(_("الذهاب الى آيا"),self)
        aya.addAction(GoToAya)
        aya.setDefaultAction(GoToAya)
        GoToAya.triggered.connect(self.gotoayah)
        aya_info=qt1.QAction(_("معلومات الآيا الحالية"),self)
        aya.addAction(aya_info)
        aya_info.triggered.connect(self.getAyahInfo)
        aya_trans=qt1.QAction(_("ترجمة الآيا الحالية"),self)
        aya.addAction(aya_trans)
        aya_trans.triggered.connect(self.getCurentAyahTranslation)
        aya_tafsseer=qt1.QAction(_("تفسير الآيا الحالية"),self)
        aya.addAction(aya_tafsseer)
        aya_tafsseer.triggered.connect(self.getCurentAyahTafseer)
        aya_arab=qt1.QAction(_("إعراب الآيا الحالية"),self)
        aya.addAction(aya_arab)
        aya_arab.triggered.connect(self.getCurentAyahIArab)        
        aya_tanzeel=qt1.QAction(_("أسباب نزول الآيا الحالية"),self)
        aya.addAction(aya_tanzeel)
        aya_tanzeel.triggered.connect(self.getCurrentAyahTanzel)        
        addNewBookMark=qt1.QAction(_("إضافة علامة مرجعية"),self)
        aya.addAction(addNewBookMark)
        addNewBookMark.triggered.connect(self.onAddBookMark)

        Previous_aya=qt1.QAction(_("الآيا السابقة"),self)
        aya.addAction(Previous_aya)
        Previous_aya.triggered.connect(self.onPreviousAyah)
        next_aya=qt1.QAction(_("الآيا التالية"),self)
        aya.addAction(next_aya)
        next_aya.triggered.connect(self.onNextAyah)
        menu.setFocus()
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)
        menu.addMenu(aya)
        menu.addMenu(fontMenu)        
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def increase_font_size(self):
        self.font_size += 1
        guiTools.speak(str(self.font_size ))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        guiTools.speak(str(self.font_size ))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def update_font_size(self):
        cursor=self.text.textCursor()
        self.text.selectAll()
        font=self.text.font()
        font.setPointSize(self.font_size)
        self.text.setCurrentFont(font)        
        self.text.setTextCursor(cursor)
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
            if os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"reciters",reciters[self.getCurrentReciter()].split("/")[-3],self.on_set())):
                path=qt2.QUrl.fromLocalFile(os.path.join(os.getenv('appdata'),settings.app.appName,"reciters",reciters[self.getCurrentReciter()].split("/")[-3],self.on_set()))
            else:
                path=qt2.QUrl(reciters[self.getCurrentReciter()] + self.on_set())
            if not self.media.source()==path:
                self.media.setSource(path)
            self.media.play()
            self.PPS.setText(_("إيقاف مؤقت"))
        else:
            self.media.pause()
            self.PPS.setText(_("تشغيل"))
    def gotoayah(self):
        self.media.stop()
        number,ok=qt.QInputDialog.getInt(self,_("الذهاب إلى آية"),_("أكتب رقم الآية"),self.index+1,1,len(self.quranText),1)
        if ok:
            self.currentTime=1
            self.index=number-1
            self.text.setText(self.quranText[self.index])
            self.on_play()
    def onNextAyah(self):
        self.currentTime=1
        if self.index+1==len(self.quranText):
            self.index=0
        else:
            self.index+=1
        self.text.setText(self.quranText[self.index])
        self.media.stop()
        self.on_play()
    def onPreviousAyah(self):
        self.currentTime=1
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
            if self.times==self.currentTime:
                qt2.QTimer.singleShot(int(settings.settings_handler.get("quranPlayer","duration"))*1000,qt2.Qt.TimerType.PreciseTimer,self.onNextAyah)
            else:
                self.currentTime+=1
                qt2.QTimer.singleShot(int(settings.settings_handler.get("quranPlayer","duration"))*1000,qt2.Qt.TimerType.PreciseTimer,self.media.play)
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
    def onAddBookMark(self):
        name,OK=qt.QInputDialog.getText(self,_("إضافة علامة مرجعية"),_("أكتب أسم للعلامة المرجعية"))
        if OK:
            functions.bookMarksManager.addNewQuranBookMark(self.type,self.category,self.index,True,name)