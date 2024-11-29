from settings import settings_handler
import guiTools,gui,gettext
_=gettext.gettext
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class Download(qt.QDialog):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.types=guiTools.QListWidget()
        self.types.addItems([_("تفسير"),_("ترجمة قرآن"),_("كتاب حديث"),_("قارئ"),_("أذكار")])
        self.types.clicked.connect(self.onItemClicked)
        layout.addWidget(self.types)
    def onItemClicked(self):
        index=self.types.currentRow()
        if index==0:
            gui.download.SelectItem(self,"all_tafaseers.json","tafaseer").exec()
        elif index==1:    
            gui.download.SelectItem(self,"all_translater.json","Quran Translations").exec()
        elif index==2:    
            gui.download.SelectItem(self,"all_ahadeeth.json","ahadeeth").exec()        