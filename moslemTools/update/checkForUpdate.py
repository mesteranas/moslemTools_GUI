import settings,guiTools
from .updater import DownloadUpdateGUI
import requests
import PyQt6.QtWidgets as qt
from settings.app import appdirname
def check(p,message=True):
    try:
        r=requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/{}/update/app.json".format(settings.settings_handler.appName,appdirname))
        info=r.json()
        if info["version"]>settings.app.version:
            if info["is_beta"] and settings.settings_handler.get("update","beta")=="False":
                if message: qt.QMessageBox.information(p,_("معلومة"),_("لا تتوفر تحديثات جديدة . أنت تستخدم أحدث إصدار"))
            else:
                download(p,info["version"],info["download"],info["what is new"]).exec()
        else:
            if message: qt.QMessageBox.information(p,_("معلومة"),_("لا تتوفر تحديثات جديدة . أنت تستخدم أحدث إصدار"))
    except:
        if message:qt.QMessageBox.critical(p,_("خطأ"),_("حدث خطأ أثناء الإتصال بالخادم . ألرجاء المحاولة في وقت لاحق."))
class download(qt.QDialog):
    def __init__(self,p,version,URL,whatsNew):
        super().__init__(p)
        self.resize(600,500)
        layout=qt.QVBoxLayout(self)
        self.setWindowTitle(_("جديد {} إصدار {}").format(settings.app.name,str(version)))
        whatsn=guiTools.QReadOnlyTextEdit()
        whatsn.setAccessibleName(_("ما الجديد"))
        whatsn.setText(whatsNew)
        self.URL=URL
        self.download=qt.QPushButton(_("تحميل"))
        self.download.setDefault(True)
        self.download.clicked.connect(self.onUpdate)
        self.URL=URL
        self.Close=qt.QPushButton(_("إغلاق"))
        self.Close.clicked.connect(lambda:self.close())
        layout.addWidget(whatsn)
        layout.addWidget(self.download)
        layout.addWidget(self.Close)
    def onUpdate(self):
        self.close()
        DownloadUpdateGUI(self,self.URL).exec()