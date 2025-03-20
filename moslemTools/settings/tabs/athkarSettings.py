from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class AthkarSettings(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.items=[_("5 دقائق"),_("10 دقائق"),_("20 دقيقة"),_("نصف ساعة"),_("ساعة"),_("إيقاف")]
        layout=qt.QVBoxLayout(self)
        self.voiceSelection_laybol=qt.QLabel(_("تشغيل الأذكار الصوتية كل"))
        self.voiceSelection_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.voiceSelection=qt.QComboBox()
        self.voiceSelection.addItems(self.items)
        self.voiceSelection.setCurrentIndex(int(settings_handler.get("athkar","voice")))
        self.voiceSelection.setAccessibleName(_("تشغيل الأذكار الصوتية كل"))
        self.voiceVolumeLabel=qt.QLabel(_("مستوا صوت الأذكار الصوتية"))
        self.voiceVolumeLabel.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.voiceVolume=qt.QSlider(qt2.Qt.Orientation.Horizontal)
        self.voiceVolume.setAccessibleName(_("مستوا صوت الأذكار الصوتية"))
        self.voiceVolume.setRange(0,100)
        self.voiceVolume.setValue(int(settings_handler.get("athkar","voiceVolume")))
        self.textSelection_laybol=qt.QLabel(_("عرض الأذكار النصية كل"))
        self.textSelection_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.textSelection=qt.QComboBox()
        self.textSelection.addItems(self.items)
        self.textSelection.setCurrentIndex(int(settings_handler.get("athkar","text")))
        self.textSelection.setAccessibleName(_("عرض الأذكار النصية كل"))
        self.info=qt.QLineEdit()
        self.info.setReadOnly(True)
        self.info.setText(_("تنبيه هام, حتى تظل الأذكار تعمل في الخلفية, يجب إخفاء البرنامج, لا الخروج منه"))
        self.info.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.voiceSelection_laybol)
        layout.addWidget(self.voiceSelection)        
        layout.addWidget(self.voiceVolumeLabel)
        layout.addWidget(self.voiceVolume)
        layout.addWidget(self.textSelection_laybol)
        layout.addWidget(self.textSelection)
        layout.addWidget(self.info)