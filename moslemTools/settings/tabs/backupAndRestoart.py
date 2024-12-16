import guiTools,update
import zipfile
import sys
import os,shutil
from settings import settings_handler,app
from settings import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
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
            with zipfile.ZipFile(os.path.join(file.selectedFiles()[0],settings_handler.appName + ".zip"),"w") as zipf:
                for root,ders,files in os.walk(os.path.join(os.getenv('appdata'),settings_handler.appName)):
                    for ffiles in files:
                        ffile=os.path.join(root,ffiles)
                        zipf.write(ffile,os.path.relpath(ffile,os.path.join(os.getenv('appdata'),settings_handler.appName)))
    def onrestoar(self):
        file=qt.QFileDialog(self.p)
        if file.exec()==qt.QFileDialog.DialogCode.Accepted:
            shutil.rmtree(os.path.join(os.getenv('appdata'),settings_handler.appName))
            with zipfile.ZipFile(file.selectedFiles()[0]) as zfile:
                zfile.extractall(os.path.join(os.getenv('appdata'),settings_handler.appName))
            mb=qt.QMessageBox(self.p)
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
            elif ex==rl:
                self.p.close()
        