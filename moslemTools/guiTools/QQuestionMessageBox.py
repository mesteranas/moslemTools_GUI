import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtCore import Qt
from .QReadOnlyTextEdit import QReadOnlyTextEdit
import winsound
class QQuestionMessageBox(qt.QDialog):
    def __init__(self, parent, title: str, label: str,yesLabel:str,noLabel:str):
        super().__init__(parent)
        self.result=1
        self.resize(300, 150)
        self.setWindowTitle(title)
        layout = qt.QVBoxLayout(self)
        self.label = QReadOnlyTextEdit()
        self.label.setText(label)        
        layout.addWidget(self.label)
        self.OKBTN = qt.QPushButton(yesLabel)
        self.OKBTN.setDefault(True)
        self.OKBTN.clicked.connect(self.onOk)
        self.OKBTN.setStyleSheet("background-color: #0000AA; color: #e0e0e0;")
        layout.addWidget(self.OKBTN,alignment=qt2.Qt.AlignmentFlag.AlignLeft)
        self.noBTN=qt.QPushButton(noLabel)
        self.noBTN.clicked.connect(self.reject)
        layout.addWidget(self.noBTN)
        qt1.QShortcut("Escape", self).activated.connect(self.reject)
    def onOk(self):
        self.result=0
        self.accept()
    @staticmethod
    def view(parent,title:str,label:str,yesLabel:str,noLabel:str):
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        dlg=QQuestionMessageBox(parent,title,label,yesLabel,noLabel)
        result=dlg.exec()
        return dlg.result