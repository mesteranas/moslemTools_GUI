from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class QuranPlayerSettings(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.times=qt.QSpinBox()
        self.times.setRange(1,10)
        self.times.setValue(int(settings_handler.get("quranPlayer","times")))
        self.times.setAccessibleName(_("عدد مرات تكرار الآيات"))
        layout.addWidget(qt.QLabel(_("عدد مرات تكرار الآيات")))
        layout.addWidget(self.times)
        self.duration=qt.QLineEdit()
        self.duration.setInputMask("999")
        self.duration.setText(settings_handler.get("quranPlayer","duration"))
        self.duration.setAccessibleName(_("مدة الانتظار بين التكرار بالثواني"))
        layout.addWidget(qt.QLabel(_("مدة الانتظار بين التكرار بالثواني")))
        layout.addWidget(self.duration)