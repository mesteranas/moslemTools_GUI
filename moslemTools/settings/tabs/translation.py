from functions import translater
from settings import settings_handler,app
import os,guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import gettext
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
        self.selecttranslation.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.selecttranslation.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
    def onDelete(self):
        selectedItem=self.selecttranslation.currentText()
        if selectedItem:
            itemText=selectedItem
            if itemText=="English by Talal Itani":
                qt.QMessageBox.critical(self,_("تنبيه"),_("لا يمكنك حذف هذا الكتاب "))
            else:
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا الكتاب"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    name=translater.translations[itemText]
                    os.remove(os.path.join(os.getenv('appdata'),app.appName,"Quran Translations",name))
                    translater.settranslation()
                    self.selecttranslation.clear()
                    self.selecttranslation.addItems(translater.translations.keys())
                    guiTools.speak(_("تم الحذف"))
