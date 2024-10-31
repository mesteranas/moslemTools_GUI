import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class QReadOnlyTextEdit(qt.QTextEdit):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setTextInteractionFlags(qt2.Qt.TextInteractionFlag.TextSelectableByKeyboard|qt2.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setAcceptRichText(True)
        self.setLineWrapMode(qt.QTextEdit.LineWrapMode.NoWrap)