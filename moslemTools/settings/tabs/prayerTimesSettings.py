from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import os,shutil
class PrayerTimesSettings(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.adaanReminder=qt.QCheckBox(_("التنبيه بالأذان"))
        self.adaanReminder.setChecked(p.cbts(settings_handler.get("prayerTimes","adaanReminder")))
        self.adaanReminder.stateChanged.connect(self.onprayerTimesReminderCheckboxStateChanged)
        layout.addWidget(self.adaanReminder)
        self.changeFajrSound=qt.QPushButton(_("تغيير صوت أذان الفجر"))
        self.changeFajrSound.setVisible(p.cbts(settings_handler.get("prayerTimes","adaanReminder")))
        self.changeFajrSound.clicked.connect(lambda:self.onChangeAdaanButtonClicked("fajr.mp3"))
        layout.addWidget(self.changeFajrSound)
        self.changeAdaanSound=qt.QPushButton(_("تغيير صوت الأذان"))
        self.changeAdaanSound.setVisible(p.cbts(settings_handler.get("prayerTimes","adaanReminder")))
        self.changeAdaanSound.clicked.connect(lambda:self.onChangeAdaanButtonClicked("genral.mp3"))
        layout.addWidget(self.changeAdaanSound)
        self.worning=qt.QLineEdit()
        self.worning.setReadOnly(True)
        self.worning.setVisible(p.cbts(settings_handler.get("prayerTimes","adaanReminder")))
        self.worning.setText(_("تنبيه هام, في حالة اختيار صوت للأذان من الجهاز, الرجاء اختيار ملف صوتي بامتداد .mp3"))
        self.worning.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.worning)
    def onprayerTimesReminderCheckboxStateChanged(self,state):
        self.changeAdaanSound.setVisible(state)
        self.changeFajrSound.setVisible(state)
        self.worning.setVisible(state)
    def onChangeAdaanButtonClicked(self,adaanName):
        contextMenu=qt.QMenu(_("اختر صوت"),self)
        contextMenu.setAccessibleName(_("اختر صوت"))
        default=qt1.QAction(_("الأذان الإفتراضي"),self)
        contextMenu.addAction(default)
        contextMenu.setDefaultAction(default)
        default.triggered.connect(lambda:self.onDefaultActionTriggered(adaanName))
        chooseFromDevice=qt1.QAction(_("اختر من الجهاز"),self)
        contextMenu.addAction(chooseFromDevice)
        chooseFromDevice.triggered.connect(lambda:self.onChooseFromDevice(adaanName))
        contextMenu.setFocus()
        mouse_position=qt1.QCursor.pos()
        contextMenu.exec(mouse_position)
    def onDefaultActionTriggered(self,adaanName):
        path=os.path.join(os.getenv('appdata'),settings_handler.appName,"addan",adaanName)
        try:
            os.remove(path)
            shutil.copy("data/sounds/adaan/" + adaanName,path)
            qt.QMessageBox.information(self,_("تم"),_("تم تغيير صوت الأذان بنجاح"))
        except:
            qt.QMessageBox.critical(self,_("خطأ"),_("حدث خطأ غير متوقع"))
    def onChooseFromDevice(self,adaanName):
        path=os.path.join(os.getenv('appdata'),settings_handler.appName,"addan",adaanName)
        fileDialog=qt.QFileDialog(self,_("اختر صوت"))
        fileDialog.setDefaultSuffix("mp3")
        fileDialog.setNameFilters(["audio files(*.mp3)"])
        if fileDialog.exec()==fileDialog.DialogCode.Accepted:
            try:
                os.remove(path)
                shutil.copy(fileDialog.selectedFiles()[0],path)
                qt.QMessageBox.information(self,_("تم"),_("تم تغيير صوت الأذان بنجاح"))
            except:
                qt.QMessageBox.critical(self,_("خطأ"),_("حدث خطأ غير متوقع"))