import sys
from custome_errors import *
sys.excepthook=my_excepthook
import gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,gettext
_=gettext.gettext
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
class NamesOfAllah(qt.QWidget):
    def __init__(self):
        super().__init__()
        with open("data/json/namesOfAllah.json","r",encoding="utf-8") as file:
            self.data=json.load(file)
        layout=qt.QVBoxLayout(self)
        self.information=qt.QListWidget()
        for item in self.data["names"]:
            self.information.addItem(item["name"] + " : \n" + item["meaning"])
        layout.addWidget(self.information)
        qt1.QShortcut("ctrl+c",self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+a",self).activated.connect(self.copy_all_items)
    def copy_all_items(self):
        all_text="\n".join([self.information.item(i).text() for i in range(self.information.count())])
        guiTools.clikboard.copyText(all_text)
        winsound.Beep(1000,100)
    def copy_selected_item(self):
        selected_item=self.information.currentItem()
        if selected_item:
            guiTools.clikboard.copyText(selected_item.text())
            winsound.Beep(1000,100)

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
        guiTools.clikboard.copyText(all_text)
        winsound.Beep(1000,100)
    def copy_selected_item(self):
        selected_item=self.information.currentItem()
        if selected_item:
            guiTools.clikboard.copyText(selected_item.text())
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
            response=requests.get('http://api.aladhan.com/v1/timings', params={
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
                self.result.setText(result_str)
            except Exception:
                self.result.setText(_("تاريخ هجري غير صالح."))
        else:
            try:
                gregorian_date=Gregorian(year, month, day)
                hijri_date=gregorian_date.to_hijri()
                result_str=f"{hijri_date.day} {self.get_hijri_month_name(hijri_date.month)} {hijri_date.year}"
                self.result.setText(result_str)
            except Exception:
                self.result.setText(_("تاريخ ميلادي غير صالح."))            
        self.result.setFocus()
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
        self.tools.addTab(NamesOfAllah(),_("أسماء الله الحُسْنة"))
        self.tools.addTab(Athker(),_("الأذكار والأدعية"))
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
App.exec()