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
        self.reciter=qt.QComboBox()
        self.reciter.addItems(gui.reciters.keys())
        self.reciter.setCurrentIndex(int(settings_handler.get("g","reciter")))
        self.reciter.setAccessibleName(_("تحديد القارئ للقرآن المكتوب"))
        layout1.addWidget(qt.QLabel(_("تحديد القارئ للقرآن المكتوب")))
        layout1.addWidget(self.reciter)