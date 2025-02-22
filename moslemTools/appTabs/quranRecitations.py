import json,os,gui
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class QuranRecitations(qt.QWidget):
    def __init__(self):
        super().__init__()
        with open("data/json/files/all_quran_recitations.json","r",encoding="utf-8") as file:
            self.recitationData=json.load(file)
        layout=qt.QVBoxLayout(self)        
        self.select_laybol=qt.QLabel(_("اختر قراءة"))
        self.select_laybol.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.select_laybol)
        self.selectRecitation=qt.QComboBox()
        self.selectRecitation.addItems(self.recitationData)
        self.data={}
        self.selectRecitation.currentTextChanged.connect(self.onRecitationChanged)
        self.selectRecitation.setAccessibleName(_("اختر قراءة"))        
        layout.addWidget(self.selectRecitation)
        self.surahs=qt.QListWidget()
        self.surahs.itemActivated.connect(self.onSurahClicked)
        layout.addWidget(self.surahs)
        self.onRecitationChanged(self.selectRecitation.currentText())
    def onRecitationChanged(self,text):
        recitationPath=os.path.join("data","json","quranRecitations",self.recitationData[text])
        self.surahs.clear()
        with open(recitationPath,"r",encoding="utf-8-sig") as file:
            self.data=json.load(file)
        self.surahs.addItems(self.data.keys())
    def onSurahClicked(self):
        surahText=self.surahs.currentItem().text()
        surahVerses=self.data[surahText]
        gui.QuranRecitationViewer(self,"\n".join(surahVerses)).exec()