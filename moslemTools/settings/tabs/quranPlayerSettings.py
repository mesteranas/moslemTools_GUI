from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class QuranPlayerSettings(qt.QWidget):
    def __init__(self, p):
        super().__init__()
        self.setStyleSheet("""            
            }
            QSpinBox, QLineEdit, QCheckBox, QLabel {                
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 4px;
                font-size: 13px;
            }
        """)
        layout = qt.QVBoxLayout(self)
        self.times = qt.QSpinBox()
        self.times.setRange(1, 10)
        self.times.setValue(int(settings_handler.get("quranPlayer", "times")))
        self.times.setAccessibleName(_("عدد مرات تكرار الآيات"))
        self.times.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.times_laybol = qt.QLabel(_("عدد مرات تكرار الآيات"))
        self.times_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.times_laybol)
        layout.addWidget(self.times)
        self.duration = qt.QLineEdit()
        self.duration.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.duration.setInputMask("999")
        self.duration.setText(settings_handler.get("quranPlayer", "duration"))
        self.duration.setAccessibleName(_("مدة الانتظار بين التكرار بالثواني"))
        self.duration_laybol = qt.QLabel(_("مدة الانتظار بين التكرار بالثواني"))
        self.duration_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.duration_laybol)
        layout.addWidget(self.duration)
        self.replayLabel = qt.QLabel(_("في حالة اختيار التشغيل الى نهاية الفئة أو التشغيل من آية الى آية"))
        self.replayLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.replayLabel)
        self.replay = qt.QCheckBox(_("إعادة القراءة بعد الانتهاء"))
        self.replay.setAccessibleDescription(_("في حالة اختيار التشغيل الى نهاية الفئة أو التشغيل من آية الى آية"))
        self.replay.setChecked(p.cbts(settings_handler.get("quranPlayer", "replay")))
        layout.addWidget(self.replay)