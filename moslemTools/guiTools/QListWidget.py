import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class QListWidget(qt.QListWidget):
    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        
        if event.key()==qt2.Qt.Key.Key_Return or event.key()==qt2.Qt.Key.Key_Enter:
            try:
                self.clicked.emit(self.currentIndex())
            except Exception as error:
                print(error)
                pass