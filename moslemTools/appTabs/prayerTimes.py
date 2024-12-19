import pyperclip,requests,geocoder,winsound,gui
from settings import settings_handler
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
        qt1.QShortcut("f5",self).activated.connect(self.display_prayer_times)
        self.prayers=[]
        self.times=[]
        self.timer=qt2.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.information=qt.QListWidget()        
        layout=qt.QVBoxLayout()
        layout.addWidget(self.information)        
        self.setLayout(layout)
        self.display_prayer_times()
    def onTimer(self):
        currentTime=datetime.now().strftime("%I:%M %p")
        for time in self.times:
            if currentTime==time:
                if self.times.index(time)==1:
                    return
                if settings_handler.get("prayerTimes","adaanReminder")=="True":
                    gui.AdaanDialog(self,self.times.index(time),self.prayers[self.times.index(time)]).exec()
                    self.timer.stop()
                    self.timer.singleShot(60000,qt2.Qt.TimerType.PreciseTimer,lambda:self.timer.start(10000))
                    return
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
        self.information.clear()
        gregorian_months=[
            _("يَنَايِر"),
            _("فِبْرَايِر"),
            _("مَارِس"),
            _("أَبْرِيل"),
            _("مَايُو"),
            _("يُونْيُو"),
            _("يُولْيُو"),
            _("أَغُسْطُس"),
            _("سِبْتَمْبَر"),
            _("أُكْتُوبَر"),
            _("نُوفَمْبَر"),
            _("دِيسَمْبَر"),
        ]
        hijri_months=[
            _("مُحَرَّم"),
            _("صَفَر"),
            _("رَبِيع ٱلْأَوَّل"),
            _("رَبِيع ٱلثَّانِي"),
            _("جُمَادَىٰ ٱلْأُولَىٰ"),
            _("جُمَادَىٰ ٱلثَّانِيَة"),
            _("رَجَب"),
            _("شَعْبَان"),
            _("رَمَضَان"),
            _("شَوَّال"),
            _("ذُو ٱلْقَعْدَة"),
            _("ذُو ٱلْحِجَّة"),
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
                self.prayers=list(prayers_ar.values())
                self.times=["03:40 PM"]
                self.timer.start(10000)
                for prayer_en, prayer_ar in prayers_ar.items():
                    time_24h=data[prayer_en]
                    time_12h=datetime.strptime(time_24h, "%H:%M").strftime("%I:%M %p")
                    self.times.append(time_12h)
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