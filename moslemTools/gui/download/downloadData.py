import json,os,requests,gettext
_=gettext.gettext
import guiTools,gui,settings,settings,functions
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class SelectItem(qt.QDialog):
    def __init__(self,p,fileName:str,dirName):
        super().__init__(p)
        self.data={}
        self.dirName=dirName
        layout=qt.QVBoxLayout(self)
        self.item=guiTools.QListWidget()
        layout.addWidget(self.item)        
        self.item.clicked.connect(lambda:StartDownloading(self,self.data[self.item.currentItem().text()],self.dirName).exec())        
        self.fileName=fileName
        self.onLoad()
    def onLoad(self):
        try:
            url="https://raw.githubusercontent.com/mesteranas/moslemTools_GUI/refs/heads/main/moslemTools/data/json/files/" + self.fileName
            r=requests.get(url)
            if r.status_code==200:
                jsonContent=r.json()
                with open("data/json/files/" + self.fileName,"w",encoding="utf-8") as file:
                    json.dump(jsonContent,file,ensure_ascii=False,indent=4)
                self.data=jsonContent
                self.item.addItems(self.data)
            else:
                qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء تحميل البيانات"))
                self.close()
        except:
            qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء تحميل البيانات"))
            self.close()
class DownloadObjects(qt2.QObject):
    finished=qt2.pyqtSignal(bool)
class DownloadThread(qt2.QRunnable):
    def __init__(self,fileName:str,DIRName:str):
        super().__init__()
        self.fileName=fileName
        self.DIRName=DIRName
        self.objects=DownloadObjects()
    def run (self):
        try:
            url="https://raw.githubusercontent.com/mesteranas/moslemTools_GUI/refs/heads/main/moslemTools/data/json/" + self.DIRName + "/" + self.fileName
            r=requests.get(url)
            if r.status_code==200:
                jsonContent=r.json()
                with open(os.path.join(os.getenv('appdata'),settings.app.appName,self.DIRName,self.fileName),"w",encoding="utf-8") as file:
                    json.dump(jsonContent,file,ensure_ascii=False,indent=4)
                functions.tafseer.setTafaseer()
                functions.translater.settranslation()
                functions.ahadeeth.setahadeeth()
                self.objects.finished.emit(True)                
            else:
                self.objects.finished.emit(False)    
        except:
            self.objects.finished.emit(False)    
class StartDownloading(qt.QDialog):
    def __init__(self,p,FileName:str,DIRName:str):
        super().__init__(p)
        thread=DownloadThread(FileName,DIRName)
        thread.objects.finished.connect(self.onFinished)
        qt2.QThreadPool(self).start(thread)
    def onFinished(self,state):
        if state:
            qt.QMessageBox.information(self,_("تم"),_("تم تحميل بنجاح"))
            self.accept()
        else:
            qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء التحميل"))
            self.close()