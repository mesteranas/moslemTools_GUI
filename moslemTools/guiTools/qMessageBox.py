import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
class MessageBox(qt.QDialog):
    def __init__(self, parent, title: str, label: str):
        super().__init__(parent)
        self.resize(300, 150)
        self.setWindowTitle(title)
        layout = qt.QVBoxLayout(self)
        self.label = qt.QLabel(label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout.addWidget(self.label)
        self.OKBTN = qt.QPushButton(_("موافق")        )
        self.OKBTN.setDefault(True)
        self.OKBTN.clicked.connect(self.accept)
        layout.addWidget(self.OKBTN)
        qt1.QShortcut("Escape", self).activated.connect(self.reject)
    @staticmethod
    def view(parent,title:str,label:str):
        dlg=MessageBox(parent,title,label)
        result=dlg.exec()
        print(result)