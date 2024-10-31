import requests
from PyQt6.QtWidgets import QMessageBox
from guiTools import TextViewer
from . import app
def Licence(p):
    try:
        r=requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/LICENSE".format(app.appName))
        TextViewer(p,_("license"),r.text).exec()
    except:
        QMessageBox.information(p,_("error"),_("server error"))