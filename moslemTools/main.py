import sys
from custome_errors import *
sys.excepthook=my_excepthook
import gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,gettext,webbrowser,functions,time
from random import choice
_=gettext.gettext
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
language.init_translation()                
class hadeeth(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list_of_ahadeeth=guiTools.QListWidget()
        self.list_of_ahadeeth.addItem(_("صحيح البخاري"))                
        self.list_of_ahadeeth.itemClicked.connect(self.open)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_ahadeeth)
    def open(self):
        gui.hadeeth_viewer(self,"bukhari.json").exec()
class protcasts(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.list=guiTools.QListWidget()
        self.list.itemClicked.connect(self.play_procast)
        self.list.addItem(_("إذاعة القرآن الكريم من القاهرة"))                        
        self.list.addItem(_("إذاعة القرآن الكريم من السعودية"))
        self.list.addItem(_("إذاعة القرآن الكريم من دبي"))
        self.list.addItem(_("إذاعة للقرآن الكريم"))
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
        gui.QuranViewer(self,result[self.info.currentItem().text()][1])
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
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.information.setFont(font)
        layout.addWidget(self.information)
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)
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
        cursor=self.information.textCursor()
        self.information.selectAll()
        font=self.information.font()
        font.setPointSize(self.font_size)
        self.information.setCurrentFont(font)        
        self.information.setTextCursor(cursor)
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
        self.Converter_combo.currentIndexChanged.connect(self.update_button_text)  # ربط تغيير النص بالاختيار        
        self.l_year=qt.QLabel(_("العام"))
        self.year=qt.QLineEdit()
        self.year.setAccessibleName(_("العام"))    
        self.l_month=qt.QLabel(_("الشهر"))
        self.month=qt.QLineEdit()
        self.month.setAccessibleName(_("الشهر"))            
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
        layout.addWidget(self.month)
        layout.addWidget(self.l_day)
        layout.addWidget(self.day)
        layout.addWidget(self.Convert)
        layout.addWidget(self.l_result)
        layout.addWidget(self.result)
        layout.addWidget(self.copy_result)
        self.setLayout(layout)
    def copy(self):
        pyperclip.copy(self.result.text())
        winsound.Beep(1000,100)
    def update_button_text(self):        
        if self.Converter_combo.currentIndex() == 0:
            self.Convert.setText(_("التحويل الى ميلادي"))
        else:
            self.Convert.setText(_("التحويل الى هجري"))
    def convert_date(self):        
        year_text=self.year.text()
        month_text=self.month.text()
        day_text=self.day.text()            
        if not (year_text.isdigit() and month_text.isdigit() and day_text.isdigit()):
            self.result.setFocus()
            self.result.setText(_("الرجاء إدخال أرقام صحيحة."))
            return    
        year=int(year_text)
        month=int(month_text)
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
    def get_gregorian_month_name(self, month):
        months=[
            "يناير", "فبراير", "مارس", "أبريل",
            "مايو", "يونيو", "يوليو", "أغسطس",
            "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        return months[month - 1]
    def get_hijri_month_name(self, month):
        months=[
            "محرم", "صفر", "ربيع الأول", "ربيع الآخر",
            "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
            "رمضان", "شوّال", "ذو القعدة", "ذو الحجة"
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
        self.setGeometry(100,100,800,500)
        layout=qt.QVBoxLayout()        
        self.tools=qt.QTabWidget()
        self.tools.addTab(prayer_times(),_("مواقيت الصلاة والتاريخ"))
        self.tools.addTab(DateConverter(),(_("محول التاريخ")))
        self.tools.addTab(sibha(),(_("سبحة إلكترونية")))
        self.tools.addTab(NamesOfAllah(),_("أسماء الله الحُسْنة"))
        self.tools.addTab(Athker(),_("الأذكار والأدعية"))
        self.tools.addTab(Quran(),_("القرآن الكريم"))        
        self.tools.addTab(hadeeth(),_("الأحاديث النبوية والقدسية"))
        self.tools.addTab(protcasts(),(_("الإذاعات الإسلامية")))
        self.tools.addTab(About_developers(),(_("عن المطورين")))
        layout.addWidget(self.tools)
        self.setting=guiTools.QPushButton(_("الإعدادات"))
        self.setting.clicked.connect(lambda: settings(self).exec())        
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
App=qt.QApplication([])
App.setStyle('fusion')
w=main()
w.show()
App.setApplicationDisplayName(app.name)
App.setApplicationName(app.name)
App.setApplicationVersion(str(app.version))
App.setOrganizationName(app.creater)
App.exec()