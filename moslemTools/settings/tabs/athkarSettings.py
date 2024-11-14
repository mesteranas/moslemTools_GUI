from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class AthkarSettings(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.items=[_("5 دقائق"),_("10 دقائق"),_("20 دقيقة"),_("نصف ساعة"),_("ساعة"),_("إيقاف")]
        layout=qt.QVBoxLayout(self)
        self.voiceSelection=qt.QComboBox()
        self.voiceSelection.addItems(self.items)
        self.voiceSelection.setCurrentIndex(int(settings_handler.get("athkar","voice")))
        self.voiceSelection.setAccessibleName(_("مدة تشغيل الأذكار الصوتية"))
        layout.addWidget(qt.QLabel(_("مدة تشغيل الأذكار الصوتية")))
        layout.addWidget(self.voiceSelection)