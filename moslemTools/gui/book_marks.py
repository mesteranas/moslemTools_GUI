import gui,guiTools,functions,json,os,re,time
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class book_marcks(qt.QDialog):
    def __init__(self,p,tabName):
        super().__init__(p)
        self.tabName=tabName
        self.p=p
        self.resize(300,300)
        self.setWindowTitle(_("العلامات المرجعية"))
        self.results=guiTools.QListWidget()
        self.results.clicked.connect(self.onItemClicked)
        self.dl=qt.QPushButton(_("حذف العلامة المرجعية"))
        self.dl.clicked.connect(self.onRemove)
        layout=qt.QVBoxLayout(self)
        serch=qt.QLabel(_("بحث"))
        serch.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        self.search_bar=qt.QLineEdit()        
        self.search_bar.setPlaceholderText(_("بحث ..."))
        self.search_bar.textChanged.connect(self.onsearch)        
        self.search_bar.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serch)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.results)
        layout.addWidget(self.dl)
        self.onCategoryChanged()
        qt1.QShortcut("delete",self).activated.connect(self.onRemove)
    def onItemClicked(self):
        data=functions.bookMarksManager.GetAudioBookByName(self.tabName,self.results.currentItem().text())
        if self.tabName=="quran":
            self.p.recitersListWidget.setCurrentRow(data["type"])
            time.sleep(0.5)
            self.p.surahListWidget.setCurrentRow(data["category"])
            time.sleep(0.5)
            self.p.play_selected_audio()
        elif self.tabName=="stories":
            self.p.categoriesListWidget.setCurrentRow(data["type"])
            time.sleep(0.5)
            self.p.storiesListWidget.setCurrentRow(data["category"])
            time.sleep(0.5)
            self.p.play_selected_story()
        self.p.bookmarksPosition=data["position"]
        self.p.isAMustToGoToBookmark=True
        self.close()
    def onRemove(self):
        try:
            functions.bookMarksManager.removeaudioBookMark(self.tabName,self.results.currentItem().text())
            self.onCategoryChanged()
        except:
            qt.QMessageBox.critical(self,_("تحذير"),_("حدث خطأ أثناء حذف العلامة المرجعية"))
    def onCategoryChanged(self):
        bookMarksData=functions.bookMarksManager.openBookMarksFile()
        self.results.clear()
        self.bookMarks1=[]
        try:
            for item in bookMarksData["audio " + self.tabName]:
                self.bookMarks1.append(item["name"])
        except:
            pass
        self.results.addItems(self.bookMarks1)
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
        self.results.clear()
        result=self.search(search_text,self.bookMarks1)
        self.results.addItems(result)