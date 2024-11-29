from functions import translater
from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import gettext
_=gettext.gettext
class translationSettings(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.selecttranslation=qt.QComboBox()
        self.selecttranslation.addItems(translater.translations.keys())
        self.selecttranslation.setCurrentText(translater.gettranslationByIndex(settings_handler.get("translation","translation")))
        self.selecttranslation.setAccessibleName(_("اختر ترجمة للقرآن الكريم"))
        layout.addWidget(qt.QLabel(_("اختر  ترجمة للقرآن الكريم")))
        layout.addWidget(self.selecttranslation)