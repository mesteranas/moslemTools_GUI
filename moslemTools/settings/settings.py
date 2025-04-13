import guiTools, update, functions
import sys
import os, shutil, gettext
from . import settings_handler, app, tabs
from . import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class settings(qt.QDialog):
    def __init__(self, p):
        super().__init__(p)
        self.resize(600,300)
        self.setWindowTitle(_("الإعدادات"))
        self.p = p        
        layout = qt.QVBoxLayout()        
        self.sectian = guiTools.ComboBook()
        self.sectian.setStyleSheet("color: #e0e0e0;")
        self.sectian.setAccessibleName(_("اختر قسم"))
        layout.addWidget(self.sectian)
        layout.addWidget(self.sectian.w)        
        self.update = tabs.Update(self)        
        buttonsLayout = qt.QHBoxLayout()
        self.ok = qt.QPushButton(_("موافق"))
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.fok)
        self.ok.setStyleSheet("background-color: #4CAF50; color: #e0e0e0; padding: 8px; font-weight: bold;")        
        self.defolt = qt.QPushButton(_("استعادة الإعدادات الإفتراضية"))
        self.defolt.clicked.connect(self.default)
        self.defolt.setStyleSheet("background-color: #F44336; color: #e0e0e0; padding: 8px; font-weight: bold;")        
        self.cancel = qt.QPushButton(_("إلغاء"))
        self.cancel.clicked.connect(self.fcancel)        
        self.cancel.setStyleSheet("background-color: #808080; color: #e0e0e0; padding: 8px; font-weight: bold;")        
        self.layout1 = tabs.Genral(self)
        self.sectian.add(_("عام"), self.layout1)
        self.tafaseerSettings = tabs.TafaseerSettings()
        self.sectian.add(_("إعدادات التفسير والترجمة"), self.tafaseerSettings)
        self.prayerTimesSettings = tabs.PrayerTimesSettings(self)
        self.sectian.add(_("إعدادات الأذان"), self.prayerTimesSettings)
        self.quranPlayerTimes = tabs.QuranPlayerSettings(self)
        self.sectian.add(_("إعدادات مشغل القرآن للقرآن المكتوب"), self.quranPlayerTimes)
        self.sectian.add(_("إعدادات التحديثات"), self.update)
        self.sectian.add(_("تحميل موارد"), tabs.Download())
        self.athkar = tabs.AthkarSettings()
        self.sectian.add(_("إعدادات الأذكار"), self.athkar)
        restoar = tabs.Restoar(self)
        self.sectian.add(_("النسخ الاحتياطي والاستعادةة"), restoar)        
        buttonsLayout.addWidget(self.ok)
        buttonsLayout.addWidget(self.defolt)
        buttonsLayout.addWidget(self.cancel)
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)
    def fok(self):
        aa = 0
        if settings_handler.get("g", "lang") != str(language.lang()[self.layout1.language.currentText()]):
            aa = 1
        settings_handler.set("g", "lang", str(language.lang()[self.layout1.language.currentText()]))
        settings_handler.set("g", "exitDialog", str(self.layout1.ExitDialog.isChecked()))
        settings_handler.set("g", "reciter", str(self.layout1.reciter.currentIndex()))
        try:
            settings_handler.set("tafaseer", "tafaseer", functions.tafseer.tafaseers[self.tafaseerSettings.selectTafaseer.currentText()])
        except:
            pass
        try:
            settings_handler.set("translation", "translation", functions.translater.translations[self.tafaseerSettings.selecttranslation.currentText()])
        except:
            pass
        settings_handler.set("athkar", "voice", str(self.athkar.voiceSelection.currentIndex()))
        settings_handler.set("athkar", "text", str(self.athkar.textSelection.currentIndex()))
        settings_handler.set("quranPlayer", "times", str(self.quranPlayerTimes.times.value()))
        settings_handler.set("quranPlayer", "duration", self.quranPlayerTimes.duration.text())
        settings_handler.set("prayerTimes", "adaanReminder", str(self.prayerTimesSettings.adaanReminder.isChecked()))
        settings_handler.set("update", "autoCheck", str(self.update.update_autoDect.isChecked()))
        settings_handler.set("athkar", "voiceVolume", str(self.athkar.voiceVolume.value()))
        settings_handler.set("quranPlayer", "replay", str(self.quranPlayerTimes.replay.isChecked()))
        settings_handler.set("update", "beta", str(self.update.update_beta.isChecked()))
        settings_handler.set("prayerTimes", "playPrayerAfterAdhaan", str(self.prayerTimesSettings.playPrayerAfterAdhaan.isChecked()))
        self.p.runAudioThkarTimer()
        self.p.notification_random_thecker()
        self.p.audio_output.setVolume(int(settings_handler.get("athkar", "voiceVolume")) / 100)
        if aa == 1:
            mb = qt.QMessageBox(self)
            mb.setWindowTitle(_("تم تحديث الإعدادات"))
            mb.setText(_("يجب عليك إعادة تشغيل البرنامج لتطبيق التغييرات. هل تريد إعادة التشغيل الآن؟"))
            rn = mb.addButton(qt.QMessageBox.StandardButton.Yes)
            rn.setText(_("إعادة التشغيل الآن"))
            rl = mb.addButton(qt.QMessageBox.StandardButton.No)
            rl.setText(_("إعادة التشغيل لاحقا"))
            mb.exec()
            ex = mb.clickedButton()
            if ex == rn:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif ex == rl:
                self.close()
        else:
            self.close()
    def default(self):
        mb = qt.QMessageBox(self)
        mb.setWindowTitle(_("تنبيه"))
        mb.setText(_("هل تريد إعادة تعيين إعداداتك؟ إذا قمت بالنقر على إعادة تعيين، سيعيد البرنامج التشغيل لإكمال إعادة التعيين."))
        rn = mb.addButton(qt.QMessageBox.StandardButton.Yes)
        rn.setText(_("إعادة التعيين وإعادة التشغيل"))
        rl = mb.addButton(qt.QMessageBox.StandardButton.No)
        rl.setText(_("إلغاء"))
        mb.exec()
        ex = mb.clickedButton()
        if ex == rn:
            os.remove(os.path.join(os.getenv('appdata'), app.appName, "settings.ini"))
            os.execl(sys.executable, sys.executable, *sys.argv)
    def fcancel(self):
        self.close()
    def cbts(self, string):
        return True if string == "True" else False
def formatDuration(sectionName: str, keyName: str):
    value = int(settings_handler.get(sectionName, keyName))
    result = 0
    if value == 0:
        result = 300
    elif value == 1:
        result = 600
    elif value == 2:
        result = 1200
    elif value == 3:
        result = 1800
    elif value == 4:
        result = 3600
    return result * 1000