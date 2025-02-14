import gui,guiTools,functions,os
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class hadeeth(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("f5",self).activated.connect(self.refresh)
        self.list_of_ahadeeth=guiTools.QListWidget()
        self.list_of_ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())
        self.list_of_ahadeeth.itemClicked.connect(self.open)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.list_of_ahadeeth)
        self.info=qt.QLineEdit()
        self.info.setReadOnly(True)
        self.info.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.info.setText(_("في حالة تحميل كتاب جديد, يرجى إعادة تحميل قائمة الكتب بالضغت على زر F5"))
        layout.addWidget(self.info)
        self.list_of_ahadeeth.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_of_ahadeeth.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
    def onDelete(self):
        selectedItem=self.list_of_ahadeeth.currentItem()
        if selectedItem:
            itemText=selectedItem.text()
            if itemText=="الأربعون نووية" or itemText=="الأربعون قُدسية":
                qt.QMessageBox.critical(self,_("تنبيه"),_("لا يمكنك حذف هذا الكتاب "))
            else:
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا الكتاب"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    name=functions.ahadeeth.ahadeeths[itemText]
                    os.remove(os.path.join(os.getenv('appdata'),app.appName,"ahadeeth",name))
                    functions.ahadeeth.setahadeeth()
                    self.list_of_ahadeeth.clear()
                    self.list_of_ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())
                    guiTools.speak(_("تم الحذف"))
    def open(self):
        gui.hadeeth_viewer(self,functions.ahadeeth.ahadeeths[self.list_of_ahadeeth.currentItem().text()]).exec()
    def refresh(self):
        functions.ahadeeth.setahadeeth()
        self.list_of_ahadeeth.clear()
        self.list_of_ahadeeth.addItems(functions.ahadeeth.ahadeeths.keys())