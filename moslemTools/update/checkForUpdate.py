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
                if message: guiTools.qMessageBox.MessageBox.view(p,_("معلومة"),_("لا تتوفر تحديثات جديدة . أنت تستخدم أحدث إصدار"))
            else:
                download(p,info["version"],info["download"],info["what is new"]).exec()
        else:
            if message: guiTools.qMessageBox.MessageBox.view(p,_("معلومة"),_("لا تتوفر تحديثات جديدة . أنت تستخدم أحدث إصدار"))
    except:
        if message:guiTools.qMessageBox.MessageBox.view(p,_("خطأ"),_("حدث خطأ أثناء الإتصال بالخادم . ألرجاء المحاولة في وقت لاحق."))
class download(qt.QDialog):
    def __init__(self,p,version,URL,whatsNew):
        super().__init__(p)
        self.resize(700,500)
        layout=qt.QVBoxLayout(self)
        layout1=qt.QHBoxLayout()
        self.setWindowTitle(_("جديد {} إصدار {}").format(settings.app.name,str(version)))
        self.p=p
        whatsn=guiTools.QReadOnlyTextEdit()
        whatsn.setAccessibleName(_("ما الجديد"))
        whatsn.setText(whatsNew)
        self.URL=URL
        self.download=qt.QPushButton(_("تحميل"))
        self.download.setDefault(True)
        self.download.setStyleSheet("background-color: #0000AA; color: white;")        
        self.download.clicked.connect(self.onUpdate)
        self.URL=URL
        self.Close=qt.QPushButton(_("إغلاق"))
        self.Close.clicked.connect(lambda:self.close())
        self.Close.setStyleSheet("background-color: #0000AA; color: white;")
        layout.addWidget(whatsn)        
        layout1.addWidget(self.download)
        layout1.addWidget(self.Close)
        layout.addLayout(layout1)
    def onUpdate(self):
        self.close()
        settings.app.exit=False
        DownloadUpdateGUI(self,self.URL).exec()