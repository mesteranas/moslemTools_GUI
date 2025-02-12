from functions import tafseer
from settings import settings_handler,app
import os,guiTools
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
        self.selectTafaseer_laybol=qt.QLabel(_("اختر تفسير"))
        self.selectTafaseer_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selectTafaseer_laybol)
        layout.addWidget(self.selectTafaseer)
        self.selectTafaseer.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.selectTafaseer.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
    def onDelete(self):
        selectedItem=self.selectTafaseer.currentText()
        if selectedItem:
            itemText=selectedItem
            if itemText=="الميصر":
                qt.QMessageBox.critical(self,_("تنبيه"),_("لا يمكنك حذف هذا الكتاب "))
            else:
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا الكتاب"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    name=tafseer.tafaseers[itemText]
                    os.remove(os.path.join(os.getenv('appdata'),app.appName,"tafaseer",name))
                    tafseer.setTafaseer()
                    self.selectTafaseer.clear()
                    self.selectTafaseer.addItems(tafseer.tafaseers.keys())
                    guiTools.speak(_("تم الحذف"))
