import sys
from custome_errors import *
sys.excepthook = my_excepthook
import update, guiTools,json,random,os,shutil,datetime,webbrowser,requests
from hijri_converter import Gregorian
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from appTabs import *
language.init_translation()
try:
    updatePath=os.path.join(os.getenv('appdata'),settings_handler.appName,"update")
    if os.path.exists(updatePath):
        shutil.rmtree(updatePath)
except:
    pass
class main(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("الإصدار:") + str(app.version))
        self.resize(1100,600)
        self.media_player=QMediaPlayer()
        self.audio_output=QAudioOutput()
        self.audio_output.setVolume(int(settings_handler.get("athkar","voiceVolume"))/100)
        self.media_player.setAudioOutput(self.audio_output)
        self.timer=qt2.QTimer(self)
        self.timer.timeout.connect(self.random_audio_theker)
        layout=qt.QVBoxLayout()
        self.info=qt.QLineEdit()
        self.info.setReadOnly(True)
        self.info.setAlignment(qt2.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info)
        self.viewInfoTextEdit()
        content_layout=qt.QHBoxLayout()
        self.list_widget=qt.QListWidget()
        self.list_widget.currentItemChanged.connect(self.onToolChanged)
        self.stacked_widget=qt.QStackedWidget()        
        self.quranPlayer=QuranPlayer()
        self.storiesPlayer=StoryPlayer()
        tabs=[
            (prayer_times(), _("مواقيت الصلاة والتاريخ")),
            (Quran(), _("القرآن الكريم مكتوب")),
            (self.quranPlayer, _("القرآن الكريم صوتي")),
            (QuranRecitations(),_("قراءات القرآن الكريم")),
            (hadeeth(), _("الأحاديث النبوية والقدسية")),
            (IslamicBooks(),_("الكتب الإسلامية")),
            (ProphetStories(),_("القصص الإسلامية المكتوبة")),
            (self.storiesPlayer,_("القصص الإسلامية الصوتية")),            
            (Albaheth(), _("الباحث في القرآن والأحاديث")),
            (protcasts(), _("الإذاعات الإسلامية")),
            (Athker(), _("الأذكار والأدعية")),
            (sibha(), _("سبحة إلكترونية")),
            (NamesOfAllah(), _("أسماء الله الحُسْنى")),
            (DateConverter(), _("محول التاريخ"))            
        ]
        for widget_class, label in tabs:
            self.list_widget.addItem(label)
            instance=widget_class
            self.stacked_widget.addWidget(instance)        
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.list_widget.setCurrentRow(0)
        content_layout.addWidget(self.list_widget, 1)
        content_layout.addWidget(self.stacked_widget, 3)
        layout.addLayout(content_layout)        
        self.setting=guiTools.QPushButton(_("الإعدادات"))
        self.setting.setShortcut("f3")
        self.setting.setAccessibleDescription("f three")
        self.setting.clicked.connect(lambda: settings(self).exec())
        self.whats_new=guiTools.QPushButton(_("ما الجديد في هذا الإصدار"))
        self.whats_new.setShortcut("ctrl+w")
        self.whats_new.setAccessibleDescription("control plus w")
        self.whats_new.clicked.connect(self.whats_new_funktion)
        self.viewLastMessage=guiTools.QPushButton(_("إظهار آخر رسالة من المطورين"))
        self.viewLastMessage.setShortcut("ctrl+m")
        self.viewLastMessage.setAccessibleDescription("control plus m")
        self.viewLastMessage.clicked.connect(self.onViewLastMessageButtonClicked)
        self.user_guide=guiTools.QPushButton(_("دليل المستخدم"))        
        self.user_guide.setShortcut("f1")
        self.user_guide.setAccessibleDescription("f one")
        self.user_guide.clicked.connect(self.open_user_g_window)
        self.about_devs=guiTools.QPushButton(_("عن المطورين"))                
        self.about_devs.setShortcut("f2")
        self.about_devs.setAccessibleDescription("f two")
        self.about_devs.clicked.connect(self.open_developers_window)
        self.bookMark=guiTools.QPushButton(_("العلامات المرجعية"))        
        self.bookMark.clicked.connect(lambda: book_marcks(self).exec())
        self.bookMark.setShortcut("ctrl+b")
        self.bookMark.setAccessibleDescription("control plus b")
        buttons_layout=qt.QHBoxLayout()
        buttons_layout.addWidget(self.setting)
        buttons_layout.addWidget(self.whats_new)
        buttons_layout.addWidget(self.viewLastMessage)
        buttons_layout.addWidget(self.bookMark)
        buttons_layout.addWidget(self.user_guide)
        buttons_layout.addWidget(self.about_devs)        
        layout.addLayout(buttons_layout)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        qt1.QShortcut("ctrl+tab",self).activated.connect(self.Nexttab)
        qt1.QShortcut("ctrl+shift+tab",self).activated.connect(self.previousTab)
        self.tray_icon=qt.QSystemTrayIcon(self)
        self.tray_icon.setIcon(qt1.QIcon("data/icons/tray_icon.jpg"))
        self.tray_icon.setToolTip(app.name)
        self.tray_menu=qt.QMenu(self)        
        self.random_thecker_audio=qt1.QAction(_("تشغيل ذكر عشوائي"))
        self.random_thecker_audio.triggered.connect(self.random_audio_theker)
        self.random_thecker_text=qt1.QAction(_("عرض ذكر عشوائي"))
        self.random_thecker_text.triggered.connect(self.show_random_theker)
        self.show_action=qt1.QAction(_("إخفاء البرنامج"))
        self.show_action.triggered.connect(self.toggle_visibility)
        self.close_action=qt1.QAction(_("إغلاق البرنامج"))
        self.close_action.triggered.connect(lambda: qt.QApplication.quit())
        self.tray_menu.addAction(self.random_thecker_audio)
        self.tray_menu.addAction(self.random_thecker_text)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.close_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.TIMER1=qt2.QTimer(self)
        self.TIMER1.timeout.connect(self.show_random_theker)        
        self.runAudioThkarTimer()
        self.notification_random_thecker()
        guiTools.messageHandler.check(self)
        if settings_handler.get("update", "autoCheck") == "True":
            update.check(self, message=False)
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.show_action.setText(_("إظهار البرنامج"))
        else:
            self.show()
            self.show_action.setText(_("إخفاء البرنامج"))
    def show_random_theker(self):
        with open("data/json/text_athkar.json", "r", encoding="utf_8") as f:
            data=json.load(f)
        random_theckr=random.choice(data)
        guiTools.SendNotification(_("ذكر عشوائي"), random_theckr)
    def notification_random_thecker(self):
        self.TIMER1.stop()
        if formatDuration("athkar", "text") != 0:
            self.TIMER1.start(formatDuration("athkar", "text"))
    def runAudioThkarTimer(self):
        self.timer.stop()
        if formatDuration("athkar", "voice") != 0:
            self.timer.start(formatDuration("athkar", "voice"))
    def closeEvent(self,event):
        if app.exit:
            if settings_handler.get("g", "exitDialog") == "True":
                m = guiTools.ExitApp(self)
                m.exec()
                if m:
                    event.ignore()
            else:
                self.close()
        else:
            self.close()
    def random_audio_theker(self):
        folder_path=r"data\sounds\athkar"
        sound_files=[f for f in os.listdir(folder_path) if f.endswith(('.ogg'))]
        if sound_files:
            chosen_file=random.choice(sound_files)
            file_path=os.path.join(folder_path, chosen_file)
            self.media_player.setSource(qt2.QUrl.fromLocalFile(file_path))
            self.media_player.play()
    def open_user_g_window(self)    :
        webbrowser.open("https://drive.google.com/file/d/1GLp5kR6SIY2OhXfc6bZXjWn5beRflsEP/view?usp=drivesdk")
    def open_developers_window(self):
        self.developers_window=About_developers()
        self.developers_window.show()
    def Nexttab(self):
        if self.list_widget.currentRow()==self.list_widget.count()-1:
            self.list_widget.setCurrentRow(0)
        else:
            self.list_widget.setCurrentRow(int(self.list_widget.currentRow())+1)
    def previousTab(self):
        if self.list_widget.currentRow()==0:
            self.list_widget.setCurrentRow(self.list_widget.count()-1)
        else:
            self.list_widget.setCurrentRow(self.list_widget.currentRow()-1)
    def viewInfoTextEdit(self):
        try:
            hijri_date_obj=Gregorian.today().to_hijri()
            if hijri_date_obj.month==9:
                self.info.setText(_("رمضان كريم"))
            elif hijri_date_obj.month==10 and hijri_date_obj.day==1 or hijri_date_obj.month==12 and hijri_date_obj.day==10:
                self.info.setText(_("عيد مبارك"))
            elif hijri_date_obj.month==10:
                self.info.setText(_("صيام الست أيام البيض في هذا الشهر وهي سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month==8:
                self.info.setText(_("يستحب الصيام في هذا الشهر"))
            elif hijri_date_obj.day in [13,14,15]:
                self.info.setText(_("صيام الأيام القمرية سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month==1 and hijri_date_obj.day==10:
                self.info.setText(_("صيام عاشوراء مستحب عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month==12 and hijri_date_obj.day in [1,2,3,4,5,6,7,8]:
                self.info.setText(_("صيام العشر الأوائل من ذي الحجة سنة عن النبي صل الله عليه وسلم"))
            elif hijri_date_obj.month==12 and hijri_date_obj.day==9:
                self.info.setText(_("صيام وقفة عرفات"))
            elif datetime.datetime.now().weekday() in [0,3]:
                self.info.setText(_("صيام اليوم سنة عن النبي صل الله عليه وسلم"))
            else:
                self.info.setText(_("لا تَنْسى ذِكْر الله"))
        except:
            self.info.setText(_("لا تَنْسى ذِكْر الله"))
    def onToolChanged(self,index):
        if self.quranPlayer.mp.isPlaying():
            self.quranPlayer.mp.stop()
        if self.storiesPlayer.mp.isPlaying():
            self.storiesPlayer.mp.stop()
    def onViewLastMessageButtonClicked(self):
        with open(os.path.join(os.getenv('appdata'),settings_handler.appName,"message.json"),"r",encoding="utf-8") as file:
            data=json.load(file)
        guiTools.TextViewer(self,_("آخر رسالة من المطورين"),data["message"]).exec()
    def whats_new_funktion(self):
        try:
            r=requests.get("https://raw.githubusercontent.com/mesteranas/{}/main/{}/update/app.json".format(settings_handler.appName,app.appdirname))
            info=r.json()
            guiTools.TextViewer(self,_("ما الجديد"),info["what is new"]).exec()
        except Exception as e:
            print(e)
            qt.QMessageBox.critical(self,_("خطأ"),_("فشلت عملية جلب المعلومات, الرجاء الإتصال بالإنترنت"))
App=qt.QApplication([])
App.setApplicationDisplayName(app.name)
App.setApplicationName(app.name)
App.setApplicationVersion(str(app.version))
App.setOrganizationName(app.creater)
App.setWindowIcon(qt1.QIcon("data/icons/app_icon.ico"))
App.setStyle('fusion')
window=main()
window.show()
App.exec()