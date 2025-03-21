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
class Update(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        UpdateLayout=qt.QVBoxLayout(self)
        self.update_autoDect=qt.QCheckBox(_("تحقق تلقائيًا من التحديثات عند بدء البرنامج"))
        self.update_autoDect.setChecked(p.cbts(settings_handler.get("update","autoCheck")))
        UpdateLayout.addWidget(self.update_autoDect)
        self.update_beta=qt.QCheckBox(_("تحميل التحديثات التجريبية"))
        self.update_beta.setChecked(p.cbts(settings_handler.get("update","beta")))
        UpdateLayout.addWidget(self.update_beta)
        self.update_check=qt.QPushButton(_("التحقق من وجود تحديثات"))
        self.update_check.clicked.connect(lambda:update.check(self))
        UpdateLayout.addWidget(self.update_check)
