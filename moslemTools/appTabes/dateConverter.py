import shutil,gui,update,guiTools,pyperclip,requests,geocoder,winsound,json,webbrowser,functions,time,random,os,re
from settings import *
from hijri_converter import Gregorian,Hijri
from datetime import datetime
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
language.init_translation()

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
        if self.Converter_combo.currentIndex() == 0:
            months=[
            _("مُحرَّم"), _("صَفَر"), _("رَبيع الأوَّل"), _("رَبيع الآخِر"),
            _("جُمادى الأُولى"), _("جُمادى الآخِرة"), _("رَجَب"), _("شَعبان"),
            _("رَمَضان"), _("شَوَّال"), _("ذو القَعدة"), _("ذو الحِجَّة")
        ]
        else:
            months=[
            _("يَنايِر"),
            _("فَبرايِر"),
            _("مارِس"),
            _("أبريل"),
            _("مايو"),
            _("يونيو"),
            _("يوليو"),
            _("أغسطس"),
            _("سِبتمبر"),
            _("أكتوبر"),
            _("نوفمبر"),
            _("ديسمبر"),
        ]
        self.month_combo.addItems(months)
    def convert_date(self):        
        year_text=self.year.text()
        day_text=self.day.text()
        month=self.month_combo.currentIndex() + 1
        if not (year_text.isdigit() and day_text.isdigit()):
            self.result.setFocus()
            self.result.setText(_("الرجاء إدخال أرقام صحيحة."))
            return    
        year=int(year_text)
        day=int(day_text)
        if self.Converter_combo.currentIndex() == 0:
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
            _("يَنايِر"),
            _("فَبرايِر"),
            _("مارِس"),
            _("أبريل"),
            _("مايو"),
            _("يونيو"),
            _("يوليو"),
            _("أغسطس"),
            _("سِبتمبر"),
            _("أكتوبر"),
            _("نوفمبر"),
            _("ديسمبر"),
        ]
        return months[month - 1]
    def get_hijri_month_name(self,month):
        months=[
            _("مُحرَّم"), _("صَفَر"), _("رَبيع الأوَّل"), _("رَبيع الآخِر"),
            _("جُمادى الأُولى"), _("جُمادى الآخِرة"), _("رَجَب"), _("شَعبان"),
            _("رَمَضان"), _("شَوَّال"), _("ذو القَعدة"), _("ذو الحِجَّة")
        ]
        return months[month - 1]
