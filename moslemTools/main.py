import sys
from custome_errors import *
sys.excepthook=my_excepthook
import update,guiTools,json,random,os
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput,QMediaPlayer
from appTabs import *
language.init_translation()
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()        
        self.setWindowTitle(app.name+_("الإصدار:") + str(app.version))
        self.resize(1200,600)
        self.media_player=QMediaPlayer()
        self.audio_output=QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.timer=qt2.QTimer(self)
        self.timer.timeout.connect(self.random_audio_theker)
        layout=qt.QVBoxLayout()        
        self.tools=qt.QTabWidget()
        self.tools.addTab(prayer_times(),_("مواقيت الصلاة والتاريخ"))
        self.tools.addTab(Quran(),_("القرآن الكريم مكتوب"))        
        self.tools.addTab(QuranPlayer(),_("القرآن الكريم صوتي"))        
        self.tools.addTab(hadeeth(),_("الأحاديث النبوية والقدسية"))        
        self.tools.addTab(book_marcks(),_("العلامات المرجعية"))                        
        self.tools.addTab(Albaheth(),_("الباحث في القرآن والأحاديث"))
        self.tools.addTab(protcasts(),(_("الإذاعات الإسلامية")))        
        self.tools.addTab(Athker(),_("الأذكار والأدعية"))                                        
        self.tools.addTab(sibha(),(_("سبحة إلكترونية")))
        self.tools.addTab(NamesOfAllah(),_("أسماء الله الحُسْنة"))                                
        self.tools.addTab(DateConverter(),(_("محول التاريخ")))        
        self.tools.addTab(UserGuide(),(_("دليل المستخدم")))
        self.tools.addTab(About_developers(),(_("عن المطورين")))                
        self.tray_icon=qt.QSystemTrayIcon(self)
        self.tray_icon.setIcon(qt1.QIcon("data/icons/app_icon.jpg"))
        self.tray_icon.setToolTip(app.name)
        self.tray_menu=qt.QMenu(self)
        self.random_thecker_audio=qt1.QAction(_("تشغيل ذكر عشوائي"))
        self.random_thecker_audio.triggered.connect(self.random_audio_theker)        
        self.random_thecker_text=qt1.QAction(_("عرض ذكر عشوائي"))
        self.random_thecker_text.triggered.connect(self.show_random_theker)                
        self.show_action = qt1.QAction(_("إخفاء البرنامج"))
        self.show_action.triggered.connect(self.toggle_visibility)        
        self.close_action=qt1.QAction(_("إغلاق البرنامج"))
        self.close_action.triggered.connect(lambda:qt.QApplication.quit())
        self.tray_menu.addAction(self.random_thecker_audio)
        self.tray_menu.addAction(self.random_thecker_text)
        self.tray_menu.addAction(self.show_action)        
        self.tray_menu.addAction(self.close_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()    
        self.TIMER1=qt2.QTimer(self)
        self.TIMER1.timeout.connect(self.show_random_theker)        
        layout.addWidget(self.tools)            
        self.setting=guiTools.QPushButton(_("الإعدادات"))
        self.setting.clicked.connect(lambda: settings(self).exec())        
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.runAudioThkarTimer()
        self.notification_random_thecker()        
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)                    
    def toggle_visibility(self):        
        if self.isVisible():
            self.hide()
            self.show_action.setText(_("إظهار البرنامج"))
        else:
            self.show()
            self.show_action.setText(_("إخفاء البرنامج"))
    def show_random_theker(self):
        with open("data/json/text_athkar.json","r",encoding="utf_8") as f:
            data=json.load(f)
        random_theckr=random.choice(data)
        guiTools.SendNotification(_("ذكر عشوائي"),random_theckr)
    def notification_random_thecker(self):
        self.TIMER1.stop()
        if formatDuration("athkar","text")!=0:
            self.TIMER1.start(formatDuration("athkar","text"))
    def runAudioThkarTimer(self):
        self.timer.stop()
        if formatDuration("athkar","voice")!=0:
            self.timer.start(formatDuration("athkar","voice"))    
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def random_audio_theker(self):        
        folder_path=r"data\sounds\athkar"
        sound_files=[f for f in os.listdir(folder_path) if f.endswith(('.ogg'))]
        if sound_files:
            chosen_file=random.choice(sound_files)
            file_path=os.path.join(folder_path,chosen_file)
            self.media_player.setSource(qt2.QUrl.fromLocalFile(file_path))
            self.media_player.play()    
App=qt.QApplication([])
App.setApplicationDisplayName(app.name)
App.setApplicationName(app.name)
App.setApplicationVersion(str(app.version))
App.setOrganizationName(app.creater)
App.setWindowIcon(qt1.QIcon("data/icons/app_icon.jpg"))
App.setStyle('fusion')
window=main()
window.show()
App.exec()    