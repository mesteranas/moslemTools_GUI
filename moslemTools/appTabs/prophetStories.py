import gui,guiTools,functions,os,re,json
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class ProphetStories(qt.QWidget):
    def __init__(self):
        super().__init__()
        with open("data/json/prophetStories.json","r",encoding="utf-8-sig") as file:
            self.stories=json.load(file)
        self.list_of_aProphetStories=guiTools.QListWidget()
        self.list_of_aProphetStories.addItems(self.stories.keys())
        self.list_of_aProphetStories.itemClicked.connect(self.open)
        layout=qt.QVBoxLayout(self)
        serch=qt.QLabel(_("بحث"))
        serch.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serch)
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        self.search_bar.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.search_bar)

        layout.addWidget(self.list_of_aProphetStories)
    def open(self):
        guiTools.TextViewer(self,_("قصص الأنبياء"),self.stories[self.list_of_aProphetStories.currentItem().text()]).exec()
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
        self.list_of_aProphetStories.clear()
        result=self.search(search_text,list(self.stories.keys()))
        self.list_of_aProphetStories.addItems(result)
