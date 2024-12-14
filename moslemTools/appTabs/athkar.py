import gui,guiTools,os,json
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Athker(qt.QWidget):
    def __init__(self):
        super().__init__()
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
        with open("data/json/athkar.json","r",encoding="utf-8-sig") as data:
            self.data=json.load(data)
        layout=qt.QVBoxLayout(self)
        self.athkerList=guiTools.QListWidget()
        for athker in self.data:
            self.athkerList.addItem(athker["name"])
        self.athkerList.clicked.connect(lambda:gui.AthkerDialog(self,self.athkerList.currentItem().text(),self.data[self.athkerList.currentRow()]["content"]).exec())        
        self.athkerList.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.athkerList.customContextMenuRequested.connect(self.onDelete)
        layout.addWidget(self.athkerList)
    def onDelete(self):
        itemText=self.athkerList.currentItem()
        if itemText:
            reciterText=itemText.text()
            path=os.path.join(os.getenv('appdata'),app.appName,"athkar",reciterText)
            if os.path.exists(path):
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف الأذكار الصوتية"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    shutil.rmtree(path)
                    guiTools.speak(_("تم الحذف"))