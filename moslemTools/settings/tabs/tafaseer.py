from functions import tafseer
from settings import settings_handler
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class TafaseerSettings(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.selectTafaseer=qt.QComboBox()
        self.selectTafaseer.addItems(tafseer.tafaseers.keys())
        self.selectTafaseer.setCurrentText(tafseer.getTafaseerByIndex(settings_handler.get("tafaseer","tafaseer")))
        self.selectTafaseer.setAccessibleName(_("اختر تفسير"))
        layout.addWidget(qt.QLabel(_("اختر تفسير")))
        layout.addWidget(self.selectTafaseer)