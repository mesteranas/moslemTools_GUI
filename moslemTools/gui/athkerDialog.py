import time
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
import guiTools
class AthkerDialog (qt.QDialog):
    def __init__(self,p,title:str,athkerList:list):
        super().__init__(p)
        self.setGeometry(100,100,800,500)
        self.setWindowTitle(title)
        layout=qt.QVBoxLayout(self)
        self.media=QMediaPlayer(self)
        self.audioOutput=QAudioOutput(self)
        self.media.setAudioOutput(self.audioOutput)
        self.media.setSource(qt2.QUrl.fromLocalFile("data/sounds/001001.mp3"))
        self.media.play()
        time.sleep(0.5)
        self.media.stop()
        self.athkerList=athkerList
        self.athkerViewer=guiTools.QListWidget()
        for thker in self.athkerList:
            self.athkerViewer.addItem(thker["text"])
        layout.addWidget(self.athkerViewer)
        self.athkerViewer.clicked.connect(self.onPlay)
    def onPlay(self):
        if self.media.isPlaying():
            self.media.stop()
        else:
            url=qt2.QUrl(self.athkerList[self.athkerViewer.currentRow()]["audio"])
            if url==self.media.source():
                pass
            else:
                self.media.setSource(url)
            self.media.play()