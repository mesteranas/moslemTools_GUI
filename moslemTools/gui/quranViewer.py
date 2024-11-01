import time,winsound,pyperclip,gettext,os
_=gettext.gettext
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import guiTools,settings,functions
reciters={
    "إبراهيم الأخضر": "https://verse.mp3quran.net/arabic/ibrahim_alakhdar/32/",
    "الشيخ أبو بكر الشاطري": "https://verse.mp3quran.net/arabic/shaik_abu_baker_alshatri/128/",
    "أحمد العجمي": "https://verse.mp3quran.net/arabic/ahmed_alajmy/128/",
    "أحمد نعناع": "https://verse.mp3quran.net/arabic/ahmed_neana/128/",
    "أكرم العلاقمي": "https://verse.mp3quran.net/arabic/akram_alalaqmy/128/",
    "ورش": "http://www.everyayah.com/data/warsh/warsh_ibrahim_aldosary_128kbps/",
    "خالد القحطاني": "https://verse.mp3quran.net/arabic/khalid_alqahtani/128/",
    "خليفة الطنيجي": "https://verse.mp3quran.net/arabic/khalefa_altunaiji/64/",
    "سعود الشريم": "https://verse.mp3quran.net/arabic/saud_alshuraim/128/",
    "سهل ياسين": "https://verse.mp3quran.net/arabic/sahl_yassin/128/",
    "صلاح البدير": "https://verse.mp3quran.net/arabic/salah_albudair/128/",
    "صلاح بو خاطر": "https://verse.mp3quran.net/arabic/salaah_bukhatir/128/",
    "عبد الباسط عبد الصمد - مجود": "https://verse.mp3quran.net/arabic/abdulbasit_abdulsamad_mujawwad/128/",
    "عبد الرحمن السديس": "https://verse.mp3quran.net/arabic/abdurrahmaan_alsudais/128/",
    "عبد الله المطرود": "https://verse.mp3quran.net/arabic/abdullah_almatroud/128/",
    "عبد الله بصفر": "https://verse.mp3quran.net/arabic/abdullah_basfar/128/",
    "عبد الله الجهني": "https://verse.mp3quran.net/arabic/abdullaah_aljohani/128/",
    "عبد المحسن القاسم": "https://verse.mp3quran.net/arabic/abdulmohsin_alqasim/128/",
    "علي الحذيفي": "https://verse.mp3quran.net/arabic/ali_alhuthaify/128/",
    "علي جابر": "https://verse.mp3quran.net/arabic/ali_jaber/64/",
    "علي حجاج": "https://verse.mp3quran.net/arabic/ali_hajjaj/128/",
    "فارس عباد": "https://verse.mp3quran.net/arabic/fares_abbad/64/",
    "ناصر القطامي": "https://verse.mp3quran.net/arabic/nasser_alqatami/128/",
    "هاني الرفاعي": "https://verse.mp3quran.net/arabic/hani_alrifai/128/",
    "ياسر الدوسري": "https://verse.mp3quran.net/arabic/yasser_aldossary/128/",
    "ماهر المعيقلي": "https://verse.mp3quran.net/arabic/maher_almuaiqly/128/",
    "محمد الطبلاوي": "https://verse.mp3quran.net/arabic/mohammad_altablaway/128/",
    "محمد أيوب": "https://verse.mp3quran.net/arabic/mohammad_ayyoub/128/",
    "محمد جبريل": "https://verse.mp3quran.net/arabic/mohammad_jibreel/128/",
    "محمد المنشاوي": "https://verse.mp3quran.net/arabic/mohammad_alminshawi/128/",
    "محمد المنشاوي - مجود": "https://verse.mp3quran.net/arabic/mohammad_alminshawi_mujawwd/128/",
    "محمد عبد الكريم": "https://verse.mp3quran.net/arabic/mohammad_abdulkarim/64/",
    "محمود الحصري": "https://verse.mp3quran.net/arabic/mahmood_alhusary/128/",
    "محمود الحصري - مجود": "https://verse.mp3quran.net/arabic/mahmood_alhusary_mujawwd/128/",
    "محمود علي البنا": "https://verse.mp3quran.net/arabic/mahmoud_ali_albanna/32/",
    "مشاري العفاسي": "https://verse.mp3quran.net/arabic/mishary_alafasy/128/",
    "ياسر سلامة": "https://verse.mp3quran.net/arabic/yaser_salamah/128/",
    "محمود الحصري - معلم": "https://verse.mp3quran.net/arabic/mahmood_alhusary_muallim/128/"
}
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
    def oncontextMenu(self):
        menu=qt.QMenu(_("خيارات الآية"),self)
        menu.setAccessibleName(_("خيارات الآية"))
        menu.setFocus()
        goToAyah=qt1.QAction(_("الذهاب إلى آية"))
        menu.addAction(goToAyah)
        goToAyah.triggered.connect(self.goToAyah)
        menu.setDefaultAction(goToAyah)
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
        Ayah,surah,juz,page=functions.quranJsonControl.getAyah(self.getcurrentAyahText())
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
                self.text.print_(printer)
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