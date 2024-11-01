import guiTools,update
import zipfile
import sys
import os,shutil
from . import settings_handler,app,tabs
from . import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class settings (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("الإعدادات"))
        layout=qt.QVBoxLayout()
        self.sectian=guiTools.listBook(layout,_("اختر قسم"))
        self.update=tabs.Update(self)
        self.ok=qt.QPushButton(_("موافق"))
        self.ok.setDefault(True)
        self.ok.clicked.connect(self.fok)
        self.defolt=qt.QPushButton(_("استعادة الإعدادات الإفتراضية"))
        self.defolt.clicked.connect(self.default)
        self.cancel=qt.QPushButton(_("إلغاء"))
        self.cancel.clicked.connect(self.fcancel)
        self.layout1=tabs.Genral(self)
        self.sectian.add(_("عام"),self.layout1)
        self.sectian.add(_("إعدادات التحديثات"),self.update)
        restoar=tabs.Restoar(self)
        self.sectian.add(_("النسخ الاحتياطي والاستعادةة"),restoar)
        layout.addWidget(self.ok)
        layout.addWidget(self.defolt)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        aa=0
        if settings_handler.get("g","lang")!=str(language.lang()[self.layout1.language.currentText()]):
            aa=1
        settings_handler.set("g","lang",str(language.lang()[self.layout1.language.currentText()]))
        settings_handler.set("g","exitDialog",str(self.layout1.ExitDialog.isChecked()))
        settings_handler.set("g","reciter",str(self.layout1.reciter.currentIndex()))
        settings_handler.set("update","autoCheck",str(self.update.update_autoDect.isChecked()))
        settings_handler.set("update","beta",str(self.update.update_beta.isChecked()))
        if aa==1:
            mb=qt.QMessageBox(self)
            mb.setWindowTitle(_("تم تحديث الإعدادات"))
            mb.setText(_("يجب عليك إعادة تشغيل البرنامج لتطبيق التغييرات. هل تريد إعادة التشغيل الآن؟"))
            rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
            rn.setText(_("اعادة التشغيل الآن"))
            rl=mb.addButton(qt.QMessageBox.StandardButton.No)
            rl.setText(_("اعادة التشغيل لاحقا"))
            mb.exec()
            ex=mb.clickedButton()
            if ex==rn:
                os.execl(sys.executable, sys.executable, *sys.argv)
            elif ex==rl:
                self.close()
        else:
            self.close()
    def default(self):
        mb=qt.QMessageBox(self)
        mb.setWindowTitle(_("تنبيه"))
        mb.setText(_("هل تريد إعادة تعيين إعداداتك؟ إذا قمت بالنقر على إعادة تعيين، سيعيد البرنامج التشغيل لإكمال إعادة التعيين."))
        rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
        rn.setText(_("إعادة التعيين وإعادة التشغيل"))
        rl=mb.addButton(qt.QMessageBox.StandardButton.No)
        rl.setText(_("إلغاء"))
        mb.exec()
        ex=mb.clickedButton()
        if ex==rn:
            shutil.rmtree(os.path.join(os.getenv('appdata'),app.appName))
            os.execl(sys.executable, sys.executable, *sys.argv)

    def fcancel(self):
        self.close()
    def cbts(self,string):
        if string=="True":
            return True
        else:
            return False

