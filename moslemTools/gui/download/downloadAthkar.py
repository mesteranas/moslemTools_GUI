from functions import quranJsonControl
import json,os,requests,gettext
_=gettext.gettext
import guiTools,gui,settings,settings,functions
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class SelectAthkar(qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.resize(500,500)
        layout=qt.QVBoxLayout(self)
        with open("data/json/athkar.json","r",encoding="utf-8-sig") as data:
            self.reciterData=json.load(data)
        self.reciters=guiTools.QListWidget()
        for athker in self.reciterData:
            self.reciters.addItem(athker["name"])
        self.reciters.clicked.connect(lambda:DownloadReciter(self,self.reciterData[self.reciters.currentRow()]["content"],self.reciters.currentItem().text()).exec())
        layout.addWidget(self.reciters)
class downloadObjects(qt2.QObject):
    progress=qt2.pyqtSignal(int)
    downloaded=qt2.pyqtSignal(int)
    pauseDownloading=qt2.pyqtSignal(str)
    finch=qt2.pyqtSignal(bool)
class downloadThread(qt2.QRunnable):
    def __init__(self,p,url,name):
        super().__init__()        
        self.objects=downloadObjects()
        self.name=name
        self.url=url
        self.pause=False
        self.objects.pauseDownloading.connect(self.on_pause)        
    def on_pause(self,s):
        self.pause=True
    def  run(self):
        try:
            count=0
            for item in self.url:
                if not self.pause:
                    if not os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar")):
                        os.makedirs(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar"))
                    if not os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar",self.name)):
                        os.makedirs(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar",self.name))
                    file=str(self.url.index(item)) + ".mp3"
                    if os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar",self.name,file)):
                        count+=1
                        self.objects.downloaded.emit(count)
                    else:
                        with requests.get(item["audio"],stream=True) as r:
                            if r.status_code!=200:
                                self.objects.finsh.emit(False)
                                return
                            size=r.headers.get("content-length")
                            try:
                                size=int(size)
                            except TypeError:
                                self.objects.finsh.emit(False)
                                return
                            recieved=0
                            progress=0
                            with open(os.path.join(os.getenv('appdata'),settings.app.appName,"athkar",self.name,file),"wb") as file:
                                for pk in r.iter_content(1024):
                                    file.write(pk)
                                    recieved+=len(pk)
                                    progress=int((recieved/size)*100)
                                    self.objects.progress.emit(progress)
                        count+=1
                        self.objects.downloaded.emit(count)
            self.objects.finch.emit(True)
        except Exception as e:
            print(e)
            self.objects.finch.emit(False)
class DownloadReciter(qt.QDialog):
    def __init__(self,p,url,name):
        super().__init__(p)                    
        self.setWindowTitle(_("جاري التحميل"))        
        qt1.QShortcut("escape",self).activated.connect(lambda:self.run.objects.pauseDownloading.emit("a"))
        self.progress=qt.QProgressBar()
        self.downloaded=qt.QSpinBox()
        self.downloaded.setAccessibleName(_("عدد الأذكار التي تم تحميلها"))
        self.downloaded.setRange(0,7000)
        self.downloaded.setReadOnly(True)
        self.pause=qt.QPushButton(_("إيقاف مؤقت"))
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.progress)
        layout.addWidget(qt.QLabel(_("عدد الأذكار التي تم تحميلها")))
        layout.addWidget(self.downloaded)
        layout.addWidget(self.pause)
        thread=qt2.QThreadPool(self)
        self.run=downloadThread(self,url,name)
        self.run.objects.finch.connect(self.on)
        self.run.objects.progress.connect(self.on_progress)
        self.run.objects.downloaded.connect(self.on_downloaded)
        thread.start(self.run)
        self.pause.clicked.connect(lambda:self.run.objects.pauseDownloading.emit("a"))
    def closeEvent(self,event):
        self.run.objects.pauseDownloading.emit("a")
    def on(self,state):
        if state==True:
            qt.QMessageBox.information(self,_("تم"),_("تم التحميل بنجاح"))
            self.close()
        else:
            qt.QMessageBox.information(self,_("خطأ"),_("تعظر التحميل"))
            self.close()
    def on_progress(self,progress):
        self.progress.setValue(progress)
    def on_downloaded(self,count):
        self.downloaded.setValue(count)