import os
import sys
import winreg as reg
import gui
import gettext
_=gettext.gettext
from settings import settings_handler,app
from settings import language
import PyQt6.QtWidgets as qt
language.init_translation()
class Genral(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        label=qt.QLabel(_("لغى التطبيق"))
        self.language=qt.QComboBox()
        self.language.setAccessibleName(_("لغى التطبيق"))
        self.language.addItems(language.lang().keys())
        languages={index:language for language, index in enumerate(language.lang().values())}
        try:
            self.language.setCurrentIndex(languages[settings_handler.get("g","lang")])
        except Exception as e:
            self.language.setCurrentIndex(0)
        self.ExitDialog=qt.QCheckBox(_("عرض نافذة الخروج عند الخروج من البرنامج"))
        self.ExitDialog.setChecked(p.cbts(settings_handler.get("g","exitDialog")))
        layout1=qt.QVBoxLayout(self)
        layout1.addWidget(label)
        layout1.addWidget(self.language)
        layout1.addWidget(self.ExitDialog)
        self.startup=qt.QCheckBox(_("بدء تشغيل البرنامج عند بدء تشغيل النظام"))
        self.startup.setChecked(self.check_in_startup())
        self.startup.checkStateChanged.connect(self.onStartupChanged)
        layout1.addWidget(self.startup)
        self.reciter=qt.QComboBox()
        self.reciter.addItems(gui.reciters.keys())
        self.reciter.setCurrentIndex(int(settings_handler.get("g","reciter")))
        self.reciter.setAccessibleName(_("تحديد القارئ للقرآن المكتوب"))
        layout1.addWidget(qt.QLabel(_("تحديد القارئ للقرآن المكتوب")))
        layout1.addWidget(self.reciter)

    def add_to_startup(self):
        try:
            app_name = app.appName
            app_path = sys.executable
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key, app_name, 0, reg.REG_SZ, app_path)
            reg.CloseKey(key)

            
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"),_("تعظر اتمام العملية"))

    def check_in_startup(self):
        try:
            app_name = app.appName
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_READ)
            index = 0

            while True:
                try:
                    name, value, _ = reg.EnumValue(key, index)
                    if name == app_name:
                        return True
                        reg.CloseKey(key)
                        return
                    index += 1
                except OSError:
                    break

            reg.CloseKey(key)
            return False
        except Exception as e:
            return False

    def remove_from_startup(self):
        try:
            app_name = app.appName
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.DeleteValue(key, app_name)
            reg.CloseKey(key)

            
        except FileNotFoundError:
            qt.QMessageBox.critical(self, _("خطأ"),_("تعظر اتمام العملية"))
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"),_("تعظر اتمام العملية"))


    def onStartupChanged(self,value):
        if value:
            self.add_to_startup()
        else:
            self.remove_from_startup()