import guiTools, update, functions,gui
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
        self.resize(600,400)
        self.center()
        self.setWindowTitle(_("الإعدادات"))
        self.p = p        
        layout = qt.QVBoxLayout()        
        self.sectian = guiTools.ComboBook()
        font = qt1.QFont()
        font.setBold(True)        
        self.sectian.setStyleSheet("color: #e0e0e0;")
        self.sectian.setAccessibleName(_("اختر قسم"))
        self.sectian.setFont(font)
        layout.addWidget(self.sectian)
        layout.addWidget(self.sectian.w)        
        self.update = tabs.Update(self)        
        buttonsLayout = qt.QHBoxLayout()
        self.ok = qt.QPushButton(_("موافق"))
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.fok)
        self.ok.setStyleSheet("background-color: #006400; color: #e0e0e0; padding: 12px; font-weight: bold;")        
        self.defolt = qt.QPushButton(_("استعادة الإعدادات الإفتراضية"))
        self.defolt.clicked.connect(self.default)
        self.defolt.setStyleSheet("background-color: #8B0000; color: #e0e0e0; padding: 12px; font-weight: bold;")        
        self.cancel = qt.QPushButton(_("إلغاء"))
        self.cancel.clicked.connect(self.fcancel)        
        self.cancel.setStyleSheet("background-color: #333333; color: #e0e0e0; padding: 12px; font-weight: bold;")        
        self.layout1 = tabs.Genral(self)
        self.sectian.add(_("عام"), self.layout1)
        self.tafaseerSettings = tabs.TafaseerSettings()
        self.sectian.add(_("إعدادات التفسير والترجمة"), self.tafaseerSettings)
        self.prayerTimesSettings = tabs.PrayerTimesSettings(self)
        self.sectian.add(_("إعدادات الأذان"), self.prayerTimesSettings)
        self.locationSettings=tabs.LocationSettings(self)
        self.sectian.add(_("إعدادات تحديد الموقع الجغرافي لمواقيت الصلاة"),self.locationSettings)
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
    def center(self):        
        frame_geometry = self.frameGeometry()        
        screen_center = qt1.QGuiApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)        
        self.move(frame_geometry.topLeft())
    def fok(self):
        aa = 0
        if settings_handler.get("g", "lang") != str(language.lang()[self.layout1.language.currentText()]):
            aa = 1
        settings_handler.set("g", "lang", str(language.lang()[self.layout1.language.currentText()]))
        settings_handler.set("g", "exitDialog", str(self.layout1.ExitDialog.isChecked()))
        settings_handler.set("g", "reciter", str(list(gui.reciters.keys()).index(self.layout1.reciter.currentText())))
        settings_handler.set("prayerTimes","volume",str(self.prayerTimesSettings.Sound_level.value()))
        settings_handler.set("location","autoDetect",str(self.locationSettings.autoDetectLocation.isChecked()))
        settings_handler.set("location","LT1",str(self.locationSettings.LT1.value()))
        settings_handler.set("location","LT2",str(self.locationSettings.LT2.value()))
        settings_handler.set("prayerTimes","remindBeforeAdaan",str(self.prayerTimesSettings.before.currentIndex()))
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
            mb = guiTools.QQuestionMessageBox.view(self,_("تم تحديث الإعدادات"),_("يجب عليك إعادة تشغيل البرنامج لتطبيق التغييرات. هل تريد إعادة التشغيل الآن؟"),_("إعادة التشغيل الآن"),_("إعادة التشغيل لاحقا"))
            if mb==0:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                self.close()
        else:
            self.close()
    def default(self):
        mb = guiTools.QQuestionMessageBox.view(self,_("تنبيه"),_("هل تريد إعادة تعيين إعداداتك؟ إذا قمت بالنقر على إعادة تعيين، سيعيد البرنامج التشغيل لإكمال إعادة التعيين."),_("إعادة التعيين وإعادة التشغيل"),_("إلغاء"))
        if mb==0:
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