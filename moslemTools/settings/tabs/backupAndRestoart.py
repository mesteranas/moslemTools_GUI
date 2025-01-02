import guiTools,update
import zipfile
import sys
import os,shutil
from settings import settings_handler,app
from settings import language
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class Objects(qt2.QObject):
    finish=qt2.pyqtSignal(bool)
class Thread (qt2.QRunnable):
    def __init__(self,path,choice):
        super().__init__()
        self.path=path
        self.choice=choice
        self.objects=Objects()
    def run(self):
        if self.choice==0:
            with zipfile.ZipFile(os.path.join(self.path,settings_handler.appName + ".zip"),"w") as zipf:
                for root,ders,files in os.walk(os.path.join(os.getenv('appdata'),settings_handler.appName)):
                    for ffiles in files:
                        ffile=os.path.join(root,ffiles)
                        zipf.write(ffile,os.path.relpath(ffile,os.path.join(os.getenv('appdata'),settings_handler.appName)))
        else:
            shutil.rmtree(os.path.join(os.getenv('appdata'),settings_handler.appName))
            with zipfile.ZipFile(self.path) as zfile:
                zfile.extractall(os.path.join(os.getenv('appdata'),settings_handler.appName))
        self.objects.finish.emit(True)
class GUIForThread(qt.QDialog):
    def __init__ (self,p,path,choice):
        super().__init__(p)
        self.resize(500,500)
        self.setWindowTitle(_("جاري إتمام العملية . يرجى الانتظار ..."))
        self.thread=Thread(path,choice)
        self.thread.objects.finish.connect(self.onFinished)
        qt2.QThreadPool(self).start(self.thread)
        self.choice=choice
    def onFinished(self,state):
        if state:
            if self.choice==0:
                qt.QMessageBox.information(self,_("تم"),_("تم نسخ الإعدادات بنجاح"))
            else:
                mb=qt.QMessageBox(self)
                mb.setWindowTitle(_("تم تحديث الإعدادات"))
                mb.setText(_("يجب عليك إعادة تشغيل البرنامج لتطبيق التغييرات. هل تريد إعادة التشغيل الآن؟"))
                rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
                rn.setText(_("إعادة التشغيل الآن"))
                rl=mb.addButton(qt.QMessageBox.StandardButton.No)
                rl.setText(_("إعادة التشغيل لاحقا"))
                mb.exec()
                ex=mb.clickedButton()
                if ex==rn:
                    os.execl(sys.executable, sys.executable, *sys.argv)
        self.close()
class Restoar(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        layout=qt.QVBoxLayout(self)
        self.createCopy=qt.QPushButton(_("النسخ الاحتياطي"))
        layout.addWidget(self.createCopy)
        self.createCopy.clicked.connect(self.onbackup)
        self.restoar=qt.QPushButton(_("استعادة"))
        layout.addWidget(self.restoar)
        self.restoar.clicked.connect(self.onrestoar)
        self.p=p
    def onbackup(self):
        file=qt.QFileDialog(self.p)
        file.setFileMode(qt.QFileDialog.FileMode.Directory)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            GUIForThread(self,file.selectedFiles()[0],0).exec()
    def onrestoar(self):
        file=qt.QFileDialog(self.p)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            GUIForThread(self,file.selectedFiles()[0],1).exec()