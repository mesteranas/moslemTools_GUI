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
class QuranViewer(qt.QDialog):
    def __init__(self,p,text):
        super().__init__(p)        
        self.showFullScreen()
        self.media=QMediaPlayer(self)
        self.audioOutput=QAudioOutput(self)
        self.media.setAudioOutput(self.audioOutput)
        self.media.setSource(qt2.QUrl.fromLocalFile("data/sounds/001001.mp3"))
        self.media.play()
        time.sleep(0.5)
        self.media.stop()
        self.quranText=text
        self.text=guiTools.QReadOnlyTextEdit()
        self.text.setText(text)
        self.text.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.text.customContextMenuRequested.connect(self.oncontextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.text.setFont(font)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        qt1.QShortcut("space",self).activated.connect(self.on_play)
        qt1.QShortcut("ctrl+g",self).activated.connect(self.goToAyah)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                
        qt1.QShortcut("escape",self).activated.connect(self.close)
    def oncontextMenu(self):
        menu=qt.QMenu(_("الخيارات "),self)
        menu.setAccessibleName(_("الخيارات "))
        menu.setFocus()
        ayahOptions=qt.QMenu(_("خيارات الآية"))
        goToAyah=qt1.QAction(_("الذهاب إلى آية"))
        ayahOptions.addAction(goToAyah)
        goToAyah.triggered.connect(self.goToAyah)
        ayahOptions.setDefaultAction(goToAyah)
        playCurrentAyahAction=qt1.QAction(_("تشغيل الآية الحالية"),self)
        ayahOptions.addAction(playCurrentAyahAction)
        playCurrentAyahAction.triggered.connect(self.on_play)
        tafaserCurrentAyahAction=qt1.QAction(_("تفسير الآية"),self)
        ayahOptions.addAction(tafaserCurrentAyahAction)
        tafaserCurrentAyahAction.triggered.connect(self.getCurentAyahTafseer)
        copyCurrentAyahAction=qt1.QAction(_("نسخ الآية المحددة"),self)
        ayahOptions.addAction(copyCurrentAyahAction)
        copyCurrentAyahAction.triggered.connect(self.copy_line)
        menu.addMenu(ayahOptions)
        surahOption=qt.QMenu(_("خيارات السورة"),self)
        copySurahAction=qt1.QAction(_("نسخ السورة"),self)
        surahOption.addAction(copySurahAction)
        surahOption.setDefaultAction(copySurahAction)
        copySurahAction.triggered.connect(self.copy_text)
        saveSurahAction=qt1.QAction(_("حفظ السورة كملف نصي"),self)
        surahOption.addAction(saveSurahAction)
        saveSurahAction.triggered.connect(self.save_text_as_txt)
        printSurah=qt1.QAction(_("طباعة السورة"),self)
        surahOption.addAction(printSurah)
        printSurah.triggered.connect(self.print_text)
        tafaseerSurahAction=qt1.QAction(_("تفسير السورة"),self)
        surahOption.addAction(tafaseerSurahAction)
        tafaseerSurahAction.triggered.connect(self.getTafaseerForSurah)
        SurahInfoAction=qt1.QAction(_("معلومات السورة"),self)
        surahOption.addAction(SurahInfoAction)
        SurahInfoAction.triggered.connect(self.onSurahInfo)
        menu.addMenu(surahOption)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def goToAyah(self):
        ayah,OK=qt.QInputDialog.getInt(self,_("الذهاب إلى آية"),_("أكتب رقم الآية "),self.getCurrentAyah()+1,1,len(self.quranText.split("\n")))
        if OK:
            cerser=self.text.textCursor()
            cerser.movePosition(cerser.MoveOperation.Start)
            for i in range(ayah-1):
                cerser.movePosition(cerser.MoveOperation.Down)
            self.text.setTextCursor(cerser)
    def getCurrentAyah(self):
        cerser=self.text.textCursor()
        return cerser.blockNumber()
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
            self.media.stop()
    def getCurrentReciter(self):
        index=int(settings.settings_handler.get("g","reciter"))
        name=list(reciters.keys())[index]
        return name
    def getcurrentAyahText(self):
        line=self.getCurrentAyah()
        return self.quranText.split("\n")[line]
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.text.print(printer)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def save_text_as_txt(self):
        try:
            file_dialog=qt.QFileDialog()
            file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setDefaultSuffix("txt")
            if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
                file_name=file_dialog.selectedFiles()[0]
                with open(file_name, 'w', encoding='utf-8') as file:
                    text = self.text.toPlainText()
                    file.write(text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def increase_font_size(self):
        self.font_size += 1
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        self.update_font_size()
    def update_font_size(self):
        cursor=self.text.textCursor()
        self.text.selectAll()
        font=self.text.font()
        font.setPointSize(self.font_size)
        self.text.setCurrentFont(font)        
        self.text.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.text.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.text.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def getCurentAyahTafseer(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        TafaseerViewer(self,AyahNumber,AyahNumber).exec()
    def getTafaseerForSurah(self):
        ayahList=self.quranText.split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        TafaseerViewer(self,AyahNumber1,AyahNumber2).exec()
    def onSurahInfo(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        with open("data/json/files/all_surahs.json","r",encoding="utf-8") as file:
            data=json.load(file)
        surahInfo=data[int(surah)-1]
        numberOfAyah=surahInfo["n"]
        if surahInfo["r"]==0:
            type=_("مكية")
        else:
            type=_("مدنية")
        qt.QMessageBox.information(self,_("معلومات السورة"),_("رقم السورة {} \n عدد آياتها {} \n نوع السورة {}").format(str(surah),str(numberOfAyah),type))
    def closeEvent(self,event):
        self.media.stop()
        self.close()