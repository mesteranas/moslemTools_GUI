import json,os,requests,gettext
_=gettext.gettext
import guiTools,gui,settings,settings,functions
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class SelectItem(qt.QDialog):
    def __init__(self,p,fileName:str,dirName):
        super().__init__(p)
        self.resize(500,500)
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
                downloadedData=[]
                if self.fileName=="all_tafaseers.json":
                    downloadedData=list(functions.tafseer.tafaseers.keys())
                elif self.fileName=="all_translater.json":
                    downloadedData=list(functions.translater.translations.keys())
                elif self.fileName=="all_ahadeeth.json":
                    downloadedData=list(functions.ahadeeth.ahadeeths.keys())
                for data in downloadedData:
                    del jsonContent[data]
                self.data=jsonContent
                self.item.addItems(self.data)
            else:
                qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء تحميل البيانات"))
                self.close()
        except:
            qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء تحميل البيانات"))
            self.close()
class DownloadThread(qt2.QThread):
    progress=qt2.pyqtSignal(int)
    finished=qt2.pyqtSignal(bool)
    def __init__(self,fileName:str,DIRName:str):
        super().__init__()
        self.fileName=fileName
        self.DIRName=DIRName        
    def run (self):
        try:
            url="https://raw.githubusercontent.com/mesteranas/moslemTools_GUI/refs/heads/main/moslemTools/data/json/" + self.DIRName + "/" + self.fileName
            with requests.get(url,stream=True) as r:
                if r.status_code==200:
                    total_size=int(r.headers.get('content-length', 0))
                    downloaded_size=0                    
                    with open(os.path.join(os.getenv('appdata'),settings.app.appName,self.DIRName,self.fileName),"wb") as file:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                downloaded_size+=len(chunk)
                                progress_percent=int((downloaded_size / total_size) * 100)
                                self.progress.emit(progress_percent)                                            
                    functions.tafseer.setTafaseer()
                    functions.translater.settranslation()
                    functions.ahadeeth.setahadeeth()
                    self.finished.emit(True)                
                else:
                    self.finished.emit(False)    
        except:
            self.finished.emit(False)    
class StartDownloading(qt.QDialog):
    def __init__(self,p,FileName:str,DIRName:str):
        super().__init__(p)
        layout=qt.QVBoxLayout(self)
        self.progressBar=qt.QProgressBar()        
        layout.addWidget(self.progressBar)
        self.thread=DownloadThread(FileName,DIRName)
        self.thread.finished.connect(self.onFinished)
        self.thread.progress.connect(self.onProgreesBarChanged)
        self.thread.start()
    def onFinished(self,state):
        if state:
            qt.QMessageBox.information(self,_("تم"),_("تم تحميل بنجاح"))
            self.accept()
        else:
            qt.QMessageBox.critical(self,_("تنبيه"),_("حدث خطأ أثناء التحميل"))
            self.close()
    def onProgreesBarChanged(self,value):
        self.progressBar.setValue(value)