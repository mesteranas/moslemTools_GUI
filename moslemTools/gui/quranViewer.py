import guiTools
import PyQt6.QtWidgets as qt
class QuranViewer(qt.QDialog):
    def __init__(self,p,text):
        super().__init__(p)
        self.setWindowTitle(_("القرآن الكريم"))
        self.showFullScreen()
        self.text=guiTools.QReadOnlyTextEdit()
        self.text.setText(text)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)