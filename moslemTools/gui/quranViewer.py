from .translationViewer import translationViewer
from .tafaseerViewer import TafaseerViewer
from .quranPlayer import QuranPlayer
import time,winsound,pyperclip,gettext,os,json
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import guiTools,settings,functions
with open("data/json/files/all_reciters.json","r",encoding="utf-8-sig") as file:
    reciters=json.load(file)
class QuranViewer(qt.QDialog):
    def __init__(self,p,text:str,type:int,category,index=0,enableNextPreviouseButtons=False,typeResult=[],CurrentIndex=0):
        super().__init__(p)        
        self.typeResult=typeResult
        self.CurrentIndex=CurrentIndex
        self.resize(1200,600)
        self.type=type
        self.category=category
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
        self.font_size=12
        font=self.font()
        font.setPointSize(self.font_size)
        self.text.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.font_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.show_font.setText(str(self.font_size))
        self.show_font.setText(str(self.font_size))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.show_font)
        layout.addWidget(self.font_laybol)
        buttonsLayout=qt.QHBoxLayout()
        self.next=qt.QPushButton(_("التالي"))
        self.next.clicked.connect(self.onNext)
        self.next.setEnabled(enableNextPreviouseButtons)
        self.next.setShortcut("alt+right")
        buttonsLayout.addWidget(self.next)
        self.previous=qt.QPushButton(_("السابق"))
        self.previous.clicked.connect(self.onPreviouse)
        self.previous.setShortcut("alt+left")
        self.previous.setEnabled(enableNextPreviouseButtons)
        buttonsLayout.addWidget(self.previous)
        layout.addLayout(buttonsLayout)
        if not index==0:
            cerser=self.text.textCursor()
            cerser.movePosition(cerser.MoveOperation.Start)
            for i in range(index-1):
                cerser.movePosition(cerser.MoveOperation.Down)
            self.text.setTextCursor(cerser)
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
        ayahOptions=qt.QMenu(_("خيارات الآية الحالية"))
        goToAyah=qt1.QAction(_("الذهاب إلى آية"))
        ayahOptions.addAction(goToAyah)
        goToAyah.triggered.connect(self.goToAyah)
        ayahOptions.setDefaultAction(goToAyah)
        playCurrentAyahAction=qt1.QAction(_("تشغيل الآية الحالية"),self)
        ayahOptions.addAction(playCurrentAyahAction)
        playCurrentAyahAction.triggered.connect(self.on_play)
        tafaserCurrentAyahAction=qt1.QAction(_("تفسير الآية الحالية"),self)
        ayahOptions.addAction(tafaserCurrentAyahAction)
        tafaserCurrentAyahAction.triggered.connect(self.getCurentAyahTafseer)
        IArabCurrentAyah=qt1.QAction(_("إعراب الآية الحالية"),self)
        ayahOptions.addAction(IArabCurrentAyah)
        IArabCurrentAyah.triggered.connect(self.getCurentAyahIArab)
        tanzelCurrentAyahAction=qt1.QAction(_("أسباب نزول الآية الحالية"),self)
        ayahOptions.addAction(tanzelCurrentAyahAction)
        tanzelCurrentAyahAction.triggered.connect(self.getCurrentAyahTanzel)
        translationCurrentAyahAction=qt1.QAction(_("ترجمة الآية الحالية"),self)
        ayahOptions.addAction(translationCurrentAyahAction)
        translationCurrentAyahAction.triggered.connect(self.getCurentAyahTranslation)
        ayahInfo=qt1.QAction(_("معلومات الآية الحالية"),self)
        ayahOptions.addAction(ayahInfo)
        ayahInfo.triggered.connect(self.getAyahInfo)        
        copy_aya=qt1.QAction(_("نسخ الآية الحالية"),self)
        ayahOptions.addAction(copy_aya)
        copy_aya.triggered.connect(self.copyAya)
        addNewBookMark=qt1.QAction(_("إضافة علامة مرجعية"),self)
        ayahOptions.addAction(addNewBookMark)
        addNewBookMark.triggered.connect(self.onAddBookMark)
        menu.addMenu(ayahOptions)
        surahOption=qt.QMenu(_("خيارات الفئة"),self)
        copySurahAction=qt1.QAction(_("نسخ الفئة"),self)
        surahOption.addAction(copySurahAction)
        surahOption.setDefaultAction(copySurahAction)
        copySurahAction.triggered.connect(self.copy_text)
        saveSurahAction=qt1.QAction(_("حفظ الفئة كملف نصي"),self)
        surahOption.addAction(saveSurahAction)
        saveSurahAction.triggered.connect(self.save_text_as_txt)
        printSurah=qt1.QAction(_("طباعة الفئة"),self)
        surahOption.addAction(printSurah)
        printSurah.triggered.connect(self.print_text)
        tafaseerSurahAction=qt1.QAction(_("تفسير الفئة"),self)
        surahOption.addAction(tafaseerSurahAction)
        tafaseerSurahAction.triggered.connect(self.getTafaseerForSurah)
        IArabSurah=qt1.QAction(_("إعراب الفئة"),self)
        surahOption.addAction(IArabSurah)
        IArabSurah.triggered.connect(self.getIArabForSurah)
        translationSurahAction=qt1.QAction(_("ترجمة  الفئة"),self)
        surahOption.addAction(translationSurahAction)
        translationSurahAction.triggered.connect(self.getTranslationForSurah)
        SurahInfoAction=qt1.QAction(_("معلومات السورة"),self)
        surahOption.addAction(SurahInfoAction)
        SurahInfoAction.triggered.connect(self.onSurahInfo)
        tafseerFromVersToVersAction=qt1.QAction(_("التفسير من آية إلى آية"))
        surahOption.addAction(tafseerFromVersToVersAction)
        tafseerFromVersToVersAction.triggered.connect(self.TafseerFromVersToVers)
        translateFromVersToVersAction=qt1.QAction(_("الترجمة من آية إلى آية"))
        surahOption.addAction(translateFromVersToVersAction)
        translateFromVersToVersAction.triggered.connect(self.translateFromVersToVers)
        IArabFromVersToVersAction=qt1.QAction(_("الإعراب من آية إلى آية"),self)
        surahOption.addAction(IArabFromVersToVersAction)
        IArabFromVersToVersAction.triggered.connect(self.IArabFromVersToVers)
        playFromVersToVersAction=qt1.QAction(_("التشغيل من آية إلى آية"),self)
        surahOption.addAction(playFromVersToVersAction)
        playFromVersToVersAction.triggered.connect(self.playFromVersToVers)
        playSurahToEnd=qt1.QAction(_("التشغيل إلى نهاية الفئة"),self)
        surahOption.addAction(playSurahToEnd)
        playSurahToEnd.triggered.connect(lambda:QuranPlayer(self,self.quranText,self.getCurrentAyah(),self.type,self.category).exec())
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
    def copyAya(self):
        a=self.getcurrentAyahText()
        pyperclip.copy(a)
        winsound.Beep(1000,100)
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
            if os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"reciters",reciters[self.getCurrentReciter()].split("/")[-3],self.on_set())):
                path=qt2.QUrl.fromLocalFile(os.path.join(os.getenv('appdata'),settings.app.appName,"reciters",reciters[self.getCurrentReciter()].split("/")[-3],self.on_set()))
            else:
                path=qt2.QUrl(reciters[self.getCurrentReciter()] + self.on_set())
            if not self.media.source()==path:
                self.media.stop()
                self.media.setSource(path)
            self.media.play()
        else:
            self.media.pause()
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
        if self.font_size < 50:
            self.font_size += 1
            guiTools.speak(str(self.font_size))
            self.show_font.setText(str(self.font_size))
            self.update_font_size()
    def decrease_font_size(self):
        if self.font_size > 1:
            self.font_size -= 1
            guiTools.speak(str(self.font_size))
            self.show_font.setText(str(self.font_size))
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
        qt.QMessageBox.information(self,_("معلومات {}").format(juz[1]),_("رقم السورة {} \n عدد آياتها {} \n نوع السورة {}").format(str(surah),str(numberOfAyah),type))
    def closeEvent(self,event):
        self.media.stop()
        self.close()
    def getCurentAyahIArab(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        result=functions.iarab.getIarab(AyahNumber,AyahNumber)
        guiTools.TextViewer(self,_("إعراب"),result).exec()
    def getIArabForSurah(self):
        ayahList=self.quranText.split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        result=functions.iarab.getIarab(AyahNumber1,AyahNumber2)
        guiTools.TextViewer(self,_("إعراب"),result).exec()
    def getCurrentAyahTanzel(self):
        Ayah,surah,juz,page,AyahNumber=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
        result=functions.tanzil.gettanzil(AyahNumber)
        if result:
            guiTools.TextViewer(self,_("أسباب النزول"),result).exec()
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
    def getTranslationForSurah(self):
        ayahList=self.quranText.split("\n")
        Ayah,surah,juz,page,AyahNumber1=functions.quranJsonControl.getAyah(ayahList[0])
        Ayah,surah,juz,page,AyahNumber2=functions.quranJsonControl.getAyah(ayahList[-1])
        translationViewer(self,AyahNumber1,AyahNumber2).exec()
    def onAddBookMark(self):
        name,OK=qt.QInputDialog.getText(self,_("إضافة علامة مرجعية"),_("أكتب أسم للعلامة المرجعية"))
        if OK:
            functions.bookMarksManager.addNewQuranBookMark(self.type,self.category,self.getCurrentAyah(),False,name)
    def playFromVersToVers(self):
        FromVers,ok=qt.QInputDialog.getInt(self,_("من الآية"),_("أكتب الرقم"),self.getCurrentAyah()+1,1,len(self.quranText.split("\n")))
        if ok:
            toVers,ok=qt.QInputDialog.getInt(self,_("إلى الآية"),_("أكتب الرقم"),len(self.quranText.split("\n")),1,len(self.quranText.split("\n")))
            if ok:
                verses=[]
                allVerses=self.quranText.split("\n")
                for vers in allVerses:
                    index=allVerses.index(vers)+1
                    if index>=FromVers and index<=toVers:
                        verses.append(vers)
                QuranPlayer(self,"\n".join(verses),0,self.type,self.category).exec()
    def TafseerFromVersToVers(self):
        FromVers,ok=qt.QInputDialog.getInt(self,_("من الآية"),_("أكتب الرقم"),self.getCurrentAyah()+1,1,len(self.quranText.split("\n")))
        if ok:
            toVers,ok=qt.QInputDialog.getInt(self,_("إلى الآية"),_("أكتب الرقم"),len(self.quranText.split("\n")),1,len(self.quranText.split("\n")))
            if ok:
                TafaseerViewer(self,FromVers,toVers).exec()
    def translateFromVersToVers(self):
        FromVers,ok=qt.QInputDialog.getInt(self,_("من الآية"),_("أكتب الرقم"),self.getCurrentAyah()+1,1,len(self.quranText.split("\n")))
        if ok:
            toVers,ok=qt.QInputDialog.getInt(self,_("إلى الآية"),_("أكتب الرقم"),len(self.quranText.split("\n")),1,len(self.quranText.split("\n")))
            if ok:
                translationViewer(self,FromVers,toVers).exec()
    def IArabFromVersToVers(self):
        FromVers,ok=qt.QInputDialog.getInt(self,_("من الآية"),_("أكتب الرقم"),self.getCurrentAyah()+1,1,len(self.quranText.split("\n")))
        if ok:
            toVers,ok=qt.QInputDialog.getInt(self,_("إلى الآية"),_("أكتب الرقم"),len(self.quranText.split("\n")),1,len(self.quranText.split("\n")))
            if ok:
                result=functions.iarab.getIarab(FromVers,toVers)
                guiTools.TextViewer(self,_("إعراب"),result).exec()
    def onNext(self):
        if self.CurrentIndex==len(self.typeResult)-1:
            self.CurrentIndex=0
        else:
            self.CurrentIndex+=1
        indexs=list(self.typeResult.keys())[self.CurrentIndex]
        self.quranText=self.typeResult[indexs][1]
        self.text.setText(self.quranText)
        winsound.PlaySound("data/sounds/next_page.wav",1)
        guiTools.speak(str(indexs))
    def onPreviouse(self):
        if self.CurrentIndex==0:
            self.CurrentIndex=len(self.typeResult)-1
        else:
            self.CurrentIndex-=1
        indexs=list(self.typeResult.keys())[self.CurrentIndex]
        self.quranText=self.typeResult[indexs][1]
        self.text.setText(self.quranText)
        winsound.PlaySound("data/sounds/previous_page.wav",1)
        guiTools.speak(str(indexs))