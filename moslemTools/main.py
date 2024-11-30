import sys
from custome_errors import *
sys.excepthook=my_excepthook
import gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,gettext,webbrowser,functions,time,random,os,re
_=gettext.gettext
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
language.init_translation()
class DownloadThread(qt2.QThread):
    progress=qt2.pyqtSignal(int)
    finished=qt2.pyqtSignal()
    def __init__(self, url, filepath):
        super().__init__()
        self.url=url
        self.filepath=filepath
    def run(self):
        response=requests.get(self.url, stream=True)
        total_size=int(response.headers.get('content-length', 0))
        downloaded_size=0
        with open(self.filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size+=len(chunk)
                    progress_percent=int((downloaded_size / total_size) * 100)
                    self.progress.emit(progress_percent)
            self.finished.emit()
class QuranPlayer(qt.QWidget):
    def __init__(self):
        super().__init__()        
        qt1.QShortcut("ctrl+s",self).activated.connect(lambda: self.mp.stop())
        qt1.QShortcut("space", self).activated.connect(self.play)
        qt1.QShortcut("alt+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 5000))
        qt1.QShortcut("alt+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 5000))
        qt1.QShortcut("alt+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 10000))
        qt1.QShortcut("alt+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 10000))
        qt1.QShortcut("ctrl+right", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 30000))
        qt1.QShortcut("ctrl+left", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 30000))
        qt1.QShortcut("ctrl+up", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() + 60000))
        qt1.QShortcut("ctrl+down", self).activated.connect(lambda: self.mp.setPosition(self.mp.position() - 60000))
        qt1.QShortcut("ctrl+1", self).activated.connect(self.t10)
        qt1.QShortcut("ctrl+2", self).activated.connect(self.t20)
        qt1.QShortcut("ctrl+3", self).activated.connect(self.t30)
        qt1.QShortcut("ctrl+4", self).activated.connect(self.t40)
        qt1.QShortcut("ctrl+5", self).activated.connect(self.t50)
        qt1.QShortcut("ctrl+6", self).activated.connect(self.t60)
        qt1.QShortcut("ctrl+7", self).activated.connect(self.t70)
        qt1.QShortcut("ctrl+8", self).activated.connect(self.t80)
        qt1.QShortcut("ctrl+9", self).activated.connect(self.t90)
        qt1.QShortcut("shift+up", self).activated.connect(self.increase_volume)
        qt1.QShortcut("shift+down", self).activated.connect(self.decrease_volume)                
        self.reciters_data=self.load_reciters()        
        self.show_reciters=qt.QLabel(_("إختيار قارئ"))
        self.comboBox = qt.QComboBox()
        self.comboBox.setAccessibleName(_("إختيار قارئ"))
        self.listWidget=guiTools.QListWidget()
        self.listWidget.clicked.connect(self.play_selected_audio)
        self.progressBar=qt.QProgressBar()
        self.progressBar.setVisible(False)
        self.mp=QMediaPlayer()
        self.au=QAudioOutput()
        self.mp.setAudioOutput(self.au)
        self.Slider=qt.QSlider(qt2.Qt.Orientation.Horizontal)
        self.Slider.setRange(0,100)
        self.Slider.setAccessibleName(_("الوقت المنقدي"))
        self.mp.durationChanged.connect(self.update_slider)
        self.mp.positionChanged.connect(self.update_slider)        
        self.duration=qt.QLineEdit()
        self.duration.setReadOnly(True)
        self.duration.setAccessibleName(_("مدة المقطع"))
        self.dl_all=qt.QPushButton(_("تحميل جميع السور المتاحة لهذا القارئ في الجهاز"))
        self.dl_all.setDefault(True)
        self.dl_all.clicked.connect(self.download_all_soar)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.show_reciters)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.dl_all)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.Slider)
        layout.addWidget(self.duration)
        self.setLayout(layout)        
        self.comboBox.addItems(self.reciters_data.keys())
        self.comboBox.currentIndexChanged.connect(self.load_reciter_files)
        self.listWidget.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.open_context_menu)        
        self.load_reciter_files()        
    def download_all_soar(self):
        reciter_name=self.comboBox.currentText()        
        self.files_to_download=list(self.reciters_data.get(reciter_name, {}).items())
        self.current_file_index=0                
        save_folder=qt.QFileDialog.getExistingDirectory(self,_("اختيار مجلد لحفظ السور"))
        if not save_folder:            
            return                
        response=qt.QMessageBox.question(self, _("تأكيد التحميل"),
        _("هل أنت متأكد من تحميل جميع السور؟"),
        qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No,
        qt.QMessageBox.StandardButton.No)        
        if response == qt.QMessageBox.StandardButton.Yes:
                self.save_folder=save_folder
                self.download_next_sora()
        else:
            qt.QMessageBox.information(self, _("إلغاء التحميل"), _("تم إلغاء التحميل."))
    def download_next_sora(self):    
        if self.current_file_index < len(self.files_to_download):
            file_name,url=self.files_to_download[self.current_file_index]
            filepath=f"{self.save_folder}/{file_name}.mp3"
            self.current_file_index+=1
            self.download_thread=DownloadThread(url,filepath)
            self.download_thread.progress.connect(self.update_progress)
            self.download_thread.finished.connect(self.download_finished)
            self.download_thread.start()
        else:
            self.progressBar.setVisible(False)
            qt.QMessageBox.information(self, _("تم التحميل"), _("تم تحميل جميع الصور."))
    def update_progress(self,progress_percent):
        self.progressBar.setValue(progress_percent)
    def load_reciter_files(self):
        try:
            self.listWidget.clear()
            reciter=self.comboBox.currentText()
            if reciter:
                for surah,link in self.reciters_data[reciter].items():
                    self.listWidget.addItem(surah)
        except:
            qt.QMessageBox.critical(self, _("تنبيه"), _("حدث خطأ ما"))
    def open_context_menu(self, position):
        menu=qt.QMenu(self)
        play_action=qt1.QAction(_("تشغيل السورة المحددة من الإنترنت"), self)
        download_action=qt1.QAction(_("تحميل السورة المحددة في الجهاز"), self)
        play_action.triggered.connect(self.play_selected_audio)
        download_action.triggered.connect(self.download_selected_audio)
        menu.addAction(play_action)
        menu.addAction(download_action)
        menu.exec(self.listWidget.viewport().mapToGlobal(position))
    def play_selected_audio(self):
        try:
            reciter=self.comboBox.currentText()
            selected_item=self.listWidget.currentItem()
            if selected_item:
                url=self.reciters_data[reciter][selected_item.text()]
                self.mp.setSource(qt2.QUrl(url))
                self.mp.play()
        except:
            qt.QMessageBox.critical(self, _("تنبيه"), _("حدث خطأ ما"))
    def download_selected_audio(self):
        try:
            reciter=self.comboBox.currentText()
            selected_item=self.listWidget.currentItem()
            if selected_item:
                url=self.reciters_data[reciter][selected_item.text()]
                filepath,_=qt.QFileDialog.getSaveFileName(self,"save surah","","Audio Files (*.mp3)")
                if filepath:
                    self.progressBar.setVisible(True)                                        
                    self.download_thread=DownloadThread(url, filepath)
                    self.download_thread.progress.connect(self.progressBar.setValue)
                    self.download_thread.finished.connect(self.download_complete)
                    self.download_thread.start()                    
        except:
            qt.QMessageBox.critical(self, _("تنبيه"), _("حدث خطأ ما"))
    def download_finished(self):
        self.progressBar.setVisible(True)
        self.download_next_sora()        
    def download_complete(self):
        self.progressBar.setVisible(False)
        qt.QMessageBox.information(self, _("تم"), _("تم تحميل السورة"))        
    @staticmethod
    def load_reciters():            
        file_path="data/json/reciters.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)        
    def t10(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.1))
    def t20(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.2))
    def t30(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.3))
    def t40(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.4))
    def t50(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.5))
    def t60(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.6))
    def t70(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.7))
    def t80(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.8))
    def t90(self): 
        total_duration = self.mp.duration()
        self.mp.setPosition(int(total_duration * 0.9))            
    def play(self):
        if self.mp.isPlaying():
            self.mp.pause()
        else:
            self.mp.play()
    def increase_volume(self):
        current_volume=self.ao.volume()
        new_volume=current_volume+0.10
        self.au.setVolume(new_volume)
    def decrease_volume(self):
        current_volume=self.ao.volume()
        new_volume=current_volume-0.10
        self.au.setVolume(new_volume)        
    def update_slider(self):
        try:
            self.Slider.setValue(int((self.mp.position()/self.mp.duration())*100))
            self.time_VA()
        except:
            self.duration.setText(_("خطأ في الحصول على مدة المقطع"))
    def time_VA(self):
        position=self.mp.position()
        duration=self.mp.duration()
        position_hours=(position // 3600000) % 24
        position_minutes=(position // 60000) % 60
        position_seconds=(position // 1000) % 60
        duration_hours=(duration // 3600000) % 24
        duration_minutes=(duration // 60000) % 60
        duration_seconds=(duration // 1000) % 60
        position_str=qt2.QTime(position_hours, position_minutes, position_seconds).toString("HH:mm:ss")
        duration_str=qt2.QTime(duration_hours, duration_minutes, duration_seconds).toString("HH:mm:ss")        
        self.duration.setText(_(f"الوقت المنقضي: {position_str}، مدة المقطع: {duration_str}"))
class UserGuide(qt.QWidget):
    def __init__(self):
        super().__init__()                
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                
        self.guide=guiTools.QReadOnlyTextEdit()        
        self.guide.setText(_("دليل المستخدم لبرنامج Moslem Tools\n\nمقدمة\nبرنامج Moslem Tools هو أداة شاملة للمسلمين، يقدم مجموعة من الميزات التي تلبي احتياجاتهم اليومية في العبادة والتعلم. يوفر البرنامج تجربة مريحة وسهلة الاستخدام مع أدوات متنوعة لتحسين حياتك الدينية.\n\nميزات برنامج Moslem Tools\n\n1. قراءة واستماع للقرآن الكريم\nقراءة القرآن الكريم بالتقسيمات المختلفة (سور، صفحات، أجزاء، أرباع، وأحزاب).\nالاستماع للقرآن الكريم بعدة أصوات لمجموعة كبيرة من القراء.\nإمكانية تحميل القراء للاستماع بدون الحاجة إلى الإنترنت.\nتوفر الترجمات والتفاسير للقرآن الكريم، قابلة للتنزيل والاستخدام.\nإعراب الآيات أو الصور المحددة.\nالبحث السهل في القرآن الكريم.\n\n2. الأذكار\nقراءة أذكار الصباح والمساء وغيرها من الأذكار اليومية.\nإمكانية إرسال إشعارات تحتوي على ذكر صوتي أو كتابي بشكل عشوائي حسب المدة المحددة.\n\n3. السبحة الإلكترونية\nعداد إلكتروني للأذكار ليس له حدود للعد.\n\n4. محول التاريخ\nتحويل التاريخ من هجري إلى ميلادي والعكس بسهولة.\n\n5. معاني أسماء الله الحسنى\nاستعراض معاني أسماء الله الحسنى الموجودة في الأحاديث الصحيحة.\n\n6. الأحاديث الصحيحة\nقراءة وتحميل كتب الأحاديث الصحيحة.\nالبحث السهل في الأحاديث.\n\n7. الراديو الإسلامي\nاستماع إلى محطات إذاعية إسلامية تتعلق بالقرآن الكريم، التفسير، والعلوم الدينية.\n\n8. وضع العلامات المرجعية\nوضع علامات مرجعية للعودة إلى مكان القراءة سواء في القرآن أو الأحاديث.\n\n9. عرض مواقيت الصلاة والتاريخ الميلادي والهجري\nيعرض البرنامج مواقيت الصلاة والتاريخ الميلادي والهجري لليوم الحالي.\n\nاختصارات لوحة المفاتيح في Moslem Tools\n\nالتحكم في السبحة الإلكترونية\nCTRL + S: قراءة الرقم الحالي للسبحة لمستخدمي قارئ الشاشة.\n\nنسخ وتنسيق النصوص\nCTRL + A: نسخ كل النص.\nCTRL + C: نسخ النص المحدد.\nCTRL + S: الحفظ كملف نصي.\nCTRL + P: طباعة النص.\nCTRL + +: تكبير النص.\nCTRL + -: تصغير النص.\n\nالتحكم في القراءة والتشغيل\nزر المسافة (Space): تشغيل، إيقاف، أو إيقاف مؤقت.\nALT + السهم الأيمن: الانتقال إلى الذكر التالي، الآية التالية، أو الحديث التالي.\nALT + السهم الأيسر: العودة إلى الذكر السابق، الآية السابقة، أو الحديث السابق.\nCTRL + G: الانتقال مباشرة إلى آية أو حديث.\n\nالعلامات المرجعية\nزر الحذف (Delete): حذف العلامة المرجعية المحددة.\n\nتشغيل الإذاعات الإسلامية\nزر الإدخال (Enter): تشغيل أو إيقاف الإذاعة الحالية.\n\nاختصارات التحكم في المقطع للقرآن\nزر المسافة: تشغيل/إيقاف مؤقت\nإيقاف: CTRL + S\nالتقديم السريع لمدة 5 ثواني: ALT + السهم الأيمن\nالترجيع السريع لمدة 5 ثواني: ALT + السهم الأيسر\nالتقديم السريع لمدة 10 ثواني: ALT + السهم الأعلى\nالترجيع السريع لمدة 10 ثواني: ALT + السهم الأسفل\nالتقديم السريع لمدة 30 ثانية: CTRL + السهم الأيمن\nالترجيع السريع لمدة 30 ثانية: CTRL + السهم الأيسر\nالتقديم السريع لمدة دقيقة: CTRL + السهم الأعلى\nالترجيع السريع لمدة دقيقة: CTRL + السهم الأسفل\nاختصارات Ctrl + الرقم للانتقال مباشرة إلى نسبة محددة من المقطع، على سبيل المثال، Ctrl + 1 للانتقال إلى 10% من المقطع، Ctrl + 2 للانتقال إلى 20%، وهكذا\nرفع الصوت: SHIFT + السهم الأعلى\nخفض الصوت: SHIFT + السهم الأسفل\n\nالمطورين\nعبد الرحمن محمد، أنس محمد.\n\nالخاتمة\nبرنامج Moslem Tools هو رفيقك اليومي لتعزيز تجربتك الدينية، سواء كنت تقرأ القرآن، تستمع للأذكار، أو تبحث في الأحاديث. مع هذه الميزات المتنوعة والاختصارات العملية، ستجد البرنامج سهلاً ومفيداً."))
        self.guide.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.guide.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.guide.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))
        layout=qt.QVBoxLayout(self)        
        layout.addWidget(self.guide)
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        text_options=qt.QMenu(_("خيارات النص"),self)
        save=text_options.addAction(_("حفظ كملف نصي"))
        save.triggered.connect(self.save_text_as_txt)        
        print=text_options.addAction(_("طباعة"))
        print.triggered.connect(self.print_text)
        copy_all=text_options.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=text_options.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)        
        menu.addMenu(text_options)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.guide.print(printer)
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
                    text = self.guide.toPlainText()
                    file.write(text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
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
        cursor=self.guide.textCursor()
        self.guide.selectAll()
        font=self.guide.font()
        font.setPointSize(self.font_size)
        self.guide.setCurrentFont(font)        
        self.guide.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.guide.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.guide.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
class Albaheth(qt.QWidget):
    def __init__(self):
        super().__init__()                
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)        
        self.serch_laibol=qt.QLabel(_("ابحث في"))
        self.serch=qt.QComboBox()
        self.serch.addItem(_("القرآن الكريم"))
        self.serch.addItem(_("الأحاديث"))
        self.serch.setAccessibleName(_("ابحث في"))        
        self.ahadeeth_laibol=qt.QLabel(_("إختيار الكتاب"))
        self.ahadeeth=qt.QComboBox()
        self.ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())
        self.ahadeeth.setAccessibleName(_("إختيار الكتاب"))        
        self.serch.currentIndexChanged.connect(self.toggle_ahadeeth_visibility)
        self.serch_input=qt.QLineEdit()
        self.serch_input.setAccessibleName(_("أكتب محتوى البحث"))
        self.start=guiTools.QPushButton(_("البحث"))
        self.start.clicked.connect(self.onSearchClicked)
        self.results=guiTools.QReadOnlyTextEdit()                
        self.results.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.results.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.results.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))        
        self.show_font.setText(str(self.font_size))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.serch_laibol)
        layout.addWidget(self.serch)
        layout.addWidget(self.ahadeeth_laibol)
        layout.addWidget(self.ahadeeth)
        layout.addWidget(qt.QLabel(_("أكتب محتوى البحث")))
        layout.addWidget(self.serch_input)
        layout.addWidget(self.start)
        layout.addWidget(self.results)        
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        self.ahadeeth_laibol.hide()
        self.ahadeeth.hide()                    
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()        
        copy_all=menu.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=menu.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
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
        cursor=self.results.textCursor()
        self.results.selectAll()
        font=self.results.font()
        font.setPointSize(self.font_size)
        self.results.setCurrentFont(font)        
        self.results.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.results.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.results.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def search(self,pattern,text_list):    
        tashkeel_pattern=re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')        
        normalized_pattern=tashkeel_pattern.sub('', pattern)        
        matches=[
            text for text in text_list
            if normalized_pattern in tashkeel_pattern.sub('', text)
        ]        
        return matches        
    def onSearchClicked(self):
        I=self.serch.currentIndex()
        if I==0:
            listOfWords=functions.quranJsonControl.getQuran()
        elif I==1:
            bookName=functions.ahadeeth.ahadeeths[self.ahadeeth.currentText()]
            with open("data/json/ahadeeth/" + bookName,"r",encoding="utf-8") as file:
                ahadeeth=json.load(file)
            listOfWords=[]
            for item in ahadeeth:
                listOfWords.append(str(ahadeeth.index(item)+1) + item)
        result=self.search(self.serch_input.text(),listOfWords)
        if result:
            self.results.setText("عدد نتائج البحث " + str(len(result)) + "\n" + "\n".join(result))
        else:
            self.results.setText(_("لم يتم العثور على نتائج"))
        self.results.setFocus()
    def toggle_ahadeeth_visibility(self):
        if self.serch.currentText() == _("الأحاديث"):
            self.ahadeeth_laibol.show()
            self.ahadeeth.show()
        else:
            self.ahadeeth_laibol.hide()
            self.ahadeeth.hide()
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
class hadeeth(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_ahadeeth=guiTools.QListWidget()
        self.list_of_ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())
        self.list_of_ahadeeth.itemClicked.connect(self.open)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_ahadeeth)
    def open(self):
        gui.hadeeth_viewer(self,functions.ahadeeth.ahadeeths[self.list_of_ahadeeth.currentItem().text()]).exec()
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
class Quran(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("بحث")))
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        layout.addWidget(self.search_bar)
        layout.addWidget(qt.QLabel(_("التصفح ب")))
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("التصفح ب"))
        self.type.addItems([_("سور"),_("صفحات"),_("أجزاء"),_("أرباع"),_("أحزاب")])
        self.type.currentIndexChanged.connect(self.onTypeChanged)                
        layout.addWidget(self.type)        
        self.info=guiTools.QListWidget()
        self.info.clicked.connect(self.onItemTriggered)
        layout.addWidget(self.info)                
        self.onTypeChanged(0)
    def onsearch(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.info.count()):
            item = self.info.item(i)
            item.setHidden(search_text not in item.text().lower())    
    def onItemTriggered(self):
        index=self.type.currentIndex()
        if index==0:
            result=functions.quranJsonControl.getSurahs()
        elif index==1:
            result=functions.quranJsonControl.getPage()
        elif index==2:
            result=functions.quranJsonControl.getJuz()
        elif index==3:
            result=functions.quranJsonControl.getHezb()
        elif index==4:
            result=functions.quranJsonControl.getHizb()
        gui.QuranViewer(self,result[self.info.currentItem().text()][1],index,self.info.currentItem().text()).exec()
    def onTypeChanged(self,index:int):
        self.info.clear()
        if index==0:
            self.info.addItems(functions.quranJsonControl.getSurahs().keys())
        elif index==1:
            for i in range(1,605):
                self.info.addItem(str(i))
        elif index==2:
            for i in range(1,31):
                self.info.addItem(str(i))
        elif index==3:
            for i in range(1,241):
                self.info.addItem(str(i))
        elif index==4:
            for  i in range(1,61):
                self.info.addItem(str(i))
