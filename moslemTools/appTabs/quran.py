import gui,guiTools,functions,re
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtCore as qt2
language.init_translation()
class Quran(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.infoData=[]
        layout=qt.QVBoxLayout(self)
        self.serch=qt.QLabel(_("بحث"))
        self.serch.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)        
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        self.search_bar.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)        
        self.by=qt.QLabel(_("التصفح ب"))
        self.by.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.by)        
        self.type=qt.QComboBox()
        self.type.setAccessibleName(_("التصفح ب"))
        self.type.addItems([_("سور"), _("صفحات"), _("أجزاء"), _("أرباع"), _("أحزاب")])
        self.type.currentIndexChanged.connect(self.onTypeChanged)                        
        self.custom=guiTools.QPushButton(_("مخصص"))        
        self.custom.clicked.connect(lambda: self.fromToSuraah.exec())
        layout.addWidget(self.type)        
        layout.addWidget(self.custom)
        layout.addWidget(self.serch)
        layout.addWidget(self.search_bar)
        self.info=guiTools.QListWidget()
        self.info.clicked.connect(self.onItemTriggered)
        layout.addWidget(self.info)                
        self.fromToSuraah=guiTools.FromToSurahWidget(self)        
        self.onTypeChanged(0)
    def search(self,pattern,text_list):    
        tashkeel_pattern=re.compile(r'[\u0617-\u061A\u064B-\u0652\u0670]')        
        normalized_pattern=tashkeel_pattern.sub('', pattern)        
        matches=[
            text for text in text_list
            if normalized_pattern in tashkeel_pattern.sub('', text)
        ]        
        return matches        
    def onsearch(self):
        search_text=self.search_bar.text().lower()
        self.info.clear()
        result=self.search(search_text,self.infoData)
        self.info.addItems(result)
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
        gui.QuranViewer(self,result[self.info.currentItem().text()][1],index,self.info.currentItem().text(),enableNextPreviouseButtons=True,typeResult=result,CurrentIndex=self.info.currentRow()).exec()
    def onTypeChanged(self,index:int):
        state=True
        self.info.clear()
        self.infoData=[]
        if index==0:
            self.infoData=functions.quranJsonControl.getSurahs().keys()
        elif index==1:
            for i in range(1,605):
                self.infoData.append(str(i))
        elif index==2:
            for i in range(1,31):
                self.infoData.append(str(i))
        elif index==3:
            for i in range(1,241):
                self.infoData.append(str(i))
        elif index==4:
            for  i in range(1,61):
                self.infoData.append(str(i))                        
        self.info.addItems(self.infoData)