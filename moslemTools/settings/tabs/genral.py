import os,sys,gui,guiTools,shutil
from settings import settings_handler,app
from settings import language
import win32com.client
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
startUpPath=os.path.join(os.getenv('appdata'),"Microsoft","Windows","Start Menu","Programs","Startup","moslemTools.lnk")
class Genral(qt.QWidget):
    def __init__(self,p):
        super().__init__()
        label=qt.QLabel(_("لغة التطبيق"))
        self.language=qt.QComboBox()
        self.language.setAccessibleName(_("لغة التطبيق"))
        self.language.addItems(language.lang().keys())
        languages={index:language for language, index in enumerate(language.lang().values())}
        try:
            self.language.setCurrentIndex(languages[settings_handler.get("g","lang")])
        except Exception as e:
            self.language.setCurrentIndex(0)
        self.ExitDialog=qt.QCheckBox(_("عرض نافذة الخروج عند الخروج من البرنامج"))
        self.ExitDialog.setChecked(p.cbts(settings_handler.get("g","exitDialog")))
        layout1=qt.QVBoxLayout(self)
        layout1.addWidget(label)
        layout1.addWidget(self.language)
        layout1.addWidget(self.ExitDialog)
        self.startup=qt.QCheckBox(_("بدء تشغيل البرنامج عند بدء تشغيل النظام"))
        self.startup.setChecked(self.check_in_startup())
        self.startup.checkStateChanged.connect(self.onStartupChanged)
        layout1.addWidget(self.startup)
        self.reciter=qt.QComboBox()
        self.reciter.addItems(gui.reciters.keys())
        self.reciter.setCurrentIndex(int(settings_handler.get("g","reciter")))
        self.reciter.setAccessibleName(_("تحديد القارئ للقرآن المكتوب"))
        self.reciter.setContextMenuPolicy(qt2.Qt.ContextMenuPolicy.CustomContextMenu)
        self.reciter.customContextMenuRequested.connect(self.onDelete)
        qt1.QShortcut("delete",self).activated.connect(self.onDelete)
        layout1.addWidget(qt.QLabel(_("تحديد القارئ للقرآن المكتوب")))
        layout1.addWidget(self.reciter)
    def add_to_startup(self):
        try:
            shell=win32com.client.Dispatch("WScript.Shell")
            shortcut=shell.CreateShortcut(startUpPath)
            shortcut.TargetPath = sys.executable
            shortcut.WorkingDirectory = os.path.dirname(sys.executable)
            shortcut.Description = "a shortcut for opening moslem tools when windows start"
            shortcut.Save()
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"),_("تعذر إتمام العملية"))
    def check_in_startup(self):
        try:
            if os.path.exists(startUpPath):
                return True
            else:
                return False
        except Exception as e:
            return False
    def remove_from_startup(self):
        try:
            os.remove(startUpPath)
        except Exception as e:
            qt.QMessageBox.critical(self, _("خطأ"),_("تعظر اتمام العملية"))
    def onStartupChanged(self,value):
        if self.check_in_startup():
            self.remove_from_startup()
        else:
            self.add_to_startup()
    def onDelete(self):
        itemText=self.reciter.currentText()
        if itemText:
            reciterText=gui.quranViewer.reciters[itemText].split("/")[-3]
            path=os.path.join(os.getenv('appdata'),app.appName,"reciters",reciterText)
            if os.path.exists(path):
                question=qt.QMessageBox.question(self,_("تنبيه"),_("هل تريد حذف هذا القارئ"),qt.QMessageBox.StandardButton.Yes|qt.QMessageBox.StandardButton.No)
                if question==qt.QMessageBox.StandardButton.Yes:
                    shutil.rmtree(path)
                    guiTools.speak(_("تم الحذف"))