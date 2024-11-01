import functions,settings
import guiTools
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2

class TafaseerViewer(qt.QDialog):
    def __init__(self,p,From,to):
        super().__init__(p)
        self.index=settings.settings_handler.get("tafaseer","tafaseer")
        self.From=From
        self.to=to
        self.showFullScreen()
        self.text=guiTools.QReadOnlyTextEdit()
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        self.changeTafaseer=qt.QPushButton(_("تغيير التفسير"))
        self.changeTafaseer.clicked.connect(self.on_change_tafaseer)
        layout.addWidget(self.changeTafaseer)
        self.getResult()
    def getResult(self):
        content=functions.tafseer.getTafaseer(functions.tafseer.getTafaseerByIndex(self.index),self.From,self.to)
        self.text.setText(content)
    def on_change_tafaseer(self):
        menu=qt.QMenu(_("اختر تفسير"),self)
        tafaseer=list(functions.tafseer.tafaseers.keys())
        tafaseer.remove(functions.tafseer.getTafaseerByIndex(self.index))
        selectedTafaseer=qt1.QAction(functions.tafseer.getTafaseerByIndex(self.index),self)
        menu.addAction(selectedTafaseer)
        menu.setDefaultAction(selectedTafaseer)
        selectedTafaseer.setCheckable(True)
        selectedTafaseer.setChecked(True)
        selectedTafaseer.triggered.connect(lambda:self.onTafaseerChanged(functions.tafseer.getTafaseerByIndex(self.index)))
        for t in tafaseer:
            tAction=qt1.QAction(t,self)
            menu.addAction(tAction)
            tAction.triggered.connect(lambda:self.onTafaseerChanged(t))
        menu.setAccessibleName(_("اختر تفسير"))
        menu.setFocus()
        menu.exec()
    def onTafaseerChanged(self,name:str):
        self.index=functions.tafseer.tafaseers[name]
        self.getResult()