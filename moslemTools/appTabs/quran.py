import gui,guiTools,functions
from settings import *
import PyQt6.QtWidgets as qt
language.init_translation()
class Quran(qt.QWidget):
    def __init__(self):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        layout.addWidget(qt.QLabel(_("بحث")))
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        layout.addWidget(self.search_bar)
        layout.addWidget(qt.QLabel(_("التصفح ب")))
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("التصفح ب"))
        self.type.addItems([_("سور"),_("صفحات"),_("أجزاء"),_("أرباع"),_("أحزاب")])
        self.type.currentIndexChanged.connect(self.onTypeChanged)                
        layout.addWidget(self.type)        
        self.info=guiTools.QListWidget()
        self.info.clicked.connect(self.onItemTriggered)
        layout.addWidget(self.info)                
        self.onTypeChanged(0)
    def onsearch(self):
        search_text = self.search_bar.text().lower()
        for i in range(self.info.count()):
            item = self.info.item(i)
            item.setHidden(search_text not in item.text().lower())    
    def onItemTriggered(self):
        index=self.type.currentIndex()
        if index==0:
            result=functions.quranJsonControl.getSurahs()
        elif index==1:
            result=functions.quranJsonControl.getPage()
        elif index==2:
            result=functions.quranJsonControl.getJuz()
        elif index==3:
            result=functions.quranJsonControl.getHezb()
        elif index==4:
            result=functions.quranJsonControl.getHizb()
        gui.QuranViewer(self,result[self.info.currentItem().text()][1],index,self.info.currentItem().text()).exec()
    def onTypeChanged(self,index:int):
        self.info.clear()
        if index==0:
            self.info.addItems(functions.quranJsonControl.getSurahs().keys())
        elif index==1:
            for i in range(1,605):
                self.info.addItem(str(i))
        elif index==2:
            for i in range(1,31):
                self.info.addItem(str(i))
        elif index==3:
            for i in range(1,241):
                self.info.addItem(str(i))
        elif index==4:
            for  i in range(1,61):
                self.info.addItem(str(i))