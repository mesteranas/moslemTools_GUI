import sys
from custome_errors import *
sys.excepthook=my_excepthook
import gui,update,guiTools,pyperclip,requests,geocoder,winsound
from settings import *
from hijri_converter import Gregorian
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
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
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        self.setGeometry(100,100,800,500)
        layout=qt.QVBoxLayout()        
        self.tools=qt.QTabWidget()
        self.tools.addTab(prayer_times(),_("مواقيت الصلاة والتاريخ"))
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
w=main()
w.show()
App.setStyle('fusion')
App.exec()