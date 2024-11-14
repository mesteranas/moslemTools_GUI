import time,winsound,pyperclip,gettext
_=gettext.gettext
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
        self.athkerViewer=guiTools.QReadOnlyTextEdit()
        self.inex=0
        self.athkerViewer.setText(self.athkerList[self.inex]["text"])
        layout.addWidget(self.athkerViewer)
        qt1.QShortcut("alt+right",self).activated.connect(self.onNextThker)
        qt1.QShortcut("alt+left",self).activated.connect(self.onPreviousThker)
        qt1.QShortcut("space",self).activated.connect(self.onPlay)
        qt1.QShortcut("escape",self).activated.connect(lambda:self.closeEvent(None))
        qt1.QShortcut("ctrl+c",self).activated.connect(self.copy_selected_item)
        qt1.QShortcut("ctrl+a",self).activated.connect(self.copy_all_items)
    def copy_all_items(self):
        all_text="\n".join([self.athkerViewer.item(i).text() for i in range(self.athkerViewer.count())])
        pyperclip.copy(all_text)        
        winsound.Beep(1000,100)
    def copy_selected_item(self):
        selected_item=self.athkerViewer.currentItem()
        if selected_item:
            pyperclip.copy(selected_item.text())
            winsound.Beep(1000,100)
    def onPlay(self):
        if self.media.isPlaying():
            self.media.stop()
        else:
            url=qt2.QUrl(self.athkerList[self.inex]["audio"])
            if url==self.media.source():
                pass
            else:
                self.media.setSource(url)
            self.media.play()
    def closeEvent (self,event):
        self.media.stop()
        self.close()
    def onNextThker(self):
        if self.inex+1==len(self.athkerList):
            self.inex=0
        else:
            self.inex+=1
        self.athkerViewer.setText(self.athkerList[self.inex]["text"])
    def onPreviousThker(self):
        if self.inex==0:
            self.inex=len(self.athkerList)-1
        else:
            self.inex-=1
        self.athkerViewer.setText(self.athkerList[self.inex]["text"])