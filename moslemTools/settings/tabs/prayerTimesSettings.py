from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class PrayerTimesSettings(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.adaanReminder=qt.QCheckBox(_("التنبيه بالآذان"))
        self.adaanReminder.setChecked(p.cbts(settings_handler.get("prayerTimes","adaanReminder")))
        layout.addWidget(self.adaanReminder)