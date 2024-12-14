import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
class AdaanDialog(qt.QDialog):
    def __init__(self,p,index:int,title:str):
        super().__init__(p)
        self.setWindowTitle(title)
        self.setWindowIcon(qt1.QIcon("data/icons/app_icon.jpg"))
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
    def closeEvent(self,event):
        self.media_player.stop()
        self.accept()
    def onStateChanged(self,state):
        if state==self.media_player.MediaStatus.EndOfMedia :
            self.accept()