class About_developers(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.info=guiTools.QListWidget()
        self.info.itemClicked.connect(self.open_link)        
        self.info.addItem(_("عبد الرحمن محمد alcoder"))
        self.info.addItem(_("قناة عبد الرحمن على YouTube"))
        self.info.addItem(_("حساب عبد الرحمن على telegram"))
        self.info.addItem(_("حساب عبد الرحمن على GitHub"))
        self.info.addItem(_("أنس محمد"))
        self.info.addItem(_("قناة أنس على telegram"))
        self.info.addItem(_("حساب أنس على telegram"))
        self.info.addItem(_("حساب أنس على GitHub"))
        self.info.addItem(_("التواصل مع أنس عبر البريد الإكتروني"))        
        self.info_text=qt.QLineEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setText(_("اللهم اجعل عملنا هذا في ميزان حسناتنا وصدقة جارية لنا"))
        layout=qt.QVBoxLayout()
        layout.addWidget(self.info)
        layout.addWidget(self.info_text)
        self.setLayout(layout)                
    def open_link(self):    
        current_item=self.info.currentItem()
        if current_item:
            text=current_item.text()
            if text == _("قناة عبد الرحمن على YouTube"):
                webbrowser.open("https://youtube.com/@alcoder01?feature=shared")
            elif text == _("حساب عبد الرحمن على telegram"):
                webbrowser.open("https://t.me/P1_1_1")
            elif text == _("حساب عبد الرحمن على GitHub"):
                webbrowser.open("https://github.com/MesterAbdAlrhmanMohmed")
            elif text == _("قناة أنس على telegram"):
                webbrowser.open("https://t.me/tprogrammers")
            elif text == _("حساب أنس على telegram"):
                webbrowser.open("https://t.me/mesteranasm")
            elif text == _("حساب أنس على GitHub"):
                webbrowser.open("https://github.com/mesteranas/")
            elif text == _("التواصل مع أنس عبر البريد الإكتروني"):
                webbrowser.open("mailto:anasformohammed@gmail.com")
class sibha(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("ctrl+s",self).activated.connect(self.speak_number)
        self.reset=qt.QPushButton(_("إعادة تعين"))
        self.reset.setDefault(True)
        self.reset.clicked.connect(self.reset_count)  # ربط الزر بوظيفة إعادة التعيين
        self.numbers=qt.QLabel("0")
        self.numbers.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.numbers.setStyleSheet("font-size:300px;")
        self.add=qt.QPushButton(_("التسبيح"))
        self.add.setDefault(True)
        self.add.clicked.connect(self.increment_count)  # ربط الزر بوظيفة الزيادة
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
class NamesOfAllah(qt.QWidget):
    def __init__(self):
        super().__init__()
        with open("data/json/namesOfAllah.json","r",encoding="utf-8") as file:
            self.data=json.load(file)
        layout=qt.QVBoxLayout(self)
        self.information=guiTools.QReadOnlyTextEdit()
        result=""
        for item in self.data["names"]:
            result+=item["name"] + " : \n" + item["meaning"]+"\n"
        self.information.setText(result)
        self.information.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.information.customContextMenuRequested.connect(self.OnContextMenu)
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.information.setFont(font)
        self.font_laybol=qt.QLabel(_("حجم الخط"))
        self.show_font=qt.QLineEdit()
        self.show_font.setReadOnly(True)
        self.show_font.setAccessibleName(_("حجم النص"))                
        self.show_font.setText(str(self.font_size))
        layout.addWidget(self.information)
        layout.addWidget(self.font_laybol)
        layout.addWidget(self.show_font)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)        
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        text_options=qt.QMenu(_("خيارات النص"),self)
        save=text_options.addAction(_("حفظ كملف نصي"))
        save.triggered.connect(self.save_text_as_txt)        
        print=text_options.addAction(_("طباعة"))
        print.triggered.connect(self.print_text)
        copy_all=text_options.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=text_options.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)
        menu.addMenu(text_options)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def increase_font_size(self):
        self.font_size += 1
        guiTools.speak(str(self.font_size))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        guiTools.speak(str(self.font_size))
        self.show_font.setText(str(self.font_size))
        self.update_font_size()
    def update_font_size(self):
        cursor=self.information.textCursor()
        self.information.selectAll()
        font=self.information.font()
        font.setPointSize(self.font_size)
        self.information.setCurrentFont(font)        
        self.information.setTextCursor(cursor)
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.information.print(printer)
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
                    text = self.information.toPlainText()
                    file.write(text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_line(self):
        try:
            cursor=self.information.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.information.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))    
