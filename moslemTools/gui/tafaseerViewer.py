import functions,settings
import guiTools
import PyQt6.QtWidgets as qt
class TafaseerViewer(qt.QDialog):
    def __init__(self,p,From,to):
        super().__init__(p)
        self.index=int(settings.settings_handler.get("g","tafaseer"))
        self.From=From
        self.to=to
        self.showFullScreen()
        self.text=guiTools.QReadOnlyTextEdit()
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
        self.getResult()
    def getResult(self):
        content=functions.tafseer.getTafaseer(functions.tafseer.getTafaseerByIndex(self.index),self.From,self.to)
        self.text.setText(content)