import time,winsound,pyperclip,gettext
_=gettext.gettext
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
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
        self.font_size=20
        font=self.font()
        font.setPointSize(self.font_size)
        self.athkerViewer.setFont(font)
        self.N_theker=qt.QPushButton(_("الذكر التالي"))
        self.N_theker.clicked.connect(self.onNextThker)
        self.PPS=qt.QPushButton(_("تشغيل"))
        self.PPS.clicked.connect(self.onPlay)
        self.P_thekr=qt.QPushButton(_("الذكر السابق"))
        self.P_thekr.clicked.connect(self.onPreviousThker)
        layout.addWidget(self.athkerViewer)
        layout.addWidget(self.N_theker)
        layout.addWidget(self.PPS)
        layout.addWidget(self.P_thekr)
        qt1.QShortcut("alt+right",self).activated.connect(self.onNextThker)
        qt1.QShortcut("alt+left",self).activated.connect(self.onPreviousThker)
        qt1.QShortcut("space",self).activated.connect(self.onPlay)
        qt1.QShortcut("escape",self).activated.connect(lambda:self.closeEvent(None))        
        qt1.QShortcut("ctrl+c", self).activated.connect(self.copy_line)
        qt1.QShortcut("ctrl+a", self).activated.connect(self.copy_text)
        qt1.QShortcut("ctrl+=", self).activated.connect(self.increase_font_size)
        qt1.QShortcut("ctrl+-", self).activated.connect(self.decrease_font_size)
        qt1.QShortcut("ctrl+s", self).activated.connect(self.save_text_as_txt)
        qt1.QShortcut("ctrl+p", self).activated.connect(self.print_text)                
    def onPlay(self):
        if self.media.isPlaying():
            self.media.stop()
            self.PPS.setText(_("تشغيل"))
        else:            
            url=qt2.QUrl(self.athkerList[self.inex]["audio"])
            if url==self.media.source():
                pass
            else:
                self.media.setSource(url)
            self.media.play()            
            self.PPS.setText(_("إيقاف"))
    def closeEvent (self,event):
        self.media.stop()
        self.close()
    def onNextThker(self):
        if self.inex+1==len(self.athkerList):
            self.inex=0
        else:
            self.inex+=1
        self.athkerViewer.setText(self.athkerList[self.inex]["text"])
        winsound.PlaySound("data/sounds/next_page.wav",1)
    def onPreviousThker(self):
        if self.inex==0:
            self.inex=len(self.athkerList)-1
        else:
            self.inex-=1
        self.athkerViewer.setText(self.athkerList[self.inex]["text"])
        winsound.PlaySound("data/sounds/previous_page.wav",1)        
    def OnContextMenu(self):
        menu=qt.QMenu(_("الخيارات"),self)
        menu.setAccessibleName(_("الخيارات"))
        menu.setFocus()
        save=menu.addAction(_("حفظ كملف نصي"))
        save.triggered.connect(self.save_text_as_txt)
        menu.setDefaultAction(save)
        print=menu.addAction(_("طباعة"))
        print.triggered.connect(self.print_text)
        copy_all=menu.addAction(_("نسخ النص كاملا"))        
        copy_all.triggered.connect(self.copy_text)
        copy_selected_text=menu.addAction(_("نسخ النص المحدد"))
        copy_selected_text.triggered.connect(self.copy_line)
        fontMenu=qt.QMenu(_("حجم الخط"),self)
        incressFontAction=qt1.QAction(_("تكبير الخط"),self)
        fontMenu.addAction(incressFontAction)
        fontMenu.setDefaultAction(incressFontAction)
        incressFontAction.triggered.connect(self.increase_font_size)
        decreaseFontSizeAction=qt1.QAction(_("تصغير الخط"),self)
        fontMenu.addAction(decreaseFontSizeAction)
        decreaseFontSizeAction.triggered.connect(self.decrease_font_size)
        menu.addMenu(fontMenu)
        menu.exec(self.mapToGlobal(self.cursor().pos()))
    def print_text(self):
        try:
            printer=QPrinter()
            dialog=QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                self.athkerViewer.print(printer)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def save_text_as_txt(self):
        try:
            file_dialog=qt.QFileDialog()
            file_dialog.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")
            file_dialog.setDefaultSuffix("txt")
            if file_dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
                file_name=file_dialog.selectedFiles()[0]
                with open(file_name, 'w', encoding='utf-8') as file:
                    text=self.athkerViewer.toPlainText()
                    file.write(text)                
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def increase_font_size(self):
        self.font_size += 1
        guiTools.speak(str(self.font_size ))
        self.update_font_size()
    def decrease_font_size(self):
        self.font_size -= 1
        guiTools.speak(str(self.font_size ))
        self.update_font_size()
    def update_font_size(self):
        cursor=self.athkerViewer.textCursor()
        self.athkerViewer.selectAll()
        font=self.athkerViewer.font()
        font.setPointSize(self.font_size)
        self.athkerViewer.setCurrentFont(font)        
        self.athkerViewer.setTextCursor(cursor)
    def copy_line(self):
        try:
            cursor=self.athkerViewer.textCursor()
            if cursor.hasSelection():
                selected_text=cursor.selectedText()
                pyperclip.copy(selected_text)                
                winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))
    def copy_text(self):
        try:
            text=self.athkerViewer.toPlainText()
            pyperclip.copy(text)            
            winsound.Beep(1000,100)
        except Exception as error:
            qt.QMessageBox.warning(self, "تنبيه حدث خطأ", str(error))