class prayer_times(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("ctrl+c",self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+a",self).activated.connect(self.copy_all_items)
        self.information=qt.QListWidget()        
        layout=qt.QVBoxLayout()
        layout.addWidget(self.information)        
        self.setLayout(layout)
        self.display_prayer_times()
    def copy_all_items(self):
        all_text="\n".join([self.information.item(i).text() for i in range(self.information.count())])
        pyperclip.copy(all_text)
        winsound.Beep(1000,100)
    def copy_selected_item(self):
        selected_item=self.information.currentItem()
        if selected_item:
            pyperclip.copy(selected_item.text())
            winsound.Beep(1000,100)
    def display_prayer_times(self):    
        gregorian_months=[
            "يَنَايِر", "فِبْرَايِر", "مَارِس", "أَبْرِيل",
            "مَايُو", "يُونْيُو", "يُولْيُو", "أَغُسْطُس",
            "سِبْتَمْبَر", "أُكْتُوبَر", "نُوفَمْبَر", "دِيسَمْبَر"
        ]
        hijri_months=[
            "مُحَرَّم", "صَفَر", "رَبِيع ٱلْأَوَّل", "رَبِيع ٱلثَّانِي",
            "جُمَادَىٰ ٱلْأُولَىٰ", "جُمَادَىٰ ٱلثَّانِيَة", "رَجَب", "شَعْبَان",
            "رَمَضَان", "شَوَّال", "ذُو ٱلْقَعْدَة", "ذُو ٱلْحِجَّة"
        ]        
        g=geocoder.ip('me')
        if g.ok:
            latitude=g.latlng[0]
            longitude=g.latlng[1]
            method=5
            response=requests.get('http://api.aladhan.com/v1/timings',params={
                'latitude': latitude,
                'longitude': longitude,
                'method': method
            })            
            if response.status_code == 200:
                data=response.json()['data']['timings']                
                prayers_ar={
                    'Fajr': _('الفجر'),
                    'Sunrise': _('الشروق'),
                    'Dhuhr': _('الظهر'),
                    'Asr': _('العصر'),
                    'Maghrib': _('المغرب'),
                    'Isha': _('العشاء')
                }                
                for prayer_en, prayer_ar in prayers_ar.items():
                    time_24h=data[prayer_en]
                    time_12h=datetime.strptime(time_24h, "%H:%M").strftime("%I:%M %p")
                    self.information.addItem(f"{prayer_ar}: {time_12h}")                
                now=datetime.now()
                gregorian_date=f"{now.day} {gregorian_months[now.month - 1]} {now.year}"                
                hijri_date_obj=Gregorian.today().to_hijri()
                hijri_date=f"{hijri_date_obj.day} {hijri_months[hijri_date_obj.month - 1]} {hijri_date_obj.year}"                
                self.information.addItem(_("التاريخ الميلادي: ") + gregorian_date)
                self.information.addItem(_("التاريخ الهجري: ") + hijri_date)
            else:
                self.information.addItem(_("حدث خطأ في جلب مواقيت الصلاة."))
        else:
            self.information.addItem(_("لم يتم تحديد الموقع الجغرافي. تأكد من اتصال الإنترنت."))
class DateConverter(qt.QWidget):
    def __init__(self):
        super().__init__()            
        self.l_Converter=qt.QLabel(_("إختيار نوع التحويل"))
        self.Converter_combo=qt.QComboBox()
        self.Converter_combo.setAccessibleName(_("إختيار نوع التحويل"))
        self.Converter_combo.addItem(_("التحويل من هجري الى ميلادي"))
        self.Converter_combo.addItem(_("التحويل من ميلادي الى هجري"))
        self.Converter_combo.currentIndexChanged.connect(self.update_month_combo)
        self.Converter_combo.currentIndexChanged.connect(self.update_button_text)
        self.l_year=qt.QLabel(_("العام"))
        self.year=qt.QLineEdit()
        self.year.setAccessibleName(_("العام"))
        self.l_month=qt.QLabel(_("الشهر"))
        self.month_combo=qt.QComboBox()
        self.month_combo.setAccessibleName(_("الشهر"))
        self.l_day=qt.QLabel(_("اليوم"))
        self.day=qt.QLineEdit()
        self.day.setAccessibleName(_("اليوم"))
        self.Convert=qt.QPushButton(_("التحويل الى ميلادي"))
        self.Convert.setDefault(True)
        self.Convert.clicked.connect(self.convert_date)
        self.l_result=qt.QLabel(_("النتيجة"))
        self.result=qt.QLineEdit()
        self.result.setReadOnly(True)
        self.result.setAccessibleName(_("النتيجة"))
        self.copy_result=qt.QPushButton(_("نسخ النتيجة"))
        self.copy_result.setDefault(True)
        self.copy_result.clicked.connect(self.copy)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.l_Converter)
        layout.addWidget(self.Converter_combo)
        layout.addWidget(self.l_year)
        layout.addWidget(self.year)
        layout.addWidget(self.l_month)
        layout.addWidget(self.month_combo)
        layout.addWidget(self.l_day)
        layout.addWidget(self.day)
        layout.addWidget(self.Convert)
        layout.addWidget(self.l_result)
        layout.addWidget(self.result)
        layout.addWidget(self.copy_result)
        self.setLayout(layout)
        self.update_month_combo()
    def copy(self):
        pyperclip.copy(self.result.text())
        winsound.Beep(1000,100)
    def update_button_text(self):        
        if self.Converter_combo.currentIndex() == 0:
            self.Convert.setText(_("التحويل الى ميلادي"))
        else:
            self.Convert.setText(_("التحويل الى هجري"))
    def update_month_combo(self):
        self.month_combo.clear()
        if self.Converter_combo.currentIndex() == 0:  # هجري إلى ميلادي
            months=[
            "مُحرَّم", "صَفَر", "رَبيع الأوَّل", "رَبيع الآخِر",
            "جُمادى الأُولى", "جُمادى الآخِرة", "رَجَب", "شَعبان",
            "رَمَضان", "شَوَّال", "ذو القَعدة", "ذو الحِجَّة"
        ]
        else:
            months=[
            "يَنايِر", "فَبرايِر", "مارِس", "أبريل", 
            "مايو", "يونيو", "يوليو", "أغسطس", 
            "سِبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        self.month_combo.addItems(months)
    def convert_date(self):        
        year_text=self.year.text()
        day_text=self.day.text()
        month=self.month_combo.currentIndex() + 1  # الشهر يبدأ من 1        
        if not (year_text.isdigit() and day_text.isdigit()):
            self.result.setFocus()
            self.result.setText(_("الرجاء إدخال أرقام صحيحة."))
            return    
        year=int(year_text)
        day=int(day_text)
        if self.Converter_combo.currentIndex() == 0:  # التحويل من هجري إلى ميلادي
            try:
                hijri_date=Hijri(year, month, day)
                gregorian_date=hijri_date.to_gregorian()
                result_str=f"{gregorian_date.day} {self.get_gregorian_month_name(gregorian_date.month)} {gregorian_date.year}"
                self.result.setFocus()
                self.result.setText(result_str)
            except Exception:
                self.result.setFocus()
                self.result.setText(_("تاريخ هجري غير صالح."))
        else:
            try:
                gregorian_date=Gregorian(year, month, day)
                hijri_date=gregorian_date.to_hijri()
                result_str=f"{hijri_date.day} {self.get_hijri_month_name(hijri_date.month)} {hijri_date.year}"
                self.result.setFocus()
                self.result.setText(result_str)
            except Exception:
                self.result.setFocus()
                self.result.setText(_("تاريخ ميلادي غير صالح."))                    

    def get_gregorian_month_name(self,month):
        months=[
            "يَنايِر", "فَبرايِر", "مارِس", "أبريل", 
            "مايو", "يونيو", "يوليو", "أغسطس", 
            "سِبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        return months[month - 1]
    def get_hijri_month_name(self,month):
        months=[
            "مُحرَّم", "صَفَر", "رَبيع الأوَّل", "رَبيع الآخِر",
            "جُمادى الأُولى", "جُمادى الآخِرة", "رَجَب", "شَعبان",
            "رَمَضان", "شَوَّال", "ذو القَعدة", "ذو الحِجَّة"
        ]
        return months[month - 1]
class Athker (qt.QWidget):
    def __init__(self):
        super().__init__()
        with open("data/json/athkar.json","r",encoding="utf-8-sig") as data:
            self.data=json.load(data)
        layout=qt.QVBoxLayout(self)
        self.athkerList=guiTools.QListWidget()
        for athker in self.data:
            self.athkerList.addItem(athker["name"])
        self.athkerList.clicked.connect(lambda:gui.AthkerDialog(self,self.athkerList.currentItem().text(),self.data[self.athkerList.currentRow()]["content"]).exec())
        layout.addWidget(self.athkerList)
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))        
        self.resize(1200,600)
        self.media_player=QMediaPlayer()
        self.audio_output=QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.timer=qt2.QTimer(self)
        self.timer.timeout.connect(self.random_audio_theker)
        layout=qt.QVBoxLayout()        
        self.tools=qt.QTabWidget()
        self.tools.addTab(prayer_times(),_("مواقيت الصلاة والتاريخ"))
        self.tools.addTab(Quran(),_("القرآن الكريم مكتوب"))        
        self.tools.addTab(QuranPlayer(),_("القرآن الكريم صوتي"))        
        self.tools.addTab(hadeeth(),_("الأحاديث النبوية والقدسية"))        
        self.tools.addTab(book_marcks(),_("العلامات المرجعية"))                        
        self.tools.addTab(Albaheth(),_("الباحث في القرآن والأحاديث"))
        self.tools.addTab(protcasts(),(_("الإذاعات الإسلامية")))        
        self.tools.addTab(Athker(),_("الأذكار والأدعية"))                                        
        self.tools.addTab(sibha(),(_("سبحة إلكترونية")))
        self.tools.addTab(NamesOfAllah(),_("أسماء الله الحُسْنة"))                                
        self.tools.addTab(DateConverter(),(_("محول التاريخ")))        
        self.tools.addTab(UserGuide(),(_("دليل المستخدم")))
        self.tools.addTab(About_developers(),(_("عن المطورين")))                
        self.tray_icon=qt.QSystemTrayIcon(self)
        self.tray_icon.setIcon(qt1.QIcon("data/icons/app_icon.jpg"))
        self.tray_icon.setToolTip(app.name)
        self.tray_menu=qt.QMenu(self)
        self.random_thecker_audio=qt1.QAction(_("تشغيل ذكر عشوائي"))
        self.random_thecker_audio.triggered.connect(self.random_audio_theker)        
        self.random_thecker_text=qt1.QAction(_("عرض ذكر عشوائي"))
        self.random_thecker_text.triggered.connect(self.show_random_theker)                
        self.show_action = qt1.QAction(_("إخفاء البرنامج"))
        self.show_action.triggered.connect(self.toggle_visibility)        
        self.close_action=qt1.QAction(_("إغلاق البرنامج"))
        self.close_action.triggered.connect(lambda:qt.QApplication.quit())
        self.tray_menu.addAction(self.random_thecker_audio)
        self.tray_menu.addAction(self.random_thecker_text)
        self.tray_menu.addAction(self.show_action)        
        self.tray_menu.addAction(self.close_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()    
        self.TIMER1=qt2.QTimer(self)
        self.TIMER1.timeout.connect(self.show_random_theker)        
        layout.addWidget(self.tools)            
        self.setting=guiTools.QPushButton(_("الإعدادات"))
        self.setting.clicked.connect(lambda: settings(self).exec())        
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.runAudioThkarTimer()
        self.notification_random_thecker()        
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)                    
    def toggle_visibility(self):        
        if self.isVisible():
            self.hide()
            self.show_action.setText(_("إظهار البرنامج"))
        else:
            self.show()
            self.show_action.setText(_("إخفاء البرنامج"))
    def show_random_theker(self):
        with open("data/json/text_athkar.json","r",encoding="utf_8") as f:
            data=json.load(f)
        random_theckr=random.choice(data)
        guiTools.SendNotification(_("ذكر عشوائي"),random_theckr)
    def notification_random_thecker(self):
        self.TIMER1.stop()
        if formatDuration("athkar","text")!=0:
            self.TIMER1.start(formatDuration("athkar","text"))
    def runAudioThkarTimer(self):
        self.timer.stop()
        if formatDuration("athkar","voice")!=0:
            self.timer.start(formatDuration("athkar","voice"))    
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def random_audio_theker(self):
        folder_path=r"data\sounds\athkar"
        sound_files=[f for f in os.listdir(folder_path) if f.endswith(('.ogg'))]
        if sound_files:
            chosen_file=random.choice(sound_files)
            file_path=os.path.join(folder_path,chosen_file)
            self.media_player.setSource(qt2.QUrl.fromLocalFile(file_path))
            self.media_player.play()    
App=qt.QApplication([])
App.setStyle('fusion')
w=main()
w.show()
App.setApplicationDisplayName(app.name)
App.setApplicationName(app.name)
App.setApplicationVersion(str(app.version))
App.setOrganizationName(app.creater)
App.setWindowIcon(qt1.QIcon("data/icons/app_icon.jpg"))
App.exec()