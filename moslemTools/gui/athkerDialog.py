import time,winsound
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
import guiTools
class AthkerDialog (qt.QDialog):
    def __init__(self,p,title:str,athkerList:list):
        super().__init__(p)
        self.showFullScreen()
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
            self.athkerViewer.addItem(thker["text"] + " " + str(thker["times"]) + _(" مرات"))
        layout.addWidget(self.athkerViewer)
        self.athkerViewer.clicked.connect(self.onPlay)
        qt1.QShortcut("escape",self).activated.connect(lambda:self.closeEvent(None))
        qt1.QShortcut("ctrl+c",self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+a",self).activated.connect(self.copy_all_items)
    def copy_all_items(self):
        all_text="\n".join([self.athkerViewer.item(i).text() for i in range(self.athkerViewer.count())])
        guiTools.clikboard.copyText(all_text)
        winsound.Beep(1000,100)
    def copy_selected_item(self):
        selected_item=self.athkerViewer.currentItem()
        if selected_item:
            guiTools.clikboard.copyText(selected_item.text())
            winsound.Beep(1000,100)

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
    def closeEvent (self,event):
        self.media.stop()
        self.close()