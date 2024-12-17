import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
class AdaanDialog(qt.QDialog):
    def __init__(self,p,index:int,title:str):
        super().__init__(p)
        self.setGeometry(100,100,400,400)
        self.setWindowTitle(title)
        self.lay=qt.QLabel()
        self.lay.setGeometry(50,50,300,300)
        self.lay.setPixmap(qt1.QPixmap("data/icons/app_icon.jpg"))
        self.lay.setScaledContents(True)
        self.media_player=QMediaPlayer()
        self.media_player.mediaStatusChanged.connect(self.onStateChanged)
        self.audio_output=QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        if index==0:
            self.media_player.setSource(qt2.QUrl.fromLocalFile("data/sounds/adaan/fajr.mp3"))
        else:
            self.media_player.setSource(qt2.QUrl.fromLocalFile("data/sounds/adaan/genral.webm"))
        self.media_player.play()
        qt1.QShortcut("escape",self).activated.connect(self.close)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.lay)
    def closeEvent(self,event):
        self.media_player.stop()
        self.accept()
    def onStateChanged(self,state):
        if state==self.media_player.MediaStatus.EndOfMedia:            
            self.accept()            
            from afterAdaan import AfterAdaan
            window=AfterAdaan(self)
            window.exec()